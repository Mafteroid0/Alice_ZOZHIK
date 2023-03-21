from __future__ import annotations
import inspect
import typing


class State:
    def __init__(self, machine: FSM | None = None, state: str | None = None, group_name: str | None = None):
        self.machine = machine
        self.name = state
        self.group_name = group_name

    def set(self, user: str):
        return self.machine.set_state(user, self)

    def __repr__(self):
        return f'State("{self.name}")'

    def __str__(self):
        return f'{self.name}'


class FSM:
    def __init__(self):
        self._data = {}

    def _check_and_create_user(self, user: str):
        if self._data.get(user, None) is None:
            self._data[user] = {'state': None, 'data': {}}

    def set_state(self, user: str, state: State | None) -> State | None:
        self._check_and_create_user(user)
        self._data[user]['state'] = state
        return self._data[user]

    def set_data(self, user: str, data: dict) -> dict:
        self._check_and_create_user(user)
        self._data[user]['data'] = data
        return self._data[user]

    def reset_state(self, user: str, with_data: bool = False):
        self.set_state(user, None)
        if with_data:
            self.reset_data(user)

    def reset_data(self, user: str):
        self.set_data(user, {})

    def get_state(self, user: str) -> State | None:
        return self._data.get(user, {'state': None})['state']

    def get_data(self, user: str) -> dict:
        return self._data.get(user, {'data': {}})['data']

    def filter(self, state: State):
        def sub_wrapper(f: typing.Callable):
            def wrapper(*args, **kwargs):
                req = args[0]
                # Тут надо проверять стейт
                f(*args, **kwargs)

        return sub_wrapper


class StatesGroupMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super(StatesGroupMeta, mcs).__new__(mcs, name, bases, namespace)

        states = []
        childs = []

        cls._group_name = name

        for name, prop in namespace.items():

            if isinstance(prop, State):
                prop.machine = namespace['_fsm']
                prop.name = name
                prop.group_name = name
                states.append(prop)
            elif inspect.isclass(prop) and issubclass(prop, StatesGroup):
                childs.append(prop)
                prop._parent = cls

        cls._parent = None
        cls._childs = tuple(childs)
        cls._states = tuple(states)
        cls._state_names = tuple(state.name for state in states)

        return cls

    @property
    def __group_name__(cls) -> str:
        return cls._group_name

    @property
    def __full_group_name__(cls) -> str:
        if cls._parent:
            return '.'.join((cls._parent.__full_group_name__, cls._group_name))
        return cls._group_name

    @property
    def states(cls) -> tuple:
        return cls._states

    @property
    def childs(cls) -> tuple:
        return cls._childs

    @property
    def all_childs(cls):
        result = cls.childs
        for child in cls.childs:
            result += child.childs
        return result

    @property
    def all_states(cls):
        result = cls.states
        for group in cls.childs:
            result += group.all_states
        return result

    @property
    def all_states_names(cls):
        return tuple(state.name for state in cls.all_states)

    @property
    def states_names(cls) -> tuple:
        return tuple(state.name for state in cls.states)

    def __contains__(cls, item):
        if isinstance(item, str):
            return item in cls.all_states_names
        if isinstance(item, State):
            return item in cls.all_states
        if isinstance(item, StatesGroup):
            return item in cls.all_childs
        return False


class StatesGroup(metaclass=StatesGroupMeta):
    def __contains__(self, state: State):
        if state in self._states:
            return True

        return any((state in child) for child in self._childs)
