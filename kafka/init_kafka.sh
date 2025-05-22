
KAFKA_DIRECTORY="/Users/jmgiorgi/Documents/kafka_2.13-3.9.0"

cd "$KAFKA_DIRECTORY"
# Delete previous logs
rm -rf /tmp/kraft-combined-logs
# Generate Cluster ID
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"

# Format Log Directories
bin/kafka-storage.sh format --standalone -t "$KAFKA_CLUSTER_ID" -c config/kraft/reconfig-server.properties
# Start the Kafka Server
bin/kafka-server-start.sh config/kraft/reconfig-server.properties 

# Wait for Kafka to start before creating a topic
sleep 5

# Create stock topic
bin/kafka-topics.sh --create --topic stock-events --bootstrap-server localhost:9092