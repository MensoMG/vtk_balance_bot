import logging
import aiohttp
import re
import bs4

from aiogram import Bot, Dispatcher, executor, types
from db import utils
from bs4 import BeautifulSoup as bs
from os import getenv
from sys import exit


bot_token = getenv('BOT_TOKEN')
if not bot_token:
    exit('Error: no token provided')

bot = Bot(token=bot_token)
dp = Dispatcher(bot=bot)

logging.basicConfig(level=logging.INFO)


async def clear_response(response):
    formatted_data = re.sub(r'^\s+|\s+$', ' ', response, re.UNICODE)
    return re.sub(r' +', ' ', formatted_data, re.UNICODE)


async def post_account(request):
    session = aiohttp.ClientSession()
    vtk_url = 'https://balance.vt.ru/'
    async with session.post(vtk_url, data={'account': request}) as resp:
        html: str = await resp.text()
        parsed_html: bs4.element.Tag = bs(html, features='html5lib')
        try:
            response: str = parsed_html.body.find(
                'div', attrs={'class': 'alert alert-success'}).get_text()
        except AttributeError:
            return None
        finally:
            await session.close()
    return response

# temporary change to save_user() bot request handler
#@dp.message_handler(commands="start")
#async def save_user(message: types.Message):
#    utils.init_user(message.from_user.id, message.from_user.first_name)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def balance_handler(message: types.Message):
    alert_info = 'Для проверки баланса введите 10\-значный лицевой счет в формате `1123456789` \(без букв и пробелов\)'
    utils.init_user(message.from_user.id, message.from_user.first_name)
    if message.text.startswith('11') and len(message.text) == 10:
        response_info = await post_account(message.text)
        if response_info is None:
            response_info = 'Введен неправильный лицевой счет'
            await bot.send_message(message.from_user.id, response_info, parse_mode=types.ParseMode.HTML)
        else:
            clear_info = await clear_response(response_info)
            await bot.send_message(message.from_user.id, clear_info, parse_mode=types.ParseMode.HTML)
    else:
        await bot.send_message(message.from_user.id, alert_info, parse_mode=types.ParseMode.MARKDOWN_V2)


if __name__ == '__main__':
    utils.db.setup()
    executor.start_polling(dispatcher=dp, skip_updates=True)
