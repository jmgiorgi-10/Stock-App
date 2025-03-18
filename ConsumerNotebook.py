from kafka import KafkaConsumer
import json

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

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