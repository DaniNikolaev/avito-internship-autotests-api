from typing import Any, Dict

from pydantic import BaseModel, ConfigDict, Field


class BadRequestResultSchemaV1(BaseModel):
    message: str
    messages: Dict[str, Any] = Field(default_factory=dict)


class BadRequestErrorResponseSchemaV1(BaseModel):
    """
    Модель, описывающая структуру ошибки Bad request v1.
    """
    model_config = ConfigDict(populate_by_name=True)

    result: BadRequestResultSchemaV1
    status: str


class NotFoundResultSchemaV1(BaseModel):
    message: str
    messages: None


class NotFoundErrorResponseSchemaV1(BaseModel):
    """
    Модель, описывающая структуру ошибки Not Found v1.
    """
    model_config = ConfigDict(populate_by_name=True)

    result: NotFoundResultSchemaV1
    status: str
