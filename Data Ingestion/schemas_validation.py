from typing import Optional
from pydantic import BaseModel, ValidationError


class WeatherRecord(BaseModel):
    city: str
    timestamp: str
    temperature_2m: Optional[float]
    windspeed_10m: Optional[float]
    shortwave_radiation: Optional[float]


def weather_record_check(hourly_weather_data: dict):
    try:
        # Method 1: Pass dict directly to the constructor
        weather_record_1 = WeatherRecord(**hourly_weather_data)
        print("WeatherRecord1:", weather_record_1)

    except ValidationError as e:
        print("Validation error:", e)




