from http import HTTPStatus

import allure
import pytest

from clients.v1.errors_schema import (BadRequestErrorResponseSchemaV1,
                                      NotFoundErrorResponseSchemaV1)
from clients.v1.statistic.statistic_client import StatisticV1Client
from clients.v1.statistic.statistic_schema import GetStatisticV1ResponseSchema
from clients.v2.errors_schema import (BadRequestErrorResponseSchemaV2,
                                      NotFoundErrorResponseSchemaV2)
from clients.v2.item.item_client import ItemV2Client
from clients.v2.statistic.statistic_client import StatisticV2Client
from clients.v2.statistic.statistic_schema import GetStatisticV2ResponseSchema
from fixtures.advertisement_v1 import AdvertisementV1Fixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.v1.statistics_v1 import (
    assert_check_statistics_v1, assert_get_statistic_v1_bad_request_response,
    assert_get_statistic_v1_not_found_response,
    assert_get_statistic_v1_response)
from tools.assertions.v2.statistics_v2 import (
    assert_check_statistics_v2, assert_get_statistic_v2_bad_request_response,
    assert_get_statistic_v2_not_found_response,
    assert_get_statistic_v2_response)
from tools.fakers import fake


@allure.epic(AllureEpic.API_TESTING)
@allure.feature(AllureFeature.STATISTICS_V1)
@allure.story(AllureStory.GET_STATISTICS)
@pytest.mark.regression
@pytest.mark.statistics_v1
class TestStatisticsV1:

    @allure.title("Test get statistic v1")
    @allure.tag(AllureTag.POSITIVE, AllureTag.GET, AllureTag.STATISTICS)
    def test_get_statistic_v1(self,
                              statistic_v1_client: StatisticV1Client,
                              function_v1_advertisement: AdvertisementV1Fixture):
        response = statistic_v1_client.get_statistic_api(function_v1_advertisement.id)
        response_data = GetStatisticV1ResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_get_statistic_v1_response(response_data, function_v1_advertisement.request)

        validate_json_schema(response.json(), GetStatisticV1ResponseSchema.model_json_schema())

    @allure.title("Test idempotence get statistic v1")
    @allure.tag(AllureTag.POSITIVE, AllureTag.IDEMPOTENCY, AllureTag.GET, AllureTag.STATISTICS)
    def test_idempotence_get_statistic_v1(self,
                                          statistic_v1_client: StatisticV1Client,
                                          function_v1_advertisement: AdvertisementV1Fixture):
        response1 = statistic_v1_client.get_statistic_api(function_v1_advertisement.id)
        response1_data = GetStatisticV1ResponseSchema.model_validate_json(response1.text)
        response2 = statistic_v1_client.get_statistic_api(function_v1_advertisement.id)
        response2_data = GetStatisticV1ResponseSchema.model_validate_json(response2.text)

        assert_status_code(response1.status_code, HTTPStatus.OK)
        assert_status_code(response2.status_code, HTTPStatus.OK)

        assert_check_statistics_v1(response1_data.statistics, response2_data.statistics)

    @allure.title("Test get non exist statistic v1")
    @allure.tag(AllureTag.NEGATIVE, AllureTag.NOT_FOUND, AllureTag.STATISTICS)
    def test_get_non_exists_statistic_v1(self,
                                         statistic_v1_client: StatisticV1Client):
        incorrect_id = fake.uuid()
        response = statistic_v1_client.get_statistic_api(incorrect_id)
        response_data = NotFoundErrorResponseSchemaV1.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)

        assert_get_statistic_v1_not_found_response(response_data, incorrect_id)

        validate_json_schema(response.json(), NotFoundErrorResponseSchemaV1.model_json_schema())

    @allure.title("Test get statistic v1 with incorrect advertisement_id")
    @allure.tag(AllureTag.NEGATIVE, AllureTag.BAD_REQUEST, AllureTag.INVALID_UUID, AllureTag.STATISTICS)
    def test_get_statistic_v1_with_incorrect_advertisement_id(self,
                                                              statistic_v1_client: StatisticV1Client):
        incorrect_id = "incorrect_id"
        response = statistic_v1_client.get_statistic_api(incorrect_id)
        response_data = BadRequestErrorResponseSchemaV1.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

        assert_get_statistic_v1_bad_request_response(response_data)

        validate_json_schema(response.json(), BadRequestErrorResponseSchemaV1.model_json_schema())

    @allure.title("Test get statistic v1 after delete advertisement")
    @allure.tag(AllureTag.NEGATIVE, AllureTag.NOT_FOUND, AllureTag.STATISTICS)
    @pytest.mark.xfail(reason="API returns 200 status code, but should returns 404")
    def test_get_statistic_v1_after_delete_advertisement(self,
                                                         statistic_v1_client: StatisticV1Client,
                                                         item_v2_client: ItemV2Client,
                                                         function_v1_advertisement: AdvertisementV1Fixture):
        delete_response = item_v2_client.delete_advertisement_api(function_v1_advertisement.id)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_response = statistic_v1_client.get_statistic_api(function_v1_advertisement.id)
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)

        get_response_data = NotFoundErrorResponseSchemaV1.model_validate_json(get_response.text)

        assert_get_statistic_v1_not_found_response(get_response_data, function_v1_advertisement.id)

        validate_json_schema(get_response.json(), NotFoundErrorResponseSchemaV1.model_json_schema())


@allure.epic(AllureEpic.API_TESTING)
@allure.feature(AllureFeature.STATISTICS_V2)
@allure.story(AllureStory.GET_STATISTICS)
@pytest.mark.regression
@pytest.mark.statistics_v2
class TestStatisticsV2:

    @allure.title("Test get statistic v2")
    @allure.tag(AllureTag.POSITIVE, AllureTag.GET, AllureTag.STATISTICS)
    def test_get_statistic_v2(self,
                              statistic_v2_client: StatisticV2Client,
                              function_v1_advertisement: AdvertisementV1Fixture):
        response = statistic_v2_client.get_statistic_api(function_v1_advertisement.id)
        response_data = GetStatisticV2ResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_get_statistic_v2_response(response_data, function_v1_advertisement.request)

    @allure.title("Test idempotence get statistic v2")
    @allure.tag(AllureTag.POSITIVE, AllureTag.IDEMPOTENCY, AllureTag.GET, AllureTag.STATISTICS)
    def test_idempotence_get_statistic_v2(self,
                                          statistic_v2_client: StatisticV2Client,
                                          function_v1_advertisement: AdvertisementV1Fixture):
        response1 = statistic_v2_client.get_statistic_api(function_v1_advertisement.id)
        response1_data = GetStatisticV2ResponseSchema.model_validate_json(response1.text)
        response2 = statistic_v2_client.get_statistic_api(function_v1_advertisement.id)
        response2_data = GetStatisticV2ResponseSchema.model_validate_json(response2.text)

        assert_status_code(response1.status_code, HTTPStatus.OK)
        assert_status_code(response2.status_code, HTTPStatus.OK)

        assert_check_statistics_v2(response1_data.statistics, response2_data.statistics)

    @allure.title("Test get statistic v2 after delete advertisement")
    @allure.tag(AllureTag.NEGATIVE, AllureTag.NOT_FOUND, AllureTag.STATISTICS)
    @pytest.mark.xfail(reason="API returns 200 status code, but should returns 404")
    def test_get_statistic_v2_after_delete_advertisement(self,
                                                         statistic_v2_client: StatisticV1Client,
                                                         item_v2_client: ItemV2Client,
                                                         function_v1_advertisement: AdvertisementV1Fixture):
        delete_response = item_v2_client.delete_advertisement_api(function_v1_advertisement.id)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_response = statistic_v2_client.get_statistic_api(function_v1_advertisement.id)
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)

        get_response_data = NotFoundErrorResponseSchemaV2.model_validate_json(get_response.text)

        assert_get_statistic_v2_not_found_response(get_response_data, function_v1_advertisement.id)

        validate_json_schema(get_response.json(), NotFoundErrorResponseSchemaV2.model_json_schema())

    @allure.title("Test get non exist statistic v2")
    @allure.tag(AllureTag.NEGATIVE, AllureTag.NOT_FOUND, AllureTag.STATISTICS)
    def test_get_non_exists_statistic_v2(self,
                                         statistic_v2_client: StatisticV2Client):
        incorrect_id = fake.uuid()
        response = statistic_v2_client.get_statistic_api(incorrect_id)
        response_data = NotFoundErrorResponseSchemaV2.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)

        assert_get_statistic_v2_not_found_response(response_data, incorrect_id)

        validate_json_schema(response.json(), NotFoundErrorResponseSchemaV2.model_json_schema())

    @allure.title("Test get statistic v2 with incorrect advertisement_id")
    @allure.tag(AllureTag.NEGATIVE, AllureTag.BAD_REQUEST, AllureTag.INVALID_UUID, AllureTag.STATISTICS)
    @pytest.mark.xfail(reason="API returns 404 status code, but should returns 400 status code")
    def test_get_statistic_v2_with_incorrect_advertisement_id(self,
                                                              statistic_v2_client: StatisticV2Client):
        incorrect_id = "incorrect_id"
        response = statistic_v2_client.get_statistic_api(incorrect_id)
        response_data = BadRequestErrorResponseSchemaV2.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

        assert_get_statistic_v2_bad_request_response(response_data)

        validate_json_schema(response.json(), BadRequestErrorResponseSchemaV2.model_json_schema())
