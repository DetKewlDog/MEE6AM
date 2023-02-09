from interactions import *
from levels import *


class Ext(Extension):

    def __init__(self, client: Client) -> None:
        self.client: Client = client

    def chunks(self, lst):
        for i in range(0, len(lst), 10):
            yield lst[i:i + 10]

    def calc_lb(self):
        lb = calc_leaderboard()
        new_lb = []
        for id, usr in lb.items():
            part1 = f"> **{list(lb.keys()).index(id) + 1}. <@{id}>"
            part2 = f"Level {usr.lvl}**"
            part3 = f"{usr.xp}/{calc_level_xp(usr.lvl)} XP"
            new_lb.append(f"{part1:>32}{part2:>16}{part3:>16}")
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
        try:
            lb = self.calc_lb()
            p = '\n'.join(lb[page - 1])
            await ctx.send(f"**Showing Page #{page}/{len(lb)}**\n{p}",
                           allowed_mentions=AllowedMentions(users=[]))
        except Exception as e:
            await ctx.send('Invalid page number!', ephemeral=True)


def setup(client):
    Ext(client)
