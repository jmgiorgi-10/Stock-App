# Stock Prediction #

This project demonstrates a scalable architecture for real-time stock data processing and prediction using Apache Kafka. We leverage the Alpha Vantage API to stream intra-day stock price data into a Kafka pub/sub framework, enabling decoupled and scalable data ingestion and processing. 

A lagged linear regression model, built with scikit-learn, is applied to perform short-term stock price prediction based on historical patterns. The project showcases data visualization, feature engineering using lagged variables, and the potential of Kafka for real-time analytics pipelines.

## model & data ##

We are pulling data from the Alpha Vantage API: https://www.alphavantage.co/documentation/, from a 5 minute time-series intra-day ticker, and using a pub/sub framework to test the use of kafka to enable scalability. The features are OHLV: 'open', 'high', 'low', and 'close', corresponding Stock prediction and plotting using lagged linear regression model with scikit-learn.

![Online LSTM Training](Online-training.png)

## results ##
