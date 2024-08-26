import pika
import psycopg2
import time
import json

def wait_for_postgres():
    while True:
        try:
            global connection  
            connection = psycopg2.connect(
                dbname="sensor_data",
                user="postgres",
                password="postgres",
                host="postgres"
            )
            global cursor
            cursor = connection.cursor()
            break
        except psycopg2.OperationalError:
            print("Waiting for PostgreSQL to become available...")
            time.sleep(5)

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        cursor.execute("SELECT AVG(avg_temperature), AVG(avg_humidity) FROM processed_data")
        avg_temperature, avg_humidity = cursor.fetchone()
        if avg_temperature is None:
            avg_temperature = data['temperature']
            avg_humidity = data['humidity']
        else:
            avg_temperature = (data['temperature'] + avg_temperature) / 2
            avg_humidity = (data['humidity'] + avg_humidity) / 2
        cursor.execute(
            "INSERT INTO processed_data (avg_temperature, avg_humidity) VALUES (%s, %s)",
            (avg_temperature, avg_humidity)
        )
        connection.commit()
        print(f"Processed and saved: {body}")
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    wait_for_postgres()
    try:
        connection_rabbit = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection_rabbit.channel()
        channel.queue_declare(queue='data_queue')
        channel.basic_consume(queue='data_queue', on_message_callback=callback, auto_ack=True)
        
        print('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        if connection_rabbit.is_open:
            connection_rabbit.close()
        if connection:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    main()
