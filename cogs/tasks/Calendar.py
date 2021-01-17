from datetime import datetime
import asyncio

from discord.ext.commands import Cog
from discord.ext import tasks
import pytz

from configs.config import BOT_SETTINGS


class Calendar(Cog):
    def __init__(self, bot):
        self.skyrim_day = [
            'Morndas',
            'Tirdas',
            'Middas',
            'Turdas',
            'Fredas',
            'Loredas',
            'Sundas',
        ]
        self.skyrim_month = [
            'Primétoile',
            'Clairciel',
            'Semailles',
            'Ondepluie',
            'Plantaisons',
            "Mi-l'an",
            'Hautzénith',
            'Vifazur',
            'Âtrefeu',
            'Soufflegivre',
            'Sombreciel',
            'Soirétoile',
        ]
        self.channel = None
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        self.channel = self.bot.get_channel(BOT_SETTINGS['calendar_chan'])
        self.calendar.start()
        print(f' - [Tasks] - [{self.qualified_name}] cog loaded')

    @tasks.loop(hours=24)
    async def calendar(self):
        """
        Met à jour le channel voulut avec la date de skyrim
        :return: void
        """
        date_now = datetime.now()
        timezone = pytz.timezone("Europe/Amsterdam")
        date = date_now.astimezone(timezone)

        await self.channel.edit(
            name=f'{self.skyrim_day[date.weekday()]} {date.day} {self.skyrim_month[date.month - 1]}')
        print('Calendar up to date')

    @calendar.before_loop
    async def before_calendar(self):
        """
        Check chaque second si il est 0h et 0minute
        :return:
        """
        for _seconds in range(60 * 60 * 24):
            date_now = datetime.now()
            timezone = pytz.timezone("Europe/Amsterdam")
            date = date_now.astimezone(timezone)
            if date.hour == 0 and date.minute == 0:
                return
            await asyncio.sleep(1)


def setup(bot):
    bot.add_cog(Calendar(bot))
