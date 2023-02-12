import interactions
import os
import keep_alive
import threading
import time
from levels import *
import random

cogs: list = ["Cogs.rank", "Cogs.levels", "Cogs.customize"]
client = 0
client = interactions.Client(
    token=os.getenv('TOKEN'),
    intents=interactions.Intents.GUILD_MEMBERS | interactions.Intents.DEFAULT,
)

BOT_ID = '1072826728642252913'


@client.event
async def on_ready():
    global users
    # fetch(922185010205822976)
    print("Bot is ready!")
    for cog in cogs:
        try:
            print(f"Loading cog {cog}")
            client.load(cog)
            print(f"Loaded cog {cog}")
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load cog {}\n{}".format(cog, exc))


cooldown_dict = {}


def do_cooldown(id, guild_id):
    print(cooldown_dict[guild_id])
    time.sleep(60)
    cooldown_dict[guild_id].remove(id)
    print(cooldown_dict[guild_id])


@client.event
async def on_message_create(message):
    users = []
    id = str(message.author.id)
    if message.author.bot: return
    guild_id = message.guild_id
    if not guild_id in cooldown_dict.keys():
        cooldown_dict[guild_id] = []
    if id in cooldown_dict[guild_id]: return

    cooldown_dict[guild_id].append(id)
    t = threading.Thread(target=do_cooldown, args=(
        id,
        guild_id,
    ))
    t.start()

    with open(f'{guild_id}.txt', 'r') as f:
        users = load(f.read())

    if not id in users.keys():
        users[id] = User(message.author.username, 0, 0, '#00F9FF')
    res = users[id].add_xp(random.randint(15, 25))
    users[id].name = message.author.username
    if res == 1:
        channel = await message.get_channel()
        await channel.send(
            f'GG <@{id}>, you just advanced to level {users[id].lvl}!')

    with open(f'{message.guild_id}.txt', 'w') as f:
        f.write(dump(users))


keep_alive.keep_alive()

try:
    client.start()
except:
    os.system('kill 1')
