from mongoengine import *


class Salary(EmbeddedDocument):
    loop = IntField(default=1, min_value=1)
    amount = IntField(min_value=1, required=True)


class Character(Document):
    discord_id = IntField(required=True)
    name = StringField(required=True)
    money = IntField(required=True)
    salary = EmbeddedDocumentField(Salary)
    inventory = ListField(StringField())
    status = StringField(default="Actif")

    meta = {'collection': 'characters'}
