from pydantic import BaseModel, Field
from datetime import date

class TravelRequest(BaseModel):
    destination: str
    start_date: date
    end_date: date
    currency: str = Field(default='USD')

class WeatherResponseModel(BaseModel):
    date: str
    condition: str
    temperature: float
    humidity: float
    rain_chance: float
    