from http import HTTPStatus

import allure

from clients.v1.errors_schema import (BadRequestErrorResponseSchemaV1,
                                      BadRequestResultSchemaV1,
                                      NotFoundErrorResponseSchemaV1,
                                      NotFoundResultSchemaV1)
from clients.v1.item.item_schema import (AdvertisementV1Schema,
                                         CreateAdvertisementV1RequestSchema,
                                         CreateAdvertisementV1ResponseSchema,
                                         GetAdvertisementV1ResponseSchema)
from clients.v1.seller.seller_schema import GetAdvertisementsV1ResponseSchema
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.v1.errors_v1 import (assert_equal_bad_request_error_v1,
                                           assert_equal_not_found_error_v1)
from tools.assertions.v1.statistics_v1 import assert_equal_statistics_v1
from tools.helpers import get_id_from_response
from tools.logger import get_logger

logger = get_logger("ADVERTISEMENTS_V1_ASSERTIONS")


@allure.step("Check advertisement v1")
def assert_advertisement_v1(actual: AdvertisementV1Schema, expected: AdvertisementV1Schema):
    """
    Проверяет, что фактические данные объявления соответствуют ожидаемым.

    :param actual: Фактические данные объявления.
    :param expected: Ожидаемые данные объявления.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check advertisement v1")
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.seller_id, expected.seller_id, "seller_id")
    assert_equal(actual.name, expected.name, "name")
    assert_equal(actual.price, expected.price, "price")
    assert_equal_statistics_v1(actual.statistics, expected.statistics)
    assert_equal(actual.created_at, expected.created_at, "created_at")


@allure.step("Check advertisements v1")
def assert_advertisements_v1(actual: list[AdvertisementV1Schema], expected: list[AdvertisementV1Schema]):
    """
    Проверяет, что фактические данные списка объявлений соответствуют ожидаемым.

    :param actual: Фактические данные списка объявлений.
    :param expected: Ожидаемые данные списка объявлений.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check advertisements v1")
    for index, adv in enumerate(expected):
        assert_advertisement_v1(actual[index], adv)


@allure.step("Check create advertisement v1 response")
def assert_create_advertisement_v1_response(response: CreateAdvertisementV1ResponseSchema):
    """
    Проверяет, что ответ на создание объявления соответствует ожидаемому формату.

    :param response: Ответ API при создании объявления.
    :raises AssertionError: Если статус ответа не соответствует ожидаемому.
    """
    logger.info("Check create advertisement v1 response")
    response_id = get_id_from_response(response.status)
    assert_equal(f"Сохранили объявление - {response_id}", response.status, "status")


@allure.step("Check create advertisement v1 with null fields bad request response")
def assert_create_advertisement_v1_with_null_fields_bad_request_response(actual: BadRequestErrorResponseSchemaV1,
                                                                         field: str):
    """
    Проверяет ответ при передаче null в обязательные поля.

    :param actual: Фактический ответ API.
    :param field: Название поля, в которое был передан null.
    :raises AssertionError: Если фактический ответ не соответствует ожидаемой ошибке.
    """
    expected = BadRequestErrorResponseSchemaV1(
        result=BadRequestResultSchemaV1(
            message=f"поле {field} обязательно",
            messages={}
        ),
        status=HTTPStatus.BAD_REQUEST
    )

    logger.info(f"Check create advertisement v1 with null fields bad request response for field: {field}")
    assert_equal_bad_request_error_v1(actual, expected)


@allure.step("Check create advertisement v1 with empty fields bad request response")
def assert_create_advertisement_v1_with_empty_fields_bad_request_response(actual: BadRequestErrorResponseSchemaV1):
    """
    Проверяет ответ при передаче пустых значений в обязательные поля.

    :param actual: Фактический ответ API.
    :raises AssertionError: Если фактический ответ не соответствует ожидаемой ошибке.
    """
    expected = BadRequestErrorResponseSchemaV1(
        result=BadRequestResultSchemaV1(
            message="не передан объект - объявление",
            messages={}
        ),
        status=HTTPStatus.BAD_REQUEST
    )

    logger.info("Check create advertisement v1 with empty fields bad request response")
    assert_equal_bad_request_error_v1(actual, expected)


@allure.step("Check create advertisement v1 with incorrect fields bad request response")
def assert_create_advertisement_v1_with_incorrect_fields_bad_request_response(actual: BadRequestErrorResponseSchemaV1):
    """
    Проверяет ответ при передаче некорректных типов данных в поля.

    :param actual: Фактический ответ API.
    :raises AssertionError: Если фактический ответ не соответствует ожидаемой ошибке.
    """
    expected = BadRequestErrorResponseSchemaV1(
        result=BadRequestResultSchemaV1(
            message="не передано тело объявления",
            messages={}
        ),
        status=HTTPStatus.BAD_REQUEST
    )

    logger.info("Check create advertisement v1 with incorrect fields bad request response")
    assert_equal_bad_request_error_v1(actual, expected)


@allure.step("Check that advertisement create request equals to advertisement get response")
def assert_equal_advertisement_request_and_response(request: CreateAdvertisementV1RequestSchema,
                                                    response: AdvertisementV1Schema):
    """
    Проверяет соответствие данных запроса на создание и ответа на получение объявления.

    :param request: Запрос на создание объявления.
    :param response: Ответ на запрос получения объявления.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check advertisement request equals to get response")
    assert_equal(request.seller_id, response.seller_id, "seller_id")
    assert_equal(request.name, response.name, "name")
    assert_equal(request.price, response.price, "price")
    assert_equal_statistics_v1(request.statistics, response.statistics)


@allure.step("Check get advertisement v1 response")
def assert_get_advertisement_v1_response(request: CreateAdvertisementV1RequestSchema,
                                         response: GetAdvertisementV1ResponseSchema):
    """
    Проверяет, что ответ на получение объявления соответствует запросу на его создание.

    :param request: Данные запроса на создание объявления.
    :param response: Ответ на запрос получения объявления.
    :raises AssertionError: Если данные из запроса и ответа не совпадают.
    """
    logger.info("Check get advertisement v1 response")
    for adv in response.advertisements:
        assert_equal_advertisement_request_and_response(request, adv)


@allure.step("Check get advertisements v1 response")
def assert_get_advertisements_v1_response(get_advertisements_response: GetAdvertisementsV1ResponseSchema,
                                          create_advertisement_requests: list[CreateAdvertisementV1RequestSchema]):
    """
    Проверяет, что ответ на получение списка объявлений соответствует запросам на их создание.

    :param get_advertisements_response: Ответ API при запросе списка объявлений.
    :param create_advertisement_requests: Список запросов на создание объявлений.
    :raises AssertionError: Если данные объявлений не совпадают.
    """
    logger.info("Check get advertisements v1 response")
    assert_length(get_advertisements_response.advertisements, create_advertisement_requests, "advertisements")

    for index, advertisement in enumerate(create_advertisement_requests):
        assert_equal_advertisement_request_and_response(
            advertisement, get_advertisements_response.advertisements[index]
        )


@allure.step("Check get empty advertisements v1 response")
def assert_get_empty_advertisements_v1_response(get_advertisements_response: GetAdvertisementsV1ResponseSchema):
    """
    Проверяет, что ответ на получение списка объявлений возвращает пустой массив.

    :param get_advertisements_response: Ответ API при запросе списка объявлений.
    :raises AssertionError: Если ответ не является пустым массивом.
    """
    logger.info("Check get empty advertisements v1 response")
    assert_length(get_advertisements_response.advertisements, [], "advertisements")


@allure.step("Check get advertisement v1 not found response")
def assert_get_advertisement_v1_not_found_response(actual: NotFoundErrorResponseSchemaV1, advertisement_id: str):
    """
    Проверяет ответ при запросе несуществующего объявления.

    :param actual: Фактический ответ API.
    :param advertisement_id: ID несуществующего объявления.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "Not found".
    """
    expected = NotFoundErrorResponseSchemaV1(
        result=NotFoundResultSchemaV1(
            message=f"item {advertisement_id} not found",
            messages=None
        ),
        status=HTTPStatus.NOT_FOUND
    )

    logger.info(f"Check get advertisement v1 not found response for id: {advertisement_id}")
    assert_equal_not_found_error_v1(actual, expected)


@allure.step("Check get advertisements v1 bad request response")
def assert_get_advertisements_v1_bad_request_response(actual: BadRequestErrorResponseSchemaV1):
    """
    Проверяет ответ при передаче некорректного идентификатора продавца.

    :param actual: Фактический ответ API.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "Bad request".
    """
    expected = BadRequestErrorResponseSchemaV1(
        result=BadRequestResultSchemaV1(
            message="передан некорректный идентификатор продавца",
            messages={}
        ),
        status=HTTPStatus.BAD_REQUEST
    )

    logger.info("Check get advertisements v1 bad request response")
    assert_equal_bad_request_error_v1(actual, expected)


@allure.step("Check get advertisement v1 bad request response")
def assert_get_advertisement_v1_bad_request_response(actual: BadRequestErrorResponseSchemaV1, advertisement_id: str):
    """
    Проверяет ответ при передаче некорректного UUID объявления.

    :param actual: Фактический ответ API.
    :param advertisement_id: Некорректный ID объявления.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "Bad request".
    """
    expected = BadRequestErrorResponseSchemaV1(
        result=BadRequestResultSchemaV1(
            message=f"ID айтема не UUID: {advertisement_id}",
            messages={}
        ),
        status=HTTPStatus.BAD_REQUEST
    )

    logger.info(f"Check get advertisement v1 bad request response for id: {advertisement_id}")
    assert_equal_bad_request_error_v1(actual, expected)


@allure.step("Check delete advertisement v1 not found response")
def assert_delete_advertisement_v1_not_found_response(actual: NotFoundErrorResponseSchemaV1, advertisement_id: str):
    """
    Проверяет ответ при удалении несуществующего объявления.

    :param actual: Фактический ответ API.
    :param advertisement_id: ID несуществующего объявления.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "Not found".
    """
    expected = NotFoundErrorResponseSchemaV1(
        result=NotFoundResultSchemaV1(
            message="",
            messages=None
        ),
        status=HTTPStatus.NOT_FOUND
    )

    logger.info(f"Check delete advertisement v1 not found response for id: {advertisement_id}")
    assert_equal_not_found_error_v1(actual, expected)


@allure.step("Check delete advertisement v1 bad request response")
def assert_delete_advertisement_v1_bad_request_response(actual: BadRequestErrorResponseSchemaV1):
    """
    Проверяет ответ при попытке удаления с некорректным ID объявления.

    :param actual: Фактический ответ API.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "Bad request".
    """
    expected = BadRequestErrorResponseSchemaV1(
        result=BadRequestResultSchemaV1(
            message="переданный id айтема некорректный",
            messages={}
        ),
        status=HTTPStatus.BAD_REQUEST
    )

    logger.info("Check delete advertisement v1 bad request response")
    assert_equal_bad_request_error_v1(actual, expected)
