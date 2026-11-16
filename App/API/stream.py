import asyncio
import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from App.Services.sim import generate_sensor_batch

router = APIRouter(prefix="/api/stream", tags=["stream"])


async def event_gen():
    yield "data: " + json.dumps({"type": "hello"}) + "\\n\\n"
    while True:
        batch = generate_sensor_batch()
        payload = [item.model_dump() for item in batch]
        yield "data: " + json.dumps({"type": "sensors", "payload": payload}) + "\\n\\n"
        await asyncio.sleep(1.5)


@router.get("")
async def stream():
    return StreamingResponse(event_gen(), media_type="text/event-stream")
