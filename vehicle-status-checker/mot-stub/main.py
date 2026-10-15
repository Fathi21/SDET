from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}    

@app.get("/vehicles/{registration_number}")
def get_mot_status(registration_number: str):
    # returns: 
    #     tax status
    #     MOT status,
    #     with MOT shown 
    #     as “Unavailable” 
    #     if the stub fails.
    
    if registration_number.length == 0:
        raise HTTPException(status_code=400, detail="Invalid registration number")
    
app.post("/vehicles/{registration_number}/mot")
def update_mot_status(registration_number: str, mot_status: str, expiry_date: str):
    # Simulate updating the MOT status for a vehicle
    
    if registration_number.length == 0:
        raise HTTPException(status_code=400, detail="Invalid registration number")
    
    
    