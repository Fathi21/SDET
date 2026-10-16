from fastapi import FastAPI, HTTPException
import json
from pathlib import Path

# Loaded once at startup
seed_file = Path(__file__).with_name("seedingData.json")
with open(seed_file, "r", encoding="utf-8") as file:
    seed_data = json.load(file)

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/mot/{reg}")
def get_mot_status(reg: str):
    clean_reg = reg.replace(" ", "").upper()

    for item in seed_data:
        if item["reg"].replace(" ", "") == clean_reg:
            return {"reg": item["reg"], "mot_expiry": item["mot_expiry"]}

    raise HTTPException(status_code=404, detail="Vehicle not found")