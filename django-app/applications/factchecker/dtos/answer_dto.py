from dataclasses import dataclass


@dataclass(frozen=True)
class AnswerDto:
    title: str
    content: str
    verdict: str
