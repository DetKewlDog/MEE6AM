import json
import requests

SUCCESS = 0
LEVELUP = 1


def calc_level_xp(lvl):
    return 5 * lvl**2 + 50 * lvl + 100


class User:

    def __init__(self, name, lvl, xp):
        self.name = name
        self.lvl = lvl
        self.xp = xp

    def add_xp(self, xp_to_add):
        xp_left = calc_level_xp(self.lvl) - self.xp - xp_to_add
        if xp_left <= 0:
            self.lvl += 1
            self.xp = 0
            return LEVELUP
        self.xp += xp_to_add
        return SUCCESS


def dump(dict):
    return json.dumps({key: value.__dict__ for key, value in dict.items()})


def load(dat):
    return {key: User(**value) for key, value in json.loads(dat).items()}


def fetch(guild_id):
    req = requests.get(
        f'https://mee6.xyz/api/plugins/levels/leaderboard/{guild_id}')
    dat = json.loads(req.text)
    users = {}
    for user in dat['players']:
        xp = user['xp'] - sum(
            [calc_level_xp(lvl) for lvl in range(0, user['level'])])
        users[user['id']] = User(user['username'], user['level'], xp)
    with open(f'{guild_id}.txt', 'w') as f:
        f.write(dump(users))

def calc_total_xp(lvl, xp):
    return xp + sum([calc_level_xp(lvl) for lvl in range(0, lvl)])

def calc_leaderboard():
    with open('922185010205822976.txt', 'r') as f:
        users = load(f.read())
    return dict(sorted(users.items(), key=lambda item: calc_total_xp(item[1].lvl, item[1].xp), reverse=True))
