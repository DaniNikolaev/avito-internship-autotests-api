import allure
from httpx import Response

from clients.api_client import APIClient
from clients.http_builder import get_http_client
from tools.routes import APIRoutes


class StatisticV2Client(APIClient):
    """
    Клиент для работы с /api/2/statistic
    """

    @allure.step("Get statistic on an advertisement by id {advertisement_id} v2")
    def get_statistic_api(self, advertisement_id: str) -> Response:
        """
        Метод получения статистики по объявлению v2.

        :param advertisement_id: Идентификатор объявления.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"{APIRoutes.STATISTIC_V2}/{advertisement_id}")


def get_statistic_v2_client() -> StatisticV2Client:
    """
    Функция создаёт экземпляр StatisticV2Client с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию StatisticV2Client.
    """
    return StatisticV2Client(client=get_http_client())
