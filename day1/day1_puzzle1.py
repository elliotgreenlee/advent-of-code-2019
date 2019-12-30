def solve_day1puzzle1():
    with open("day1_data.txt", 'r') as f:
        fuel_sum = 0
        for line in f:
            mass = int(line)
            fuel = find_fuel(mass)
            fuel_sum += fuel
    return fuel_sum


def find_fuel(mass):
    return int(mass/3) - 2


def tests_day1puzzle1():
    if find_fuel(12) != 2:
        return False

    if find_fuel(14) != 2:
        return False

    if find_fuel(1969) != 654:
        return False

    if find_fuel(100756) != 33583:
        return False

    return True


def main():
    if tests_day1puzzle1():
        print("Day 1 Puzzle 1 answer: ", solve_day1puzzle1())


if __name__ == "__main__":
    main()
