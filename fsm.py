from __future__ import annotations

import dataclasses
import inspect
import typing


@dataclasses.dataclass
class State:
    _help_message: str | None = None

    machine: FSM | None = None
    name: str | None = None
    group: type[StatesGroup] | None = None

    def set(self, user: str):
        return self.machine.set_state(user, self)
    
    @property
    def help_message(self):
        if self._help_message:
            return self._help_message
        if self.group is not None:
            return self.group.help_message
        return 'Затычка помощи для состояния'

    def __repr__(self):
        return f'{self.group}.{self.name}'

    # __str__ == __repr__


class FSM:
    def __init__(self):
        self._data = {}

    def _check_and_create_user(self, user: str):
        if self._data.get(user, None) is None:
            self._data[user] = {'state': None, 'data': {}}

    def set_state(self, user: str, state: State | None) -> State | None:
        self._check_and_create_user(user)
        self._data[user]['state'] = state
        return self._data[user]['state']

    def set_data(self, user: str, data: dict | None = None, **kwargs) -> dict:
        data = data or {}
        self._check_and_create_user(user)
        self._data[user]['data'] = {**data, **kwargs}
        return self._data[user]['data']

    def update_data(self, user, udata: dict | None = None, **kwargs) -> dict:
        udata = udata or {}
        self._check_and_create_user(user)
        self._data[user]['data'].update({**udata, **kwargs})
        return self._data[user]['data']

    def reset_state(self, user: str, with_data: bool = True):
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
        cls._parent = None
        cls._group_name = name

        fsm = namespace.get('_fsm', None)

        for name, prop in namespace.items():
            if isinstance(prop, State):
                prop.machine = fsm
                prop.name = name
                prop.group = cls
                states.append(prop)
                continue
            if inspect.isclass(prop) and issubclass(prop, StatesGroup):
                prop._fsm = fsm
                childs.append(prop)
                prop._parent = cls

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
    def help_message(cls) -> str:
        if hasattr(cls, '_help_message') and cls._help_message:
            return cls._help_message
        elif cls._parent is not None:
            return cls._parent.help_message
        return 'Затычка помощи для этой ветки даилога'

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

    def __repr__(self):
        return self.__full_group_name__

    def __contains__(self, state: State):
        if state in self._states:
            return True

        return any((state in child) for child in self._childs)


class StatesGroup(metaclass=StatesGroupMeta):
    pass
