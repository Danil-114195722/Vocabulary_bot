from os.path import abspath


# путь до папки с проектом "Vocabulary_bot"
path_list = abspath('constants.py').split('/')
PROJECT_PATH = '/'.join(path_list[:path_list.index('Vocabulary_bot') + 1])
# print(PROJECT_PATH)

DEFAULT_PAGE = 'https://ru.wiktionary.org/wiki/'

# для локалки
# TIME_ZONE = 0
# для сервака
TIME_ZONE = 3
