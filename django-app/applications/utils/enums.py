from enum import Enum


class Engines(Enum):
    GOOGLE = "Google"
    BING = "Bing"
    WIKI = "Wiki"
    EMPTY = "No Engine"


class VerdictsNLI(Enum):
    SUPPORTED = "Supported"
    REFUTED = "Refuted"
    NEUTRAL = "Not Enough Info"


class VerdictsDPR(Enum):
    HIGH_SIMILARITY = "High similarity"
    LOW_SIMILARITY = "Low similarity"
    NO_SIMILARITY = "No similarity"
