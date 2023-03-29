# Telegram Бот-ассистент
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)

## Описание
Бот обращается к API сервиса Практикум.Домашка, узнает статус домашней работы и оповещает об этом пользователя. Бот умеет логировать свою работу и сообщать о важных проблемах в Telegram.

## Возможности
- Проверяет статусы домашней работы (их всего три)
- Оповещает пользователя о статусе домашней работы в телеграме
- Оповещает пользователя, если появились неполадки в доступе
- Логирует свою работу

## Технологии
 - Python 3.7.13
 - python-telegram-bot 13.7
 - подробнее см. прилагаемый файл зависимостей requrements.txt

## Установка
Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:Alimovriq/homework_bot.git
```

```bash
cd homework_bot
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv env
```

```bash
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

В консоле импортируем токены для Яндекс.Практикум и для Телеграмм:

```bash
export PRACTICUM_TOKEN=<PRACTICUM_TOKEN>
export TELEGRAM_TOKEN=<TELEGRAM_TOKEN>
export CHAT_ID=<CHAT_ID>
```

Запустить проект:

```
python3 manage.py homework.py
```

### Автор
Алимов Ринат
https://github.com/Alimovriq