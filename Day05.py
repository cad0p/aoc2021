def solve_part_one(vent_lines):
    """--- Day 5: Hydrothermal Venture ---
You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce large, opaque clouds, so it would be best to avoid them if possible.

They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at both ends. In other words:

An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....
In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the number of lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap. In the above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two lines overlap?

"""
    # let's use a hash map to keep track of the points already passed
    dangerous_n_points = 0
    visited_points = {}
    """ hash map to keep track of the points already passed """
    for vent_line in vent_lines:
        start_loc, end_loc = vent_line
        start_x, start_y = start_loc
        end_x, end_y = end_loc

        x_range = min(start_x, end_x), max(start_x, end_x) + 1
        y_range = min(start_y, end_y), max(start_y, end_y) + 1
        
        # add constraint to only follow straight lines:
        if x_range[1] - x_range[0] > 1 and y_range[1] - y_range[0] > 1:
            continue

        for x in range(*x_range):
            for y in range(*y_range):
                point_string = f'{x},{y}'
                if point_string in visited_points:
                    if visited_points[point_string] == 1:
                        dangerous_n_points += 1
                    visited_points[point_string] += 1
                else:
                    visited_points[point_string] = 1

    return dangerous_n_points

def solve_part_two(vent_lines):
    """--- Part Two ---
Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture; you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever be horizontal, vertical, or a diagonal line at exactly 45 degrees. In other words:

An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
Considering all lines from the above example would now produce the following diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....
You still need to determine the number of points where at least two lines overlap. In the above example, this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?"""
    # let's use a hash map to keep track of the points already passed
    dangerous_n_points = 0
    visited_points = {}
    """ hash map to keep track of the points already passed """
    for vent_line in vent_lines:
        start_loc, end_loc = vent_line
        start_x, start_y = start_loc
        end_x, end_y = end_loc

        x_range = min(start_x, end_x), max(start_x, end_x) + 1
        y_range = min(start_y, end_y), max(start_y, end_y) + 1
        
        # add constraint to only follow straight lines and diagonal lines:
        if      (x_range[1] - x_range[0] > 1 and y_range[1] - y_range[0] > 1
                and x_range[1] - x_range[0] != y_range[1] - y_range[0]):
            continue

        x, y = start_x, start_y
        for i in range(max(x_range[1] - x_range[0], y_range[1] - y_range[0])):
            point_string = f'{x},{y}'
            if point_string in visited_points:
                if visited_points[point_string] == 1:
                    dangerous_n_points += 1
                visited_points[point_string] += 1
            else:
                visited_points[point_string] = 1
            
            if start_x == end_x:
                pass
            elif x_range[0] == start_x:
                x += 1
            elif x_range[0] == end_x:
                x -= 1
            # don't need to act on horizontal lines
            # same for y
            if start_y == end_y:
                pass
            elif y_range[0] == start_y:
                y += 1
            elif y_range[0] == end_y:
                y -= 1
            

    return dangerous_n_points

def preprocess_input(input):
    vent_lines = []
    for line in input.splitlines():
        locations = []
        for location in line.split(' -> '):
            locations.append([int(num) for num in location.split(',')])
        vent_lines.append(locations)
    return vent_lines


#----- COPY BELOW ------
import requests
from secret import SESSION_ID, USER_AGENT # create a file named "secret.py"
# with the bearer token from your browser to log in to Advent Of Code

def get_aoc_input_auto(filename: str):
    year = int(filename[-13:-9])
    day = int(filename[-5:-3])
    return get_aoc_input(year, day, local=False)

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
            0,9 -> 5,9
            8,0 -> 0,8
            9,4 -> 3,4
            2,2 -> 2,1
            7,0 -> 7,4
            6,4 -> 2,0
            0,9 -> 2,9
            3,4 -> 1,4
            0,0 -> 8,8
            5,5 -> 8,2""")

if __name__ == "__main__":
    input = get_aoc_input_auto(__file__)
    input = preprocess_input(input)
    print(solve_part_one(input))
    print(solve_part_two(input))