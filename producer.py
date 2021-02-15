# amqps://aiimmbpf:***@beaver.rmq.cloudamqp.com/aiimmbpf  
import pika, json

params = pika.URLParameters('amqps://aiimmbpf:99CmvXDsq5Rm5_YWpK3jRkDKGeWHpLaZ@beaver.rmq.cloudamqp.com/aiimmbpf')


connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)