from asyncio import TimeoutError

from discord import Member
from discord.ext.commands import Cog, command, has_permissions, group

import services.character_service as char_service
from utils.message import select_char, validation, character_embed


class Character(Cog, name="Personnage"):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f' - [Command] - [{self.qualified_name}] cog loaded')

    @group(aliases=['perso', 'char'], invoke_without_command=True)
    async def character(self, ctx, member: Member = None):
        role_player = ctx.author if not member else member
        try:
            char_selected = await select_char(self.bot, ctx, role_player)
        except TimeoutError:
            return
        await ctx.send(embed=character_embed(role_player, char_selected))

    @character.command(aliases=['n'], usage="<user_mention> <character_name>")
    @has_permissions(administrator=True)
    async def new(self, ctx, member: Member, *, name):
        try:
            txt = f'Voulez vous vraiment créer le personnage `{name}` pour {member.mention} ?'
            choice = await validation(self.bot, ctx, txt)
        except TimeoutError:
            return

        if choice:
            try:
                res = char_service.create(member.id, name)
                await ctx.send(f'Le personnage {res["name"]} à été créer pour le joueur <@{res["discord_id"]}>')
            except char_service.CharacterLimit:
                await ctx.send(f'{member.mention} à déjà 9 personnages de créer !')
        else:
            await ctx.send(f'Creation de personnage annuler')

    @character.command(aliases=['s'])
    @has_permissions(administrator=True)
    async def status(self, ctx, member: Member = None):
        role_player = ctx.author if not member else member
        try:
            char_selected = await select_char(self.bot, ctx, role_player)
            txt = f'Voulez vous vraiment changer le statut de : `{char_selected.name}` ?'
            choice = await validation(self.bot, ctx, txt)
        except TimeoutError:
            return

        if choice:
            char_service.change_status(char_selected.id)
            await ctx.send(f'Le statut de `{char_selected.name}` à correctement été mis à jour')
        else:
            await ctx.send(f'Changement de statut annuler')

    @character.command(aliases=['d'])
    @has_permissions(administrator=True)
    async def delete(self, ctx, member: Member = None):
        role_player = ctx.author if not member else member

        try:
            char_selected = await select_char(self.bot, ctx, role_player)
            txt = f'Voulez vous vraiment supprimer : `{char_selected.name}` ?'
            choice = await validation(self.bot, ctx, txt)
        except TimeoutError:
            return

        if choice:
            char_service.delete_character(char_selected.id)
            await ctx.send(f'Le personnage `{char_selected.name}` à correctement été supprimer')
        else:
            await ctx.send(f'Suppression annuler')


def setup(bot):
    bot.add_cog(Character(bot))
