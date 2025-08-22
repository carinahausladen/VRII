import os
import json
import pandas as pd
from glob import glob

data_path = "data"

# keys we want to extract
KEEP_KEYS = [
    "tag1_vote1",
    "tag2_vote1",
    "tag3_vote1",
    "tag4_vote1",
    "tag5_vote1",
    "tag6_vote1",
    "tag1_vote3",
    "question1",
    "question4",
    "question5",
    "question6",
    "question7",
    "drag_and_drop_dragger",
    "vote_overall",
]

rows = []

for fp in glob(os.path.join(data_path, "participant*_responses.json")):
    participant = os.path.basename(fp).split("_")[0]
    with open(fp, "r", encoding="utf-8") as f:
        obj = json.load(f)

    entries = obj if isinstance(obj, list) else [obj]

    for entry in entries:
        survey = entry.get("surveyData", {}) if isinstance(entry, dict) else {}
        ts = entry.get("timestamp") if isinstance(entry, dict) else None

        row = {
            "participant": participant,
        }
        for k in KEEP_KEYS:
            row[k] = survey.get(k)

        rows.append(row)

df_votes = pd.DataFrame(rows)

# note that I know changed this on SurveyJS to have better var names for future
rename_map = {
    "tag1_vote1": "residents_vote1",
    "tag2_vote1": "traffic_vote1",
    "tag3_vote1": "greenery_vote1",
    "tag4_vote1": "sponge_vote1",
    "tag5_vote1": "biodiversity_vote1",
    "tag6_vote1": "canopy_vote1",
}
df_votes = df_votes.rename(columns=rename_map)

drag_map = {
    "tag1": "residents",
    "tag2": "traffic",
    "tag3": "greenery",
    "tag4": "canopy",
    "tag5": "biodiversity",
    "tag6": "sponge",
}
def map_drag_list(lst):
    if isinstance(lst, list):
        return [drag_map.get(x, x) for x in lst]
    return lst
df_votes["drag_and_drop_dragger"] = df_votes["drag_and_drop_dragger"].apply(map_drag_list)


rename_map_round2 = {
    "tag1_vote3": "residents_vote2",
    "question1": "traffic_vote2",
    "question4": "greenery_vote2",
    "question5": "canopy_vote2",
    "question6": "biodiversity_vote2",
    "question7": "sponge_vote2",
}
df_votes = df_votes.rename(columns=rename_map_round2)

importance_map = {
    0: "not_important",
    1: "slightly_important",
    2: "moderately_important",
    3: "very_important",
    4: "extremely_important",
}
vote2_cols = [
    "residents_vote2",
    "traffic_vote2",
    "greenery_vote2",
    "canopy_vote2",
    "biodiversity_vote2",
    "sponge_vote2",
]
for col in vote2_cols:
    if col in df_votes.columns:
        df_votes[col] = df_votes[col].map(importance_map).fillna(df_votes[col])


df_votes.to_csv("data_processed/df_votes.csv", index=False)