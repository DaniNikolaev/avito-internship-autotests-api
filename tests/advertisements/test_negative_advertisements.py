from http import HTTPStatus
from typing import Any

import allure
import pytest

from clients.v1.errors_schema import (BadRequestErrorResponseSchemaV1,
                                      NotFoundErrorResponseSchemaV1)
from clients.v1.item.item_client import ItemV1Client
from clients.v1.seller.seller_client import SellerV1Client
from clients.v1.seller.seller_schema import GetAdvertisementsV1ResponseSchema
from clients.v2.item.item_client import ItemV2Client
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.v1.items_v1 import (
    assert_create_advertisement_v1_with_empty_fields_bad_request_response,
    assert_create_advertisement_v1_with_incorrect_fields_bad_request_response,
    assert_create_advertisement_v1_with_null_fields_bad_request_response,
    assert_delete_advertisement_v1_bad_request_response,
    assert_delete_advertisement_v1_not_found_response,
    assert_get_advertisement_v1_bad_request_response,
    assert_get_advertisement_v1_not_found_response,
    assert_get_advertisements_v1_bad_request_response,
    assert_get_empty_advertisements_v1_response)
from tools.fakers import fake
from tools.generators import generate_seller_id
from tools.helpers import get_request_data_to_tests


@allure.epic(AllureEpic.API_TESTING)
@allure.feature(AllureFeature.ADVERTISEMENTS_V1)
@allure.story(AllureStory.NEGATIVE_SCENARIOS)
@pytest.mark.regression
@pytest.mark.negative_advertisements_v1
class TestNegativeAdvertisementsV1:

    @allure.title("Test create advertisement v1 with null fields")
    @allure.tag(AllureTag.NEGATIVE, AllureTag.VALIDATION, AllureTag.NULL_FIELDS)
    @pytest.mark.parametrize("field", [
        "sellerID",
        "name",
        "price",
        "statistics.likes",
        "statistics.viewCount",
        "statistics.contacts"
    ])
    def test_create_advertisement_v1_with_null_fields(self, item_v1_client: ItemV1Client, field: str):
        request_data, field = get_request_data_to_tests(field, None)

        response = item_v1_client.try_create_advertisement_api(request_data)
        response_data = BadRequestErrorResponseSchemaV1.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

        assert_create_advertisement_v1_with_null_fields_bad_request_response(response_data, field)

        validate_json_schema(response.json(), BadRequestErrorResponseSchemaV1.model_json_schema())

    @allure.title("Test create advertisement v1 with empty fields")
    @allure.tag(AllureTag.NEGATIVE, AllureTag.VALIDATION, AllureTag.EMPTY_FIELDS)
    @pytest.mark.xfail(
        reason="API returns 400 status code, but in response body message is empty and status is not 400")
    @pytest.mark.parametrize("field", [
        "sellerID",
        "name",
        "price",
        "statistics.likes",
        "statistics.viewCount",
        "statistics.contacts"
    ])
    def test_create_advertisement_v1_with_empty_fields(self, item_v1_client: ItemV1Client, field: str):
        request_data, field = get_request_data_to_tests(field, "")

        response = item_v1_client.try_create_advertisement_api(request_data)
        response_data = BadRequestErrorResponseSchemaV1.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

        assert_create_advertisement_v1_with_empty_fields_bad_request_response(response_data)

        validate_json_schema(response.json(), BadRequestErrorResponseSchemaV1.model_json_schema())

    @allure.title("Test create advertisement v1 with incorrect fields")
    @allure.tag(AllureTag.NEGATIVE, AllureTag.VALIDATION, AllureTag.INCORRECT_TYPES)
    @pytest.mark.xfail(
        reason="API returns 400 status code, but in response body message is empty and status is not 400")
    @pytest.mark.parametrize("field,incorrect_value", [
        ("sellerID", "incorrect"),
        ("sellerID", 0.5),
        ("sellerID", []),
        ("sellerID", False),
        ("sellerID", {}),

        ("name", 123),
        ("name", 0.5),
        ("name", False),
        ("name", []),
        ("name", {}),

        ("price", "incorrect"),
        ("price", 0.5),
        ("price", []),
        ("price", False),
        ("price", {}),

        ("statistics.likes", "incorrect"),
        ("statistics.likes", 0.5),
        ("statistics.likes", []),
        ("statistics.likes", False),
        ("statistics.likes", {}),

        ("statistics.viewCount", "incorrect"),
        ("statistics.viewCount", 0.5),
        ("statistics.viewCount", []),
        ("statistics.viewCount", False),
        ("statistics.viewCount", {}),

        ("statistics.contacts", "incorrect"),
        ("statistics.contacts", 0.5),
        ("statistics.contacts", []),
        ("statistics.contacts", False),
        ("statistics.contacts", {}),
    ])
    def test_create_advertisement_v1_with_incorrect_fields(self,
                                                           item_v1_client: ItemV1Client,
                                                           field: str,
                                                           incorrect_value: Any):
        request_data, field = get_request_data_to_tests(field, incorrect_value)

        response = item_v1_client.try_create_advertisement_api(request_data)
        response_data = BadRequestErrorResponseSchemaV1.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

        assert_create_advertisement_v1_with_incorrect_fields_bad_request_response(response_data)

        validate_json_schema(response.json(), BadRequestErrorResponseSchemaV1.model_json_schema())

    @allure.title("Test create advertisement v1 with negative int fields")
    @allure.tag(AllureTag.NEGATIVE, AllureTag.VALIDATION, AllureTag.NEGATIVE_VALUES)
    @pytest.mark.xfail(
        reason="API returns 200 status code, but should returns 400")
    @pytest.mark.parametrize("field,incorrect_value", [
        ("sellerID", -1),
        ("price", -1),
        ("statistics.likes", -1),
        ("statistics.viewCount", -1),
        ("statistics.contacts", -1),
    ])
    def test_create_advertisement_v1_with_negative_int_fields(self,
                                                              item_v1_client: ItemV1Client,
                                                              field: str,
                                                              incorrect_value: Any):
        request_data, field = get_request_data_to_tests(field, incorrect_value)

        response = item_v1_client.try_create_advertisement_api(request_data)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        response_data = BadRequestErrorResponseSchemaV1.model_validate_json(response.text)

        assert_create_advertisement_v1_with_incorrect_fields_bad_request_response(response_data)

        validate_json_schema(response.json(), BadRequestErrorResponseSchemaV1.model_json_schema())

    @allure.title("Test create advertisement v1 with zero price")
    @allure.tag(AllureTag.ZERO, AllureTag.VALIDATION)
    @pytest.mark.xfail(
        reason="API returns 400 status code, but should returns 200")
    def test_create_advertisement_v1_with_zero_price(self,
                                                     item_v1_client: ItemV1Client,
                                                     ):
        request_data, _ = get_request_data_to_tests("price", 0)

        response = item_v1_client.try_create_advertisement_api(request_data)
        assert_status_code(response.status_code, HTTPStatus.OK)
        response_data = BadRequestErrorResponseSchemaV1.model_validate_json(response.text)

        assert_create_advertisement_v1_with_incorrect_fields_bad_request_response(response_data)

        validate_json_schema(response.json(), BadRequestErrorResponseSchemaV1.model_json_schema())

    @allure.title("Test create advertisement v1 with very long name")
    @allure.tag(AllureTag.ZERO, AllureTag.VALIDATION)
    @pytest.mark.xfail(
        reason="API returns 200 status code, but should returns 400")
    def test_create_advertisement_v1_with_very_long_name(self,
                                                         item_v1_client: ItemV1Client,
                                                         ):
        request_data, _ = get_request_data_to_tests("name", "A" * 1000)

        response = item_v1_client.try_create_advertisement_api(request_data)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        response_data = BadRequestErrorResponseSchemaV1.model_validate_json(response.text)

        assert_create_advertisement_v1_with_incorrect_fields_bad_request_response(response_data)

        validate_json_schema(response.json(), BadRequestErrorResponseSchemaV1.model_json_schema())

    @allure.title("Test create advertisement v1 with zero statistics fields")
    @allure.tag(AllureTag.ZERO, AllureTag.VALIDATION)
    @pytest.mark.xfail(
        reason="API returns 400 status code, but should returns 200")
    @pytest.mark.parametrize("field,incorrect_value", [
        ("statistics.likes", 0),
        ("statistics.viewCount", 0),
        ("statistics.contacts", 0),
    ])
    def test_create_advertisement_v1_with_zero_statistics_fields(self,
                                                                 item_v1_client: ItemV1Client,
                                                                 field: str,
                                                                 incorrect_value: Any):
        request_data, field = get_request_data_to_tests(field, incorrect_value)

        response = item_v1_client.try_create_advertisement_api(request_data)
        assert_status_code(response.status_code, HTTPStatus.OK)
        response_data = BadRequestErrorResponseSchemaV1.model_validate_json(response.text)

        assert_create_advertisement_v1_with_incorrect_fields_bad_request_response(response_data)

        validate_json_schema(response.json(), BadRequestErrorResponseSchemaV1.model_json_schema())

    @allure.title("Test get non exist advertisement v1")
    @allure.tag(AllureTag.NEGATIVE, AllureTag.NOT_FOUND, AllureTag.ADVERTISEMENT_ID)
    def test_get_non_exist_advertisement_v1(self,
                                            item_v1_client: ItemV1Client):
        incorrect_id = fake.uuid()
        response = item_v1_client.get_advertisement_api(incorrect_id)
        response_data = NotFoundErrorResponseSchemaV1.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)

        assert_get_advertisement_v1_not_found_response(response_data, incorrect_id)

        validate_json_schema(response.json(), NotFoundErrorResponseSchemaV1.model_json_schema())

    @allure.title("Test get advertisement v1 with incorrect id")
    @allure.tag(AllureTag.NEGATIVE, AllureTag.BAD_REQUEST, AllureTag.INVALID_UUID)
    def test_get_advertisement_v1_with_incorrect_id(self,
                                                    item_v1_client: ItemV1Client):
        incorrect_id = "incorrect_id"
        response = item_v1_client.get_advertisement_api(incorrect_id)
        response_data = BadRequestErrorResponseSchemaV1.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

        assert_get_advertisement_v1_bad_request_response(response_data, incorrect_id)

        validate_json_schema(response.json(), BadRequestErrorResponseSchemaV1.model_json_schema())

    @allure.title("Test get advertisements v1 with non exist seller id")
    @allure.tag(AllureTag.NEGATIVE, AllureTag.NOT_FOUND, AllureTag.SELLER_ID, AllureTag.EMPTY_LIST)
    def test_get_advertisements_v1_with_non_exist_seller_id(self,
                                                            seller_v1_client: SellerV1Client):
        incorrect_id = generate_seller_id()
        response = seller_v1_client.get_all_seller_advertisements_api(incorrect_id)
        response_data = GetAdvertisementsV1ResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_get_empty_advertisements_v1_response(response_data)

        validate_json_schema(response.json(), GetAdvertisementsV1ResponseSchema.model_json_schema())

    @allure.title("Test get advertisements v1 with incorrect seller id")
    @allure.tag(AllureTag.NEGATIVE, AllureTag.BAD_REQUEST, AllureTag.INVALID_SELLER_ID)
    def test_get_advertisements_v1_with_incorrect_seller_id(self,
                                                            seller_v1_client: SellerV1Client):
        incorrect_id = "incorrect_id"
        response = seller_v1_client.get_all_seller_advertisements_api(incorrect_id)
        response_data = BadRequestErrorResponseSchemaV1.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

        assert_get_advertisements_v1_bad_request_response(response_data)

        validate_json_schema(response.json(), BadRequestErrorResponseSchemaV1.model_json_schema())


@allure.epic(AllureEpic.API_TESTING)
@allure.feature(AllureFeature.ADVERTISEMENTS_V2)
@allure.story(AllureStory.NEGATIVE_SCENARIOS)
@pytest.mark.regression
@pytest.mark.negative_advertisements_v2
class TestNegativeAdvertisementsV2:

    @allure.title("Test delete not exist advertisement v2")
    @allure.tag(AllureTag.NEGATIVE, AllureTag.NOT_FOUND, AllureTag.DELETE)
    @pytest.mark.xfail(reason="API returns 404 status code, but in response body status code 500")
    def test_delete_non_exist_advertisement_v2(self,
                                               item_v2_client: ItemV2Client):
        incorrect_id = fake.uuid()
        response = item_v2_client.delete_advertisement_api(incorrect_id)
        response_data = NotFoundErrorResponseSchemaV1.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)

        assert_delete_advertisement_v1_not_found_response(response_data, incorrect_id)

        validate_json_schema(response.json(), NotFoundErrorResponseSchemaV1.model_json_schema())

    @allure.title("Test delete advertisement v2 with incorrect id")
    @allure.tag(AllureTag.NEGATIVE, AllureTag.BAD_REQUEST, AllureTag.INVALID_UUID, AllureTag.DELETE)
    def test_delete_advertisement_v2_with_incorrect_id(self,
                                                       item_v2_client: ItemV2Client):
        incorrect_id = "incorrect_id"
        response = item_v2_client.delete_advertisement_api(incorrect_id)
        response_data = BadRequestErrorResponseSchemaV1.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

        assert_delete_advertisement_v1_bad_request_response(response_data)

        validate_json_schema(response.json(), BadRequestErrorResponseSchemaV1.model_json_schema())
