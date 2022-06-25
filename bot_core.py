import logging
import requests
import aiohttp
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType
from bs4 import BeautifulSoup as bs
from requests import models


Response = models.Response

bot = Bot(token='5469238337:AAFkTlOZMaWHLXkZGildNOlDqolPqwwB9Uw')
dp = Dispatcher(bot=bot)

logging.basicConfig(level=logging.INFO)


def clear_response(data):
    pass


async def post_account(request):
    alert_info = 'Для проверки баланса введите 10-значный лицевой счет в формате `1123456789` (без букв и пробелов)'
    async with aiohttp.ClientSession() as session:
        if request.startswith('11') and len(request) == 10:
            vtk_url = 'https://balance.vt.ru/'
            async with session.post(vtk_url, data={'account': request}) as resp:
                html = await resp.read()
                parsed_html = bs(html, features='html5lib')
                response = parsed_html.body.find('div', attrs={'class': 'alert alert-success'})
            if response is None:
                return 'Введен неправильный лицевой счет'
            return response
        else:
            return alert_info


@dp.message_handler(content_types=ContentType.TEXT)
async def cmd_test(message: types.Message):
    p_a = await post_account(message.text)
    await bot.send_message(message.from_user.id, p_a, parse_mode='Markdown')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)
