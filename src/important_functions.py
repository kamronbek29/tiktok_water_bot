import json

from main import users_db, bot
from config import ADMIN_ID
from message_strings import msg_dict


async def save_user_actions():
    statistics = users_db.get('STATISTICS')

    if statistics is None:
        statistic_dict = {'downloads': 0}
        users_db.set('STATISTICS', json.dumps(statistic_dict))
        statistics = users_db.get('STATISTICS')

    statistic_dict = json.loads(statistics)
    statistic_dict['downloads'] = int(statistic_dict['downloads']) + 1

    users_db.set('STATISTICS', json.dumps(statistic_dict))


# Send notification that bot started working
async def on_startup(args):  # send errors to admin
    await bot.send_message(ADMIN_ID, msg_dict['admin-bot-start'])
