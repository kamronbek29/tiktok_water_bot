# coding=utf-8
from admin.admin_cmd_func import send_everyone_func, backup_users_id, get_bot_stat, update_limitation


async def admin_commands(message):
    if message.text == '/send_everyone':
        await send_everyone_func(message)

    elif message.text == '/backup_users_id':
        await backup_users_id(message)

    elif message.text == '/bot_stat':
        await get_bot_stat(message)

    elif message.text == '/update_limitation':
        await update_limitation(message)
