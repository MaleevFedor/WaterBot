from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from data.user_class import User
from fsm import AddDrinks
from data import db_session
from BHI import bhi, to_rus


router = Router()


@router.message(F.text.startswith('/drink_'))
async def start(message: types.Message, state: FSMContext):
    args = message.text.split('_')
    if len(args) == 2:
        if args[1].lower() not in bhi.keys():
            await message.answer('Некорректный ввод, попробуйте снова')
        else:
            kb = [
                [types.KeyboardButton(text="200")],
                [types.KeyboardButton(text="300")],
                [types.KeyboardButton(text="500")]
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
            await state.set_data({'drink': args[1].lower()})
            await state.set_state(AddDrinks.waiting_amount.state)
            await message.answer('Сколько вы выпили?', reply_markup=keyboard)
    else:
        await message.answer('Некорректный ввод, попробуйте снова')


@router.message(AddDrinks.waiting_amount)
async def add_amount(message: types.Message, state: FSMContext):
    data = await state.get_data()
    amount = int(message.text)
    total = bhi[data['drink']] * amount
    builder = InlineKeyboardBuilder()
    builder.adjust(1, 3)
    builder.button(text='✅', callback_data=f'1-{total}')
    builder.button(text='❌', callback_data=f'0-{total}')
    await state.set_data({'amount': amount})
    await state.clear()
    await message.answer(f"Вы выпили {amount} мл {to_rus[data['drink']]}", reply_markup=builder.as_markup())


@router.callback_query()
async def confirm(callback: types.CallbackQuery):
    data = callback.data.split('-')
    tg_id = int(callback.from_user.id)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.tg_id == tg_id).first()
    if data[0] == '1':
        db_sess.query(User).filter(User.tg_id == tg_id).update({'drinked': User.drinked + data[1]})
        db_sess.commit()
    await callback.message.answer(f'Сегодня вы уже выпили {user.drinked}/{user.goal}мл💧')
    if user.drinked >= user.goal:
        db_sess.query(User).filter(User.tg_id == tg_id).update({'streak': User.streak + 1})
        db_sess.commit()
        await callback.message.answer('Вы выполнили ежедневную цель🔥')
        await callback.message.answer(f'Вы держитесь уже {user.streak} день🔥🔥🔥')
    db_sess.close()
