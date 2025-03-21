# Stock-App #

## Model ##

We are using an LSTM, with online training based on a sliding window of OLHC features, from $[t-n, t-1]$, and evaluation on the closing price at time t, which is tested for accuracy against the actual closing price at time $t$.

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
