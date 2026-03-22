import allure
from httpx import Response

from clients.api_client import APIClient
from clients.http_builder import get_http_client
from tools.routes import APIRoutes


class ItemV2Client(APIClient):
    """
    Клиент для работы с /api/2/item
    """

    @allure.step("Delete advertisement by id {advertisement_id} v2")
    def delete_advertisement_api(self, advertisement_id: str) -> Response:
        """
        Метод удаления объявления v2.

        :param advertisement_id: Идентификатор объявления.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(f"{APIRoutes.ITEM_V2}/{advertisement_id}")


def get_item_v2_client() -> ItemV2Client:
    """
    Функция создаёт экземпляр ItemV2Client с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию ItemV2Client.
    """
    return ItemV2Client(client=get_http_client())
