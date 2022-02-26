## list all kafka topics
kafka-topics --list --bootstrap-server kafka:9092

## create kafka topic
kafka-topics --bootstrap-server kafka:9092 --create --topic cargo-delivery-truck --partitions 1 --replication-factor 2 --config retention.ms=18000000

## describe kafka topic
kafka-topics --bootstrap-server kafka:9092 --topic cargo-delivery-truck --describe

## Flush kafka topic
kafka-configs --zookeeper zookeeper:2181 --alter --entity-type topics --entity-name cargo-delivery-truck --add-config retention.ms=1000
kafka-configs --zookeeper zookeeper:2181 --alter --entity-type topics --entity-name cargo-delivery-truck --add-config retention.ms=18000000

## get current offset for kafka topic
kafka-run-class kafka.tools.GetOffsetShell --broker-list kafka:9092 --topic cargo-delivery-truck

## delete kafka topic
kafka-topics --bootstrap-server kafka:9092 --delete --topic cargo-delivery-truck

## produce message to kafka topic
kafka-console-producer --broker-list kafka:9092 --topic cargo-delivery-truck

## consume message from kafka topic
kafka-console-consumer --bootstrap-server kafka:9092 --topic cargo-delivery-truck --from-beginning


