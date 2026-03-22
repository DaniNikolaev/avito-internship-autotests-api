from pydantic import BaseModel, ConfigDict, Field, RootModel

from clients.v1.statistic.statistic_schema import StatisticV1Schema
from tools.fakers import fake
from tools.generators import generate_seller_id


class AdvertisementV1Schema(BaseModel):
    """
    Описание структуры объявления v1.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    seller_id: int = Field(alias="sellerId")
    name: str
    price: int
    statistics: StatisticV1Schema
    created_at: str = Field(alias="createdAt")


class GetAdvertisementV1ResponseSchema(RootModel):
    root: list[AdvertisementV1Schema]

    @property
    def advertisements(self) -> list[AdvertisementV1Schema]:
        return self.root


class CreateAdvertisementV1RequestSchema(BaseModel):
    """
    Описание структуры запроса на создание объявления v1.
    """
    model_config = ConfigDict(populate_by_name=True)

    seller_id: int | None = Field(alias="sellerID", default_factory=generate_seller_id)
    name: str | None = Field(default_factory=fake.name)
    price: int | None = Field(default_factory=fake.price)
    statistics: StatisticV1Schema = Field(default_factory=fake.statistics)


class CreateAdvertisementV1ResponseSchema(BaseModel):
    """
    Описание структуры ответа создания объявления v1.
    """
    status: str
