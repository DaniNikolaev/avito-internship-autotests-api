from enum import Enum


class AllureStory(str, Enum):
    """Пользовательские истории для Allure отчетов"""
    POSITIVE_SCENARIOS = "Позитивные сценарии"
    NEGATIVE_SCENARIOS = "Негативные сценарии"
    IDEMPOTENCY = "Идемпотентность"
    CREATE_ADVERTISEMENT = "Создание объявления"
    GET_ADVERTISEMENT = "Получение объявления"
    GET_ADVERTISEMENTS = "Получение списка объявлений"
    DELETE_ADVERTISEMENT = "Удаление объявления"
    GET_STATISTICS = "Получение статистики"
