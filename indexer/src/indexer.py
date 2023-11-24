import logging
import json
from opensearchpy import OpenSearch
from time import sleep
from confluent_kafka import Consumer
from confluent_kafka.admin import AdminClient

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
logging.info("indexer container started")
logging.info("Waiting for Kafka broker and Opensearch to be ready. Sleep for 20s.")

kafka_conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'indexer-1'    # when run multiple instances this groups them in one consumer group
}

host = 'opensearch'
port = 9200
auth = ('admin', 'admin') # For testing only. Don't store credentials in code.

def get_kafka_broker():
    consumer_instance = Consumer(kafka_conf)
    logging.debug("Trying if Kafka broker is running.")
    # Check if kafka broker is running using confuent_kafka.admin
    kafka_broker = {'bootstrap.servers': 'kafka:9092'}
    admin_client = AdminClient(kafka_broker)
    topics = admin_client.list_topics().topics

    if not topics: 
        logging.debug("No respose from Kafka broker, so it is not running yet. Will wait and try again.")
        return None
    logging.info("Kafka broker is running.")
    return consumer_instance


consumer = None
while not consumer:
    sleep(2)
    consumer = get_kafka_broker()
    
consumer.subscribe(['blog.new_blogpost'])

def get_opensearch_client():
    try:
        logging.info("Trying if Opensearch is running.")
        client = OpenSearch(
            hosts = [{'host': host, 'port': port}],
            http_auth = auth,
            use_ssl = True,            
            verify_certs = False,       # DONT USE IN PRODUCTION
            ssl_assert_hostname = False,
            ssl_show_warn = False
        )
        info = client.info()
        logging.info(f"Welcome to {info['version']['distribution']} {info['version']['number']}!")
    except Exception as e:
        logging.debug("No respose from Opensearch, so it is not running yet. Will wait and try again.")
        sleep(5)
        return None
    return client

client = None
while not client:
    client = get_opensearch_client()


try:
    index_name = 'blog-index'
    index_body = {
        'settings': {
            'index': {
            'number_of_shards': 4
            }
        },
        "mappings": {
            "properties": {
                "id": { "type" : "text" },
                "title": { "type" : "text" },
                "body": { "type" : "text" },
                "author": { "type" : "text" },
                "created_at": { "type" : "date" },
                "url": { "type" : "text" },
                "timestamp": { "type" : "date" },
                }
              }
    }

    response = client.indices.create(
    index_name, 
    body=index_body
    )

    logging.debug(response)
except Exception as e:
    logging.error(e)

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue

    if msg.error():
        logging.error("Consumer error: {}".format(msg.error()))
        continue

    logging.info('Received message: {}'.format(msg.value().decode('utf-8')))
    blog = json.loads(msg.value().decode('utf-8'))
    logging.info('Blog title: {}'.format(blog['title']))

    response = client.index(
    index = index_name,
    body = blog,
    id = blog['id'],
    refresh = True
    )
    logging.debug(response)
