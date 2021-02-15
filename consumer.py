# amqps://aiimmbpf:***@beaver.rmq.cloudamqp.com/aiimmbpf  
import pika, json
from main import Product, db

params = pika.URLParameters('amqps://aiimmbpf:99CmvXDsq5Rm5_YWpK3jRkDKGeWHpLaZ@beaver.rmq.cloudamqp.com/aiimmbpf')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print('recive in main')
    print(body)
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        print('product created')
        db.session.commit()

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        print('product updated')

        db.session.commit()

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('product deleted')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started consuming')

channel.start_consuming()

channel.close()

