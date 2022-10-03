from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from confluent_kafka import Consumer, KafkaException
import asyncio

from CosineSimilarity import CosineSimilarity


async def send_request_for_orders_data():
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    try:
        await producer.send_and_wait("requestOrdersDataFromOrchestrator", b"Async string from python: give me orders data from DB")
    finally:
        await producer.stop()


async def send_recommended_products_data(data: str) -> None:
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    try:
        await producer.send_and_wait("sendRecommendedProductsData", data.encode('utf-8'))
    finally:
        await producer.stop()


async def consume_request_for_user():
    print("consume_request_for_user runs")
    consumer = AIOKafkaConsumer(
        'requestForUser',
        bootstrap_servers='localhost:9092',
        group_id="requestForUser")
    await consumer.start()
    try:
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value.decode('UTF-8'))
            data = msg.value.decode('UTF-8')
            print(data)
            await send_request_for_orders_data()
            await asyncio.sleep(0.1)

    finally:
        await consumer.stop()

async def consume_orders_data():
    print("consume_orders_data runs")
    consumer = AIOKafkaConsumer(
        'sendOrdersDataToRecommendationModule',
        bootstrap_servers='localhost:9092',
        group_id="receiveOrdersDataGroup")
    await consumer.start()
    try:
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value.decode('UTF-8'))
            data_from_kafka = msg.value.decode('UTF-8')
            print(data_from_kafka)

            consumerConf = {
                'bootstrap.servers': "localhost:9092",
                'group.id': "syncConsumerGroup",
                'auto.offset.reset': "earliest"
            }
            c = Consumer(consumerConf)
            try:
                c.subscribe(["requestForUser"])
                print("Trying to get id from Kafka...")
                msg = c.poll(timeout=1.0)
                if msg is None: continue
                if msg.error():
                    raise KafkaException(msg.error())
                else:
                    data = data_from_kafka
                    cs = CosineSimilarity(eval(msg.value().decode('utf-8')), data)
                    recommended_products_data = str(cs.define_recommended_product())
                    print(recommended_products_data)
                    await send_recommended_products_data(recommended_products_data)
            finally:
                c.close()

            await asyncio.sleep(0.1)

    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


# methods for Danil's algorithms



async def main():
    await asyncio.gather(consume_request_for_user(), consume_orders_data())
