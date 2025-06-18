# ========================================================================
# UTFPR - Sistemas Distribuidos
# ========================================================================
# MS Pagamento (publisher/subscriber)
# ========================================================================
import pika 
import json
import base64
from random import choice

def callback(ch, method, properties, body):
      mensagem = json.loads(body)
      print(mensagem)

def publica_na_fila(routing_key, mensagem):
      nova_mensagem = mensagem
      connection = pika.BlockingConnection(pika.ConnectionParameters("localhost")) 
      channel = connection.channel()

      exchange = "sistema_exchange"
      
      channel.exchange_declare(exchange=exchange,
                               exchange_type="direct",
                               durable=True) 
      channel.queue_declare(queue=routing_key, durable=True)
      channel.queue_bind(exchange=exchange,
                         queue=routing_key,
                         routing_key=routing_key) 

      channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(nova_mensagem),
            properties=pika.BasicProperties(delivery_mode=2)
      )   

      connection.close()

      print(f"Mensagem '{routing_key}' publicada")

def escutar_fila():
      print("MS Pagamento aguardando reservas...")

      connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
      channel = connection.channel()

      exchange_name = 'sistema_exchange'
      routing_key = 'reserva-criada'

      channel.queue_declare(queue=routing_key, durable=True)

      channel.queue_bind(exchange=exchange_name,
                         queue=routing_key,
                         routing_key=routing_key)
      
      channel.basic_consume(queue=routing_key, 
                            on_message_callback=callback, 
                            auto_ack=True)

      channel.start_consuming()
