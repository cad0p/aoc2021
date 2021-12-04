from collections import deque
import re
import numpy as np
import os
from copy import deepcopy

def solve_part_one(bingo_subsystem):
    """--- Day 4: Giant Squid ---
You're already almost 1.5km (almost a mile) below the surface of the ocean, already so deep that you can't see any sunlight. What you can see, however, is a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are chosen at random, and the chosen number is marked on all boards on which it appears. (Numbers may not appear on all boards.) If all numbers in any row or any column of a board are marked, that board wins. (Diagonals don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass the time. It automatically generates a random order in which to draw numbers and a random set of boards (your puzzle input). For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners, but the boards are marked as follows (shown here adjacent to each other to save space):

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still no winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
At this point, the third board wins because it has at least one complete row or column of marked numbers (in this case, the entire top row is marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers on that board; in this case, the sum is 188. Then, multiply that sum by the number that was just called when the board won, 24, to get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win first. What will your final score be if you choose that board?

"""
    draw_order = bingo_subsystem["draw_order"]
    boards = bingo_subsystem["boards"]
    winner = None
    boards_status = boards.copy()
    draw_number = DrawNumber()
    i = 0
    while not winner and i < 50:
        draw = draw_order.popleft()
        winner, boards_status = draw_number(boards_status, draw)
        i += 1
    # print(f'\n\n\n\ndraw: {draw:2} iteration: {i:2}')
    # print_boards(boards_status, parallel=6)
    return get_score(boards_status[winner], draw)


def solve_part_two(bingo_subsystem):
    pass


def preprocess_input(input: str):
    lines = input.splitlines()
    bingo_subsystem = {
        "draw_order": deque(int(x) for x in lines[0].split(',')),
        "boards": get_boards(lines[1:])
    }
    return bingo_subsystem


def print_boards(boards, parallel=0):
    parallel_i = 0
    parallel_boards = []
    for board_i, board in enumerate(boards):
        if not parallel_boards:
            parallel_boards = deepcopy(board)
        elif parallel_i <= parallel:
            for i in range(len(board)):
                parallel_boards[i].extend(['    '] + board[i])
        parallel_i += 1
        
        if parallel_i > parallel or board_i == len(boards) - 1:
            print_board(parallel_boards)
            parallel_boards = []
            parallel_i = 0


def print_board(board):
    print()
    for row in board:
        for num in row:
            print(f'{num:2}', end=' ')
        print()


def get_score(board_status, last_draw):
    sum_unmarked_numbers = 0
    for row in board_status:
        for num in row:
            if isinstance(num, int):
                sum_unmarked_numbers += num
    return sum_unmarked_numbers * last_draw

class DrawNumber:
    def __init__(self):
        self.draw_i = 0
        """ the draw iteration """
    def __call__(self, boards_status, draw):
        self.draw_i += 1
        winner = None
        for b, board in enumerate(list(boards_status)):
            ver = [True] * len(board)
            hor = ver.copy()
            for i, row in enumerate(board):
                for j, num in enumerate(row):
                    if num == draw:
                        boards_status[b][i][j] = num = ''
                    
                    hor[i] = hor[i] and num == ''
                    ver[j] = ver[j] and num == ''
                    
                    if (j == len(board) - 1 and hor[i] 
                            or i == len(board) - 1 and ver[j]):
                        winner = b
                        # print("WINNER", winner)
        return winner, boards_status

def get_boards(boards_lines):
    boards = []
    board = []
    boards_lines.append('')
    for line in boards_lines:
        if line == '':
            if board:
                boards.append(board)
            board = []
            i = 0
            continue
        row = []
        if line[0] == ' ':
            line = line[1:]
        for num in re.split(' +', line):
            # CHECKED regular expression in line.split()
            row.append(int(num))
            pass
        board.append(row)
    return boards



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
    elif os.path.exists(save_path):
        with open(save_path, 'r') as f:
            return f.read()
    else:
        from inspect import cleandoc as indent
        # https://stackoverflow.com/questions/2504411/proper-indentation-for-python-multiline-strings
        return indent("""
            7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1
        
            22 13 17 11  0
             8  2 23  4 24
            21  9 14 16  7
             6 10  3 18  5
             1 12 20 15 19

             3 15  0  2 22
             9 18 13 17  5
            19  8  7 25 23
            20 11 10 24  4
            14 21 16 12  6

            14 21 17 24  4
            10 16 15  9 19
            18  8 23 26 20
            22 11 13  6  5
             2  0 12  3  7""")

input = get_aoc_input_auto(__file__)
input = preprocess_input(input)
print(solve_part_one(input))
print(solve_part_two(input))