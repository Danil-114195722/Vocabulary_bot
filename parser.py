import re
import time

import lxml
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

import asyncio
import aiohttp
import aiofiles

from constants import TIME_ZONE, DEFAULT_PAGE, PROJECT_PATH


async def get_meaning(term_name):
    server_error = 'Извините, у нас небольшие проблемы с сервером, скоро мы всё починим :)'
    user_error = 'Вы неверно ввели слово! Проверьте своё написание'

    user_agent = UserAgent()
    headers = {
        'User-Agent': user_agent.random
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(DEFAULT_PAGE + term_name, headers=headers, timeout=3) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')

    except Exception as error:
        print(f'Ha-ha-ha, you caught the error in project "Vocabulary_bot", in file "parser", in func "get_meaning", in request:\n\t{error}')

        async with aiofiles.open(f'{PROJECT_PATH}/bot_state', 'a') as bot_state:
            now_time = time.localtime()

            await bot_state.write(f'Ha-ha-ha, you caught the error in project "Vocabulary_bot", in file "parser", in func "get_meaning", in request:\n\t{str(error)}')
            await bot_state.write(f' {now_time.tm_hour + TIME_ZONE}.{now_time.tm_min}.{now_time.tm_sec}\n\n')
        return server_error

    try:
        meanings = soup.find('ol').text
        all_meaning = list(filter(lambda x: x != '' and x[0] != '◆', re.split('\n', meanings)))
        list_meanings = [re.sub('\[[≈≠▲▼]\s\d+]', '',
                                f'{i + 1}. ' + all_meaning[i][:all_meaning[i].index('◆')] + '\n\n')
                         for i in range(len(all_meaning))]

        return ''.join(list_meanings)

    except AttributeError:
        return user_error


# if __name__ == '__main__':
#     term_name = 'земля'
#
#     mean = get_meaning(term_name)
#     print(mean)
