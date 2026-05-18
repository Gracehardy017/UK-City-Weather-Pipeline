SELECT city, 
temperature_2m, 
windspeed_10m, 
shortwave_radiation,
CAST(timestamp AS TIMESTAMP) as timestamp,
CAST(LEFT(timestamp, 10) AS DATE) AS date
FROM weather
WHERE city is not null and timestamp is not null
