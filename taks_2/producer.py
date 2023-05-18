import pika
from faker import Faker
from mongoengine import connect
from models import Contact
import connect as conn


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()


fake = Faker()


def main():
    for _ in range(10):
        full_name = fake.name()
        email = fake.email()
        phone_number = fake.phone_number()
        contact = Contact(full_name=full_name, email=email, phone_number=phone_number)
        contact.save()

        channel.basic_publish(
            exchange='',
            routing_key='sms_queue',
            body=str(contact.id),
            properties=pika.BasicProperties(delivery_mode=2)
        )

        channel.basic_publish(
            exchange='',
            routing_key='email_queue',
            body=str(contact.id),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        print(f"sent for contact: {contact.full_name} ({contact.phone_number})")
        print(f"sent for contact: {contact.full_name} ({contact.email})")
    print("The producer.py script is complete.")
    connection.close()


if __name__ == '__main__':
    main()
