"""Shared schema base: camelCase, unknown fields rejected, strings trimmed (FR-225, TH-205)."""

from datetime import datetime
from typing import Annotated, ClassVar, Self
from urllib.parse import urlparse

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)
from pydantic.alias_generators import to_camel

Name = Annotated[str, StringConstraints(min_length=1, max_length=80)]
Title = Annotated[str, StringConstraints(min_length=1, max_length=120)]
SearchText = Annotated[str, StringConstraints(max_length=100)]


def _https_only(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("Must be an https URL.")
    return value


HttpsUrl = Annotated[str, StringConstraints(max_length=2048), AfterValidator(_https_only)]


class ApiModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_by_alias=True,
        validate_by_name=False,
        extra="forbid",
        str_strip_whitespace=True,
    )


class OutModel(ApiModel):
    """Responses are built from Python field names, so both spellings are accepted here.

    Requests stay strict: `ApiModel` accepts only the camelCase alias.
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_by_alias=True,
        validate_by_name=True,
        extra="forbid",
        str_strip_whitespace=False,
    )


class PatchModel(ApiModel):
    """A partial update: at least one field, and only nullable fields may be null."""

    nullable: ClassVar[frozenset[str]] = frozenset()

    @model_validator(mode="after")
    def _check_fields(self) -> Self:
        if not self.model_fields_set:
            raise ValueError("Provide at least one field to change.")
        for name in self.model_fields_set:
            if getattr(self, name) is None and name not in self.nullable:
                raise ValueError(f"{name} may not be null.")
        return self


class TimestampedOut(OutModel):
    created_at: datetime = Field(description="UTC, ISO 8601, ends in Z.")
    updated_at: datetime = Field(description="UTC, ISO 8601, ends in Z.")
