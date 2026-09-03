import httpx
from datetime import date
from app.models.planner import WeatherResponseModel
from fastapi import HTTPException, status
import os
from dotenv import load_dotenv
from app.services.cache import get_cache, set_cache

load_dotenv()


def get_weather_data(destination: str, start_date: date, end_date: date) -> list[WeatherResponseModel]:
    """ Get the weather data for the destination """

    cache_key = f"weather_{destination}_{start_date}_{end_date}"
    cached_data = get_cache(cache_key)
    if cached_data:
        return [WeatherResponseModel(**item) for item in cached_data]

    days = max((end_date - start_date).days, 1)
    api_url = (
        f"http://api.weatherapi.com/v1/forecast.json"
        f"?key={os.getenv('WEATHER_API_KEY')}&q={destination}&days={days}"
    )

    try:
        response = httpx.get(api_url)
        response.raise_for_status()
        data = response.json()
        weather_data = [
            WeatherResponseModel(
                date=day["date"],
                condition=day["day"]["condition"]["text"],
                temperature=day["day"]["avgtemp_c"],
                humidity=day["day"]["avghumidity"],
                rain_chance=day["day"]["daily_chance_of_rain"],
            )
            for day in data["forecast"]["forecastday"]
        ]
        set_cache(cache_key, [item.model_dump() for item in weather_data], ttl=3600)
        return weather_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get weather data: {e}",
        )
