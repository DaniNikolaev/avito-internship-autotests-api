import allure
from httpx import Response

from clients.api_client import APIClient
from clients.http_builder import get_http_client
from clients.v1.item.item_schema import (CreateAdvertisementV1RequestSchema,
                                         CreateAdvertisementV1ResponseSchema,
                                         GetAdvertisementV1ResponseSchema)
from tools.routes import APIRoutes


class ItemV1Client(APIClient):
    """
    Клиент для работы с /api/1/item
    """

    @allure.step("Get advertisement by id {advertisement_id} v1")
    def get_advertisement_api(self, advertisement_id: str) -> Response:
        """
        Метод получения объявления.

        :param advertisement_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"{APIRoutes.ITEM_V1}/{advertisement_id}")

    def get_advertisement(self, advertisement_id: str) -> GetAdvertisementV1ResponseSchema:
        """
        Метод получения объявления.

        :param advertisement_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта json
        """
        response = self.get_advertisement_api(advertisement_id)
        return GetAdvertisementV1ResponseSchema.model_validate_json(response.text)

    @allure.step("Create advertisement v1")
    def create_advertisement_api(self,
                                 request: CreateAdvertisementV1RequestSchema) -> Response:
        """
        Метод создания объявления.

        :param request: Словарь с sellerID, name, price, statistics: {likes, viewCount, contacts}
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post(APIRoutes.ITEM_V1, json=request.model_dump(by_alias=True))

    @allure.step("Try_create advertisement v1")
    def try_create_advertisement_api(self, request: dict) -> Response:
        """
        Метод попытки создания объявления.

        :param request: Словарь с sellerID, name, price, statistics: {likes, viewCount, contacts}
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post(APIRoutes.ITEM_V1, json=request)

    @allure.step("Create advertisement v1")
    def create_advertisement(self, request: CreateAdvertisementV1RequestSchema) -> CreateAdvertisementV1ResponseSchema:
        """
        Метод создания объявления.

        :param request: Словарь с sellerID, name, price, statistics: {likes, viewCount, contacts}
        :return: Ответ от сервера в виде объекта json
        """
        response = self.create_advertisement_api(request)
        return CreateAdvertisementV1ResponseSchema.model_validate_json(response.text)


def get_item_v1_client() -> ItemV1Client:
    """
    Функция создаёт экземпляр ItemV1Client с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию ItemV1Client.
    """
    return ItemV1Client(client=get_http_client())
