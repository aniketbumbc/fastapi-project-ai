from fastapi import APIRouter, HTTPException, status
from typing import Any
from app.models.planner import TravelRequest
from app.services.weather import get_weather_data

router = APIRouter(prefix='/api/v1/planner', tags=['planner'])


@router.post('/')
async def create_plan(travel_request: TravelRequest):
    """ Aggregate the weather, location, Currency, and activity data to create a travel plan """

    if travel_request.start_date >= travel_request.end_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Start date must be before end date')

    if not travel_request.destination:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Destination is required')

    trip_num_days = (travel_request.end_date - travel_request.start_date).days
    if trip_num_days < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Trip duration cannot be less than 1 day')
        
    weather_data = get_weather_data(travel_request.destination, travel_request.start_date, travel_request.end_date)

    # Get the weather data for the destination
    # Get the location data for the destination
    # get the currency data for the destination
    # get the activity data for the destination
    # aggregate the data to create a travel plan
    # return the travel plan
    travel_plan = None

    return {"message": "Travel plan created successfully", "weather_data": weather_data}
