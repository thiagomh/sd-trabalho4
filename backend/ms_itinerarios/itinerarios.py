import pika, json
from services import atualizar_cabines_disponiveis

def callback_criada(ch, method, properties, body):
    try:
        dados = json.loads(body)
        print("Reserva criada recebida.", dados)
        atualizar_cabines_disponiveis(
            dados["nome_navio"],
            dados["data_embarque"],
            dados["cabines"],
            "criar"
        )

    except Exception as e:
        print(f"Erro no callback-reserva-criada. {e}")

def callback_cancelada(ch, method, properties, body):
    try:
        dados = json.loads(body)
        print("Reserva cancelada recebida.", dados)
        atualizar_cabines_disponiveis(
            dados["nome_navio"],
            dados["data_embarque"],
            dados["cabines"],
            "cancelar"
        )

    except Exception as e:
        print(f"Erro no callback-reserva-cancelada. {e}")

def escutar_fila(routing_key, callback):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
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