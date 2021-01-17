from exeptions.character import MoneyLimit
from models.character_model import Character


def add_money(doc_id, money):
    char = Character.objects(id=doc_id).first()
    char.money += money
    char.save()
    return char


def remove_money(doc_id, money):
    char = Character.objects(id=doc_id).first()
    if money > char.money:
        raise MoneyLimit
    char.money -= money
    char.save()
    return char
