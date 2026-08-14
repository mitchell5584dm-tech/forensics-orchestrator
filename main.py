from fastapi import FastAPI, HTTPException
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
