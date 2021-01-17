from discord import Embed

import services.character_service as char_service
from configs.config import COLOR


async def select_char(bot, ctx, rp, emote_list):
    chars = char_service.get_chars_by_user(rp.id)

    if len(chars) == 0:
        await ctx.send('Vous n\'avez aucun personnage')
        return

    react = []
    chars_str = ''
    for i, char in enumerate(chars):
        status = ":green_circle:" if char.status == "Actif" else ":red_circle:"
        chars_str += f'>  〘{emote_list[i]}〙➤ {char.name} {status} \n> \n'
        react.append(emote_list[i])
    msg = await ctx.send(content=(f'`Personnage(s) `{rp.mention}` :`\n'
                                  'ஜ══════════════════ஜ\n'
                                  '> \n'
                                  f'{chars_str}'
                                  'ஜ══════════════════ஜ'))
    for r in react:
        await msg.add_reaction(r)

    try:
        react_sel, _u = await bot.wait_for(
            'reaction_add',
            timeout=10.0,
            check=lambda reaction, user: user == ctx.author and reaction.emoji in react
        )
        char_selected = chars[emote_list.index(react_sel.emoji)]
    except TimeoutError:
        raise TimeoutError
    finally:
        await msg.delete()

    return char_selected


async def validation(bot, ctx, char, validation_emote, txt):
    msg = await ctx.send(txt.format(char.name, char.discord_id))
    await msg.add_reaction(validation_emote[0])
    await msg.add_reaction(validation_emote[1])
    try:
        react_sel, _u = await bot.wait_for(
            'reaction_add',
            timeout=10.0,
            check=lambda reaction, user: user == ctx.author and reaction.emoji in validation_emote
        )
        return react_sel.emoji == validation_emote[0]
    except TimeoutError:
        raise TimeoutError
    finally:
        await msg.delete()


def character_embed(role_player, char):
    char_msg = Embed(colour=COLOR['primary'])
    char_msg.title = f'Voici les infos de votre perso :'
    char_msg.set_thumbnail(url=role_player.avatar_url)
    char_msg.add_field(name='Nom :', value=char.name, inline=False)
    char_msg.add_field(name='Septims :', value=f'{char.gold} :septims:', inline=False)
    char_msg.add_field(
        name='Salaire :',
        value=(f'Montant : {char.salary["amount"]}\n'
               f'Tout les : {char.salary["loop"]}jour(s)'
               if char.salary
               else 'Vous êtes au chomage :D'),
        inline=False
    )
    char_msg.add_field(
        name='Inventaire :',
        value=char.inventory.join(' - ') if char.salary else 'Vide',
        inline=False
    )
    char_msg.add_field(
        name='Statut :',
        value=char.status,
        inline=False,
    )
    return char_msg
