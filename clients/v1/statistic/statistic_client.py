import allure
from httpx import Response

from clients.api_client import APIClient
from clients.http_builder import get_http_client
from tools.routes import APIRoutes


class StatisticV1Client(APIClient):
    """
    Клиент для работы с /api/1/statistic
    """

    @allure.step("Get statistic on an advertisement by id {advertisement_id} v1")
    def get_statistic_api(self, advertisement_id: str) -> Response:
        """
        Метод v1 получения статистики по объявлению.

        :param advertisement_id: Идентификатор объявления.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"{APIRoutes.STATISTIC_V1}/{advertisement_id}")


def get_statistic_v1_client() -> StatisticV1Client:
    """
    Функция создаёт экземпляр StatisticV1Client с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию StatisticV1Client.
    """
    return StatisticV1Client(client=get_http_client())
