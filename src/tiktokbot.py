# coding=utf-8
from aiogram.utils import executor
from aiogram.types import Message
from admin.admin import admin_commands
from important_functions import save_user_actions, on_startup
from main import dp, users_db, ADMIN_LIST_COMMANDS, TIKTOK_LIST, bot, TIKTOK_LINK
from message_strings import msg_dict
from config import ADMIN_ID
from tiktok_main import send_by_link


@dp.message_handler(lambda message: message.from_user.id == int(ADMIN_ID), commands=ADMIN_LIST_COMMANDS)
async def admin_command(message: Message):
    if message.text == '/admin':
        await bot.send_message(message.chat.id, msg_dict['admin-string'])
    else:
        await admin_commands(message)


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    await bot.send_message(message.chat.id, msg_dict['command-start'])

    user_info = users_db.get(message.chat.id)
    if user_info is None:
        users_db.set(message.chat.id, 0)

        split_text = str(message.text).split()
        if len(split_text) == 2:
            user_invited = split_text[1]
            user_invited_info = users_db.get(user_invited)
            users_db.set(user_invited, int(user_invited_info) + 1)
            await bot.send_message(user_invited,
                                   msg_dict['user-invited'].format(message.from_user.full_name, message.chat.id),
                                   parse_mode='markdown')


@dp.message_handler()
async def all_messages(message: Message):
    # Check, if there is no space in message
    if ' ' in message.text:
        await bot.send_message(message.chat.id, msg_dict['link-wrong'])
        return

    user_info = users_db.get(message.chat.id)
    if int(user_info) == 0:
        await bot.send_message(message.chat.id, msg_dict['user-invite-link'].format(message.chat.id))
        return

    # Check user message
    if TIKTOK_LINK in message.text or any(x in str(message.text) for x in TIKTOK_LIST):
        # Send video by link
        message_wait = await bot.send_message(message.chat.id, msg_dict['message-wait'])
        is_sent = await send_by_link(message)

        if not is_sent:
            await bot.send_message(message.chat.id, msg_dict['unable_download'])
        else:
            await save_user_actions()
        await bot.delete_message(message.chat.id, message_wait.message_id)

    else:
        await bot.send_message(message.chat.id, msg_dict['link-wrong'])


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
