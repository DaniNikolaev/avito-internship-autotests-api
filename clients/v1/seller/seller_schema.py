from pydantic import BaseModel, ConfigDict, Field, RootModel

from clients.v1.item.item_schema import AdvertisementV1Schema


class GetAdvertisementsQuerySchema(BaseModel):
    """
    Описание структуры запроса на получение списка объявлений.
    """
    model_config = ConfigDict(populate_by_name=True)

    seller_id: str = Field(alias="sellerID")


class GetAdvertisementsV1ResponseSchema(RootModel):
    root: list[AdvertisementV1Schema]

    @property
    def advertisements(self) -> list[AdvertisementV1Schema]:
        return self.root
