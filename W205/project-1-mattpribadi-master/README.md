# Project 1: Query Project
## Student: Matt Pribadi
## Class: W205 - Summer 2021

#### Executive Summary

This notebook serves to help Lyft Bay Wheels improve their ridership program by looking for new opportunities to increase ridership, increase number of subscribers, and to increase revenues overall. A few key questions to be answered in this file and the corresponding Project_1.ipynb jupyter notebook are below:

**What are the 5 most popular trips that you would call "commuter trips"?**

and

**What are your recommendations for offers (justify based on your findings)?**
- Sub Question 1: Which station requires the most number of bikes per hour?
- Sub Question 2: Average commuter distance? 
- Sub Question 3: Subscriber type versus average commuter time? 
- Sub Question 4: Trips taken per hour and also comparation with weekdays versus weekend?

These questions are answered throughout the Project_1.ipynb notebook and are formatted with corresponding tables and figures that will assist the recommendations given.



## Project Specific Deliverables Below:

## Part 1 - Querying Data with BigQuery

- What's the size of this dataset? (i.e., how many trips)

  * Answer: There are a total of *983,648* unique trips taken in the **bikeshare_trips** static table.
  * SQL query:
  ```sql
  SELECT COUNT(DISTINCT trip_id) FROM `bigquery-public-data.san_francisco.bikeshare_trips
  ```

- What is the earliest start date and time and latest end date and time for a trip?

  * Answer: The earliest start date in this dataset is on **Aug 29, 2013 at 09:08:00 UTC** and the latest end date in this dataset is on **Aug 31, 2016 at 23:48:00 UTC** 
  * SQL query:
  ```sql
  SELECT MIN(start_date) as Min_Start, MAX(end_date) as Max_End
    FROM `bigquery-public-data.san_francisco.bikeshare_trips`
  ```

- How many bikes are there?

  * Answer: There are a total number of **700** unique bikes in this data set. 
  * SQL query:
  ```sql
  SELECT COUNT(DISTINCT bike_number) as distinct_bikes
    FROM `bigquery-public-data.san_francisco.bikeshare_trips`
  ```

### Questions of your own
- Make up 3 questions and answer them using the Bay Area Bike Share Trips Data.  These questions MUST be different than any of the questions and queries you ran above.

- Question 1: *What are the top ten zipcodes for the most rides?*
  * Answer: The top ten zipcodes for most number of rides are **94107, 94105, 94133, 94103, 94111, 94102, 94109, 95112, 94158, and 94611**
  * SQL query:
  ```sql
  SELECT zip_code, COUNT(DISTINCT trip_id) as distinct_trips
    FROM `bigquery-public-data.san_francisco.bikeshare_trips`
    WHERE zip_code NOT LIKE 'nil' 
    GROUP BY zip_code
    ORDER BY distinct_trips DESC LIMIT 10
  ```

- Question 2: *How many of each subscriber type are there in this dataset?*
  * Answer: There are a total of **846839** subscribers and **136809** customers, indicating that the majority of these bike users are subscribers.
  * SQL query:
  ```sql
  SELECT subscriber_type, COUNT(subscriber_type) as subscribers
    FROM `bigquery-public-data.san_francisco.bikeshare_trips`
    GROUP BY subscriber_type
    ORDER BY subscribers DESC
  ```
- Question 3: *What is the average trip duration for this data set in minutes?*
  * Answer: The average time of a bike trip is about **16.98 minutes**
  * SQL query:
  ```sql
  SELECT AVG(duration_sec)/60
    FROM `bigquery-public-data.san_francisco.bikeshare_trips`
  ```

## Part 2 - Querying data from the BigQuery CLI 

### Queries

1. Rerun the first 3 queries from Part 1 using bq command line tool (Paste your bq
   queries and results here, using properly formatted markdown):

  * What's the size of this dataset? (i.e., how many trips)

  * SQL query:
 
    ```
    bq query --use_legacy_sql=false '
      SELECT count(DISTINCT trip_id)
      FROM
         `bigquery-public-data.san_francisco.bikeshare_trips`'
    ```
  * What is the earliest start time and latest end time for a trip?
    ```
    bq query --use_legacy_sql=false '
        SELECT MIN(start_date) as Min_Start, MAX(end_date) as Max_End
        FROM
           `bigquery-public-data.san_francisco.bikeshare_trips`'
    ```
  * How many bikes are there?
  
    ```
    bq query --use_legacy_sql=false '
        SELECT COUNT(DISTINCT bike_number) as distinct_bikes         
        FROM
           `bigquery-public-data.san_francisco.bikeshare_trips`'
    ```
    
2. New Query:

  * How many trips are in the morning vs in the afternoon?
  * **Morning: 459289 total trips**
  ```SQL
  SELECT COUNT(*) as morning_trips
  FROM `bigquery-public-data.san_francisco.bikeshare_trips`
  WHERE EXTRACT(HOUR FROM start_date) BETWEEN 0 AND 12
  ```
  * **Afternoon (between 1pm and 6pm): 428818 total trips**
  ```SQL
  SELECT COUNT(*) as morning_trips
  FROM `bigquery-public-data.san_francisco.bikeshare_trips`
  WHERE EXTRACT(HOUR FROM start_date) BETWEEN 13 AND 18
  ```

### Project Questions
Identify the main questions you'll need to answer to make recommendations (list
below, add as many questions as you need).

- Question 1: Which station requires the most number of bikes per hour?

- Question 2: Average commuter distance? 

- Question 3: Subscriber type versus average commuter time? 

- Question 4: Trips taken per hour and also comparation with weekdays versus weekend?

### Answers

Answer at least 4 of the questions you identified above You can use either
BigQuery or the bq command line tool.  Paste your questions, queries and
answers below.

- Question 1:**Which station requires the most number of bikes per hour?**
  * Answer: See notebook.
  * SQL query:
  ```sql
  SELECT  station_id, AVG(bikes_available) as bikes_available,
  (EXTRACT (HOUR FROM time) ) AS query_hour
  FROM
    `bigquery-public-data.san_francisco.bikeshare_status`
  GROUP BY station_id, query_hour
  ORDER BY query_hour
  ```

- Question 2: **Subscriber type versus average commuter distance?**
  * Answer: See notebook.
  * SQL query: *uses query from question 1*

- Question 3: **Subscriber type versus average commuter time?**
  * Answer: *Average commuter time is 55.5 mins for customers and 11 mins for subscribers*
  * SQL query:
  ```sql
  SELECT 
      distinct trip_id, duration_sec/60 as duration_min, subscriber_type

  FROM `bigquery-public-data.san_francisco.bikeshare_trips`

  WHERE duration_sec < 86400 and duration_sec > 300
  ```
  
- Question 4: **Trips taken per hour and also comparation with weekdays versus weekend?**
  * Answer: *See table from the query. overall, there are more subscr
  * SQL query:
  ```SQL
    SELECT EXTRACT(HOUR FROM start_date) as start_hour, count(*) as total_rides,
    SUM(CASE WHEN EXTRACT(DAYOFWEEK FROM start_date) BETWEEN 1 AND 6 
        THEN 1 ELSE 0 END) AS weekday,
    SUM(CASE WHEN EXTRACT(DAYOFWEEK FROM start_date)=0 
        OR EXTRACT(DAYOFWEEK FROM start_date)=7 
            THEN 1 ELSE 0 END) AS weekend,
    SUM(CASE WHEN subscriber_type = 'Subscriber' 
        THEN 1 ELSE 0 END) AS subscriber,
    SUM(CASE WHEN subscriber_type = 'Customer' 
        THEN 1 ELSE 0 END) AS customer  
    FROM `bigquery-public-data.san_francisco.bikeshare_trips`
    GROUP BY start_hour
    ORDER BY start_hour
  ```

