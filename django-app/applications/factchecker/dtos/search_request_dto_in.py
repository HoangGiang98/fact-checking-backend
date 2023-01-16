from dataclasses import dataclass
from .verification_methods_enum import verification_methods
from datetime import datetime


@dataclass(frozen=True)
class SearchRequestDtoOut:
    claim: str
    verification_method: verification_methods
    datetime: datetime
