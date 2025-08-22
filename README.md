# Processed Datasets

This repo contains data from our **pilot study with 10 participants**.  
Raw JSON logs are kept locally in `data/`, and all analysis-ready datasets are saved in `data_processed/` for easy viewing on GitHub.  

---

## Datasets

- **flonormale_chat_dataset.csv**  
  Chat logs with **Flo Normale**, the fact-based chatbot (finetuned to give factual information only).  
  Each row = one message turn.  

- **gustavo_chat_dataset.csv**  
  Chat logs with **Gustavo**, the opinion-oriented chatbot (finetuned to support value judgments and trade-offs).  
  Each row = one message turn.  

- **responses_dataset.csv**  
  Participants’ **recall responses and self-created tags** after watching Michael’s information videos.  
  They were instructed to use the *method of loci* to recall as much detail as possible.  
  → Here we need to carefully read and interpret what worked, what didn’t, and why.  

- **votes_dataset.csv**  
  Participants’ **evaluation of project sub-aspects**, captured in three ways:  
  1. **Approval ratings**: approve / disapprove / neutral  
  2. **Importance ratings**: not at all → extremely important  
  3. **Ranking**: drag-and-drop ordering of sub-aspects  
  Finally, they also gave an overall assessment of the project.  

- **questionnaire_dataset.csv**  
  Self-report questionnaire items, grouped into thematic blocks:  
  1. **3D distraction** – whether anything in the 3D environment was distracting  
  2. **Mode questions** – how much the visual+audio mode helped them remember, understand, and how much they liked it  
  3. **Citizens’ perspective** – how other citizens (if informed through the same material) would remember facts, be better informed, have fact-based discussion, etc.  
  4. **Guides evaluation** – usefulness and trust in Flo and Gustavo  
  5. **Neighborhood perceptions** – preferred mode of transport, community sense, and attractiveness  

---

## Scripts

- `flo_gustavo_chat.py` → builds chat datasets  
- `remember.py` → builds responses dataset  
- `vote.py` → builds votes dataset  
- `questionnaires.py` → builds questionnaire dataset  

---

## Notes

- Raw files are ignored (`data/`) → only processed datasets are committed.  
- Processed datasets (`data_processed/`) are version-controlled so they can be browsed directly on GitHub.  
