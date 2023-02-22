#!./venv/bin/python


from time import localtime

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

import asyncio
import aiofiles

from config import TOKEN
from parser import get_meaning
from constants import PROJECT_PATH, TIME_ZONE

bot = Bot(token=TOKEN)
disp = Dispatcher(bot)


@disp.message_handler(commands='start')
async def start_command(message: types.Message):
    await message.answer(
        f'Привет!\nВведи слово:\n(для справки введи /help)')


@disp.message_handler(commands='help')
async def help_command(message: types.Message):
    await message.answer(f'''
    Я использую русский онлайн словарь wiktionary.org,\nи ищу толкование твоего слова\n\nВводи слово :)''')


@disp.message_handler()
async def main_command(message: types.Message):
    word = message.text.lower()

    try:
        meaning = await asyncio.create_task(get_meaning(word))

        await message.reply(meaning)
    except Exception as error:

        async with aiofiles.open(f'{PROJECT_PATH}/bot_state', 'a') as bot_state:
            now_time = localtime()

            await bot_state.write(str(error))
            await bot_state.write(f' {now_time.tm_hour + TIME_ZONE}.{now_time.tm_min}.{now_time.tm_sec}\n\n')


if __name__ == '__main__':
    with open(f'{PROJECT_PATH}/bot_state', 'w') as bot_state:
        now_time = localtime()

        bot_state.write('Start at\n')
        bot_state.write(f'Time: {now_time.tm_hour + TIME_ZONE}.{now_time.tm_min}.{now_time.tm_sec}\n')
        bot_state.write(f'Date: {now_time.tm_mday}.{now_time.tm_mon}.{now_time.tm_year}\n\n')

    executor.start_polling(disp)
