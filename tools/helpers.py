from http import HTTPStatus
from typing import Any

import httpx

from clients.v1.item.item_client import ItemV1Client
from clients.v2.item.item_client import ItemV2Client
from tools.fakers import fake
from tools.logger import get_logger

logger = get_logger('HELPERS')


def get_id_from_response(status: str) -> str:
    return status[23:]


def delete_advertisement_by_id(item_v1_client: ItemV1Client,
                               item_v2_client: ItemV2Client,
                               advertisement_id: str) -> None:
    try:
        get_response = item_v1_client.get_advertisement_api(advertisement_id)
        if get_response.status_code == HTTPStatus.OK:
            item_v2_client.delete_advertisement_api(advertisement_id)
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error during cleanup of {advertisement_id}: {e}")
    except httpx.RequestError as e:
        logger.error(f"Request error during cleanup of {advertisement_id}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during cleanup of {advertisement_id}: {e}", exc_info=True)


def get_request_data_to_negative_tests(field: str, value: Any) -> (dict[str, Any], str):
    request_data = {
        "sellerID": fake.seller_id(),
        "name": fake.name(),
        "price": fake.price(),
        "statistics": {
            "likes": fake.likes(),
            "viewCount": fake.view_count(),
            "contacts": fake.contacts()
        }
    }
    if "." in field:
        parent_field, child_field = field.split(".")
        if parent_field in request_data and isinstance(request_data[parent_field], dict):
            request_data[parent_field][child_field] = value
            field = child_field
    else:
        request_data[field] = value
    return request_data, field
