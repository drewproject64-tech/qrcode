from aiogram.fsm.state import State, StatesGroup

class QRStates(StatesGroup):
    waiting_scan = State()
    waiting_create = State()
