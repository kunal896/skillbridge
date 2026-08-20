from __future__ import annotations

import os

MATCH_VERIFIED_WEIGHT = float(os.getenv("MATCH_VERIFIED_WEIGHT", "0.40"))
MATCH_LEVEL_WEIGHT = float(os.getenv("MATCH_LEVEL_WEIGHT", "0.60"))
MATCH_DEFAULT_LIMIT = int(os.getenv("MATCH_DEFAULT_LIMIT", "20"))
