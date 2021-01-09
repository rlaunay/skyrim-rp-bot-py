from discord.ext.commands import Cog, command


class Divers(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f' - [Command] - [{self.qualified_name}] cog loaded')

    @command()
    async def ping(self, ctx):
        await ctx.send(f'Pong {round(self.bot.latency * 1000)}ms')


def setup(bot):
    bot.add_cog(Divers(bot))
