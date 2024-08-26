import pika
import random
import time

def wait_for_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            connection.close()
            break
        except pika.exceptions.AMQPConnectionError:
            print("Waiting for RabbitMQ to become available...")
            time.sleep(5)  

def generate_data():
    return {
        'temperature': random.uniform(-10, 40),
        'humidity': random.uniform(0, 100)
    }

wait_for_rabbitmq()

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='data_queue')

while True:
    data = generate_data()
    channel.basic_publish(exchange='',
                          routing_key='data_queue',
                          body=str(data))
    print(f"Sent {data}")
    time.sleep(5)
