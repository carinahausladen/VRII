import os
import json
import pandas as pd
from glob import glob

data_path = "data"
BLOCK_MAP = [
    ("residents", 1),
    ("traffic", 2),
    ("greenery", 3),
    ("canopy", 4),
    ("biodiversity", 5),
    ("sponge", 6),
]

rows = []

for fp in glob(os.path.join(data_path, "participant*_responses.json")):
    participant = os.path.basename(fp).split("_")[0]  # e.g., "participant10"
    with open(fp, "r", encoding="utf-8") as f:
        obj = json.load(f)

    # normalize to a list of entries
    entries = obj if isinstance(obj, list) else [obj]

    for entry in entries:
        survey = entry.get("surveyData", {}) if isinstance(entry, dict) else {}
        ts = entry.get("timestamp") if isinstance(entry, dict) else None

        # only take the remember_* + create_tagN pairs
        for block, idx in BLOCK_MAP:
            remember_key = f"remember_{block}"
            tag_key = f"create_tag{idx}"

            if remember_key in survey or tag_key in survey:
                rows.append({
                    "participant": participant,
                    "block": block,
                    "response": survey.get(remember_key),
                    "tag": survey.get(tag_key),
                })

df_remember = pd.DataFrame(rows).dropna(subset=["response", "tag"], how="all").reset_index(drop=True)
df_remember.to_csv("data_processed/df_remember.csv", index=False)