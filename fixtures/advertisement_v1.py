import pytest
from pydantic import BaseModel

from clients.v1.item.item_client import ItemV1Client, get_item_v1_client
from clients.v1.item.item_schema import (CreateAdvertisementV1RequestSchema,
                                         CreateAdvertisementV1ResponseSchema)
from clients.v1.seller.seller_client import (SellerV1Client,
                                             get_seller_v1_client)
from clients.v1.statistic.statistic_client import (StatisticV1Client,
                                                   get_statistic_v1_client)
from clients.v2.item.item_client import ItemV2Client
from tools.generators import generate_seller_id
from tools.helpers import delete_advertisement_by_id, get_id_from_response


class AdvertisementV1Fixture(BaseModel):
    request: CreateAdvertisementV1RequestSchema
    response: CreateAdvertisementV1ResponseSchema

    @property
    def id(self) -> str:
        return get_id_from_response(self.response.status)


class AdvertisementsV1Fixture(BaseModel):
    requests: list[CreateAdvertisementV1RequestSchema]
    responses: list[CreateAdvertisementV1ResponseSchema]

    @property
    def id(self) -> list[str]:
        return [get_id_from_response(response.status) for response in self.responses]

    @property
    def seller_id(self) -> int:
        return self.requests[0].seller_id


@pytest.fixture
def item_v1_client() -> ItemV1Client:
    return get_item_v1_client()


@pytest.fixture
def statistic_v1_client() -> StatisticV1Client:
    return get_statistic_v1_client()


@pytest.fixture
def seller_v1_client() -> SellerV1Client:
    return get_seller_v1_client()


@pytest.fixture
def function_v1_advertisement(item_v1_client: ItemV1Client, item_v2_client: ItemV2Client) -> AdvertisementV1Fixture:
    request = CreateAdvertisementV1RequestSchema()
    response = item_v1_client.create_advertisement(request)
    advertisement_v1_fixture = AdvertisementV1Fixture(request=request, response=response)
    advertisement_id = get_id_from_response(response.status)

    yield advertisement_v1_fixture

    delete_advertisement_by_id(item_v1_client, item_v2_client, advertisement_id)


@pytest.fixture
def function_v1_advertisements(item_v1_client: ItemV1Client, item_v2_client: ItemV2Client) -> AdvertisementV1Fixture:
    requests = []
    responses = []
    advertisement_ids = []
    seller_id = generate_seller_id()
    for _ in range(3):
        request = CreateAdvertisementV1RequestSchema(seller_id=seller_id)
        response = item_v1_client.create_advertisement(request)
        advertisement_id = get_id_from_response(response.status)

        requests.append(request)
        responses.append(response)
        advertisement_ids.append(advertisement_id)

    advertisements_v1_fixture = AdvertisementsV1Fixture(requests=requests, responses=responses)

    yield advertisements_v1_fixture

    for advertisement_id in advertisement_ids:
        delete_advertisement_by_id(item_v1_client, item_v2_client, advertisement_id)
