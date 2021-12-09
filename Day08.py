


from typing import Dict, List

SIGNALS = 'abcdefg'

NUMBERS_LINES = {
    2: 1,
    3: 7,
    4: 4,
    5: [2, 3, 5],
    6: [0, 6, 9],
    7: 8
}
""" key: the number of lines, value: the numbers that have that number of lines """

NUMBERS_MAPPING = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: SIGNALS,
    9: 'abcdfg'
}

class Entry():
    def get_standard_digit(self, signal: str):
        digits = NUMBERS_LINES[len(signal)]
        if isinstance(digit:=digits, int):
            return digit
        for digit in digits:
            encoding = NUMBERS_MAPPING[digit]
            match = 0
            for c in signal:
                if c in encoding:
                    match += 1
            if match == len(encoding):
                return digit
        raise FileNotFoundError('digit not found')

    def __init__(self, signal_patterns, output_value):
        self.signal_patterns = signal_patterns
        self.output_value = output_value
        self.mapping = self.__get_mapping()
        self.decoded_digits = self.__decode_digits()
    
    def __repr__(self):
        return self.__dict__.__str__

    def __get_mapping(self):

        def update_mapping(digit, pattern):
            numbers_patterns[digit] = set(pattern)

        patterns_with_len: Dict[int, List[str]] = {}
        numbers_patterns: Dict[int, set[str]] = {n: None for n in NUMBERS_MAPPING}
        for pattern in self.signal_patterns:
            digits = NUMBERS_LINES[len(pattern)]
            # for example dab => 7
            # so, 7 (acf) a, c and f can only be in 'dab'
            if isinstance(digit:=digits, int):
                update_mapping(digit, pattern)    
            else:
                if len(pattern) not in patterns_with_len:
                    patterns_with_len[len(pattern)] = []
                patterns_with_len[len(pattern)].append(pattern)
        # print(patterns_with_len)
        # KEY THING: using 1, 4, 7 we derive 
        # got from: https://github.com/SnoozeySleepy/AdventofCode/blob/main/day8.py
        # len 5: 2, 3, 5
        # len 6: 0, 6, 9
        for len_pattern, patterns in patterns_with_len.items():
            for pattern in patterns:
                if len_pattern == 5: # 2, 3, 5
                    if (numbers_patterns[4] - numbers_patterns[1]).issubset(pattern):
                        update_mapping(5, pattern)
                    elif numbers_patterns[7].issubset(pattern):
                        update_mapping(3, pattern)
                    else:
                        update_mapping(2, pattern)
                elif len_pattern == 6: # 0, 6, 9
                    if not numbers_patterns[1].issubset(pattern):
                        update_mapping(6, pattern)
                    elif numbers_patterns[4].issubset(pattern):
                        update_mapping(9, pattern)
                    else:
                        update_mapping(0, pattern)

        
        def entry_mapping(signal: str):
            signal = set(signal)
            for number, pattern in numbers_patterns.items():
                if signal == pattern:
                    return number
        return entry_mapping

    def __decode_digits(self):
        digits = []
        for signal in self.output_value:
            digit = self.mapping(signal)
            digits.append(digit)
        return digits


def solve_part_one(notes: List[Entry]):
    """--- Day 8: Seven Segment Search ---
You barely reach the safety of the cave when the whale smashes into the cave mouth, collapsing it. Sensors indicate another exit to this cave at a much greater depth, so you have no choice but to press on.

As your submarine slowly makes its way through the cave system, you notice that the four-digit seven-segment displays in your submarine are malfunctioning; they must have been damaged during the escape. You'll be in a lot of trouble without them, so you'd better figure out what's wrong.

Each digit of a seven-segment display is rendered by turning on or off any of seven segments named a through g:

  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
So, to render a 1, only segments c and f would be turned on; the rest would be off. To render a 7, only segments a, c, and f would be turned on.

The problem is that the signals which control the segments have been mixed up on each display. The submarine is still trying to display numbers by producing output on signal wires a through g, but those wires are connected to segments randomly. Worse, the wire/segment connections are mixed up separately for each four-digit display! (All of the digits within a display use the same connections, though.)

So, you might know that only signal wires b and g are turned on, but that doesn't mean segments b and g are turned on: the only digit that uses two segments is 1, so it must mean segments c and f are meant to be on. With just that information, you still can't tell which wire (b/g) goes to which segment (c/f). For that, you'll need to collect more information.

For each display, you watch the changing signals for a while, make a note of all ten unique signal patterns you see, and then write down a single four digit output value (your puzzle input). Using the signal patterns, you should be able to work out which pattern corresponds to which digit.

For example, here is what you might see in a single entry in your notes:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf

(The entry is [was] wrapped here to two lines so it fits; in your notes, it will all be on a single line.)

Each entry consists of ten unique signal patterns, a | delimiter, and finally the four digit output value. Within an entry, the same wire/segment connections are used (but you don't know what the connections actually are). The unique signal patterns correspond to the ten different ways the submarine tries to render a digit using the current wire/segment connections. Because 7 is the only digit that uses three segments, dab in the above example means that to render a 7, signal lines d, a, and b are on. Because 4 is the only digit that uses four segments, eafb means that to render a 4, signal lines e, a, f, and b are on.

Using this information, you should be able to work out which combination of signal wires corresponds to each of the ten digits. Then, you can decode the four digit output value. Unfortunately, in the above example, all of the digits in the output value (cdfeb fcadb cdfeb cdbaf) use five segments and are more difficult to deduce.

For now, focus on the easy digits. Consider this larger example:

be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
Because the digits 1, 4, 7, and 8 each use a unique number of segments, you should be able to tell which combinations of signals correspond to those digits. Counting only digits in the output values (the part after | on each line), in the above example, there are 26 instances of digits that use a unique number of segments (highlighted above).

In the output values, how many times do digits 1, 4, 7, or 8 appear?
"""
    counter_simple_digits = 0
    for entry in notes:
        # # edit: this is for part 2
        # for pattern in entry.signal_patterns:
        #     if isinstance(NUMBERS_LINES[len(pattern)], int):
        #         # and it's not a list, meaning it's the only possible number that matches the pattern
        for digit in entry.output_value:
            if isinstance(NUMBERS_LINES[len(digit)], int):
                # and it's not a list, meaning it's the only possible number that matches the pattern
                # ant thut it's one of the simple digits
                counter_simple_digits += 1
    return counter_simple_digits

def solve_part_two(notes: List[Entry]):
    """--- Part Two ---
Through a little deduction, you should now be able to determine the remaining digits. Consider again the first example above:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf

After some careful analysis, the mapping between signal wires and segments only make sense in the following configuration:

 dddd
e    a
e    a
 ffff
g    b
g    b
 cccc
So, the unique signal patterns would correspond to the following digits:

acedgfb: 8
cdfbe: 5
gcdfa: 2
fbcad: 3
dab: 7
cefabd: 9
cdfgeb: 6
eafb: 4
cagedb: 0
ab: 1
Then, the four digits of the output value can be decoded:

cdfeb: 5
fcadb: 3
cdfeb: 5
cdbaf: 3
Therefore, the output value for this entry is 5353.

Following this same process for each entry in the second, larger example above, the output value of each entry can be determined:

fdgacbe cefdb cefbgd gcbe: 8394
fcgedb cgb dgebacf gc: 9781
cg cg fdcagb cbg: 1197
efabcd cedba gadfec cb: 9361
gecf egdcabf bgf bfgea: 4873
gebdcfa ecba ca fadegcb: 8418
cefg dcbef fcge gbcadfe: 4548
ed bcgafe cdgba cbgef: 1625
gbdfcae bgc cg cgb: 8717
fgae cfgab fg bagce: 4315
Adding all of the output values in this larger example produces 61229.

For each entry, determine all of the wire/segment connections and decode the four-digit output values. What do you get if you add up all of the output values?
"""
    sum_values = 0
    for entry in notes:
        value = ''
        for digit in entry.decoded_digits:
            value += str(digit)
        sum_values += int(value)
    return sum_values



def preprocess_input(input):
    notes = []
    for entry in input.splitlines():
        signal_patterns, output_value = entry.split(' | ')
        entry = Entry(
            signal_patterns=signal_patterns.split(' '),
            output_value=output_value.split(' ')
        )
        notes.append(entry)
    return notes
    


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
        # return("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf")
        return indent("""
            be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
            edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
            fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
            fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
            aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
            fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
            dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
            bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
            egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
            gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
            """)

if __name__ == "__main__":
    input = get_aoc_input_auto(__file__)
    input = preprocess_input(input)
    print(solve_part_one(input))
    print(solve_part_two(input))
