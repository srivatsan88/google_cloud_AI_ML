
This repo contains SQL queries for my live session on BigQuery, BigQuery ML and Google Data Studio

Live session video is available here - https://youtu.be/5l4Qb6Fy3E0

In below set of SQL queries we will be analyzing SFO bikeshare dataset and as well will be building multiple time series model using BigQuery ML

Query 1: Query to select limited columns for analysis in data studio

SELECT
   start_date, duration_sec, start_station_name, subscriber_type, zip_code
FROM
  `bigquery-public-data.san_francisco_bikeshare.bikeshare_trips`

Query 2: Select columns for understanding time series pattern

SELECT
   start_station_name,
   EXTRACT(DATE from start_date) AS date,
   COUNT(*) AS num_trips
FROM
  `bigquery-public-data.san_francisco_bikeshare.bikeshare_trips`
GROUP BY start_station_name, date
order by start_station_name, date

Query 3: Understand minimum and maximum dates grouped by station

SELECT
   start_station_name,
   min(EXTRACT(DATE from start_date)) as min_date,
   max(EXTRACT(DATE from start_date)) as max_date
FROM
  `bigquery-public-data.san_francisco_bikeshare.bikeshare_trips`
WHERE
  start_station_name IN ('Harry Bridges Plaza (Ferry Building)','Embarcadero at Sansome','2nd at Townsend')
group by start_station_name

Query 4: Create multiple time series model using SFO bikeshare data

CREATE OR REPLACE MODEL bike_share_ml.sfo_bike
OPTIONS
  (model_type = 'ARIMA',
   time_series_timestamp_col = 'date',
   time_series_data_col = 'num_trips',
   time_series_id_col = 'start_station_name'
  ) AS
SELECT
   start_station_name,
   EXTRACT(DATE from start_date) AS date,
   COUNT(*) AS num_trips
FROM
  `bigquery-public-data.san_francisco_bikeshare.bikeshare_trips`
WHERE
  start_station_name IN ('Harry Bridges Plaza (Ferry Building)','Embarcadero at Sansome','2nd at Townsend') AND
EXTRACT(DATE from start_date) <= '2016-07-31'
GROUP BY start_station_name, date

Query 5: Evaluate the developed model

SELECT
  *
FROM
  ML.EVALUATE(MODEL `bike_share_ml.sfo_bike`)

Query 6: Understand trained model co-efficients

SELECT
  *
FROM
  ML.ARIMA_COEFFICIENTS(MODEL `bike_share_ml.sfo_bike`)


Query 7: Forecast for 3 future time period

SELECT
  *
FROM
  ML.FORECAST(MODEL `bike_share_ml.sfo_bike`,
              STRUCT(3 AS horizon, 0.9 AS confidence_level))

Query 8: Combine historical data and future 365 days forecast for visualization

SELECT
 start_station_name,
 date AS timestamp,
 num_trips AS history_value,
 NULL AS forecast_value,
 NULL AS prediction_interval_lower_bound,
 NULL AS prediction_interval_upper_bound
FROM
 (
  SELECT
     start_station_name,
     EXTRACT(DATE from start_date) AS date,
     COUNT(*) AS num_trips
  FROM
    `bigquery-public-data.san_francisco_bikeshare.bikeshare_trips`
  WHERE
  start_station_name IN ('Harry Bridges Plaza (Ferry Building)','Embarcadero at Sansome','2nd at Townsend')
  GROUP BY start_station_name, date
 )
UNION ALL
SELECT
 start_station_name,
 EXTRACT(DATE from forecast_timestamp) AS timestamp,
 NULL AS history_value,
 forecast_value,
 prediction_interval_lower_bound,
 prediction_interval_upper_bound
FROM
 ML.FORECAST(MODEL `bike_share_ml.sfo_bike`,
             STRUCT(365 AS horizon, 0.9 AS confidence_level))
WHERE
  start_station_name IN ('Harry Bridges Plaza (Ferry Building)','Embarcadero at Sansome','2nd at Townsend')
