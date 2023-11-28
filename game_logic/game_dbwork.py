import redis
import pymongo
from typing import Union, Dict, Tuple

r = redis.StrictRedis(
    host="localhost",
    port="6379",
    db=0
)


def game_get_from_db(player_id: int) -> Tuple[bool, Union[Dict, None]]:
    a = r.get(str(player_id) + ".game")
    if a is None:



print(game_get_from_db(4575647))
