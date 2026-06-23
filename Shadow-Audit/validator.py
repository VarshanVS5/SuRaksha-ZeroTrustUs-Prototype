import sqlite3
from typing import Dict, Any
from pathlib import Path

def validate_compliance(task_id: str, audit_metric: str, required_threshold: int) -> Dict[str, Any]:
    """
    Validates compliance by directly querying the database
    """
    try:
        ABS_DB_PATH = Path(__file__).resolve().parent / "mock_production.db"
        
        # Query the database directly
        with sqlite3.connect(str(ABS_DB_PATH)) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT current_value FROM system_configs WHERE variable_name = ?",
                (audit_metric,)
            )
            result_row = cursor.fetchone()
            
            if result_row is None:
                live_system_value = 0
            else:
                live_system_value = result_row[0]
            
            # Determine compliance status
            is_compliant = live_system_value >= required_threshold
            audit_status = "VERIFIED_SUCCESS" if is_compliant else "AUDIT_FAILED_ALERT"
            action_taken = "Compliance verified" if is_compliant else "Task state LOCKED"
            
            # Update audit tasks table
            status_flag = "COMPLIANT" if is_compliant else "LOCKED"
            cursor.execute(
                "INSERT OR REPLACE INTO audit_tasks (task_id, status) VALUES (?, ?)",
                (task_id, status_flag)
            )
            conn.commit()
        
        return {
            "task_id": task_id,
            "audit_status": audit_status,
            "live_system_value": live_system_value,
            "action_taken": action_taken
        }
        
    except Exception as e:
        return {
            "task_id": task_id,
            "audit_status": "AUDIT_FAILED_ALERT",
            "live_system_value": 0,
            "action_taken": f"Error during compliance validation: {str(e)}"
        }
