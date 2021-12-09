


from typing import Dict, List


def solve_part_one(heatmap: List[List[int]]):
    """--- Day 9: Smoke Basin ---
These caves seem to be lava tubes. Parts are even still volcanically active; small hydrothermal vents release smoke into the caves that slowly settles like rain.

If you can model how the smoke flows through the caves, you might be able to avoid it and be that much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678
Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than any of its adjacent locations. Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are in the first row (a 1 and a 0), one is in the third row (a 5), and one is in the bottom row (also a 5). All other locations on the heightmap have some lower adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the risk levels of the low points are 2, 1, 6, and 6. The sum of the risk levels of all low points in the heightmap is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your heightmap?
"""
    risk_level = 0
    n_rows, n_cols = len(heatmap), len(heatmap[0])
    are_low_points = [[True] * n_cols for y in range(n_rows)]
    for y in range(n_rows):
        for x in range(n_cols):
            if x > 0 and are_low_points[y][x - 1]:
                # if x-1 is lower, then it remains a low point
                are_low_points[y][x - 1] = heatmap[y][x - 1] < heatmap[y][x]
            if y > 0 and are_low_points[y - 1][x]:
                are_low_points[y - 1][x] = heatmap[y - 1][x] < heatmap[y][x]
            if x < n_cols - 1 and are_low_points[y][x + 1]:
                are_low_points[y][x + 1] = heatmap[y][x + 1] < heatmap[y][x]
            if y < n_rows - 1 and are_low_points[y + 1][x]:
                are_low_points[y + 1][x] = heatmap[y + 1][x] < heatmap[y][x]
    for y in range(n_rows):
        for x in range(n_cols):
            if are_low_points[y][x]:
                risk_level += 1 + heatmap[y][x]
    return risk_level

def solve_part_two(input):
    """"""
    pass

def preprocess_input(input: str):
    heightmap = []
    for line in input.splitlines():
        heightmap.append(list(map(int, list(line))))
    return heightmap
    


#----- COPY BELOW ------
import requests
from secret import SESSION_ID, USER_AGENT # create a file named "secret.py"
# with the bearer token from your browser to log in to Advent Of Code

def get_aoc_input_auto(filename: str):
    year = int(filename[-13:-9])
    day = int(filename[-5:-3])
    return get_aoc_input(year, day, local=True)

def get_aoc_input(year, day, save=False, local=False) -> str:
    """ if you want to save the test input,
    first run it with save=True to save it,
    then run it with local=True to use the local version
    """
    import os
    BASE_URL = 'https://adventofcode.com'
    uri = f'{BASE_URL}/{year}/day/{day}/input'
    save_path = __file__[:-2]+'txt'
    if not local:
        input = requests.get(uri, 
            cookies={'session': SESSION_ID}, 
            headers={'User-Agent': USER_AGENT}
        ).text
        if save:
            with open(save_path, 'w') as f:
                f.write(input)
        return input
    # comment this to run the example below
    elif os.path.exists(save_path):
        with open(save_path, 'r') as f:
            return f.read()
    else:
        from inspect import cleandoc as indent
        # https://stackoverflow.com/questions/2504411/proper-indentation-for-python-multiline-strings
        return indent("""
            2199943210
            3987894921
            9856789892
            8767896789
            9899965678""")

if __name__ == "__main__":
    input = get_aoc_input_auto(__file__)
    input = preprocess_input(input)
    print(solve_part_one(input))
    print(solve_part_two(input))
