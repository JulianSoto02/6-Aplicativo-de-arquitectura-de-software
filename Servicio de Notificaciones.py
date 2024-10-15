from flask import Flask, request, jsonify
import pika
import json

app = Flask(__name__)

# Configuración de RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='notifications')

@app.route('/notify', methods=['POST'])
def send_notification():
    notification = request.json
    channel.basic_publish(exchange='',
                          routing_key='notifications',
                          body=json.dumps(notification))
    return jsonify({"msg": "Notification sent"}), 200

def process_notification(ch, method, properties, body):
    notification = json.loads(body)
    # Aquí iría la lógica para enviar la notificación (email, push, etc.)
    print(f"Procesando notificación: {notification}")

channel.basic_consume(queue='notifications',
                      on_message_callback=process_notification,
                      auto_ack=True)

if __name__ == '__main__':
    app.run(port=5002)
    channel.start_consuming()
