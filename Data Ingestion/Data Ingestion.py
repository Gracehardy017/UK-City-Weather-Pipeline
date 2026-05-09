import pandas as pd
import requests
from io import BytesIO
import boto3
from datetime import date
import logging
from schemas_validation import weather_record_check
from pydantic import ValidationError

cities = {
    "London": (51.5074, -0.1278),
    "Manchester": (53.4808, -2.2426),
    "Leeds": (53.8008, -1.5491),
    "Liverpool": (53.4084, -2.9916),
    "Bristol": (51.4545, -2.5879),
    "Portsmouth": (50.8198, -1.0880),
}


def get_weather_data(city, lat, lon) -> dict:
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
           f"&hourly=temperature_2m,windspeed_10m,shortwave_radiation&forecast_days=7&timezone=Europe/London")
    try:
        response = requests.get(url)
        # Check the status code = 200 which means it has been successful
        if response.status_code == 200:
            posts = response.json()
            logging.info(f'{city} Weather Data Imported Successfully')
            return posts
        # Else produce an error message with the status code
        else:
            logging.error(f'Error: {response.status_code}')
            return None
    # Where the exception code is e return error
    except requests.exceptions.RequestException as e:
        logging.error(f'Error: {e}')
        return None


def pandas_df(weather_api_result, city):
    hourly = weather_api_result["hourly"]
    results_list = []
    for timestamp, temp, wind, radiation in zip(
            hourly["time"],
            hourly["temperature_2m"],
            hourly["windspeed_10m"],
            hourly["shortwave_radiation"]
    ):
        weather_dict = {
            "city": city,
            "timestamp": timestamp,
            "temperature_2m": temp,
            "windspeed_10m": wind,
            "shortwave_radiation": radiation,
        }
        try:
            weather_record_check(weather_dict)
        except ValidationError as e:
            logging.error(f"Error caught: {e}")
            continue
        else:
            results_list.append(weather_dict)

    return pd.DataFrame(results_list)


def upload_to_s3(weather_df, city):
    bucket = 'weather-bucket-us-east-1'  # already created on S3
    buffer = BytesIO()
    today = date.today()
    s3_key = f"raw/city={city}/date={today}/weather.parquet"

    weather_df.to_parquet(buffer, index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, s3_key).put(Body=buffer.getvalue())


def main():
    for city, (lat, lon) in cities.items():
        weather_api_output = get_weather_data(city, lat, lon)
        if weather_api_output is None:
            continue
        weather_df_output = pandas_df(weather_api_output, city)
        upload_to_s3(weather_df_output, city)


if __name__ == "__main__":
    main()
