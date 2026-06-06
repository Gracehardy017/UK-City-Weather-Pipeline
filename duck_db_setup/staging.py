from datetime import date
import duckdb
from dotenv import load_dotenv
import os


def main():
    load_dotenv()

    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION")

    duckdb_weather_db = duckdb.connect("/opt/airflow/project/duckdb_weather.duckdb")

    duckdb_weather_db.execute("INSTALL httpfs;")
    duckdb_weather_db.execute("LOAD httpfs;")

    duckdb_weather_db.execute(f"SET s3_access_key_id='{aws_access_key}';")
    duckdb_weather_db.execute(f"SET s3_secret_access_key='{aws_secret_key}';")
    duckdb_weather_db.execute(f"SET s3_region='{aws_region}';")

    duckdb_weather_db.execute("""
        CREATE TABLE IF NOT EXISTS weather AS 
        SELECT * FROM read_parquet(
            's3://weather-bucket-us-east-1/raw/city=*/date=*/*.parquet',
            union_by_name=True
        )
    """)

    result = duckdb_weather_db.execute("SELECT city, COUNT(*) as rows FROM weather GROUP BY city").fetchdf()
    print(result)


if __name__ == "__main__":
    main()