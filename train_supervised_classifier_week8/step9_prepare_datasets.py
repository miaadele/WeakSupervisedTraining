#train the classifier only on CORE v. NEG
#exclude MAYBE from training but save it for later inspection and interpretation

import json
from pathlib import Path
import random

random.seed(42)

DATA_PATH = Path("data") / "merchant_labeled_chunks.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    labeled = json.load(f)

core = [(t, 1) for (t, y) in labeled if y ==1]