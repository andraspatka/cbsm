# RabbitMQ demo

Start RabbitMQ:

```
docker run -d --hostname cbsm-logs -p 5672:5672 --name cbsm-logs rabbitmq:3
```

Python library:

```
python -m pip install pika --upgrade
```

# Demo

Based on rabbitmq official guide: https://www.rabbitmq.com/tutorials/tutorial-one-python.html

Running the demo:

- start the docker container with rabbitmq
- receive.py
- send.py

Send.py sends a message to the "logs" queue, receive.py receives all mesages send to this queue.