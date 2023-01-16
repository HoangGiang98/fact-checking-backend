from dataclasses import dataclass

import datetime as datetime

from .verification_methods_enum import verification_methods
from .answer_dto import AnswerDto
from datetime import datetime


@dataclass(frozen=True)
class SearchRequestDtoOut:
    claim: str
    answers: [AnswerDto]
    verification_method: verification_methods
    datetime: datetime
