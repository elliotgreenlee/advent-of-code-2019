import numpy as np


def solve_day8puzzle1():
    with open("day8_data.txt", 'r') as f:
        digits = list(map(int, f.readline().strip()))
        actual = find_actual(digits, 25, 6)
        print(np.array(actual).reshape((6, 25)))
        return actual
        
        
def find_actual(digits, width, height):
    actual = [2] * (width * height)
    for i in range(0, len(digits), width * height):
        layer = digits[i:i + (width * height)]
        for j in range(0, len(actual)):
            if actual[j] == 2:
                actual[j] = layer[j]
    
    return actual


def tests_day8puzzle1():
    if find_actual([0, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 2, 0, 0, 0, 0], 2, 2) != [0, 1, 1, 0]:
        return False
    return True


def main():
    if tests_day8puzzle1():
        print("Day 8 Puzzle 1 answer: ", solve_day8puzzle1())


if __name__ == "__main__":
    main()