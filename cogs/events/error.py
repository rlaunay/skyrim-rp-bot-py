from discord.ext.commands import Cog, CommandNotFound


class Error(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f' - [Event] - [{self.qualified_name}] cog loaded')

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send(f'Commande `{ctx.message.content}` inconnue tapez `{ctx.prefix}help` pour plus d\'info')


def setup(bot):
    bot.add_cog(Error(bot))
