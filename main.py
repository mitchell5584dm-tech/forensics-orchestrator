from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import subprocess
import os

# 1. Define the security scheme and expected key
api_key_scheme = APIKeyHeader(name="X-API-Key")
# In a true production environment, you would pull this from an environment variable.
# For tonight's staging, we will hardcode a master key.
MASTER_KEY = "trust-anchor-q1" 

def verify_api_key(api_key: str = Depends(api_key_scheme)):
    """Validates the incoming API key against the master key."""
    if api_key != MASTER_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key. Access Denied."
        )
    return api_key

app = FastAPI(
    title="Security Operations Forensics Toolkit - API", 
    description="Enterprise Orchestration Node with API Key Authentication.",
    version="1.0.1"
)

class TargetModel(BaseModel):
    file_path: str

@app.get("/")
def system_status():
    """Health check remains open to verify the server is alive."""
    return {"status": "System Online", "module": "Orchestrator"}

# 2. Inject the security dependency into the endpoint
@app.post("/api/v1/hash", dependencies=[Depends(verify_api_key)])
def trigger_hash_validator(target: TargetModel):
    """
    Triggers the containerized Immutable Hash Validator. 
    Requires a valid X-API-Key header.
    """
    try:
        result = subprocess.run(
            [
                "sudo", "docker", "run", "--rm", 
                "-v", "/home/me/Pictures:/Pictures", 
                "hash-validator", target.file_path
            ],
            capture_output=True, text=True, check=True
        )
        return {
            "status": "success", 
            "target": target.file_path,
            "raw_output": result.stdout.strip().split('\n')
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Execution Failed: {e.stderr}")from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

app = FastAPI(
    title="Security Operations Forensics Toolkit - API", 
    description="Enterprise Orchestration Node for modular forensic utilities.",
    version="1.0.0"
)

class TargetModel(BaseModel):
    file_path: str

@app.get("/")
def system_status():
    """Health check endpoint for the enterprise dashboard."""
    return {"status": "System Online", "module": "Orchestrator"}

@app.post("/api/v1/hash")
def trigger_hash_validator(target: TargetModel):
    """
    Triggers the containerized Immutable Hash Validator from the API layer.
    """
    try:
        # Instructs the host system to run your existing Docker container
        result = subprocess.run(
            [
                "sudo", "docker", "run", "--rm", 
                "-v", "/home/me/Pictures:/Pictures", 
                "hash-validator", target.file_path
            ],
            capture_output=True, text=True, check=True
        )
        return {
            "status": "success", 
            "target": target.file_path,
            "raw_output": result.stdout.strip().split('\n')
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Execution Failed: {e.stderr}")
