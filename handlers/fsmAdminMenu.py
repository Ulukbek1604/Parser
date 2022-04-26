from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .keyboards import cancel_markup
from config import bot, ADMIN
from database import bot_dp


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def fsm_start(message: types.Message):
    if message.chat.type == 'private':
        await FSMAdmin.photo.set()
        await bot.send_message(message.chat.id,
                               f"Привет {message.from_user.full_name}, скинь фотку блюда...",
                               reply_markup=cancel_markup)
    else:
        await message.answer('В личку только')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await bot.send_message(message.chat.id, "Как ?")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, "Описание блюда?")


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, "Цена блюда?")



async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await bot_dp.sql_command_insert(state)
    await bot.send_message(message.chat.id, "Все свободен)")


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.reply("ОК")


async def delete_data(message: types.Message):
    if message.from_user.id == ADMIN:
        results = await bot_dp.sql_command_all(message)
        for result in results:
            await bot.send_photo(message.from_user.id, result[0],
                                 caption=f"Name: {result[1]}\n"
                                         f"Description: {result[2]}\n"
                                         f"Prise: {result[3]}\n",
                                 reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                     f"delete: {result[0]}",
                                     callback_data=f"delete: {result[3]}"
                                 )))
    else:
        await message.answer("Ты не админ!!!")


async def complete_delete(call: types.CallbackQuery):
    await bot_dp.sql_command_delete(call.data.replace('delete: ', ''))
    await call.answer(text=f"{call.data.replace('delete: ', '')} deleted", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


def register_hendler_fsmAdminMenu(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state="*", commands="cancel")
    dp.register_message_handler(cancel_reg, Text(equals='cancel', ignore_case=True), state="*")

    dp.register_message_handler(fsm_start, commands=["Menu"])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=["photo"])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)

    dp.register_message_handler(delete_data, commands=['delete'])
    dp.register_callback_query_handler(complete_delete, lambda call: call.data and call.data.startswith("delete: "))
