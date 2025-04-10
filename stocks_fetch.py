# # This API returns current and 20+ years of historical intraday OHLCV time series of the equity specified, covering pre-market and post-market hours where applicable (e.g., 4:00am to 8:00pm Eastern Time for the US market). 
# # You can query both raw (as-traded) and split/dividend-adjusted intraday data from this endpoint. The OHLCV data is sometimes called "candles" in finance literature.

from kafka import KafkaProducer
import requests
import json
import time

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Replace with your broker address
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),  # Serialize data as JSON
    key_serializer=lambda k: k.encode('utf-8') if k else None  # Serialize keys as strings
)

# Topic name
topic = 'stock-events'

# messages = ["Hello", "testing", "here"]

# for msg in messages:
#     producer.send(topic, value=msg)

# Flush to ensure message is sent
api_key = "FBT3PK9760PY7ONG"
# Fetch stock data
URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
response = requests.get(URL)
data = response.json()


# # Produce messages to the 'stock-events'
topic = 'stock-events'
message_count = 0
max_messages = 3000 # Set the maximum number of messages to send
polling_interval = 10


# Delivery report callback for produced messages
def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


while True:

    try:
        for timestamp, values in data['Time Series (5min)'].items():
            if message_count >= max_messages:
                print("Reached maximum number of messages. Stopping producer.")
                break
            
            record_key = timestamp
            record_value = json.dumps(values)
            
            producer.send(topic, key=record_key, value=record_value)
            # producer.poll(1)
            message_count += 1

    except Exception as e:
        print(f'Failed to produce message: {e}')

    time.sleep(polling_interval)

    # producer.flush()
    # Close the producer
producer.close()
