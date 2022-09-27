from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import json

from CosineSimilarity import CosineSimilarity


async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait("requestOrdersDataFromOrchestrator", b"Async string from python: give me orders data from DB")
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


async def consume():
    consumer = AIOKafkaConsumer(
        'sendOrdersDataToRecommendationModule',
        bootstrap_servers='localhost:9092',
        group_id="receiveOrdersDataGroup")
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value.decode('UTF-8'))
            data = msg.value.decode('UTF-8')
            print(data)
            # data = str(json.loads(data)).replace("\'", "\"")
            # print(data)
            print(type(data))
            cs = CosineSimilarity("97", data)

    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

# async def main():
#     print('before await')
#     await asyncio.sleep(1)
#     print('hello')


