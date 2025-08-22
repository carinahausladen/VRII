# file: build_questionnaire_df.py
import os
import json
import pandas as pd
from glob import glob

DATA_PATH = "data"

# variables to keep
KEEP_KEYS = [
    "q_3d",
    "q_mode_1",
    "q_mode_2",
    "q_mode_3",
    "question63",
    "q_legitimacy",
    "question62",
    "question66",
    "question67",
    "question68",
    "question11",
    "question12",
    "question9",
    "question13",
    "q_transport_1",
    "q_transport_5",
    "question8",
]

def load_questionnaires(data_path: str) -> pd.DataFrame:
    rows = []
    for fp in glob(os.path.join(data_path, "participant*_responses.json")):
        participant = os.path.basename(fp).split("_")[0]  # e.g., "participant10"

        with open(fp, "r", encoding="utf-8") as f:
            obj = json.load(f)

        # Normalize to a list (some files may be a single dict, others a list)
        entries = obj if isinstance(obj, list) else [obj]

        for entry in entries:
            if not isinstance(entry, dict):
                continue
            survey = entry.get("surveyData", {}) or {}
            ts = entry.get("timestamp")

            row = {
                "participant": participant,
            }
            for k in KEEP_KEYS:
                row[k] = survey.get(k)
            rows.append(row)

    df = pd.DataFrame(rows)

    # Optional: enforce numeric dtype where possible (keeps strings like "Car"/"Neutral")
    numeric_cols = [
        "q_3d","q_mode_1","q_mode_2","q_mode_3","question63","q_legitimacy",
        "question62","question66","question67","question68","question11",
        "question12","question9","question13",
    ]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Sort nicely
    if not df.empty:
        df = df.sort_values(["participant"]).reset_index(drop=True)

    return df


df_questionnaire = load_questionnaires(DATA_PATH)
# Optional: save
# df_questionnaire.to_csv("questionnaire_dataset.csv", index=False)


q3d_map = {
    1: "not_at_all",
    2: "slightly",
    3: "somewhat",
    4: "moderately",
    5: "quite",
    6: "very",
    7: "extremely",
}

if "q_3d" in df_questionnaire.columns:
    df_questionnaire["3d_distracting"] = df_questionnaire["q_3d"].map(q3d_map)
    df_questionnaire = df_questionnaire.drop(columns=["q_3d"])



# 1–5 Likert mapping for mode questions
likert_1to5 = {
    1: "not_at_all",
    2: "slightly",
    3: "moderately",
    4: "very",
    5: "extremely",
}

# rename + map q_mode_* variables
mode_map = {
    "q_mode_1": "mode_understanding",
    "q_mode_2": "mode_remember",
    "q_mode_3": "mode_like",
    'question63': "mode_watch_all",
}

for old, new in mode_map.items():
    if old in df_questionnaire.columns:
        df_questionnaire[new] = df_questionnaire[old].map(likert_1to5)
        df_questionnaire = df_questionnaire.drop(columns=[old])




# 1–5 Likert mapping
likert_1to5 = {
    1: "strongly_disagree",
    2: "disagree",
    3: "neutral",
    4: "agree",
    5: "strongly_agree",
}

# rename + map legitimacy-related items
legitimacy_map = {
    "q_legitimacy": "citizens_prefer",
    "question62": "citizens_betterinformed",
    "question66": "citizens_remember",
    "question67": "citizens_factbased",
    "question68": "citizens_legitimate",
}

for old, new in legitimacy_map.items():
    if old in df_questionnaire.columns:
        df_questionnaire[new] = df_questionnaire[old].map(likert_1to5)
        df_questionnaire = df_questionnaire.drop(columns=[old])




# 1–5 Likert mapping (reuse if already defined)
likert_1to5 = {
    1: "not_at_all",
    2: "slightly",
    3: "moderately",
    4: "very",
    5: "extremely",
}

# rename + map guides-related items
guides_map = {
    "question11": "guides_flo",
    "question12": "guides_gustavo",
    "question9": "guides_useful",
    "question13": "guides_trust",
    "question65": "guides_morethoughts",
}

for old, new in guides_map.items():
    if old in df_questionnaire.columns:
        df_questionnaire[new] = df_questionnaire[old].map(likert_1to5)
        df_questionnaire = df_questionnaire.drop(columns=[old])




# rename + map hood-related items
hood_map = {
    "q_transport_1": "hood_modeoftransport",
    "q_transport_5": "hood_community",
    "question8": "hood_attractive",
}

for old, new in hood_map.items():
    if old in df_questionnaire.columns:
        if old in ["q_transport_5", "question8"]:
            # map Likert scale
            df_questionnaire[new] = df_questionnaire[old].map(likert_1to5).fillna(df_questionnaire[old])
        else:
            # keep categorical (Car, Bike, etc.)
            df_questionnaire[new] = df_questionnaire[old]
        df_questionnaire = df_questionnaire.drop(columns=[old])

df_questionnaire.to_csv("data_processed/df_questionnaire.csv", index=False)