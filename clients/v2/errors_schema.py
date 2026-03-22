from pydantic import BaseModel, ConfigDict


class BadRequestResultSchemaV2(BaseModel):
    message: str
    messages: None


class BadRequestErrorResponseSchemaV2(BaseModel):
    """
    Модель, описывающая структуру ошибки Bad request v2.
    """
    model_config = ConfigDict(populate_by_name=True)

    result: BadRequestResultSchemaV2
    status: str


class NotFoundResultSchemaV2(BaseModel):
    message: str
    messages: None


class NotFoundErrorResponseSchemaV2(BaseModel):
    """
    Модель, описывающая структуру ошибки Not Found v2.
    """
    model_config = ConfigDict(populate_by_name=True)

    result: NotFoundResultSchemaV2
    status: str
