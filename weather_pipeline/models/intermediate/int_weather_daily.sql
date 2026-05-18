SELECT city,
date, 
MIN(temperature_2m) as min_temperature_2m, 
MAX(temperature_2m) as max_temperature_2m, 
AVG(temperature_2m) as avg_temperature_2m, 
MAX(windspeed_10m) as max_windspeed_10m, 
SUM(shortwave_radiation) as total_shortwave_radiation 
FROM {{ ref('stg_weather') }}
GROUP BY city, date
