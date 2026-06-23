import ollama
import json

from mapper import route_department


def generate_maps(data):

    results = []

    for row in data["impact_delta_matrix"]:

        department = route_department(
            row["regulatory_mandate"]
        )

        prompt = f"""
You are a banking compliance planner.

Convert ONE impact matrix record into ONE measurable action point.

INPUT:
{row}

Return ONLY VALID JSON.

Rules:
1. task_id → format MAP-001
2. target_department → keep existing
3. action_required → concise actionable sentence
4. audit_metric → uppercase with underscores
5. required_threshold → integer only
6. deadline → future date YYYY-MM-DD
7. No empty fields

Output:

{{
"task_id":"MAP-001",
"target_department":"DEPT_NAME",
"action_required":"text",
"audit_metric":"METRIC_NAME",
"required_threshold":95,
"deadline":"2026-09-30"
}}
"""

        response = ollama.chat(
            model="llama3",
            format="json",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        try:

            obj = json.loads(
                response["message"]["content"]
            )

        except:

            obj = {
                "task_id": "ERROR",
                "target_department": department,
                "action_required": "JSON_PARSE_FAILED",
                "audit_metric": "FAILED",
                "required_threshold": 0,
                "deadline": "2026-12-31"
            }

        obj["target_department"] = department

        results.append(obj)

    return {
        "document_id":
        data["document_id"],

        "measurable_action_points":
        results
    }