from pydantic import BaseModel, ConfigDict, Field, RootModel


class StatisticV1Schema(BaseModel):
    """
    Описание структуры статистики v1.
    """
    model_config = ConfigDict(populate_by_name=True)

    likes: int | None
    view_count: int | None = Field(alias="viewCount")
    contacts: int | None


class GetStatisticV1ResponseSchema(RootModel):
    root: list[StatisticV1Schema]

    @property
    def statistics(self):
        return self.root
