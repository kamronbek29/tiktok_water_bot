# coding=utf-8
import asyncio
import json

import aiohttp

from main import TIKTOK_HEADERS, bot
from message_strings import msg_dict


async def send_by_link(message):
    video_url, music_url = await get_tik_tok_url(message.text)

    if video_url is not None:
        await bot.send_video(message.chat.id, video_url, caption=msg_dict['downloaded-by'])
        await bot.send_audio(message.chat.id, music_url, caption=msg_dict['downloaded-by'])
    else:
        return None

    return True


async def get_tik_tok_url(link):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link, headers=TIKTOK_HEADERS) as get_request:
                get_request_content = await get_request.content.read()
                get_request_json_str = str(get_request_content, 'utf-8').split(
                    'application/json" crossorigin="anonymous">')[1].split('</script><script crossorigin')[0]

                result_json = json.loads(get_request_json_str)
                page_json = result_json['props']['pageProps']

                music_id = page_json['videoData']['musicInfos']['musicId']
                music_name = page_json['videoData']['musicInfos']['musicName']
                music_link = f'https://www.tiktok.com/music/{music_name}-{music_id}'.replace(' ', '-')

                video_url = page_json['videoData']['itemInfos']['video']['urls'][0]

            async with session.get(music_link, headers=TIKTOK_HEADERS) as get_request:
                get_request_content = await get_request.content.read()
                get_request_json_str = str(get_request_content, 'utf-8').split(
                    'application/json" crossorigin="anonymous">')[1].split('</script><script crossorigin')[0]

                result_json = json.loads(get_request_json_str)
                page_json = result_json['props']['pageProps']
                music_url = page_json['musicData']['playUrl']['UrlList'][0]

            return video_url, music_url

    except Exception as err:
        print(err, 'Error in get_tik_tok_video_url')
        return None, None


if __name__ == '__main__':
    asyncio.run(get_tik_tok_url('https://www.tiktok.com/@jazlynebaybee/video/6814512525250530566'))
