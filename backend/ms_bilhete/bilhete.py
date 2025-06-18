# ========================================================================
# UTFPR - Sistemas Distribuidos
# ========================================================================
# MS Bilhete (publisher/subscriber)
# ========================================================================
import pika 
import os, sys
import json
import uuid

def gerar_bilhete(mensagem):
      return {
            "id_bilhete": str(uuid.uuid4()),
            "id_reserva": mensagem["id_reserva"],
      }


def publicar_bilhete(bilhete):
      connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
      channel = connection.channel()

      exchange_name = "sistema_exchange"
      routing_key = "bilhete-gerado"

      channel.exchange_declare(exchange=exchange_name,
                               exchange_type='direct',
                               durable=True)
      
      channel.queue_declare(queue=routing_key, durable=True)
      channel.queue_bind(exchange=exchange_name,
                         queue=routing_key,
                         routing_key=routing_key)
      
      channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=json.dumps(bilhete),
            properties=pika.BasicProperties(delivery_mode=2)
      )

      connection.close()

      print("Bilhete publicado")


def callback(ch, method, properties, body):
      try:
            mensagem = json.loads(body)
            dados_reserva = mensagem["mensagem"]
            
            print("Assinatura validada. Gerando bilhete...")
            bilhete = gerar_bilhete(dados_reserva)
            print("Bilhete gerado.")
            publicar_bilhete(bilhete)
      except Exception as e:
            print(f"Falha callback bilhete {e}")


def main():
      connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
      channel = connection.channel()

      channel.queue_declare(queue='pagamento-aprovado', durable=True)
      channel.basic_consume(queue='pagamento-aprovado',
                            on_message_callback=callback,
                            auto_ack=True)
      
      print("MS Bilhete - aguardando aprovações de pagamento...")
      channel.start_consuming()

if __name__ == '__main__':
      try:
            main()
      except KeyboardInterrupt:
            print("Interrupted")
            try:
                  sys.exit(0)
            except SystemExit:
                  os._exit(0)
