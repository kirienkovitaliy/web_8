from mongoengine import Document, StringField, BooleanField


class Contact(Document):
    full_name = StringField()
    email = StringField()
    is_email_sent = BooleanField(default=False)
    phone_number = StringField()
    is_sms_sent = BooleanField(default=False)
    delivery_method = StringField(choices=['email', 'sms'], default='email')
