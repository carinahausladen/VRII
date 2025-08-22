import os
import json
import pandas as pd
from glob import glob

def build_chat_dataset(data_path: str, pattern: str, bot_label: str = None) -> pd.DataFrame:
    """
    Build a tidy message-level dataset from chat JSON files.

    Args:
        data_path: folder containing the JSON files
        pattern: glob pattern, e.g. "*_chat_gustavo.json"
        bot_label: optional constant to store which bot these chats belong to (e.g., "gustavo")

    Returns:
        pd.DataFrame with columns:
            participant, filename, conversation_id, turn_index, sender, role, text, bot
    """
    files = glob(os.path.join(data_path, pattern))
    rows = []

    for file in files:
        fname = os.path.basename(file)
        # conversation_id = filename without extension
        conversation_id = os.path.splitext(fname)[0]
        # participant is the prefix before first underscore (e.g., "participant11")
        participant = fname.split("_")[0]

        with open(file, "r", encoding="utf-8") as f:
            try:
                chat = json.load(f)
                for i, turn in enumerate(chat):
                    rows.append({
                        "participant": participant,
                        "filename": fname,
                        "conversation_id": conversation_id,
                        "turn_index": i,                   # order within conversation
                        "sender": turn.get("sender"),
                        "role": turn.get("role"),
                        "text": turn.get("text"),
                        "bot": bot_label
                    })
            except json.JSONDecodeError as e:
                print(f"Error reading {file}: {e}")

    return pd.DataFrame(rows)

# === Build dataset for all GUSTAVO chats ===
data_path = "data"

gustavo_df = build_chat_dataset(data_path, "*_chat_gustavo.json", bot_label="gustavo")
gustavo_df.to_csv("data_processed/gustavo_chat.csv", index=False)

flonormale_df = build_chat_dataset(data_path, "*_chat_flonormale.json", bot_label="flonormale")
flonormale_df.to_csv("data_processed/flo_chat.csv", index=False)


