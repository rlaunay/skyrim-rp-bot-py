import os

from discord.ext import commands

from configs.config import BOT_SETTINGS

# instanciation du bot
bot = commands.Bot(command_prefix=BOT_SETTINGS['prefix'])

cogs_dirs = ['commands', 'events', 'tasks']

# Charge dynamiquement les Cogs pour les dossier commands / events / tasks
for dir in cogs_dirs:
    for file in os.listdir(f'cogs/{dir}'):
        if os.path.isfile(os.path.join(f'cogs/{dir}', file)) and file.endswith('.py'):
            ext = file[:-3]
            bot.load_extension(f'cogs.{dir}.{ext}')

bot.run(BOT_SETTINGS['token'])
