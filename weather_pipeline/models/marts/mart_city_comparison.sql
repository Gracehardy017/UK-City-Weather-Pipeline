
    WITH daily_aggregations AS (
        SELECT city,
        WEEK(date) AS week_num,
        YEAR(date) AS year_num,
        MIN(min_temperature_2m) AS min_temperature_2m
        FROM {{ ref('int_weather_daily') }}
        GROUP BY city, WEEK(date), YEAR(date)
    ), 
    
    weekly_aggregations AS (
        SELECT city,
        WEEK(date) AS week_num,
        YEAR(date) AS year_num,
        MIN(min_temperature_2m) AS min_temperature_2m,
        MAX(max_windspeed_10m) AS max_windspeed_10m,
        SUM(total_shortwave_radiation) AS total_shortwave_radiation,
        AVG(avg_temperature_2m) AS avg_temperature_2m
        FROM {{ ref('int_weather_daily') }}
        GROUP BY city, WEEK(date), YEAR(date)
    )
        

SELECT 
    da.city,
    da.week_num,
    da.year_num,
    da.min_temperature_2m AS daily_min_temperature,
    wa.min_temperature_2m AS weekly_min_temperature,
    wa.max_windspeed_10m,
    wa.total_shortwave_radiation,
    wa.avg_temperature_2m
FROM daily_aggregations da
JOIN weekly_aggregations wa ON da.city = wa.city AND da.week_num = wa.week_num AND da.year_num = wa.year_num
ORDER BY wa.min_temperature_2m,
        wa.max_windspeed_10m,
        wa.total_shortwave_radiation,
        wa.avg_temperature_2m