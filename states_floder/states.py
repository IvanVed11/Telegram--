from aiogram.fsm.state import StatesGroup, State

class MultiplyState(StatesGroup):
    waiting_answer = State()