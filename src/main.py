import asyncio
import redis
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import BOT_TOKEN

loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, loop=loop)

users_db = redis.StrictRedis(host='localhost', port=6379, db=1)

ADMIN_LIST_COMMANDS = ['send_everyone', 'admin', 'backup_users_id', 'bot_stat', 'update_limitation']

TIKTOK_LINK = 'https://vm.tiktok.com/'
TIKTOK_LIST = ['tiktok.com/@', 'https://', 'likee.video', 'funimate.com/p/']
TIKTOK_HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 '
                                '(KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}


class AdminSendEveryOne(StatesGroup):
    post = State()
    ask_send = State()


class UpdateLimitation(StatesGroup):
    user_id = State()
