from enum import Enum


class APIRoutes(str, Enum):
    ITEM_V1 = "/api/1/item"
    ITEM_V2 = "/api/2/item"
    STATISTIC_V1 = "/api/1/statistic"
    STATISTIC_V2 = "/api/2/statistic"
    SELLER_V1 = "/api/1"

    def __str__(self):
        return self.value
