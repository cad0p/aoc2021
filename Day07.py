
def solve_part_one(crabs, fuel_cost=1):
    """--- Day 7: The Treachery of Whales ---
A giant whale has decided your submarine is its next meal, and it's much faster than you are. There's nowhere to run!

Suddenly, a swarm of crabs (each in its own tiny submarine - it's too deep for them otherwise) zooms in to rescue you! They seem to be preparing to blast a hole in the ocean floor; sensors indicate a massive underground cave system just beyond where they're aiming!

The crab submarines all need to be aligned before they'll have enough power to blast a large enough hole for your submarine to get through. However, it doesn't look like they'll be aligned before the whale catches you! Maybe you can help?

There's one major catch - crab submarines can only move horizontally.

You quickly make a list of the horizontal position of each crab (your puzzle input). Crab submarines have limited fuel, so you need to find a way to make all of their horizontal positions match while requiring them to spend as little fuel as possible.

For example, consider the following horizontal positions:

16,1,2,0,4,2,7,1,2,14
This means there's a crab with horizontal position 16, a crab with horizontal position 1, and so on.

Each change of 1 step in horizontal position of a single crab costs 1 fuel. You could choose any horizontal position to align them all on, but the one that costs the least fuel is horizontal position 2:

Move from 16 to 2: 14 fuel
Move from 1 to 2: 1 fuel
Move from 2 to 2: 0 fuel
Move from 0 to 2: 2 fuel
Move from 4 to 2: 2 fuel
Move from 2 to 2: 0 fuel
Move from 7 to 2: 5 fuel
Move from 1 to 2: 1 fuel
Move from 2 to 2: 0 fuel
Move from 14 to 2: 12 fuel
This costs a total of 37 fuel. This is the cheapest possible outcome; more expensive outcomes include aligning at position 1 (41 fuel), position 3 (39 fuel), or position 10 (71 fuel).

Determine the horizontal position that the crabs can align to using the least fuel possible. How much fuel must they spend to align to that position?
"""
    min_crab = max_crab = None
    avg_crab = 0
    n_crabs = 0
    for crab in crabs:
        avg_crab += crab
        n_crabs += 1
        if min_crab is None or crab < min_crab:
            min_crab = crab
        elif max_crab is None or crab > max_crab:
            max_crab = crab
    avg_crab /= n_crabs
    radius = 0
    prev_x_i = prev_x = x_i = x = None
    while (prev_x is None or x <= prev_x):
        prev_x_i, prev_x = x_i, x
        x_i, x = get_lowest_fuel(crabs, start=avg_crab, radius=radius)
        radius += 1
        

    return prev_x_i

def solve_part_two(input):
    pass


def get_fuel_sum(crabs, pos):
    return sum([abs(c - pos) for c in crabs])


def get_lowest_fuel(crabs, start=0, radius=0):
    if not radius and start == int(start):
            return start, get_fuel_sum(crabs, start)
    offset = 1 if start > 0 else -1
    if start == int(start):
        offset = 0
    start = int(start)
    pos = [start - radius, start + offset + radius]
    left_fuel_sum = get_fuel_sum(crabs, pos[0])
    right_fuel_sum = get_fuel_sum(crabs, pos[1])
    if left_fuel_sum < right_fuel_sum:
        return pos[0], left_fuel_sum
    else:
        return pos[1], right_fuel_sum

def preprocess_input(input):
    return list(map(int, input.split(',')))


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
            16,1,2,0,4,2,7,1,2,14""")

if __name__ == "__main__":
    input = get_aoc_input_auto(__file__)
    input = preprocess_input(input)
    print(solve_part_one(input))
    print(solve_part_two(input))
