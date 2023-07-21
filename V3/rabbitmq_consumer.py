import pika
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='broadcast', exchange_type='fanout')

result = channel.queue_declare(queue='',exclusive=True)
# 不指定queue名字，Rabbit会随机分配一个名字，并在使用此queue的消费者断开后,自动将queue删除
queue_name = result.method.queue
channel.queue_bind(exchange='broadcast',queue=queue_name)
print(" [*] Waiting for broadcast. To exit press Ctrl+C")

def callback(ch, method, properties, body):
    print(" [v] Get broadcast:",body)

channel.basic_consume(queue=queue_name, on_message_callback=callback)
channel.start_consuming()
