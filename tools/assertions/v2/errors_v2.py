import allure

from clients.v2.errors_schema import (BadRequestErrorResponseSchemaV2,
                                      BadRequestResultSchemaV2,
                                      NotFoundErrorResponseSchemaV2,
                                      NotFoundResultSchemaV2)
from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("ERRORS_V2_ASSERTIONS")


@allure.step("Check not found error result v2")
def assert_equal_not_found_error_result_v2(actual: NotFoundResultSchemaV2,
                                           expected: NotFoundResultSchemaV2):
    """
    Проверяет, что result ошибки Not Found соответствуют ожидаемамоу.

    :param actual: Фактические данные result.
    :param expected: Ожидаемые данные result.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check not found error result v2")
    assert_equal(actual.message, expected.message, "message")
    assert_equal(actual.messages, expected.messages, "messages")


@allure.step("Check bad request error result v2")
def assert_equal_bad_request_error_result_v2(actual: BadRequestResultSchemaV2,
                                             expected: BadRequestResultSchemaV2):
    """
    Проверяет, что result ошибки Bad Request соответствуют ожидаемамоу.

    :param actual: Фактические данные result.
    :param expected: Ожидаемые данные result.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check bad request error result v2")
    assert_equal(actual.message, expected.message, "message")
    assert_equal(actual.messages, expected.messages, "messages")


@allure.step("Check not found error v2")
def assert_equal_not_found_error_v2(actual: NotFoundErrorResponseSchemaV2,
                                    expected: NotFoundErrorResponseSchemaV2):
    """
    Проверяет, что фактические данные ошибки Not Found соответствуют ожидаемым.

    :param actual: Фактические данные ошибки.
    :param expected: Ожидаемые данные ошибки.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check not found error v2")
    assert_equal_not_found_error_result_v2(actual.result, expected.result)
    assert_equal(actual.status, expected.status, "status")


@allure.step("Check bad request error v2")
def assert_equal_bad_request_error_v2(actual: BadRequestErrorResponseSchemaV2,
                                      expected: BadRequestErrorResponseSchemaV2):
    """
    Проверяет, что фактические данные ошибки Bad Request соответствуют ожидаемым.

    :param actual: Фактические данные ошибки.
    :param expected: Ожидаемые данные ошибки.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check bad request error v2")
    assert_equal_bad_request_error_result_v2(actual.result, expected.result)
    assert_equal(actual.status, expected.status, "status")
