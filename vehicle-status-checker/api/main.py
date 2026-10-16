from fastapi import FastAPI, HTTPException

from registration import check_registration
from pathlib import Path
import json

app = FastAPI()

# loading seed data once the at start of the application
seedFile = Path(__file__).with_name("seedingData.json")

with open(seedFile, "r") as file:
    seedData = json.load(file)

@app.get("/vehicles/{reg}")
def vehicles(reg: str):

    reg = check_registration(reg)
        
    if reg is not None:
        
        for item in seedData:
            if item["reg"] == reg:
                return item   
            
    else:
        raise HTTPException(status_code=400, detail="Invalid registration number")
            
    
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/health")
def health_check():
    return {"status": "healthy"}    