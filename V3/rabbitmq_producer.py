import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='broadcast', exchange_type='fanout')
message = 'big bang!'
channel.basic_publish(
    exchange='broadcast',
    routing_key='',
    body=message,
)
print("[v] Send %r" % message)
connection.close()
