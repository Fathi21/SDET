from fastapi import FastAPI, HTTPException

from registration import check_registration
from mot_rules import calculate_mot_status
import httpx
from pathlib import Path
import json
from datetime import date

from pydantic import BaseModel

MOT_STUB_URL = "http://mot-stub:8000/mot"

app = FastAPI()

# loading seed data once at the start of the application
seed_file = Path(__file__).with_name("seedingData.json")

with open(seed_file, "r", encoding="utf-8") as file:
    seed_data = json.load(file)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/vehicles/{reg}")
def vehicles(reg: str):
    formatted = check_registration(reg)

    if formatted is None:
        raise HTTPException(status_code=400, detail="Invalid registration number")

    for item in seed_data:
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

            # MOT status, from the stub
            try:
                response = httpx.get(f"{MOT_STUB_URL}/{formatted}", timeout=2.0)
                response.raise_for_status()
                stub_expiry = response.json()["mot_expiry"]

                mot_expiry = date.fromisoformat(stub_expiry) if stub_expiry else None
                first_registered = date.fromisoformat(vehicle["first_registered"])

                vehicle["mot_status"] = calculate_mot_status(first_registered, mot_expiry)
            except (httpx.HTTPError, KeyError, ValueError):
                vehicle["mot_status"] = "Unavailable"

            return vehicle

    raise HTTPException(status_code=404, detail="Item not found")



class VehicleIn(BaseModel):
    reg: str
    make: str
    colour: str
    first_registered: date
    tax_expiry: date
    sorn: bool
    mot_expiry: date | None = None


@app.post("/vehicles", status_code=201)
def add_vehicle(payload: VehicleIn):
    
    formatted = check_registration(payload.reg)

    if formatted is None:
        raise HTTPException(status_code=400, detail="Invalid registration number")

    # Check if the vehicle already exists
    if any(item["reg"] == formatted for item in seed_data):
        raise HTTPException(status_code=409, detail="Vehicle already exists")
    
    # mode="json" turns dates into YYYY-MM-DD strings, matching the GET shape
    vehicle = payload.model_dump(mode="json")
    vehicle["reg"] = formatted
    seed_data.append(vehicle)

    return {"message": "Vehicle added successfully", "vehicle": vehicle}