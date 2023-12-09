import redis
import pymongo
import json
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
        a = json.load(a)
        r.expire(redis_player, 600)
        return True, a
    else:
        a = list(client.game.player_data.find({'player_id': player_id}))
        if not a:
            return False, None
        else:
            return False, a


def insert_to_db(player_id: int, x: int, y: int, health: int, weapons: dict, artefacts: dict, to_mongo: bool = False):
    a = {
        "player_id": player_id,
        "x": x,
        "y": y,
        "health": health,
        "weapons": weapons,
        "artefacts": artefacts
    }

    too_redis = json.dumps(a)

    r.set(name=str(player_id) + ".game", value=too_redis, ex=600)

    if to_mongo:
        a = list(client.game.player_data.find({'player_id': player_id}))
        if not a:
            client.game.player_data.insert_one(a)
        else:
            client.game.player_data.update_one({'player_id': player_id}, {'$set': a})
