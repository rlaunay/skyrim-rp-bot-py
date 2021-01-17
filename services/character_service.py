from models.character_model import Character
from exeptions.character import CharacterLimit


def get_chars_by_user(discord_id):
    chars = Character.objects(discord_id=discord_id)
    return chars


def create(discord_id, name):
    chars = get_chars_by_user(discord_id)
    if len(chars) > 9:
        raise CharacterLimit
    char = Character(discord_id=discord_id, name=name, gold=1000)
    char.save()
    return {"name": char.name, "discord_id": char.discord_id}


def delete_character(doc_id):
    Character.objects(id=doc_id).delete()


def change_status(doc_id):
    char = Character.objects(id=doc_id).first()
    char.status = 'Actif' if char.status == 'Inactif' else 'Inactif'
    char.save()
