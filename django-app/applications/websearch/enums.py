from enum import Enum

class Engines(Enum):
  GOOGLE = "Google"
  BING = "Bing"
  WIKI = "Wiki"
  COMBINED = "Combined Engines"

class Verdicts(Enum):
  SUPPORTED = "Supported"
  REFUTED = "Refuted"
  NEUTRAL = "Not Enough Info"