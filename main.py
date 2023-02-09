from interactions import *
import os
import keep_alive
import threading
import time
from levels import *
import random

cogs: list = ["Cogs.rank", "Cogs.levels"]
client = 0
try:
    client = Client(token=os.getenv('TOKEN'))
except:
    os.system('kill 1')

BOT_ID = 1072826728642252913


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


cooldown_lst = []


def do_cooldown(id):
    time.sleep(60)
    cooldown_lst.remove(id)


@client.event
async def on_message_create(message):
    users = []
    id = str(message.author.id)
    if id == BOT_ID: return
    if id in cooldown_lst: return
    cooldown_lst.append(id)
    t = threading.Thread(target=do_cooldown, args=(id, ))
    t.start()

    with open('922185010205822976.txt', 'r') as f:
        users = load(f.read())

    try:
        if not id in keys:
            users[id] = User(message.author.username, 0, 0)
        res = users[id].add_xp(random.randint(15, 25))
        users[id].name = message.author.username
        if res == 1:
            channel = await message.get_channel()
            await channel.send(
                f'GG <@{id}>, you just advanced to level {users[id].lvl}!')

        with open('922185010205822976.txt', 'w') as f:
            f.write(dump(users))
    except:
        pass


keep_alive.keep_alive()

try:
    client.start()
except:
    os.system('kill 1')
