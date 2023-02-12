from interactions import *
from datetime import datetime
import threading
import time
from levels import *
from DiscordLevelingCard import RankCard, Settings
from PIL import Image

card_settings = Settings(
    background=
    "https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png",
    text_color="white",
    bar_color="#00F9FF")


class Ext(Extension):

    def __init__(self, client: Client) -> None:
        self.client: Client = client

    @extension_command(name="rank",
                       description="Get your rank or another member's rank",
                       options=[
                           Option(name="member",
                                  description="Target @member",
                                  type=OptionType.USER,
                                  required=False)
                       ])
    async def _rank(self, ctx: CommandContext, member=None):
        if member == None:
            member = ctx.author

        with open(f'{ctx.guild_id}.txt', 'r') as f:
            users = load(f.read())


        msg = await ctx.send('Loading, please wait...')
        user = users[str(member.id)]
        lb = calc_leaderboard(ctx.guild_id)
        rank = list(lb.keys()).index(str(member.id)) + 1
        print(member)
        icon = member.user.avatar_url
        print(icon)
        a = RankCard(settings=card_settings,
                     avatar=icon,
                     level=user.lvl,
                     current_exp=user.xp,
                     max_exp=calc_level_xp(user.lvl),
                     username=user.name)
        image = await a.card2()
        img = Image.open(image)
        img.save('result.png')
        await msg.edit(content="", files=File('result.png'))


def setup(client):
    Ext(client)
