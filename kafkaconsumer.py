from kafka import KafkaConsumer
import json
import psycopg2
from psycopg2 import sql

## Features

# Open - price at which assest starts trading at beginning of time interval.
# High - highest price asset reaches during the interval.
# Low - lowest price asset reaches within interval.
# Close - price at which asset stops trading at end of interval.

## Target

# Predict the next closing price.


# Initialize Kafka Consumer
consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# PostgreSQL Table
create_table_query = '''
CREATE TABLE IF NOT EXISTS stock_events (
    id SERIAL PRIMARY KEY,
    open DECIMAL(10, 4),
    high DECIMAL(10, 4),
    low DECIMAL(10, 4),
    close DECIMAL(10, 4),
    volume INT
);
'''

# Subscribe to the 'users' topic
topic = 'stock-events'
consumer.subscribe([topic])

# Consumer Loop
try:
    for message in consumer:
        print(f"Received message from {message.topic}: {message.value}")

except KeyboardInterrupt:
    print("Consumer stopped manually.")

finally:
    consumer.close()  # Ensure the consumer is closed properly