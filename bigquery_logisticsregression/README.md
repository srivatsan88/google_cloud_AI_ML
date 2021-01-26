This folder contains demonstration of using BigQuery ML for feature engineering and for building logistics regression model

Dataset used for this demonstration is available in UCI ML repository - https://archive.ics.uci.edu/ml/datasets/Bank+Marketing

You can watch the video demonstration of code here - https://youtu.be/pX4P6uG1CuU

You can store the data in GCS bucket and import into bigquery. Once done follow the below steps

<b>Step 1 - Query table to quickly validate the load and get understanding of data </b>

select
age,	
job,	
marital,	
education,
'default',	
balance,
housing,	
loan,	
contact,	
day,	
month,	
campaign,	
pdays,
previous,	
poutcome,	
y as target
from
`srivatsan-project.bank.bank_marketing` 

<b> Step 2 - Check target value distribution. This dataset target instances are imbalanced </b>

select
y as target, count(*)
from
`srivatsan-project.bank.bank_marketing` 
group by y	

<b> Step 3: Query to split data on train/validation and test </b>

select 
age, job, marital, education, 'default', balance, housing, loan,	
contact, day, month, campaign, pdays, previous,	
poutcome, target,
CASE
    WHEN split_field < 0.8 THEN 'training'
    WHEN split_field = 0.8 THEN 'evaluation'
    WHEN split_field > 0.8 THEN 'prediction'
  END AS dataframe
from (
select
age, job, marital, education, 'default', balance, housing, loan,	
contact, day, month, campaign, pdays, previous,	
poutcome, y as target,
ROUND(ABS(RAND()),1) as split_field
from
`srivatsan-project.bank.bank_marketing` ) 

<b> Query 4: Store the data split into new table for using it in model. Creating physical table to keep consistent data sets from random splits </b>


CREATE OR REPLACE table `bank.marketing_tab` AS
select 
age, job, marital, education, 'default' as derog, balance, housing, loan,	
contact, day, month, campaign, pdays, previous,	
poutcome, target,
CASE
    WHEN split_field < 0.8 THEN 'training'
    WHEN split_field = 0.8 THEN 'evaluation'
    WHEN split_field > 0.8 THEN 'prediction'
  END AS dataframe
from (
select
age, job, marital, education, 'default', balance, housing, loan,	
contact, day, month, campaign, pdays, previous,	
poutcome, y as target,
ROUND(ABS(RAND()),1) as split_field
from
`srivatsan-project.bank.bank_marketing` ) 

<b> Query 5: validate target variable distribution in splits </b>

select 
dataframe, target, count(*)
from `srivatsan-project.bank.marketing_tab`
group by dataframe, target
order by dataframe

<b> Query 6: Create Logistics Regression model </b>


CREATE OR REPLACE MODEL
  `bank.marketing_model`
OPTIONS
  ( model_type='LOGISTIC_REG',
    auto_class_weights=TRUE,
    input_label_cols=['target']
  ) AS
SELECT
  * EXCEPT(dataframe)
FROM
  `bank.marketing_tab`
WHERE
  dataframe = 'training'

<b> Query 7: Get Training and Feature Info from trained model </b>

SELECT
  *
FROM
  ML.TRAINING_INFO(MODEL `bank.marketing_model`)

SELECT
  *
FROM
  ML.FEATURE_INFO(MODEL `bank.marketing_model`)


  SELECT
  *
FROM
  ML.WEIGHTS(MODEL `bank.marketing_model`)

<b> Query 8: Evaluate using the trained model </b>


SELECT
  *
FROM
  ML.EVALUATE (MODEL `bank.marketing_model`,
    (
    SELECT
      *
    FROM
      `bank.marketing_tab`
    WHERE
      dataframe = 'evaluation'
    )
  )

<b> Query 8: Predict new data using the trained model </b>


SELECT
  *
FROM
  ML.PREDICT (MODEL `bank.marketing_model`,
    (
    SELECT
      *
    FROM
      `bank.marketing_tab`
    WHERE
      dataframe = 'prediction'
     )
  )


<b> Query 9: Add feature engineering to the model to increase model performance </b>


CREATE OR REPLACE MODEL
  `bank.marketing_model_feat`
TRANSFORM(
    ML.QUANTILE_BUCKETIZE(age,5) OVER() AS bucketized_age, 
    ML.FEATURE_CROSS(STRUCT(job, education)) job_education,
marital, balance, housing, loan,	
contact, day, month, pdays, previous,	
poutcome, target)
OPTIONS
  ( model_type='LOGISTIC_REG',
    auto_class_weights=TRUE,
    input_label_cols=['target']
  ) AS
SELECT
  * EXCEPT(dataframe, campaign, derog)
FROM
  `bank.marketing_tab`
WHERE
  dataframe = 'training'

<b> Query 10: Get training and feature info from newly trained model </b>

SELECT
  *
FROM
  ML.TRAINING_INFO(MODEL `bank.marketing_model_feat`)

SELECT
  *
FROM
  ML.FEATURE_INFO(MODEL `bank.marketing_model_feat`)

  SELECT
  *
FROM
  ML.WEIGHTS(MODEL `bank.marketing_model_feat`)

<b> Query 11: Evaluate the model </b>


SELECT
  *
FROM
  ML.EVALUATE (MODEL `bank.marketing_model_feat`,
    (
    SELECT
      *
    FROM
      `bank.marketing_tab`
    WHERE
      dataframe = 'evaluation'
    )
  )

