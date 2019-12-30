import numpy as np
import math
from collections import defaultdict


def read_puzzle_file(filename):
    with open(filename, 'r') as f:
        points = set()
        for y, line in enumerate(f):
            for x, point in enumerate(line):
                if point is '#':
                    points.add((x, y))
        
        return points


def number_angles(starting_point, other_points):
    angles = defaultdict(list)
    for point in other_points:
        angle = math.degrees(np.arctan2(point[1] - starting_point[1], point[0] - starting_point[0]))
        if angle < -90:
            angle += 360
        angle += 90
        distance = np.sqrt((point[0] - starting_point[0])**2 + (point[1] - starting_point[1])**2)
        angles[angle].append((distance, (point[0] - starting_point[0], point[1] - starting_point[1])))
    
    for angle in angles.keys():
        angles[angle] = sorted(angles[angle])
        
    return len(angles), angles


def find_best_station(asteroids):
    all_slope_counts = {}
    for station_asteroid in asteroids:
        working_copy_asteroids = asteroids.copy()
        working_copy_asteroids.remove(station_asteroid)
        number_of_angles, angles = number_angles(station_asteroid, working_copy_asteroids)
        all_slope_counts[number_of_angles] = angles

    return max(all_slope_counts.keys()), all_slope_counts[max(all_slope_counts.keys())]


def solve_day10puzzle2():
    asteroids = read_puzzle_file("day10_data.txt")
    best_station_count, best_station_angles = find_best_station(asteroids)
    
    counter = 0
    while len(best_station_angles) > 0:
        for angle in sorted(best_station_angles.keys()):
            distance, point = best_station_angles[angle].pop(0)
            counter += 1
            if counter == 200:
                return (23 + point[0]) * 100 + (19 + point[1])  # (23, 19) is the best asteroid location
            if len(best_station_angles[angle]) == 0:
                best_station_angles.pop(angle)


def tests_day10puzzle2():
    asteroids = read_puzzle_file("day10_test1.txt")
    if find_best_station(asteroids)[0] != 8:
        return False
    
    asteroids = read_puzzle_file("day10_test2.txt")
    if find_best_station(asteroids)[0] != 33:
        return False
    
    asteroids = read_puzzle_file("day10_test3.txt")
    if find_best_station(asteroids)[0] != 35:
        return False
    
    asteroids = read_puzzle_file("day10_test4.txt")
    if find_best_station(asteroids)[0] != 41:
        return False
    
    asteroids = read_puzzle_file("day10_test5.txt")
    if find_best_station(asteroids)[0] != 210:
        return False
    
    return True


def main():
    if tests_day10puzzle2():
        print("Day 10 Puzzle 2 answer: ", solve_day10puzzle2())


if __name__ == "__main__":
    main()
