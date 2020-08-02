# coding=utf-8
import asyncio
import csv
import json
import os

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from main import UpdateLimitation, users_db, dp, bot, AdminSendEveryOne
from config import ADMIN_ID
from message_strings import msg_dict


async def send_everyone_func(message):
    await bot.send_message(message.chat.id, 'Отправьте пост, котрый вы хотите отправить всем пользователям.')
    await AdminSendEveryOne.post.set()


@dp.message_handler(state=AdminSendEveryOne.post, content_types=['photo', 'text', 'animation'])
async def admin_photo(message: Message, state: FSMContext):
    if message.text == '/start':
        await bot.send_message(message.chat.id, 'Вы отменили действия')
        await state.finish()
        return

    data = {'text': message.html_text, 'markup': message.reply_markup}

    if message.text:
        await bot.send_message(message.chat.id, data['text'], reply_markup=data['markup'], parse_mode='HTML')

    if message.photo:
        data['photo'] = message.photo[0].file_id
        await bot.send_photo(message.chat.id, data['photo'], caption=data['text'], reply_markup=data['markup'],
                             parse_mode='HTML')

    if message.animation:
        data['animation'] = message.animation.file_id
        await bot.send_animation(message.chat.id, data['animation'], caption=data['text'],
                                 reply_markup=data['markup'], parse_mode='HTML')

    await bot.send_message(message.chat.id, 'Ваш пост будет выглядеть так\n'
                                            'Чтобы начать рассылку, отправьте команду /send\n'
                                            'Чтобы отменить рассылку, отправьте команду /start')

    await state.update_data(post_info=data)
    await AdminSendEveryOne.ask_send.set()


@dp.message_handler(state=AdminSendEveryOne.ask_send)
async def admin_ask_send(message: Message, state: FSMContext):
    if message.text == '/send':
        await bot.send_message(message.chat.id, 'Рассылка началась!')
        await send_post(message, state)
    else:
        await bot.send_message(message.chat.id, 'Вы отменили действия')
        await state.finish()
        return


async def send_post(message, state):
    state_data = await state.get_data()
    data = state_data.get('post_info')

    markup = data['markup']
    text = data['text']

    delete_number = 0
    success_number = 0
    all_users = users_db.keys()

    for user_id in all_users:
        if success_number % 10 == 0:
            await asyncio.sleep(1)

        try:
            if 'photo' in data.keys():
                await bot.send_photo(int(user_id), data['photo'], caption=text, reply_markup=markup, parse_mode='HTML')
            elif 'animation' in data.keys():
                await bot.send_animation(int(user_id), data['animation'], caption=text, reply_markup=markup,
                                         parse_mode='HTML')
            else:
                await bot.send_message(int(user_id), text, caption=text, reply_markup=markup,
                                       disable_web_page_preview=True, parse_mode='HTML')

            success_number += 1
        except Exception as err:
            print(err, 'admin sure')
            delete_number += 1

    await bot.send_message(message.chat.id, "Сообщение было отправлено {} пользователяем".format(len(all_users)))
    await bot.send_message(message.chat.id, "Удалили {}".format(delete_number))
    await state.finish()


async def backup_users_id(message):
    list_users_id = users_db.keys()

    with open('@TikTokchekBot users_id.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Number", "User Id", "User info"])

    with open('@TikTokchekBot users_id.csv', 'a', newline='') as file:
        for i, user_id in enumerate(list_users_id, start=1):
            writer = csv.writer(file)
            writer.writerow([i, user_id, users_db.get(user_id)])

    await bot.send_document(message.chat.id, open('@TikTokchekBot users_id.csv', 'rb'))
    os.remove('@TikTokchekBot users_id.csv')


async def get_users_language():
    russian = 0
    english = 0
    turkish = 0
    arabic = 0
    no_lang = 0
    referral = 0

    users_id = users_db.keys()

    for user_id in users_id:
        if str(user_id, 'utf-8') == 'STATISTICS':
            continue

        user_info = json.loads(users_db.get(user_id))
        lang = user_info['lang']
        referral += user_info['ref']

        if lang == 'ru':
            russian += 1
        elif lang == 'en':
            english += 1
        elif lang == 'tr':
            turkish += 1
        elif lang == 'ar':
            arabic += 1
        else:
            no_lang += 1

    return referral, russian, english, turkish, arabic, no_lang


async def get_bot_stat(message):
    waiting_message = await bot.send_message(ADMIN_ID, msg_dict['message-wait'])

    files_db = users_db.get('STATISTICS')
    downloads_count = json.loads(files_db)['downloads']

    # Get statistics
    follow_count = len(users_db.keys())

    admin_text = f'*Статистика бота*:\n\n' \
                 f'    Пользователей: *{follow_count}*\n' \
                 f'    Скачиваний: *{downloads_count}*\n' \
                 f'\nЗапущен: *5 Июля, 2020*'

    await bot.send_message(message.chat.id, admin_text, parse_mode='markdown')
    await bot.delete_message(message.chat.id, waiting_message.message_id)


async def update_limitation(message):
    await bot.send_message(message.chat.id, 'Отправьте user id пользователя')
    await UpdateLimitation.user_id.set()


@dp.message_handler(state=UpdateLimitation.user_id)
async def update_user_limit(message: Message, state: FSMContext):
    if message.text == '/start':
        await bot.send_message(message.chat.id, 'Вы отменили действия')
        await state.finish()
        return

    users_db.set(message.text, 1)
    await bot.send_message(message.chat.id, f'Теперь пользователь с ID {message.text} может скачивать видео с ТикТок')

    await state.finish()





