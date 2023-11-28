import redis
import pymongo

r = redis.StrictRedis(
    host="localhost",
    port="6379",
    db=0
)


def game_get_from_db(player_id: int):
    a = r.get(str(player_id) + ".game")
    return a


print(game_get_from_db(4575647))
