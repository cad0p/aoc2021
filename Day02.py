# --- Day 2: Dive! ---
# Now, you need to figure out how to pilot this thing.

# It seems like the submarine can take a series of commands like forward 1, down 2, or up 3:

# forward X increases the horizontal position by X units.
# down X increases the depth by X units.
# up X decreases the depth by X units.
# Note that since you're on a submarine, down and up affect your depth, and so they have the opposite result of what you might expect.

# The submarine seems to already have a planned course (your puzzle input). You should probably figure out where it's going. For example:

# forward 5
# down 5
# forward 8
# up 3
# down 8
# forward 2
# Your horizontal position and depth both start at 0. The steps above would then modify them as follows:

# forward 5 adds 5 to your horizontal position, a total of 5.
# down 5 adds 5 to your depth, resulting in a value of 5.
# forward 8 adds 8 to your horizontal position, a total of 13.
# up 3 decreases your depth by 3, resulting in a value of 2.
# down 8 adds 8 to your depth, resulting in a value of 10.
# forward 2 adds 2 to your horizontal position, a total of 15.
# After following these instructions, you would have a horizontal position of 15 and a depth of 10. (Multiplying these together produces 150.)

# Calculate the horizontal position and depth you would have after following the planned course. What do you get if you multiply your final horizontal position by your final depth?
def solve_part_1(movements):
    position = depth = 0
    for movement in movements:
        action, amount = movement
        if action == "forward":
            position += amount
        elif action == "down":
            depth += amount
        elif action == "up":
            depth -= amount
    return position * depth

def solve_part_2(movements):
    pass



def preprocess_input(input: str):
    movements = []
    # CHECKED read line from string
    for line in input.splitlines():
        action, amount = line.split(' ')
        movements.append((action, int(amount)))
    return movements

#----- COPY BELOW ------
import requests
from secret import SESSION_ID, USER_AGENT # create a file named "secret.py"
# with the bearer token from your browser to log in to Advent Of Code

def get_aoc_input_auto(filename: str):
    year = int(filename[-13:-9])
    day = int(filename[-5:-3])
    return get_aoc_input(year, day)

def get_aoc_input(year, day) -> str:
    BASE_URL = 'https://adventofcode.com'
    uri = f'{BASE_URL}/{year}/day/{day}/input'
    # decomment this to get the real input
    return requests.get(uri, 
        cookies={'session': SESSION_ID}, 
        headers={'User-Agent': USER_AGENT}
    ).text

    from inspect import cleandoc as indent
    # https://stackoverflow.com/questions/2504411/proper-indentation-for-python-multiline-strings
    return indent("""
        forward 5
        down 5
        forward 8
        up 3
        down 8
        forward 2""")

input = get_aoc_input_auto(__file__)
input = preprocess_input(input)
print(solve_part_1(input))
print(solve_part_2(input))