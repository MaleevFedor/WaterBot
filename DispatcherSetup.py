from aiogram import Router
from handlers import start


def setup_dispatcher(dp: Dispatcher):
    start.setup(dp)
    # add all commands
