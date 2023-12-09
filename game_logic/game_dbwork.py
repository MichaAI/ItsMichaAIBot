import redis
import pymongo
import json
import bson
from typing import Union, Dict, Tuple, Any, Awaitable
from main import client

r = redis.StrictRedis(
    host="localhost",
    port="6379",
    db=0
)


def game_get_from_db(player_id: int) -> Tuple[bool, Union[Dict, None]]:
    redis_player = str(player_id) + ".game"
    a = r.get(redis_player)
    if a is not None:
        a = json.loads(a)
        r.expire(redis_player, 600)
        return True, a
    else:
        a = dict(client.game.player_data.find_one({'player_id': player_id}))
        if not a:
            return False, None
        else:
            return False, a


def insert_to_db(player_id: int, seed=int,

                 x: int = 0, y: int = 0, health: int = 3,
                 weapons: dict = dict(), artefacts: dict = dict(),
                 to_mongo: bool = False, **kwargs):
    a = {
        "player_id": player_id,
        "seed": seed,
        "x": x,
        "y": y,
        "health": health,
        "weapons": weapons,
        "artefacts": artefacts
    }

    too_redis = json.dumps(a)

    r.set(name=str(player_id) + ".game", value=too_redis, ex=600)

    if to_mongo:
        b = list(client.game.player_data.find({'player_id': player_id}))
        if b == []:
            client.game.player_data.insert_one(a)
        else:
            client.game.player_data.update_one({'player_id': player_id}, {'$set': a})
