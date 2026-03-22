import allure

from clients.v1.errors_schema import (BadRequestErrorResponseSchemaV1,
                                      BadRequestResultSchemaV1,
                                      NotFoundErrorResponseSchemaV1,
                                      NotFoundResultSchemaV1)
from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("ERRORS_V1_ASSERTIONS")


@allure.step("Check not found error result v1")
def assert_equal_not_found_error_result_v1(actual: NotFoundResultSchemaV1,
                                           expected: NotFoundResultSchemaV1):
    """
    Проверяет, что result ошибки Not Found соответствуют ожидаемамоу.

    :param actual: Фактические данные result.
    :param expected: Ожидаемые данные result.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check not found error result v1")
    assert_equal(actual.message, expected.message, "message")
    assert_equal(actual.messages, expected.messages, "messages")


@allure.step("Check bad request error result v1")
def assert_equal_bad_request_error_result_v1(actual: BadRequestResultSchemaV1,
                                             expected: BadRequestResultSchemaV1):
    """
    Проверяет, что result ошибки Bad Request соответствуют ожидаемамоу.

    :param actual: Фактические данные result.
    :param expected: Ожидаемые данные result.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check bad request error result v1")
    assert_equal(actual.message, expected.message, "message")
    assert_equal(actual.messages, expected.messages, "messages")


@allure.step("Check not found error v1")
def assert_equal_not_found_error_v1(actual: NotFoundErrorResponseSchemaV1,
                                    expected: NotFoundErrorResponseSchemaV1):
    """
    Проверяет, что фактические данные ошибки Not Found соответствуют ожидаемым.

    :param actual: Фактические данные ошибки.
    :param expected: Ожидаемые данные ошибки.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check not found error v1")
    assert_equal_not_found_error_result_v1(actual.result, expected.result)
    assert_equal(actual.status, expected.status, "status")


@allure.step("Check bad request error v1")
def assert_equal_bad_request_error_v1(actual: BadRequestErrorResponseSchemaV1,
                                      expected: BadRequestErrorResponseSchemaV1):
    """
    Проверяет, что фактические данные ошибки Bad Request соответствуют ожидаемым.

    :param actual: Фактические данные ошибки.
    :param expected: Ожидаемые данные ошибки.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check bad request error v1")
    assert_equal_bad_request_error_result_v1(actual.result, expected.result)
    assert_equal(actual.status, expected.status, "status")
