def solve_day1puzzle2():
    with open("day1_data.txt", 'r') as f:
        fuel_sum = 0
        for line in f:
            mass = int(line)
            fuel = find_fuel(mass)
            fuel_sum += fuel
        return fuel_sum


def find_fuel(mass):
    fuel_mass = int(mass/3) - 2
    if fuel_mass <= 0:
        return 0
    else:
        return fuel_mass + find_fuel(fuel_mass)


def tests_day1puzzle2():
    if find_fuel(12) != 2:
        return False

    if find_fuel(1969) != 966:
        return False

    if find_fuel(100756) != 50346:
        return False

    return True


def main():
    if tests_day1puzzle2():
        print("Day 1 Puzzle 2 answer: ", solve_day1puzzle2())


if __name__ == "__main__":
    main()
