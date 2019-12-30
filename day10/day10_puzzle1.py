import math


def read_puzzle_file(filename):
    with open(filename, 'r') as f:
        points = set()
        for y, line in enumerate(f):
            for x, point in enumerate(line):
                if point is '#':
                    points.add((x, y))
                    
        return points
    
        
def number_slopes(starting_point, other_points):
    slopes = set()
    for point in other_points:
        try:
            slope = str((point[1] - starting_point[1]) / (point[0] - starting_point[0]))
        except ZeroDivisionError:
            slope = str(math.inf)
        
        if point[0] > starting_point[0]:
            slope = 'right' + slope
        elif point[0] < starting_point[0]:
            slope = 'left' + slope
        
        if point[1] > starting_point[1]:
            slope = 'above' + slope
        elif point[1] < starting_point[1]:
            slope = 'below' + slope
        slopes.add(slope)

    if len(slopes) == 278:
        print(starting_point)
    return len(slopes)
    
    
def find_best_station(asteroids):
    # whichever starting point has the maximum number of slopes is the best
    all_slope_counts = []
    for station_asteroid in asteroids:
        working_copy_asteroids = asteroids.copy()
        working_copy_asteroids.remove(station_asteroid)
        all_slope_counts.append(number_slopes(station_asteroid, working_copy_asteroids))
        
    return max(all_slope_counts)
        

def solve_day10puzzle1():
    asteroids = read_puzzle_file("day10_data.txt")
    return find_best_station(asteroids)
    

def tests_day10puzzle1():
    asteroids = read_puzzle_file("day10_test1.txt")
    if find_best_station(asteroids) != 8:
        return False

    asteroids = read_puzzle_file("day10_test2.txt")
    if find_best_station(asteroids) != 33:
        return False
    
    asteroids = read_puzzle_file("day10_test3.txt")
    if find_best_station(asteroids) != 35:
        return False
    
    asteroids = read_puzzle_file("day10_test4.txt")
    if find_best_station(asteroids) != 41:
        return False
    
    asteroids = read_puzzle_file("day10_test5.txt")
    if find_best_station(asteroids) != 210:
        return False
    
    return True


def main():
    if tests_day10puzzle1():
        print("Day 10 Puzzle 1 answer: ", solve_day10puzzle1())


if __name__ == "__main__":
    main()
