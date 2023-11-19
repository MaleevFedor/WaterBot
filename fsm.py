from aiogram.fsm.state import State, StatesGroup


class SetUp(StatesGroup):
    waiting_weight = State()


class AddDrinks(StatesGroup):
    waiting_amount = State()
