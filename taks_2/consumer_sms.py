import pika
from mongoengine import connect
from models import Contact
import connect as conn

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='sms_queue', durable=True)


def send_sms(contact):
    print(f"Send sms to: {contact.phone_number}")


def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects.get(id=contact_id)
    send_sms(contact)
    contact.is_sms_sent = True
    contact.save()
    print(f"SMS sent for contact: {contact.full_name} ({contact.phone_number})")


channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages from the queue RabbitMQ (SMS)...')
channel.start_consuming()
