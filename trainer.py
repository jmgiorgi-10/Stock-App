##
## Online training of lstm
##

from collections import deque
from kafka import KafkaConsumer
import json
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from lstm import LSTM

## Features

# Open - price at which assest starts trading at beginning of time interval.
# High - highest price asset reaches during the interval.
# Low - lowest price asset reaches within interval.
# Close - price at which asset stops trading at end of interval.

## Target

# Predict the next closing price.

class KafkaLSTMConsumer:
    def __init__(self, topic, model, seq_length=10, bootstrap_servers="localhost:9092"):
        # Initialize Kafka Consumer
        self.consumer = KafkaConsumer(
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.model = model
        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.01)
        # number of past time steps used for prediction
        self.seq_length = seq_length

        # Queue for sliding window #
        self.sequence_window = deque(maxlen=seq_length)
        self.y_train = None

    # Process the kafka message
    def process_message(self, message):

        print("Processing the latest message")

        try:

            data = message.value

            open_price = data.get("open")
            high_price = data.get("high")
            low_price = data.get("low")
            close_price = data.get("close")

            feature_vector = [open_price, high_price, low_price, close_price]

            if None not in feature_vector:

                feature_tensor = torch.tensor(feature_vector, dtype=torch.float32)
                self.sequence_window.append(feature_tensor)

                if len(self.sequence_window) == self.seq_length:

                    if self.y_train is not None:

                        X_train = torch.stack(list(self.sequence_window)).unsqueeze(0)
                        y_train_tensor = torch.tensor([[self.y_train]], dtype=torch.float32)

                        # Online training
                        model.train()
                        self.optimizer.zero_grad()
                        y_pred = model(X_train)
                        loss = self.criterion(y_pred, y_train_tensor)
                        loss.backward()
                        self.optimizer.step()

                        print(f"Training step loss: {loss.item():.4f}")


        except Exception as e:

            print(f"Error: {e}")

    def consume(self):

        print("Listening for messages...")
        for message in self.consumer:
            self.process_message(message.value)


if __name__ == "__main__":

    topic = "stock-events"

    input_size = 5
    hidden_size = 16
    output_size = 1
    num_layers = 1
    seq_length = 10 # amount of past time steps.
    model = LSTM(input_size, hidden_size, output_size, num_layers)

    ## Start the Kafka Consumer, subscribing to stock-events topic ##
    kafka_consumer = KafkaLSTMConsumer(topic, model)

    ## Main online training and evaluation loop ##
    while True:

        kafka_consumer.consume()