from decouple import config

# recupération des variable d'envirronement du fichier .env

COLOR = {
    "primary": int(config('PRIMARY_COLOR'), 16)
}

BOT_SETTINGS = {
    "token": config('TOKEN'),
    "prefix": config('PREFIX'),
    "calendar_chan": config('CALENDAR_CHAN', cast=int),
    "select_emote": ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'],
    "valid_emote": ['✅', '❌']
}

DB_URL = config('DB_URL')
