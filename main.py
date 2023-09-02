from app.playwright.get_page_dynamic_content import get_page_html_content
from app.selectolax.magalu_parser import MagaluItemParser
from app.rabbitmq.rabbitmq_receiver import RabbitMqReceiver
from app.postgres.pg_upsert import PostgresDB
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
import json


def rabbitmq_message_callback(
    channel: BlockingChannel, 
    method: Basic.Deliver, 
    properties: BasicProperties, 
    body: bytes
  ):
  
    print('New item received. Please wait...')
    message = json.loads(body) # converte a mensagem em json
    urls = message.get('magalu-item', '') # magalu-item é o nome da chave, o valor da chave é uma lista de strings (urls magalu)
    for url in urls:
      html_content = get_page_html_content(url)

      magalu_item_parser = MagaluItemParser(url, html_content)
      item = magalu_item_parser.get_item()
      PostgresDB.upsert_item(item)
      print('Item sucessfully inserted into database. Listening to new messages...')
    
    
if __name__ == "__main__":
  try:
    RabbitMqReceiver.listen(rabbitmq_message_callback)
  except Exception as e:
    print(e)