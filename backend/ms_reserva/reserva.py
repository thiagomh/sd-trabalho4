# ========================================================================
# UTFPR - Sistemas Distribuidos
# ========================================================================
# MS Reserva (publisher/subscriber)
# ========================================================================
import pika 
import json
import requests

def publicar_reserva(id_reserva, nome_navio, data_embarque, passageiros, cabines, routing_key):
      nova_reserva = {
            "id_reserva": id_reserva,
            "nome_navio": nome_navio,
            "data_embarque": data_embarque,
            "passageiros": passageiros,
            "cabines": cabines
      }

      connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
      )
      channel = connection.channel()

      exchange_name = "sistema_exchange"

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
            body=json.dumps(nova_reserva),
            properties=pika.BasicProperties(delivery_mode=2)
      )

      connection.close()


def callback_aprovado(ch, method, properties, body):
      try:
            mensagem = json.loads(body)
            print(mensagem)

            print("Pagamento Aprovado.")
            
      except Exception as e:
            print(f"Erro no callback-pagamento-aprovado. {e}")

def callback_recusado(ch, method, properties, body):
      try:
            dados = json.loads(body)
            mensagem = dados["mensagem"]
            reserva_id = mensagem.get("reserva_id")
            try:
                  resp = requests.delete(f"http://localhost:8000/reservar/{reserva_id}")
                  if resp.status_code == 200:
                        print(f"Reserva {reserva_id} cancelada com sucesso via callback")
                  else:
                        print(f"Falha ao cancelar reserva {reserva_id}: {resp.text}")
            except Exception as e:
                  print(f"Erro ao cancelar reserva via callback: {e}")

            print("Pagamento Recusado. Reserva Cancelada.")
            
      except Exception as e:
            print(f"Erro no callback-pagamento-recusado. {e}")


def callback_bilhete(ch, method, properties, body):
      try:
            mensagem = json.loads(body)
            print(mensagem)

            print("Bilhete Gerado.")
            
      except Exception as e:
            print(f"Erro no callback-bilhete. {e}")


def escutar_fila(routing_key, callback):
      connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
      channel = connection.channel()

      exchange_name = 'sistema_exchange'
      
      channel.queue_declare(queue=routing_key, durable=True)
     

      channel.queue_bind(exchange=exchange_name,
                         queue=routing_key,
                         routing_key=routing_key)
      
      channel.basic_consume(queue=routing_key,
                            on_message_callback=callback,
                            auto_ack=True)
      
      channel.start_consuming()
