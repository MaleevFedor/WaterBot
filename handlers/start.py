from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from data.user_class import User
from fsm import SetUp
from data import db_session


router = Router()


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    db_sess = db_session.create_session()
    if db_sess.query(User).filter((User.tg_id == int(message.from_user.id))).first():
        await message.answer("Вы уже зарегистрированы")
    else:
        await message.answer('Для расчета вашей ежедневной нормы потребления воды. Отправьте ваш вес в килограммах')
        await state.set_state(SetUp.waiting_weight.state)
    db_sess.close()


@router.message(SetUp.waiting_weight)
async def get_weight(message: types.Message, state: FSMContext):
    try:
        weight = round(float(message.text.strip().replace(',', '.')), 2)
        db_sess = db_session.create_session()
        goal = round(weight * 2.2 * 0.5 * 29.57) - 200
        user = User(tg_id=int(message.from_user.id),
                    username=message.from_user.username, goal=goal)
        db_sess.add(user)
        db_sess.commit()
        timezone = db_sess.query(User).filter(User.tg_id == message.from_user.id).first().timezone
        db_sess.close()
        await message.answer(f"Добро пожаловать, {message.from_user.first_name}.\n"
                             f"Авто определён часовой пояс: GMT+{timezone}\n"
                             f"Ваша цель - {goal} мл воды в день, давайте начнем\n"
                             'Вы можете изменить информацию о себе нажав /settings')
        await state.clear()
    except Exception as e:
        await message.reply('Некорректный ввод')
