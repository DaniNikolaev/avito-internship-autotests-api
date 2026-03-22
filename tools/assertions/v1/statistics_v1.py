from http import HTTPStatus

import allure

from clients.v1.errors_schema import (BadRequestErrorResponseSchemaV1,
                                      BadRequestResultSchemaV1,
                                      NotFoundErrorResponseSchemaV1,
                                      NotFoundResultSchemaV1)
from clients.v1.item.item_schema import (CreateAdvertisementV1RequestSchema)
from clients.v1.statistic.statistic_schema import (
    GetStatisticV1ResponseSchema, StatisticV1Schema)
from tools.assertions.base import assert_equal
from tools.assertions.v1.errors_v1 import (assert_equal_bad_request_error_v1,
                                           assert_equal_not_found_error_v1)
from tools.logger import get_logger

logger = get_logger("STATISTICS_V1_ASSERTIONS")


@allure.step("Check statistics v1")
def assert_check_statistics_v1(actual: list[StatisticV1Schema], expected: list[StatisticV1Schema]):
    """
    Проверяет, что фактические данные списка статистики соответствуют ожидаемым.

    :param actual: Фактические данные списка статистики.
    :param expected: Ожидаемые данные списка статистики.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check statistics v1")
    for index, stat in enumerate(expected):
        assert_equal_statistics_v1(actual[index], stat)


@allure.step("Check statistic v1")
def assert_equal_statistics_v1(actual: StatisticV1Schema, expected: StatisticV1Schema):
    """
    Проверяет, что фактические данные статистики соответствуют ожидаемым.

    :param actual: Фактические данные статистики.
    :param expected: Ожидаемые данные статистики.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check statistic v1")
    assert_equal(actual.likes, expected.likes, "likes")
    assert_equal(actual.view_count, expected.view_count, "view_count")
    assert_equal(actual.contacts, expected.contacts, "contacts")


@allure.step("Check get statistic v1 response")
def assert_get_statistic_v1_response(get_statistic_v1_response: GetStatisticV1ResponseSchema,
                                     create_advertisement_v1_request: CreateAdvertisementV1RequestSchema):
    """
    Проверяет, что ответ на получение статистики по объявлению соответствует статистике из запроса на создание
    объявления.

    :param get_statistic_v1_response: Ответ API при запросе данных статистики по объявлению.
    :param create_advertisement_v1_request: Запрос на создание объявления.
    :raises AssertionError: Если данные статистики не совпадают.
    """
    logger.info("Check get statistic v1 response")
    for statistic in get_statistic_v1_response.statistics:
        assert_equal_statistics_v1(statistic, create_advertisement_v1_request.statistics)


@allure.step("Check get statistic v1 bad request response")
def assert_get_statistic_v1_bad_request_response(actual: BadRequestErrorResponseSchemaV1):
    """
    Проверяет ответ при передаче некорректного идентификатора объявления для статистики.

    :param actual: Фактический ответ API.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "Bad request".
    """
    expected = BadRequestErrorResponseSchemaV1(
        result=BadRequestResultSchemaV1(
            message="передан некорректный идентификатор объявления",
            messages={}
        ),
        status=HTTPStatus.BAD_REQUEST
    )

    logger.info("Check get statistic v1 bad request response")
    assert_equal_bad_request_error_v1(actual, expected)


@allure.step("Check get statistic v1 not found response")
def assert_get_statistic_v1_not_found_response(actual: NotFoundErrorResponseSchemaV1, advertisement_id: str):
    """
    Проверяет ответ при запросе статистики несуществующего объявления.

    :param actual: Фактический ответ API.
    :param advertisement_id: ID несуществующего объявления.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "Not found".
    """
    expected = NotFoundErrorResponseSchemaV1(
        result=NotFoundResultSchemaV1(
            message=f"statistic {advertisement_id} not found",
            messages=None
        ),
        status=HTTPStatus.NOT_FOUND
    )

    logger.info(f"Check get statistic v1 not found response for id: {advertisement_id}")
    assert_equal_not_found_error_v1(actual, expected)
