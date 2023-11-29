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
    if a is None:
        
    else:
        a = json.load(a)
        return True, a


print(game_get_from_db(4575647))
