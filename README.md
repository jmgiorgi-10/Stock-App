# Stock-App #

## model ##

We are pulling data from the Alpha Vantage API: https://www.alphavantage.co/documentation/, from a 5 minute time-series intra-day ticker, and using a pub/sub framework to test the use of kafka to enable scalability.

Stock prediction and plotting using lagged linear regression model with scikit-learn.

![Online LSTM Training](Online-training.png)

## apache kafka ##

Follow official apache website instructions to download Kafka on the host, and run

```
chmod +x init_kafka.sh
./init_kafka.sh
```

This will initialize a Kafka server with Zookeeper on localhost:9020, and creates (for now) a single topic named stock-events. 

## next steps ##

1. Specify a performance metric for time series (accuracy, what else?)

2. Test performance of other models on various stocks or aggregation of stocks - XGBoost and Online LSTM

3. Apache airflow orchestration of model fitting Full Extraction, Transformation, Load (ETL) pipeline ###

The next step in the data pipeline is to use apache airflow to refresh our database and refit the model after a certain amount of new datapoints are available.
The ETL data pipeline also provides the option to scale and manage our application across a distributed system.
![ETL Pipeline](ETL%20pipeline.png)
