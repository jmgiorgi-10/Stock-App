# Stock-App #

## Model ##

We are using an LSTM, with online training based on OLHC features of $[t-n, t-1]$ datapoints, and evaluation on the closing price at time t, which is evaluated against the actual closing price.

![Online LSTM Training](Online-training.png)

## Installation ##

## ETL Pipeline ##

Follow official apache website instructions to download Kafka on the host, and run

```
chmod +x init_kafka.sh
./init_kafka.sh
```

This will initialize a Kafka server on localhost:9020, and create a topic called stock-events. 

The ETL data pipeline, which uses Apache Kafka, Airflow and a PostgreSQL database, allows us to scale and manage our application across a distributed system.

![ETL Pipeline](ETL%20pipeline.png)
