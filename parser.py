import re
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


DEFAULT_PAGE = 'https://ru.wiktionary.org/wiki/'


def get_meaning(term_name):
    server_error = 'Извините, у нас небольшие проблемы с сервером, скоро мы всё починим :)'

    user_agent = UserAgent()
    headers = {
        'User-Agent': user_agent.random
    }

    try:
        html = requests.get(DEFAULT_PAGE + term_name, headers=headers, timeout=0.5).text
        soup = BeautifulSoup(html, 'html.parser')
    except Exception as error:
        pass
        print(f'Ha-ha-ha, you caught the error in project "Vocabulary_bot", in file "parser", in func "get_meaning", in request:\n\t{error}')
        # для локалки
        # with open('/home/daniil/Documents/Python/Telegram_bots/Vocabulary_bot/bot_state', 'a') as bot_state:
        # для сервака
        with open('./bot_state', 'a') as bot_state:
            now_time = time.localtime()

            bot_state.write(f'Ha-ha-ha, you caught the error in project "Vocabulary_bot", in file "parser", in func "get_meaning", in request:\n\t{str(error)}')
            # для локалки
            # bot_state.write(f' {now_time.tm_hour}.{now_time.tm_min}.{now_time.tm_sec}\n')
            # для сервака
            bot_state.write(f' {now_time.tm_hour + 3}.{now_time.tm_min}.{now_time.tm_sec}\n')
            bot_state.write('\n')
        return server_error

    try:
        meanings = soup.find('ol').text
        all_meaning = list(filter(lambda x: x != '' and x[0] != '◆', re.split('\n', meanings)))
        list_meanings = [re.sub('\[[≈≠▲▼]\s\d+]', '',
                                f'{i + 1}. ' + all_meaning[i][:all_meaning[i].index('◆')] + '\n\n')
                         for i in range(len(all_meaning))]

        # # проверка
        # for meaning in list_meanings:
        #     print(meaning)

        return ''.join(list_meanings)

    except AttributeError:
        return 'Вы неверно ввели слово! Проверьте своё написание'


# if __name__ == '__main__':
#     term_name = 'земля'
#
#     mean = get_meaning(term_name)
#     print(mean)
