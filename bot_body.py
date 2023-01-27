#!./venv/bin/python


from time import localtime

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

from config import TOKEN
from parser import get_meaning

bot = Bot(token=TOKEN)
disp = Dispatcher(bot)


@disp.message_handler(commands='start')
async def start_command(message: types.Message):
    await message.answer(
        f'Привет!\nВведи слово:\n(для справки введи /help)')


@disp.message_handler(commands='help')
async def help_command(message: types.Message):
    await message.answer(f'''
    Я использую русский онлайн словарь wiktionary.org,\nи ищу толкование твоего слова\n\nВводи слово, не томи :)''')


@disp.message_handler()
async def main_command(message: types.Message):
    word = message.text.lower()

    try:
        meaning = get_meaning(word)

        await message.reply(meaning)
    except Exception as error:

        with open('/home/daniil/Documents/Python/Telegram_bots/Vocabulary_bot/bot_state', 'a') as bot_state:
            now_time = localtime()

            bot_state.write(str(error))
            bot_state.write(f' {now_time.tm_hour}.{now_time.tm_min}.{now_time.tm_sec}')
            bot_state.write('\n')


if __name__ == '__main__':
    with open('/home/daniil/Documents/Python/Telegram_bots/Vocabulary_bot/bot_state', 'w') as bot_state:
        now_time = localtime()

        bot_state.write('Start in')
        bot_state.write(f' {now_time.tm_hour}.{now_time.tm_min}.{now_time.tm_sec}\n')

    executor.start_polling(disp)
