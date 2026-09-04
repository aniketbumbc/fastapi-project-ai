from fastapi import APIRouter, HTTPException, status
from app.models.planner import TravelRequest
from fastapi.responses import StreamingResponse
import json
import asyncio
from app.services.weather import get_weather_data
from app.services.location_details import get_location_details
from app.services.currency import get_currency_rate

router = APIRouter(
    prefix="/stream",
    tags=["stream"],
)


def format_sse(data: dict, event: str | None = None) -> str:
    json_data = json.dumps(data, default=str)
    if event is None:
        return f"data: {json_data}\n\n"
    return f"event: {event}\ndata: {json_data}\n\n"


def serialize_models(items) -> list[dict]:
    return [item.model_dump() if hasattr(item, "model_dump") else item for item in items]


async def stream_travel_plan_generator(travel_request: TravelRequest):
    yield format_sse({"message": "Starting the aggregation process..."}, event="start")

    yield format_sse({"message": "Aggregating weather data..."}, event="weather")
    weather_data = await asyncio.to_thread(
        get_weather_data,
        travel_request.destination,
        travel_request.start_date,
        travel_request.end_date,
    )
    yield format_sse({"weather_data": serialize_models(weather_data)}, event="weather_complete")

    yield format_sse({"message": "Aggregating location data..."}, event="location")
    location_data = await asyncio.to_thread(
        get_location_details,
        travel_request.destination,
    )
    yield format_sse({"location_data": serialize_models(location_data)}, event="location_complete")

    yield format_sse({"message": "Aggregating currency data..."}, event="currency")
    currency_data = await asyncio.to_thread(
        get_currency_rate,
        travel_request.currency,
    )
    yield format_sse({"currency_data": currency_data}, event="currency_complete")

    yield format_sse({"message": "Travel plan created successfully"}, event="travel_plan_complete")


@router.post("/plan/stream", response_class=StreamingResponse)
async def stream_travel_plan(travel_request: TravelRequest):
    if not travel_request.destination:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Destination is required")
    if travel_request.start_date >= travel_request.end_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start date must be before end date")

    return StreamingResponse(
        stream_travel_plan_generator(travel_request),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
