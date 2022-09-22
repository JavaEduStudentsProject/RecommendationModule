from confluent_kafka import Producer
import socket


conf = {
    'bootstrap.servers': "localhost:9092",
    # 'client.id': socket.gethostname()
}

producer = Producer(conf)

def send():
    producer.produce("stringmsg", key="2", value="string from python")
    producer.flush()

def request_to_database():
    producer.produce("requestDataFromDB", key="3", value="give me data from DB")
    producer.flush()

if __name__ == '__main__':
    send()