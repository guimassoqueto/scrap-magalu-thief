from pika import PlainCredentials, BlockingConnection, ConnectionParameters
from app.settings import (
                      RABBITMQ_DEFAULT_HOST, 
                      RABBITMQ_DEFAULT_USER, 
                      RABBITMQ_DEFAULT_PASS, 
                      RABBITMQ_RECEIVER_QUEUE
                    )


# def callback(
#     channel: BlockingChannel, 
#     method: Basic.Deliver, 
#     properties: BasicProperties, 
#     body: bytes
#   ):
#   ## Do something with body messages
#   print(body)


class RabbitMqReceiver:
  @staticmethod
  def listen(callback):
    """
    calback deve receber os mesmos parametros da funcao de mesmo nome
    (ver funcao callback)
    """
    credentials = PlainCredentials(RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS)
    connection = BlockingConnection(ConnectionParameters(RABBITMQ_DEFAULT_HOST, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(RABBITMQ_RECEIVER_QUEUE, durable=False)

    # consumer
    channel.basic_consume(
      queue=RABBITMQ_RECEIVER_QUEUE,
      auto_ack=False,
      on_message_callback=callback
    )

    print(f'Waiting for new messages [queue: {RABBITMQ_RECEIVER_QUEUE}]. To exit press CTRL+C')
    channel.start_consuming()