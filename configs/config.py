from decouple import config

# recupération des variable d'envirronement du fichier .env

COLOR = {
    "primary": int(config('PRIMARY_COLOR'), 16)
}

BOT_SETTINGS = {
    "token": config('TOKEN'),
    "prefix": config('PREFIX'),
    "calendar_chan": config('CALENDAR_CHAN', cast=int)
}

DB_URL = config('DB_URL')
