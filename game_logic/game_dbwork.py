import redis
import pymongo
import json
from typing import Union, Dict, Tuple
from main import client

r = redis.StrictRedis(
    host="localhost",
    port="6379",
    db=0
)

def game_get_from_db(player_id: int) -> Tuple[bool, Union[Dict, None]]:
    a = r.get(str(player_id) + ".game")
    if a is not None:
        a = json.load(a)
        return True, a
    else:
        a = client.game.player_data.find({'player_id': player_id})


print(game_get_from_db(4575647))
