import datetime

from perlin_noise import PerlinNoise

width = 13
height = 13
threshold = 0.035


def generate_game(seed, x_offset, y_offset):
    now = datetime.datetime.now()
    cave_map = [[0 for _ in range(height)] for _ in range(width)]
    noise = PerlinNoise(octaves=1, seed=seed)

    for x in range(width):
        for y in range(height):
            value = noise([(x + x_offset) * 0.2, (y + y_offset) * 0.2])
            if value >= threshold:
                cave_map[x][y] = "⬜"
            else:
                cave_map[x][y] = "⬛"

    cave_map[6][6] = "🕵️‍♂️"
    future = datetime.datetime.now()
    print(f"{(future - now).microseconds} ms")
    return cave_map


def find_start(seed):
    x = 0
    noise = PerlinNoise(octaves=1, seed=seed)
    value = noise([x * 0.2, 0])
    while value >= threshold:
        x += 1
        value = noise([x * 0.2, 0])
    print(x)
    return x
