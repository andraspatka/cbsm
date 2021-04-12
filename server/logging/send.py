#!/usr/bin/env python3
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='logs')
channel.basic_publish(exchange='', routing_key='logs', body='Hello world log message2')

print("Log message sent to RabbitMQ channel: logs")

connection.close()