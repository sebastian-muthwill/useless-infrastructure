from faker import Faker
import json
from uuid import uuid4
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient
import socket
from time import sleep
import logging
from datetime import datetime

# Container logs are not printed to stdout by default.
# Therefor we need to configure logging to print to stdout.
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

logging.info("producer container started")
kafka_conf = {'bootstrap.servers': 'kafka:9092',
        'client.id': "producer-1"}

def get_producer():
    producer_instance = Producer(kafka_conf)
    logging.debug("Trying if Kafka broker is running.")
    # Check if kafka broker is running using confuent_kafka.admin
    kafka_broker = {'bootstrap.servers': 'kafka:9092'}
    admin_client = AdminClient(kafka_broker)
    topics = admin_client.list_topics().topics

    if not topics: 
        logging.debug("No respose from Kafka broker, so it is not running yet. Will wait and try again.")
        return None
    logging.info("Kafka broker is running.")
    return producer_instance

producer = None
while not producer:
    sleep(2)
    producer = get_producer()

fake = Faker()

while True:
    blog = {
        "id": str(uuid4()),
        "title": fake.sentence(),
        "body": fake.text(800),
        "author": fake.name(),
        "created_at": str(fake.date_time_this_decade()),
        "url": fake.url(),
        "timestamp": datetime.now()
    }

    producer.produce('blog.new_blogpost', json.dumps(blog))
    logging.info(f"Blog {blog['id']} published successfully.")
    sleep(2)
