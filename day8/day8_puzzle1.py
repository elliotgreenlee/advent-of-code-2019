from collections import Counter
import sys


def solve_day8puzzle1():
    with open("day8_data.txt", 'r') as f:
        digits = list(map(int, f.readline().strip()))
        
        min_zeroes = sys.maxsize
        min_answer = 0
        for i in range(0, len(digits), 150):
            counts = Counter(digits[i:i+150])
            if counts[0] < min_zeroes:
                min_zeroes = counts[0]
                min_answer = counts[1] * counts[2]
                
        return min_answer
            

def tests_day8puzzle1():
    return True


def main():
    if tests_day8puzzle1():
        print("Day 8 Puzzle 1 answer: ", solve_day8puzzle1())


if __name__ == "__main__":
    main()
