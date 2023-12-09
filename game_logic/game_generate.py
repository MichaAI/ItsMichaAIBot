from perlin_noise import PerlinNoise

width = 13
height = 13
threshold = 0.035


def generate_game(seed, x_offset, y_offset):
    cave_map = [[0 for _ in range(height)] for _ in range(width)]
    noise = PerlinNoise(octaves=1, seed=seed)

    for x in range(width):
        for y in range(height):
            value = noise([(x + x_offset) * 0.2, (y + y_offset) * 0.2])
            if value > threshold:
                cave_map[x][y] = "⬜"
            else:
                cave_map[x][y] = "⬛"

    cave_map[6][6] = ("🕵️‍♂️")
    # '\n'.join([''.join(str(cell) for cell in row) for row in cave_map])
    return cave_map


cave_map = generate_game(23, 23, 23)
a = '\n'.join([''.join(str(cell) for cell in row) for row in cave_map])
print(a)
