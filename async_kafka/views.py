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


async def send_basket_recommended_products_data(data: str) -> None:
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    try:
        await producer.send_and_wait("sendBasketRecommendedProductsData", data.encode('utf-8'))
    finally:
        await producer.stop()


async def send_request_for_products_data():
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    try:
        await producer.send_and_wait("requestProductsDataFromOrchestrator",
                                     b"Async string from python: give me products data from DB")
    finally:
        await producer.stop()


async def send_recommended_category_products_data(data: str) -> None:
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    try:
        await producer.send_and_wait("sendRecommendedCategoryProductsData", data.encode('utf-8'))
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
            await send_request_for_products_data()
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
        await consumer.stop()


async def consume_products_data():
    print("consume_products_data runs")
    consumer = AIOKafkaConsumer(
        'sendProductsDataToRecommendationModule',
        bootstrap_servers='localhost:9092',
        group_id="productsDataGroup")
    await consumer.start()
    try:
        async for msg in consumer:
            print("consumed by consume_products_data: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value.decode('UTF-8'))
            data = msg.value.decode('UTF-8')

            #todo insert Danil's methods instead of print():
            print(f"data for Danil's category method: {data}") #string data (products list) for Danil's method
            data_from_danils_method = "category products data"

            await send_recommended_category_products_data(data_from_danils_method)
            await asyncio.sleep(0.1)

    finally:
        await consumer.stop()

async def consume_request_for_basket_recommendation():
    print("consume_request_for_basket_recommendation runs")
    consumer = AIOKafkaConsumer(
        'requestForUserBasket',
        bootstrap_servers='localhost:9092',
        group_id="requestForUser")
    await consumer.start()
    try:
        async for msg in consumer:
            print("consumed: ", msg.value.decode('UTF-8'))
            data = msg.value.decode('UTF-8')
            print(data)

            # await send_request_for_orders_data()
            # await send_request_for_products_data()

            consumerConf = {
                'bootstrap.servers': "localhost:9092",
                'group.id': "syncConsumerGroup",
                'auto.offset.reset': "earliest"
            }
            c = Consumer(consumerConf)
            try:
                c.subscribe(["sendOrdersDataToRecommendationModule", "sendProductsDataToRecommendationModule"])
                print("Trying to get orders and products from Kafka...")
                msg = c.poll(timeout=1.0)
                if msg is None: continue
                if msg.error():
                    raise KafkaException(msg.error())
                else:
                    # todo insert Danil's methods instead of print():
                    print(f"orders and products data from msg: {msg}")
                    print(eval(msg.value().decode('utf-8')))
                    basket_recommended_products_data = "recommended products for basket"
                    print(F"basket_recommended_products_data: {basket_recommended_products_data}")
                    await send_basket_recommended_products_data(basket_recommended_products_data)
            finally:
                c.close()



            await asyncio.sleep(0.1)

    finally:
        await consumer.stop()



async def main():
    await asyncio.gather(consume_request_for_user(), consume_orders_data(),
                         consume_products_data(), consume_request_for_basket_recommendation())
