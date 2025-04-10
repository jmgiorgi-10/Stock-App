from kafka import KafkaConsumer
import json
import mysql.connector

## Features ##

# Open - price at which assest starts trading at beginning of time interval.
# High - highest price asset reaches during the interval.
# Low - lowest price asset reaches within interval.
# Close - price at which asset stops trading at end of interval.


# Initialize Kafka Consumer
consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='riverplate10',
    database='stocks'
)

cursor = conn.cursor()

# MySQL Table
create_table_query = '''
CREATE TABLE IF NOT EXISTS StockEvents (
    open DECIMAL(10, 4),
    high DECIMAL(10, 4),
    low DECIMAL(10, 4),
    close DECIMAL(10, 4),
    volume INT
);
'''

cursor.execute(create_table_query)
conn.commit()

# Subscribe to the 'users' topic
topic = 'stock-events'
consumer.subscribe([topic])

# Consumer Loop
try:
    for message in consumer:
        print(f"Received message from {message.topic}: {message.value}")

        data = json.loads(message.value)

        print(data)
        sql = """
        INSERT INTO StockEvents (open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        values = (data['1. open'], data['2. high'], data['3. low'], data['4. close'], data['5. volume'])

        cursor.execute(sql, values)
        conn.commit()

except KeyboardInterrupt:
    print("Consumer stopped manually.")


finally:
    consumer.close()  # Ensure the consumer is closed properly