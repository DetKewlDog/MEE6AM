from interactions import *
from levels import *


class Ext(Extension):

    def __init__(self, client: Client) -> None:
        self.client: Client = client

    @extension_command(name="customize",
                       description="Customize your Level Card")
    async def _bug(self, ctx: CommandContext):
        with open(f'{ctx.guild_id}.txt', 'r') as f:
            users = load(f.read())
        user = users[ctx.author.id]
        modal = Modal(
            title="Settings",
            custom_id="settings",
            components=[
                TextInput(style=TextStyleType.SHORT,
                          label="Bar Color:",
                          custom_id="color",
                          value=user.color[1:])
            ],
        )
        await ctx.popup(modal)

    @extension_modal("settings")
    async def settings_resp(self, ctx, color):
        with open(f'{ctx.guild_id}.txt', 'r') as f:
            users = load(f.read())
        if not ctx.author.id in users.keys():
            users[ctx.author.id] = User(message.author.username, 0, 0, '#00F9FF')
        users[ctx.author.id].color = f'#{color}'
        with open(f'{ctx.guild_id}.txt', 'w') as f:
            f.write(dump(users))
        await ctx.send('Updated Settings!', ephemeral=True)


def setup(client):
    Ext(client)
