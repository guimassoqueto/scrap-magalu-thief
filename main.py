from app.scraper.magalu_scraper import Magalu
from app.settings import MAX_CONCURRENCY
from app.infra.rabbitmq.rabbitmq_receiver import RabbitMqReceiver
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from asyncio import Semaphore, run
import json


concurrency_limit = Semaphore(MAX_CONCURRENCY)

def rabbitmq_message_callback(
    channel: BlockingChannel, 
    method: Basic.Deliver, 
    properties: BasicProperties, 
    body: bytes
  ):
  
    print('New item received. Please wait...')
    
    message = json.loads(body) # converte a mensagem em json
    urls = message.get('magalu-item', []) # magalu-item é o nome da chave, o valor da chave é uma lista de strings (urls magalu)
    
    result = run(Magalu.exec(urls, concurrency_limit)) # executa a busca e inserção do elemento no banco de dados
    if result:
      channel.basic_ack(delivery_tag = method.delivery_tag)
      print("Item(s) inserted. Listening to new messages [queue: magalu-item]. Press CTRL+C to exit")
    
if __name__ == "__main__":
  try:
    RabbitMqReceiver.listen(rabbitmq_message_callback)
  except Exception as e:
    print(e)