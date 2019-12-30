import sys
x = 0
y = 1


def solve_day3puzzle1():
    with open("day3_data.txt", 'r') as f:
        wirepath1 = f.readline().strip().split(',')
        wirepath2 = f.readline().strip().split(',')
        
        return intersection_least_distance(wirepath1, wirepath2)
        
        
def intersection_least_distance(wirepath1, wirepath2):
    wirepath_points1 = find_all_points(wirepath1)
    wirepath_points2 = find_all_points(wirepath2)
    
    intersections = find_intersections(wirepath_points1, wirepath_points2)
    
    return find_least_distance(intersections)


def find_all_points(wirepath):
    wirepath_points = {}
    point1 = (0, 0)
    for instruction in wirepath:
        direction = instruction[0]
        distance = int(instruction[1:])
        for i in range(1, distance + 1):
            if direction == 'U':
                point2 = (point1[x], point1[y] + i)
            elif direction == 'R':
                point2 = (point1[x] + i, point1[y])
            elif direction == 'D':
                point2 = (point1[x], point1[y] - i)
            elif direction == 'L':
                point2 = (point1[x] - i, point1[y])
            else:
                print("oohhh noooo")
                exit(1)

            wirepath_points[point2] = 0
        point1 = point2
    
    return wirepath_points


def find_intersections(wirepath_points1, wirepath_points2):
    return set(wirepath_points1.keys()).intersection(set(wirepath_points2.keys()))


def find_least_distance(intersections):
    least_distance = sys.maxsize
    for intersection in intersections:
        manhattan_distance = abs(intersection[x]) + abs(intersection[y])
        if manhattan_distance < least_distance:
            least_distance = manhattan_distance
    return least_distance


def tests_day3puzzle1():
    if intersection_least_distance("R8,U5,L5,D3".split(','),
                                   "U7,R6,D4,L4".split(',')) != 6:
        print("did not return 6, the correct answer.\n")
        return False
    
    if intersection_least_distance("R75,D30,R83,U83,L12,D49,R71,U7,L72".split(','),
                                   "U62,R66,U55,R34,D71,R55,D58,R83".split(',')) != 159:
        print("did not return 159, the correct answer.\n")
        return False
    
    if intersection_least_distance("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(','),
                                   "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(',')) != 135:
        print("did not return 135, the correct answer.\n")
        return False
    
    return True


def main():
    if tests_day3puzzle1():
        print("Day 3 Puzzle 1 answer: ", solve_day3puzzle1())


if __name__ == "__main__":
    main()
