import logging
from types import NoneType

import requests


from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType
from bs4 import BeautifulSoup as bs
from requests import models


Response = models.Response

bot = Bot(token='5469238337:AAFkTlOZMaWHLXkZGildNOlDqolPqwwB9Uw')
dp = Dispatcher(bot=bot)

logging.basicConfig(level=logging.INFO)


def post_account(request: str) -> str:
    alert_info = 'Для проверки баланса введите 10-значный лицевой счет в формате `1123456789` (без букв и пробелов)'

    if request.startswith('11') and len(request) == 10:
        r = requests.post('https://balance.vt.ru/', data={'account': request})
        html = r.text
        parsed_html = bs(html, features='html5lib')
        response = parsed_html.body.find('div', attrs={'class': 'alert alert-success'})
        if response is None:
            return 'Введен неправильный лицевой счет'
        var = response.text
        return var
    else:
        return alert_info


@dp.message_handler(content_types=ContentType.TEXT)
async def cmd_test(message: types.Message):
    await bot.send_message(message.from_user.id, post_account(message.text), parse_mode='Markdown')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)
