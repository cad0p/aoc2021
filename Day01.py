# --- Day 1: Sonar Sweep ---
# You're minding your own business on a ship at sea when the overboard alarm goes off! You rush to see if you can help. Apparently, one of the Elves tripped and accidentally sent the sleigh keys flying into the ocean!

# Before you know it, you're inside a submarine the Elves keep ready for situations like this. It's covered in Christmas lights (because of course it is), and it even has an experimental antenna that should be able to track the keys if you can boost its signal strength high enough; there's a little meter that indicates the antenna's signal strength by displaying 0-50 stars.

# Your instincts tell you that in order to save Christmas, you'll need to get all fifty stars by December 25th.

# Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

# As the submarine drops below the surface of the ocean, it automatically performs a sonar sweep of the nearby sea floor. On a small screen, the sonar sweep report (your puzzle input) appears: each line is a measurement of the sea floor depth as the sweep looks further and further away from the submarine.

# For example, suppose you had the following report:

# 199
# 200
# 208
# 210
# 200
# 207
# 240
# 269
# 260
# 263
# This report indicates that, scanning outward from the submarine, the sonar sweep found depths of 199, 200, 208, 210, and so on.

# The first order of business is to figure out how quickly the depth increases, just so you know what you're dealing with - you never know if the keys will get carried into deeper water by an ocean current or a fish or something.

# To do this, count the number of times a depth measurement increases from the previous measurement. (There is no measurement before the first measurement.) In the example above, the changes are as follows:

# 199 (N/A - no previous measurement)
# 200 (increased)
# 208 (increased)
# 210 (increased)
# 200 (decreased)
# 207 (increased)
# 240 (increased)
# 269 (increased)
# 260 (decreased)
# 263 (increased)
# In this example, there are 7 measurements that are larger than the previous measurement.

# How many measurements are larger than the previous measurement?

def solve_part_1(measurements):
    """
    measurements: list of integers
    returns: how many numbers are larger than the previous measurement
    """
    larger = 0
    prev_measurement = measurements[0]
    for measurement in measurements:
        if measurement > prev_measurement:
            larger += 1
        prev_measurement = measurement
    return larger

# --- Part Two ---
# Considering every single measurement isn't as useful as you expected: there's just too much noise in the data.

# Instead, consider sums of a three-measurement sliding window. Again considering the above example:

# 199  A      
# 200  A B    
# 208  A B C  
# 210    B C D
# 200  E   C D
# 207  E F   D
# 240  E F G  
# 269    F G H
# 260      G H
# 263        H
# Start by comparing the first and second three-measurement windows. The measurements in the first window are marked A (199, 200, 208); their sum is 199 + 200 + 208 = 607. The second window is marked B (200, 208, 210); its sum is 618. The sum of measurements in the second window is larger than the sum of the first, so this first comparison increased.

# Your goal now is to count the number of times the sum of measurements in this sliding window increases from the previous sum. So, compare A with B, then compare B with C, then C with D, and so on. Stop when there aren't enough measurements left to create a new three-measurement sum.

# In the above example, the sum of each three-measurement window is as follows:

# A: 607 (N/A - no previous sum)
# B: 618 (increased)
# C: 618 (no change)
# D: 617 (decreased)
# E: 647 (increased)
# F: 716 (increased)
# G: 769 (increased)
# H: 792 (increased)
# In this example, there are 5 sums that are larger than the previous sum.

# Consider sums of a three-measurement sliding window. How many sums are larger than the previous sum?

def solve_part_2(measurements):
    larger_sums = 0
    k = 3
    """ sliding window """
    prev_sum = sum(measurements[:k])
    for i in range(1, len(measurements) - k + 1):
        current_sum = sum(measurements[i:i+k])
        if current_sum > prev_sum:
            larger_sums += 1
        prev_sum = current_sum

    return larger_sums


def preprocess_input(input: str):
    measurements = []
    # CHECKED read line from string
    for line in input.splitlines():
        measurements.append(int(line))
    return measurements

#----- COPY BELOW ------
import requests
from secret import SESSION_ID, USER_AGENT # create a file named "secret.py"
# with the bearer token from your browser to log in to Advent Of Code

def get_aoc_input(year, day) -> str:
    BASE_URL = 'https://adventofcode.com'
    uri = f'{BASE_URL}/{year}/day/{day}/input'
    return requests.get(uri, 
        cookies={'session': SESSION_ID}, 
        headers={'User-Agent': USER_AGENT}
    ).text
    return """199
    200
    208
    210
    200
    207
    240
    269
    260
    263"""

input = get_aoc_input(2021, 1)
input = preprocess_input(input)
print(solve_part_1(input))
print(solve_part_2(input))