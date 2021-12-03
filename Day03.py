# --- Day 3: Binary Diagnostic ---
# The submarine has been making some odd creaking noises, so you ask it to produce a diagnostic report just in case.

# The diagnostic report (your puzzle input) consists of a list of binary numbers which, when decoded properly, can tell you many useful things about the conditions of the submarine. The first parameter to check is the power consumption.

# You need to use the binary numbers in the diagnostic report to generate two new binary numbers (called the gamma rate and the epsilon rate). The power consumption can then be found by multiplying the gamma rate by the epsilon rate.

# Each bit in the gamma rate can be determined by finding the most common bit in the corresponding position of all numbers in the diagnostic report. For example, given the following diagnostic report:

# 00100
# 11110
# 10110
# 10111
# 10101
# 01111
# 00111
# 11100
# 10000
# 11001
# 00010
# 01010
# Considering only the first bit of each number, there are five 0 bits and seven 1 bits. Since the most common bit is 1, the first bit of the gamma rate is 1.

# The most common second bit of the numbers in the diagnostic report is 0, so the second bit of the gamma rate is 0.

# The most common value of the third, fourth, and fifth bits are 1, 1, and 0, respectively, and so the final three bits of the gamma rate are 110.

# So, the gamma rate is the binary number 10110, or 22 in decimal.

# The epsilon rate is calculated in a similar way; rather than use the most common bit, the least common bit from each position is used. So, the epsilon rate is 01001, or 9 in decimal. Multiplying the gamma rate (22) by the epsilon rate (9) produces the power consumption, 198.

# Use the binary numbers in your diagnostic report to calculate the gamma rate and epsilon rate, then multiply them together. What is the power consumption of the submarine? (Be sure to represent your answer in decimal, not binary.)

def solve_part_one(diagnostic_report):
    gamma_rate = int(diagnostic_report["gamma_rate"], base=2)
    epsilon_rate = int(diagnostic_report["epsilon_rate"], base=2)
    return gamma_rate * epsilon_rate

def solve_part_two(diagnostic_report):
    pass


def preprocess_input(input: str):
    diagnostic_report = {
        "gamma_rate": "",
        "epsilon_rate": ""
    }
    lines = input.splitlines()
    bit_counts = [0] * len(lines[0])
    for line in lines:
        for i, char in enumerate(line):
            if int(char):
                bit_counts[i] += 1
            else:
                bit_counts[i] -= 1
    for bit_count in bit_counts:
        diagnostic_report["gamma_rate"] += "1" if bit_count > 0 else "0"
        diagnostic_report["epsilon_rate"] += "1" if bit_count <= 0 else "0"
    return diagnostic_report



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
        00100
        11110
        10110
        10111
        10101
        01111
        00111
        11100
        10000
        11001
        00010
        01010""")

input = get_aoc_input_auto(__file__)
input = preprocess_input(input)
print(solve_part_one(input))
print(solve_part_two(input))