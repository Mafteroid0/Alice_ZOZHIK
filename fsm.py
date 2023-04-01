from __future__ import annotations

import dataclasses
import inspect


@dataclasses.dataclass
class State:
    _help_message: str | None = None

    name: str | None = None
    group: type[StatesGroup] | None = None

    def set(self, context: FSMContext):
        return context.set_state(self)

    @property
    def help_message(self):
        if self._help_message:
            return self._help_message
        if self.group is not None:
            return self.group.help_message
        return 'Затычка помощи для состояния'

    def __repr__(self):
        if not (self.name and self.group):
            return f'{super().__repr__()}'
        return f'{self.group}.{self.name}' if self.group is not None else f'{self.name}'


class FSMContext:
    def __init__(self, user_id: str | None = None, parent: FSMContext | None = None):
        if sum(map(lambda x: x is None, (user_id, parent))) not in (0, 2):
            raise ValueError()

        self._data = {}  # Так а не через однострочник чтобы подсказки работали лучше
        if parent is not None:
            self._data = parent._data

        self._user_id = user_id

    @property
    def user_id(self):
        return self._user_id
    
    def build_context(self, user_id: str):
        self._check_and_create_user(user_id)
        return FSMContext(user_id, self)

    def _check_and_create_user(self, user_id: str):
        if self._data.get(user_id, None) is None:
            self._data[user_id] = {'state': None, 'data': {}}
        print(f'{self._data[user_id]=}')

    def set_state(self, state: State | str | None, user_id: str | State | None = None) -> State | None:
        print('pre', f'{state=}', f'{user_id=}')
        if isinstance(state, str) and isinstance(user_id, State):
            state, user_id = user_id, state  # Нормализация данных во имя обратной совместимости, ведь я поменял
            # аргументы местами
        print(f'{state=}', f'{user_id=}')

        user_id = user_id or self._user_id

        self._check_and_create_user(user_id)
        self._data[user_id]['state'] = state
        return self._data[user_id]['state']

    def set_data(self, data: dict | None = None, user_id: str | None = None, **kwargs) -> dict:
        user_id = user_id or self._user_id

        data = data or {}
        self._check_and_create_user(user_id)
        self._data[user_id]['data'] = {**data, **kwargs}
        return self._data[user_id]['data']

    def update_data(self, udata: dict | None = None, user_id: str | None = None, **kwargs) -> dict:
        user_id = user_id or self._user_id

        udata = udata or {}
        self._check_and_create_user(user_id)
        self._data[user_id]['data'].update({**udata, **kwargs})
        return self._data[user_id]['data']

    def reset_state(self, with_data: bool = True, user_id: str | None = None):
        user_id = user_id or self._user_id

        self.set_state(None)
        if with_data:
            self.reset_data(user_id)

    def reset_data(self, user_id: str | None = None):
        user_id = user_id or self._user_id

        self.set_data({}, user_id)

    def get_state(self, user_id: str | None = None) -> State | None:
        user_id = user_id or self._user_id
        # print(f'{user_id=}')
        # print(self._data.get(user_id, {'state': None}))

        self._check_and_create_user(user_id)

        return self._data[user_id]['state']

    @property
    def state(self):
        if self.user_id is None:
            raise ValueError('state as property available only in user contexts')
        return self.get_state()

    @property
    def data(self):
        if self.user_id is None:
            return self._data
        return self.get_data()

    def get_data(self, user_id: str | None = None) -> dict:
        user_id = user_id or self._user_id

        return self._data.get(user_id, {'data': {}})['data']

    # def filter(self, state: State):  # TODO: Сделать фильтр состояний (лучше его перенести в StatesGroupMeta и State, чтобы было красиво)
    #     def sub_wrapper(f: typing.Callable):
    #         def wrapper(*args, **kwargs):
    #             req = args[0]
    #             # Тут надо проверять стейт
    #             f(*args, **kwargs)
    #
    #     return sub_wrapper


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
