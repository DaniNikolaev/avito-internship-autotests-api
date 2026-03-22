import allure
from httpx import Response

from clients.api_client import APIClient
from clients.http_builder import get_http_client
from tools.routes import APIRoutes


class SellerV1Client(APIClient):
    """
    Клиент для работы с /api/1/{sellerID}
    """

    @allure.step("Get all seller advertisements by id {seller_id} v1")
    def get_all_seller_advertisements_api(self, seller_id: int) -> Response:
        """
        Метод v1 получения всех объявлений пользователя.

        :param seller_id: Идентификатор пользователя.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"{APIRoutes.SELLER_V1}/{seller_id}/item")


def get_seller_v1_client() -> SellerV1Client:
    """
    Функция создаёт экземпляр SellerV1Client с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию SellerV1Client.
    """
    return SellerV1Client(client=get_http_client())
