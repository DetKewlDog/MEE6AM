from interactions import *
from datetime import datetime
import threading
import time
from levels import *


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

        user = users[str(member.id)]
        lb = calc_leaderboard(ctx.guild_id)
        rank = list(lb.keys()).index(str(member.id)) + 1
        await ctx.send(
            f"{member.mention}'s level is **{user.lvl} (rank #{rank})** ({user.xp}/{calc_level_xp(user.lvl)} XP)",
            allowed_mentions=AllowedMentions(users=[]))


def setup(client):
    Ext(client)
