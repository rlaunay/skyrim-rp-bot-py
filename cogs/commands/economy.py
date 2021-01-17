from asyncio import TimeoutError

from discord import Member
from discord.ext.commands import Cog, command, has_permissions

from exeptions.character import MoneyLimit
from utils.message import select_char, validation
from services.economy_service import add_money, remove_money


class Economy(Cog, name="Economie"):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f' - [Command] - [{self.qualified_name}] cog loaded')

    @command(aliases=['add'], usage="<user_mention> <money>")
    @has_permissions(administrator=True)
    async def add_money(self, ctx, member: Member, money: int):
        try:
            char_selected = await select_char(self.bot, ctx, member)
            txt = f'Voulez vous vraiment ajouter {money} septims à : `{char_selected.name}` ?'
            choice = await validation(self.bot, ctx, txt)
        except TimeoutError:
            return

        if choice:
            char_updated = add_money(char_selected.id, money)
            resp = f'Vous avez donné {money} septims à {char_updated.name} (total: {char_updated.money})'
        else:
            resp = 'Ajout d\'argent annuler'

        await ctx.send(resp)

    @command(aliases=['remove'], usage="<user_mention> <money>")
    @has_permissions(administrator=True)
    async def remove_money(self, ctx, member: Member, money: int):
        try:
            char_selected = await select_char(self.bot, ctx, member)
            txt = f'Voulez vous vraiment enlever {money} septims à : `{char_selected.name}` ?'
            choice = await validation(self.bot, ctx, txt)
        except TimeoutError:
            return

        if choice:
            try:
                char_updated = remove_money(char_selected.id, money)
                resp = f'Vous avez retirer {money} septims à {char_updated.name} (total: {char_updated.money})'
            except MoneyLimit:
                resp = f'Le joueur n\'a que {char_selected.money}'
        else:
            resp = 'Retrait d\'argent annuler'

        await ctx.send(resp)

    @command(aliases=['give'], usage="<user_mention> <money>")
    async def give_money(self, ctx,  member: Member, money: int):
        try:
            giver = await select_char(self.bot, ctx, ctx.author)
            receiver = await select_char(self.bot, ctx, member)
            txt = f'Voulez vous vraiment que {giver.name} donne {money} à {receiver.name} ?'
            choice = await validation(self.bot, ctx, txt)
        except TimeoutError:
            return

        if choice:
            try:
                giver_updated = remove_money(giver.id, money)
                receiver_updated = add_money(receiver.id, money)
                resp = f'{giver_updated.name} a donné {money} à {receiver_updated.name}'
            except MoneyLimit:
                resp = f'Vous n\'avez pas assez {giver.money}'
        else:
            resp = 'Echange annulé'

        await ctx.send(resp)


def setup(bot):
    bot.add_cog(Economy(bot))
