from fastapi import FastAPI
from planner import generate_maps


app = FastAPI()


@app.post("/api/v1/planner")

async def planner(
    payload: dict
):

    return generate_maps(
        payload
    )