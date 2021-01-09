from decouple import config

# recupération des variable d'envirronement du fichier .env

COLOR = {
    "primary": config('PRIMARY_COLOR')
}

BOT_SETTINGS = {
    "token": config('TOKEN'),
    "prefix": config('PREFIX'),
    "calendar_chan": config('CALENDAR_CHAN')
}