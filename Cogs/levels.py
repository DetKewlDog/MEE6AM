from interactions import *
from levels import *


class Ext(Extension):

    def __init__(self, client: Client) -> None:
        self.client: Client = client

    def chunks(self, lst):
        for i in range(0, len(lst), 10):
            yield lst[i:i + 10]

    async def calc_lb(self, ctx):
        lb = calc_leaderboard(ctx.guild_id)
        new_lb = []
        guild = await ctx.get_guild()
        print(guild)
        members = await guild.get_members().flatten()
        members = {str(member.id): member for member in members}
        for id, usr in lb.items():
            if not id in members.keys():continue
            user = members[id].user
            part1 = f"{list(lb.keys()).index(id) + 1}. {user.username}#{user.discriminator}"
            part2 = f"Level {usr.lvl}"
            part3 = f"{usr.xp}/{calc_level_xp(usr.lvl)} XP"
            part4 = f"({calc_total_xp(usr.lvl, usr.xp)} XP Total)"
            new_lb.append(
                f"**``{part1:<24}{part2:<16}{part3:<16}``**``{part4:>16}``")
        return list(self.chunks(new_lb))

    @extension_command(name="levels",
                       description="Show the server leaderboard",
                       options=[
                           Option(name="page",
                                  description="Page number",
                                  type=OptionType.INTEGER,
                                  required=False)
                       ])
    async def _levels(self, ctx: CommandContext, page=1):
        await ctx.send('Loading, please wait...')
        try:
            lb = await self.calc_lb(ctx)
            p = '\n'.join(lb[page - 1])
            await ctx.send(f"**Showing Page #{page}/{len(lb)}**\n{p}\n")
        except:
            await ctx.send('Invalid page number!', ephemeral=True)


def setup(client):
    Ext(client)
