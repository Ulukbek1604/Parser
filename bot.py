from aiogram import executor
from config import dp
import logging
from handlers import callback, client, notification, fsmAdminMenu
from database import bot_dp

async def on_start_up(_):
    bot_dp.sql_create()

client.register_hendlers_client(dp)
callback.register_hendlers_callback(dp)
# fsmAdminGetUser.register_hendler_fsmAdminGetUser(dp)
fsmAdminMenu.register_hendler_fsmAdminMenu(dp)

notification.register_hendlers_notification(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=False, on_startup=on_start_up)