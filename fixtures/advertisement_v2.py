import pytest

from clients.v2.item.item_client import ItemV2Client, get_item_v2_client
from clients.v2.statistic.statistic_client import (StatisticV2Client,
                                                   get_statistic_v2_client)


@pytest.fixture
def item_v2_client() -> ItemV2Client:
    return get_item_v2_client()


@pytest.fixture
def statistic_v2_client() -> StatisticV2Client:
    return get_statistic_v2_client()
