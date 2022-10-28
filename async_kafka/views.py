import sys

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from confluent_kafka import Consumer, KafkaException, KafkaError
import asyncio

from CosineSimilarity import CosineSimilarity
from BasketCategoriesAlgorithm import BasketCategoriesAlgorithm
from BestProductAlgorithm import BestProductsAlgorithm


async def send_request_for_orders_data():
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    try:
        await producer.send_and_wait("requestOrdersDataFromOrchestrator",
                                     b"Async string from python: give me orders data from DB")
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


async def send_request_for_products_and_orders_data():
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    try:
        await producer.send_and_wait("requestProductsAndOrdersDataFromOrchestrator",
                                     b"Async string from python: give me products and orders data from DB")
    finally:
        await producer.stop()


async def send_recommended_products_data(data: str) -> None:
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    try:
        await producer.send_and_wait("sendRecommendedProductsData", data.encode('utf-8'))
    finally:
        await producer.stop()


async def send_basket_category(data: str) -> None:
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    try:
        await producer.send_and_wait("sendBasketRecommendedProductsData", data.encode('utf-8'))
    finally:
        await producer.stop()


async def send_best_products(data: str) -> None:
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    try:
        await producer.send_and_wait("sendRecommendedBestProductsData", data.encode('utf-8'))
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
            print("consumed username: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value.decode('UTF-8'))
            data = msg.value.decode('UTF-8')
            print(data)
            await send_request_for_orders_data()
            await send_request_for_products_data()
            await asyncio.sleep(0.1)

    finally:
        await consumer.stop()


async def consume_orders_data():
    # sync_kafka_consumer()
    print("consume_orders_data runs")
    consumer = AIOKafkaConsumer(
        'sendOrdersDataToRecommendationModule',
        bootstrap_servers='localhost:9092',
        group_id="receiveOrdersDataGroup")
    await consumer.start()
    try:
        async for msg in consumer:
            print("consumed orders: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value.decode('UTF-8'))
            data_from_kafka = eval(msg.value.decode('UTF-8'))
            print(data_from_kafka)

            consumer_conf = {
                'bootstrap.servers': "localhost:9092",
                'group.id': "syncConsumer",
                'auto.offset.reset': "earliest"
            }
            c = Consumer(consumer_conf)
            try:
                c.subscribe(["syncRequestForUser"])
                print("Trying to get username from Kafka...")
                msg = c.poll(timeout=1.0)
                if msg is None: continue
                if msg.error():
                    raise KafkaException(msg.error())
                else:
                    print("msg.value():")
                    print(msg.topic())
                    print(msg.partition())
                    print(msg.value())
                    data = data_from_kafka
                    print(f"username: {eval(msg.value().decode('utf-8'))}")
                    cs = CosineSimilarity(eval(msg.value().decode('utf-8')), data)
                    recommended_products_data = str(cs.define_recommended_product())
                    print(recommended_products_data)
                    await send_recommended_products_data(recommended_products_data)
            finally:
                c.close()

            await asyncio.sleep(0.1)

    finally:
        await consumer.stop()


# def sync_kafka_consumer():
#     consumer_conf = {
#         'bootstrap.servers': "localhost:9092",
#         'group.id': "syncKafkaConsumer",
#         'auto.offset.reset': "earliest"
#     }
#     c = Consumer(consumer_conf)
#
#     try:
#         c.subscribe(["syncRequestForUser"])
#
#         while True:
#             print("Trying to get username in sync_kafka_consumer from Kafka...")
#             msg = c.poll(timeout=1.0)
#             if msg is None: continue
#
#             if msg.error():
#                 if msg.error().code() == KafkaError._PARTITION_EOF:
#                     sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
#                                      (msg.topic(), msg.partition(), msg.offset()))
#                     print('%% %s [%d] reached end at offset %d\n' %
#                                      (msg.topic(), msg.partition(), msg.offset()))
#                 elif msg.error():
#                     raise KafkaException(msg.error())
#
#             else:
#                 print("msg.value():")
#                 print(msg.topic())
#                 print(msg.partition())
#                 print(msg.value())
#     finally:
#         c.close()

async def consume_products_data():
    print("consume_products_data runs")
    consumer = AIOKafkaConsumer(
        'sendProductsDataToRecommendationModule',
        bootstrap_servers='localhost:9092',
        # group_id="productsDataGroup",
        # auto_offset_reset="latest")
        group_id="productsDataGroup")
    await consumer.start()
    try:
        async for msg in consumer:
            print("consumed by consume_products_data: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value.decode('UTF-8'))
            data = msg.value.decode('UTF-8')

            bp = BestProductsAlgorithm(data)
            best_product_data = str(bp.do_best_product_algorithm())
            best_product_data = best_product_data.replace("\'", "\"")

            await send_best_products(best_product_data)
            await asyncio.sleep(0.1)

    finally:
        await consumer.stop()


async def consume_request_for_basket_recommendation():
    print("consume_request_for_basket_recommendation runs")
    consumer = AIOKafkaConsumer(
        'requestForUserBasket',
        bootstrap_servers='localhost:9092',
        group_id="requestFromFrontBasket",
        auto_offset_reset="latest")
    await consumer.start()
    try:
        async for msg in consumer:
            print("consumed basketIdArray (first time): ", msg.value.decode('UTF-8'))
            data = msg.value.decode('UTF-8')
            print(data)
            await send_request_for_products_and_orders_data()
            await asyncio.sleep(0.1)

    finally:
        await consumer.stop()


async def consume_data_for_basket_recommendation():
    data_from_kafka = []
    data_from_front = None
    count = 0
    print("consume_data_for_basket_recommendation runs")
    consumer = AIOKafkaConsumer(
        'sendProductsDataFromDBForBasket', 'sendOrdersDataFromDBForBasket',
        bootstrap_servers='localhost:9092',
        group_id="requestForBasketRecommend")
    await consumer.start()

    try:
        async for msg in consumer:
            # print("consumed for basket (products, orders): ", msg.value.decode('UTF-8'))
            data_from_kafka.append(msg.value.decode('UTF-8'))

            raw_data = sync_basket_kafka_consumer()
            if raw_data is not None:
                data_from_front = eval(raw_data)
            print(f"data_from_front: {data_from_front}")
            # print(f"data_from_kafka:")
            # print(data_from_kafka)
            count += 1
            if count % 2 != 0:
                print("test 2")
            else:
                print("test 8")
                print(f"data_from_front: {data_from_front}")
                # print("ПРОДУКТЫ НА ВХОД МЕТОДА")
                # print(data_from_kafka[0])
                # print("ЗАКАЗЫ НА ВХОД МЕТОДА")
                # print(data_from_kafka[1])
                bs = BasketCategoriesAlgorithm(data_from_kafka[0], data_from_kafka[1], data_from_front)
                basket_categories_data = str(bs.do_basket_categories_algorithm())
                # print(f"final data_from_kafka: {data_from_kafka}")  # products and orders lists
                # print(f"final data_from_front: {data_from_front}")  # array with product ids from basket
                await send_basket_category(basket_categories_data)


        await asyncio.sleep(0.1)
    finally:
        await consumer.stop()


def sync_basket_kafka_consumer():
    print("sync_basket_kafka_consumer inited")
    consumer_conf = {
        'bootstrap.servers': "localhost:9092",
        'group.id': "syncBasketConsumerGroup",
        'auto.offset.reset': "earliest"
    }
    c = Consumer(consumer_conf)

    try:
        c.subscribe(["syncRequestForUserBasket"])

        # while True:
        print("Trying to get ids from basket in sync_basket_kafka_consumer from Kafka...")
        msg = c.poll(timeout=1.0)
        # if msg is None: continue
        if msg is None:
            return
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                 (msg.topic(), msg.partition(), msg.offset()))
                print('%% %s [%d] reached end at offset %d\n' %
                                 (msg.topic(), msg.partition(), msg.offset()))
            elif msg.error():
                raise KafkaException(msg.error())

        else:
            print("msg.value(): from basket in sync method")
            print(msg.value())
    finally:
        c.close()

    return msg.value()

async def main():
    await asyncio.gather(consume_request_for_user(), consume_orders_data(),
                         consume_products_data(), consume_request_for_basket_recommendation(),
                         consume_data_for_basket_recommendation())
