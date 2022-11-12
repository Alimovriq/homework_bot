class HomeworkStatusError(Exception):
    """Ошибка в статусе домашей работы."""


class RequestExceptionError(Exception):
    """Ошибка запроса."""


class JSONDecodeError(Exception):
    """Ответ API не соответствует ожидаемому."""
