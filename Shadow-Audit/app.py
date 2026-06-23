from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from typing import Any
from pydantic import BaseModel
import sqlite3
import uvicorn
import os
from pathlib import Path
from init_db import init_database
from validator import validate_compliance

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield

app = FastAPI(title="Compliance Checking System", lifespan=lifespan)

ABS_DB_PATH = Path(__file__).resolve().parent / "mock_production.db"

class PatchRequest(BaseModel):
    variable_name: str
    new_value: int

@app.post("/api/v1/audit/submit-patch")
async def submit_patch(request: PatchRequest) -> dict[str, Any]:
    try:
        # Save proposed adjustment to database
        with sqlite3.connect(str(ABS_DB_PATH)) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO system_configs (variable_name, current_value)
                VALUES (?, ?)
            ''', (request.variable_name, request.new_value))
            conn.commit()
        
        # Trigger our AI compliance checking routine matching the contract
        audit_report = validate_compliance(
            task_id="MAP-REG-2026-004", 
            audit_metric=request.variable_name, 
            required_threshold=2048
        )
        
        return {
            "status": "success",
            "message": f"Updated {request.variable_name} to {request.new_value}",
            "shadow_audit_result": audit_report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run on localhost with auto-redirect to /docs; PORT can override
    port = int(os.getenv("PORT", "9001"))
    uvicorn.run(app, host="127.0.0.1", port=port)