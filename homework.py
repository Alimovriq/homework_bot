import logging
import os
import sys
import time
from http import HTTPStatus
# from pprint import pprint

import requests
import telegram
from dotenv import load_dotenv

from exceptions import HomeworkStatusError

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    filemode='w',
    format='%(asctime)s, %(levelname)s, %(message)s'
)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


def send_message(bot, message):
    """Бот отправляет сообщение в Telegram."""
    try:
        logger.debug('Бот отправляет сообщение в Telegram')
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info('Бот отправил сообщение в Telegram')
    except telegram.error.TelegramError as error:
        logger.error(f' Боту отправить сообщение не удалось: {error}')
        raise error(
            f'Боту отправить сообщение не удалось: {error}')


def get_api_answer(current_timestamp):
    """Получить API ответ."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    response = requests.get(ENDPOINT,
                            headers=HEADERS,
                            params=params)
    try:
        logger.debug('Бот отправляет запрос к эндпоинту сервиса')
        response
        logger.info('Бот отправил запрос к экдпоинту сервиса')
    except telegram.error.NetworkError:
        logger.error('Ошибка соединения')
        raise telegram.error.NetworkError('Ошибка соединения')
    except Exception as error:
        logger.error(f'Ошибка доступа к эндпоинту: {error}')
        send_message(f'Ошибка доступа к эндпоинту: {error}')
    if response.status_code != HTTPStatus.OK:
        message = f'Эндпоинт {ENDPOINT} недоступен.'
        logger.error(
            f'{message} Код ответа API: {response.status_code}')
        raise telegram.error.BadRequest(
            f'{message} Код ответа API: {response.status_code}')

    return response.json()
#     if response == 200:
#         return response.json()
#     else:
#         raise Exception
# pprint(get_api_answer(1549962000))


def check_response(response):
    """Проверить ответ API."""
    logger.debug('Начало проверки ответа API')
    try:
        homework = response['homeworks']
    except KeyError as error:
        logger.error(f'Данные по ключу "homeworks" не найдены: {error}')
    if not isinstance(homework, list):
        logger.error('Тип запроса не список')
        raise TypeError('Тип запроса не список')
    return homework


def parse_status(homework):
    """Извлекает из информации о конкретной домашней работе статус работы."""
    homework_name = homework['homework_name']
    homework_status = homework['status']
    if homework_name is None:
        logger.error('Данные по ключу "homework_name" не найдены')
        raise KeyError('Данные по ключу "homework_name" не найдены')
    if homework_status not in HOMEWORK_STATUSES:
        logger.error(f'Неизвестный статус работы: {homework_status}')
        raise HomeworkStatusError(
            f'Неизвестный статус работы: {homework_status}'
        )
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверка доступности переменных окружения."""
    if all([PRACTICUM_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN]):
        return True
    else:
        False


def main():
    """Основная логика работы бота."""
    logger.debug('Начало проверки главной функции')
    if not check_tokens():
        message = 'Отсутствует обязательная переменная окружения:'
        # sys.exit('Программа принудительно остановлена.')
        if TELEGRAM_CHAT_ID is None:
            logger.critical(f'{message} TELEGRAM_CHAT_ID')
            raise telegram.error.InvalidToken(
                f'{message} TELEGRAM_CHAT_ID') and sys.exit(
                    'Программа принудительно остановлена.')
        if TELEGRAM_TOKEN is None:
            logger.critical(f'{message} TELEGRAM_TOKEN')
            raise telegram.error.InvalidToken(
                f'{message} TELEGRAM_TOKEN') and sys.exit(
                    'Программа принудительно остановлена.')
        if PRACTICUM_TOKEN is None:
            logger.critical(f'{message} PRACTICUM_TOKEN')
            raise telegram.error.InvalidToken(
                f'{message} PRACTICUM_TOKEN') and sys.exit(
                    'Программа принудительно остановлена.')

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    # current_timestamp = 0
    while True:
        try:
            response = get_api_answer(current_timestamp)
            # current_timestamp = response.get('current_date')
            current_timestamp = response.get('current_date', current_timestamp)
            homework = check_response(response)
            time.sleep(RETRY_TIME)
            if homework:
                message = parse_status(homework[0])
                send_message(bot, message)
                logger.info('Произошло изменение статуса домашней работы')
            else:
                # message = 'Изменений в статусе домашней работы нет'
                # send_message(bot, message)
                logger.info(
                    'Изменений в статусе домашней работы нет'
                )
                logger.debug('Ошибок в функции main не обнаружено')
                # time.sleep(RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            send_message(bot, message)
            time.sleep(RETRY_TIME)
        # else:
        #     ...


if __name__ == '__main__':
    # logging.basicConfig(
    #     level=logging.DEBUG,
    #     filename='main.log',
    #     filemode='w',
    #     format='%(asctime)s, %(levelname)s, %(message)s'
    # )
    # logger = logging.getLogger(__name__)
    # handler = logging.StreamHandler(sys.stdout)
    # logger.addHandler(handler)
    main()
