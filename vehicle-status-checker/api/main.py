from fastapi import FastAPI, HTTPException

from registration import check_registration
from mot_rules import calculate_mot_status
import httpx
from pathlib import Path
import json
from datetime import date

MOT_STUB_URL = "http://mot-stub:8000/mot"

app = FastAPI()

# loading seed data once the at start of the application
seedFile = Path(__file__).with_name("seedingData.json")

with open(seedFile, "r") as file:
    seedData = json.load(file)

@app.get("/vehicles/{reg}")
def vehicles(reg: str):
    formatted = check_registration(reg)

    if formatted is None:
        raise HTTPException(status_code=400, detail="Invalid registration number")

    for item in seedData:
        if item["reg"] == formatted:
            vehicle = dict(item)  # copy, so the loaded data stays unchanged
            today = date.today()

            # Tax status
            if vehicle["sorn"]:
                vehicle["tax_status"] = "SORN"
            elif vehicle["tax_expiry"] < str(today):
                vehicle["tax_status"] = "Untaxed"
            else:
                vehicle["tax_status"] = "Taxed"

            # MOT expiry from the stub, with a 2 second timeout
            response = httpx.get(f"{MOT_STUB_URL}/{formatted}", timeout=2.0)
            response.raise_for_status()
            stub_expiry = response.json()["mot_expiry"]

            mot_expiry = date.fromisoformat(stub_expiry) if stub_expiry else None
            first_registered = date.fromisoformat(vehicle["first_registered"])

            vehicle["mot_status"] = calculate_mot_status(first_registered, mot_expiry)
            return vehicle

    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/health")
def health_check():
    return {"status": "healthy"}    