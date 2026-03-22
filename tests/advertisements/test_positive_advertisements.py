from http import HTTPStatus

import allure
import pytest

from clients.v1.errors_schema import NotFoundErrorResponseSchemaV1
from clients.v1.item.item_client import ItemV1Client
from clients.v1.item.item_schema import (CreateAdvertisementV1RequestSchema,
                                         CreateAdvertisementV1ResponseSchema,
                                         GetAdvertisementV1ResponseSchema)
from clients.v1.seller.seller_client import SellerV1Client
from clients.v1.seller.seller_schema import GetAdvertisementsV1ResponseSchema
from clients.v2.item.item_client import ItemV2Client
from fixtures.advertisement_v1 import (AdvertisementsV1Fixture,
                                       AdvertisementV1Fixture)
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.v1.items_v1 import (
    assert_advertisements_v1, assert_create_advertisement_v1_response,
    assert_get_advertisement_v1_not_found_response,
    assert_get_advertisement_v1_response,
    assert_get_advertisements_v1_response)
from tools.helpers import delete_advertisement_by_id, get_id_from_response, get_request_data_to_tests


@allure.epic(AllureEpic.API_TESTING)
@allure.feature(AllureFeature.ADVERTISEMENTS_V1)
@allure.story(AllureStory.POSITIVE_SCENARIOS)
@pytest.mark.regression
@pytest.mark.positive_advertisements_v1
class TestPositiveAdvertisementsV1:

    @allure.title("Test create advertisement v1")
    @allure.tag(AllureTag.POSITIVE, AllureTag.CREATE)
    def test_create_advertisement_v1(self, item_v1_client: ItemV1Client, item_v2_client: ItemV2Client):
        request = CreateAdvertisementV1RequestSchema()
        response = item_v1_client.create_advertisement_api(request)
        response_data = CreateAdvertisementV1ResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_create_advertisement_v1_response(response_data)

        validate_json_schema(response.json(), CreateAdvertisementV1ResponseSchema.model_json_schema())

        delete_advertisement_by_id(item_v1_client, item_v2_client, get_id_from_response(response_data.status))

    @allure.title("Test create advertisement v1 with minimal positive int fields")
    @allure.tag(AllureTag.POSITIVE, AllureTag.POSITIVE_VALUES)
    @pytest.mark.parametrize("field,correct_value", [
        ("sellerID", 1),
        ("price", 1),
        ("statistics.likes", 1),
        ("statistics.viewCount", 1),
        ("statistics.contacts", 1),
    ])
    def test_create_advertisement_v1_with_minimal_positive_int_fields(self,
                                                                      item_v1_client: ItemV1Client,
                                                                      item_v2_client: ItemV2Client,
                                                                      field: str,
                                                                      correct_value: int):
        request_data, field = get_request_data_to_tests(field, correct_value)

        response = item_v1_client.try_create_advertisement_api(request_data)
        response_data = CreateAdvertisementV1ResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_advertisement_v1_response(response_data)

        validate_json_schema(response.json(), CreateAdvertisementV1ResponseSchema.model_json_schema())
        delete_advertisement_by_id(item_v1_client, item_v2_client, get_id_from_response(response_data.status))

    @allure.title("Test get advertisement v1")
    @allure.tag(AllureTag.POSITIVE, AllureTag.GET)
    def test_get_advertisement_v1(self,
                                  item_v1_client: ItemV1Client,
                                  function_v1_advertisement: AdvertisementV1Fixture):
        response = item_v1_client.get_advertisement_api(function_v1_advertisement.id)
        response_data = GetAdvertisementV1ResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_get_advertisement_v1_response(function_v1_advertisement.request, response_data)

        validate_json_schema(response.json(), GetAdvertisementV1ResponseSchema.model_json_schema())

    @allure.title("Test idempotence get advertisement v1")
    @allure.tag(AllureTag.POSITIVE, AllureTag.IDEMPOTENCY, AllureTag.GET)
    def test_idempotence_get_advertisement_v1(self,
                                              item_v1_client: ItemV1Client,
                                              function_v1_advertisement: AdvertisementV1Fixture):
        response1 = item_v1_client.get_advertisement_api(function_v1_advertisement.id)
        response1_data = GetAdvertisementV1ResponseSchema.model_validate_json(response1.text)

        response2 = item_v1_client.get_advertisement_api(function_v1_advertisement.id)
        response2_data = GetAdvertisementV1ResponseSchema.model_validate_json(response2.text)

        assert_status_code(response1.status_code, HTTPStatus.OK)
        assert_status_code(response2.status_code, HTTPStatus.OK)

        assert_advertisements_v1(response1_data.advertisements, response2_data.advertisements)

    @allure.title("Test get advertisements v1")
    @allure.tag(AllureTag.POSITIVE, AllureTag.GET)
    def test_get_advertisements_v1(self,
                                   seller_v1_client: SellerV1Client,
                                   function_v1_advertisements: AdvertisementsV1Fixture):
        response = seller_v1_client.get_all_seller_advertisements_api(function_v1_advertisements.seller_id)
        response_data = GetAdvertisementsV1ResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_get_advertisements_v1_response(response_data, function_v1_advertisements.requests)

        validate_json_schema(response.json(), GetAdvertisementsV1ResponseSchema.model_json_schema())

    @allure.title("Test idempotence get advertisements v1")
    @allure.tag(AllureTag.POSITIVE, AllureTag.IDEMPOTENCY, AllureTag.GET)
    def test_idempotence_get_advertisements_v1(self,
                                               seller_v1_client: SellerV1Client,
                                               function_v1_advertisements: AdvertisementsV1Fixture):
        response1 = seller_v1_client.get_all_seller_advertisements_api(function_v1_advertisements.seller_id)
        response1_data = GetAdvertisementsV1ResponseSchema.model_validate_json(response1.text)
        response2 = seller_v1_client.get_all_seller_advertisements_api(function_v1_advertisements.seller_id)
        response2_data = GetAdvertisementsV1ResponseSchema.model_validate_json(response2.text)

        assert_status_code(response1.status_code, HTTPStatus.OK)
        assert_status_code(response2.status_code, HTTPStatus.OK)

        assert_advertisements_v1(response1_data.advertisements, response2_data.advertisements)

    @allure.title("Test create, get and delete advertisement v1")
    @allure.tag(AllureTag.POSITIVE, AllureTag.CREATE, AllureTag.GET, AllureTag.DELETE)
    @pytest.mark.positive_advertisements_v2
    def test_create_get_and_delete_advertisement(self,
                                                 item_v1_client: ItemV1Client,
                                                 item_v2_client: ItemV2Client):
        create_request = CreateAdvertisementV1RequestSchema()
        create_response = item_v1_client.create_advertisement_api(create_request)
        create_response_data = CreateAdvertisementV1ResponseSchema.model_validate_json(create_response.text)
        assert_status_code(create_response.status_code, HTTPStatus.OK)
        response_id = get_id_from_response(create_response_data.status)

        get_response = item_v1_client.get_advertisement_api(response_id)
        get_response_data = GetAdvertisementV1ResponseSchema.model_validate_json(get_response.text)
        assert_status_code(get_response.status_code, HTTPStatus.OK)
        assert_get_advertisement_v1_response(create_request, get_response_data)

        delete_response = item_v2_client.delete_advertisement_api(response_id)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

    @allure.title("Test create, get all advertisements and delete advertisement v1")
    @allure.tag(AllureTag.POSITIVE, AllureTag.CREATE, AllureTag.GET, AllureTag.DELETE)
    @pytest.mark.positive_advertisements_v2
    def test_create_get_all_and_delete_advertisement(self,
                                                     item_v1_client: ItemV1Client,
                                                     item_v2_client: ItemV2Client,
                                                     seller_v1_client: SellerV1Client):
        create_request = CreateAdvertisementV1RequestSchema()
        create_response = item_v1_client.create_advertisement_api(create_request)
        create_response_data = CreateAdvertisementV1ResponseSchema.model_validate_json(create_response.text)
        assert_status_code(create_response.status_code, HTTPStatus.OK)
        response_id = get_id_from_response(create_response_data.status)

        get_all_response = seller_v1_client.get_all_seller_advertisements_api(create_request.seller_id)
        get_all_response_data = GetAdvertisementsV1ResponseSchema.model_validate_json(get_all_response.text)
        assert_status_code(get_all_response.status_code, HTTPStatus.OK)

        assert_get_advertisements_v1_response(get_all_response_data, [create_request])

        delete_response = item_v2_client.delete_advertisement_api(response_id)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)


@allure.epic(AllureEpic.API_TESTING)
@allure.feature(AllureFeature.ADVERTISEMENTS_V2)
@allure.story(AllureStory.POSITIVE_SCENARIOS)
@pytest.mark.regression
@pytest.mark.positive_advertisements_v2
class TestPositiveAdvertisementsV2:

    @allure.title("Test delete advertisement v2")
    @allure.tag(AllureTag.POSITIVE, AllureTag.DELETE)
    def test_delete_advertisement_v2(self,
                                     item_v2_client: ItemV2Client,
                                     item_v1_client: ItemV1Client,
                                     function_v1_advertisement):
        delete_response = item_v2_client.delete_advertisement_api(function_v1_advertisement.id)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_response = item_v1_client.get_advertisement_api(function_v1_advertisement.id)
        get_response_data = NotFoundErrorResponseSchemaV1.model_validate_json(get_response.text)

        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)

        assert_get_advertisement_v1_not_found_response(get_response_data, function_v1_advertisement.id)

        validate_json_schema(get_response.json(), NotFoundErrorResponseSchemaV1.model_json_schema())

    @allure.title("Test idempotence delete advertisement v2")
    @allure.tag(AllureTag.POSITIVE, AllureTag.IDEMPOTENCY, AllureTag.DELETE)
    def test_idempotence_delete_advertisement_v2(self,
                                                 item_v2_client: ItemV2Client,
                                                 function_v1_advertisement):
        response1 = item_v2_client.delete_advertisement_api(function_v1_advertisement.id)
        response2 = item_v2_client.delete_advertisement_api(function_v1_advertisement.id)
        response3 = item_v2_client.delete_advertisement_api(function_v1_advertisement.id)
        assert_status_code(response1.status_code, HTTPStatus.OK)
        assert_status_code(response2.status_code, HTTPStatus.NOT_FOUND)
        assert_status_code(response3.status_code, HTTPStatus.NOT_FOUND)
