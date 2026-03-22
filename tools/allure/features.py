from enum import Enum


class AllureFeature(str, Enum):
    """Фичи/функциональности для Allure отчетов"""
    ADVERTISEMENTS_V1 = "Объявления v1"
    ADVERTISEMENTS_V2 = "Объявления v2"
    STATISTICS_V1 = "Статистика v1"
    STATISTICS_V2 = "Статистика v2"
    SELLER_V1 = "Продавцы v1"
