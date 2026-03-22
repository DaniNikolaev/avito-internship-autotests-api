from pydantic import BaseModel, ConfigDict, Field, RootModel


class StatisticV2Schema(BaseModel):
    """
    Описание структуры статистики v2.
    """
    model_config = ConfigDict(populate_by_name=True)

    likes: int
    view_count: int = Field(alias="viewCount")
    contacts: int


class GetStatisticV2ResponseSchema(RootModel):
    root: list[StatisticV2Schema]

    @property
    def statistics(self):
        return self.root
