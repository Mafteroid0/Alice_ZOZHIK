from fsm import FSM, StatesGroup, State

fsm = FSM()


class MainGroup(StatesGroup):
    _fsm = fsm

    state = State()

    class SubGroup(StatesGroup):
        substate = State()

    class SubGroup2(StatesGroup):
        substate2 = State()


print(MainGroup.state in MainGroup)
print(MainGroup.SubGroup.substate in MainGroup)
print(MainGroup.state in MainGroup.SubGroup)
