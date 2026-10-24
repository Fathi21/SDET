from fastapi import FastAPI, HTTPException
import json
from pathlib import Path
from registration import check_registration
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
    formatted = check_registration(reg)

    if formatted is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid registration number"
        )

    for item in seed_data:
        if item["reg"] == formatted:
            return {
                "reg": item["reg"],
                "mot_expiry": item["mot_expiry"]
            }

    raise HTTPException(status_code=404, detail="Vehicle not found")