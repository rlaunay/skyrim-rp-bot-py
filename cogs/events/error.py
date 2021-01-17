from discord.ext.commands import Cog, CommandNotFound, MissingRequiredArgument, BadArgument, MissingPermissions


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

        if isinstance(error, (MissingRequiredArgument, BadArgument)):
            await ctx.send(f'Commande incomplète `{ctx.prefix}{ctx.command} {ctx.command.usage}`')

        if isinstance(error, MissingPermissions):
            await ctx.send(f'Vous n\'avez pas les permissions d\'utiliser cette commande `{ctx.prefix}{ctx.command}`')

        print('[ERROR] :', error)


def setup(bot):
    bot.add_cog(Error(bot))
