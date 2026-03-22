from http import HTTPStatus

import allure

from clients.v1.item.item_schema import (CreateAdvertisementV1RequestSchema)
from clients.v1.statistic.statistic_schema import (StatisticV1Schema)
from clients.v2.errors_schema import (BadRequestErrorResponseSchemaV2,
                                      BadRequestResultSchemaV2,
                                      NotFoundErrorResponseSchemaV2,
                                      NotFoundResultSchemaV2)
from clients.v2.statistic.statistic_schema import (
    GetStatisticV2ResponseSchema, StatisticV2Schema)
from tools.assertions.base import assert_equal
from tools.assertions.v2.errors_v2 import (assert_equal_bad_request_error_v2,
                                           assert_equal_not_found_error_v2)
from tools.logger import get_logger

logger = get_logger("STATISTICS_V2_ASSERTIONS")


@allure.step("Check statistics v2")
def assert_check_statistics_v2(actual: list[StatisticV2Schema], expected: list[StatisticV2Schema]):
    """
    Проверяет, что фактические данные списка статистики соответствуют ожидаемым.

    :param actual: Фактические данные списка статистики.
    :param expected: Ожидаемые данные списка статистики.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check statistics v2")
    for index, stat in enumerate(expected):
        assert_equal_statistics_v2(actual[index], stat)


@allure.step("Check statistic v2")
def assert_equal_statistics_v2(actual: StatisticV2Schema, expected: StatisticV2Schema | StatisticV1Schema):
    """
    Проверяет, что фактические данные статистики соответствуют ожидаемым.

    :param actual: Фактические данные статистики.
    :param expected: Ожидаемые данные статистики.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check statistic v2")
    assert_equal(actual.likes, expected.likes, "likes")
    assert_equal(actual.view_count, expected.view_count, "view_count")
    assert_equal(actual.contacts, expected.contacts, "contacts")


@allure.step("Check get statistic v2 response")
def assert_get_statistic_v2_response(get_statistic_v2_response: GetStatisticV2ResponseSchema,
                                     create_advertisement_v1_request: CreateAdvertisementV1RequestSchema):
    """
    Проверяет, что ответ на получение статистики по объявлению соответствует статистике из запроса на создание
    объявления.

    :param get_statistic_v2_response: Ответ API при запросе данных статистики по объявлению.
    :param create_advertisement_v1_request: Запрос на создание объявления.
    :raises AssertionError: Если данные статистики не совпадают.
    """
    logger.info("Check get statistic v2 response")
    for statistic in get_statistic_v2_response.statistics:
        assert_equal_statistics_v2(statistic, create_advertisement_v1_request.statistics)


@allure.step("Check get statistic v2 bad request response")
def assert_get_statistic_v2_bad_request_response(actual: BadRequestErrorResponseSchemaV2):
    """
    Проверяет ответ при передаче некорректного идентификатора объявления для статистики.

    :param actual: Фактический ответ API.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "Bad request".
    """
    expected = BadRequestErrorResponseSchemaV2(
        result=BadRequestResultSchemaV2(
            message="передан некорректный идентификатор объявления",
            messages=None
        ),
        status=HTTPStatus.BAD_REQUEST
    )

    logger.info("Check get statistic v2 bad request response")
    assert_equal_bad_request_error_v2(actual, expected)


@allure.step("Check get statistic v2 not found response")
def assert_get_statistic_v2_not_found_response(actual: NotFoundErrorResponseSchemaV2, advertisement_id: str):
    """
    Проверяет ответ при запросе статистики несуществующего объявления.

    :param actual: Фактический ответ API.
    :param advertisement_id: ID несуществующего объявления.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "Not found".
    """
    expected = NotFoundErrorResponseSchemaV2(
        result=NotFoundResultSchemaV2(
            message=f"statistic {advertisement_id} not found",
            messages=None
        ),
        status=HTTPStatus.NOT_FOUND
    )

    logger.info(f"Check get statistic v2 not found response for id: {advertisement_id}")
    assert_equal_not_found_error_v2(actual, expected)
