import sys
import numpy


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def stringme(self):
        return "({}, {})".format(self.x, self.y)
    
    
class Board:
    def __init__(self, boardx, boardy, centerpoint):
        self.board = numpy.full((boardx, boardy), 0)
        self.centerpoint = centerpoint
        
    def draw_wire(self, wirepath):
        point1 = self.centerpoint
        for instruction in wirepath:
            direction = instruction[0]
            distance = int(instruction[1:])
            if direction == 'U':
                point2 = Point(point1.x, point1.y + distance)
                self.board[point1.x, point1.y:point1.y + distance + 1] = int(1)
            elif direction == 'R':
                point2 = Point(point1.x + distance, point1.y)
                self.board[point1.x:point1.x + distance + 1, point1.y] = int(1)
            elif direction == 'D':
                point2 = Point(point1.x, point1.y - distance)
                self.board[point1.x, point1.y - distance:point1.y] = int(1)
            elif direction == 'L':
                point2 = Point(point1.x - distance, point1.y)
                self.board[point1.x - distance:point1.x, point1.y] = int(1)
            else:
                point2 = Point(0, 0)
                print("oohhh noooo")
                exit(1)
                
            point1 = point2
    
    def find_crosses(self, wirepath):
        cross_points = []
        point1 = self.centerpoint
        for instruction in wirepath:
            direction = instruction[0]
            distance = int(instruction[1:])
            if direction == 'U':
                point2 = Point(point1.x, point1.y + distance)
                for y in range(point1.y, point1.y + distance + 1):
                    if self.board[point1.x, y] == 1:
                        cross_points.append(Point(point1.x, y))
            elif direction == 'R':
                point2 = Point(point1.x + distance, point1.y)
                for x in range(point1.x, point1.x + distance + 1):
                    if self.board[x, point1.y] == 1:
                        cross_points.append(Point(x, point1.y))
            elif direction == 'D':
                point2 = Point(point1.x, point1.y - distance)
                for y in range(point1.y - distance, point1.y):
                    if self.board[point1.x, y] == 1:
                        cross_points.append(Point(point1.x, y))
            elif direction == 'L':
                point2 = Point(point1.x - distance, point1.y)
                for x in range(point1.x - distance, point1.x):
                    if self.board[x, point1.y] == 1:
                        cross_points.append(Point(x, point1.y))
            else:
                point2 = Point(0, 0)
                print("oohhh noooo")
                exit(1)
        
            point1 = point2
            
        return cross_points
    

def solve_day3puzzle1():
    with open("day3_data.txt", 'r') as f:
        wirepath1 = f.readline().strip().split(',')
        wirepath2 = f.readline().strip().split(',')

        # find board dimensions
        lowestx = sys.maxsize
        highestx = -sys.maxsize - 1
        lowesty = sys.maxsize
        highesty = -sys.maxsize - 1
        lowestx, highestx, lowesty, highesty = find_dimensions(wirepath1, lowestx, highestx, lowesty, highesty)
        lowestx, highestx, lowesty, highesty = find_dimensions(wirepath2, lowestx, highestx, lowesty, highesty)
        centerpoint = Point(-lowestx, -lowesty)
        boardx = abs(lowestx) + abs(highestx) + 1
        boardy = abs(lowesty) + abs(highesty) + 1
        print("boardx is now: ", boardx)
        print("boardy is now: ", boardy)
        print("centerpoint is now: ", centerpoint.x, centerpoint.y)
        
        board = Board(boardx, boardy, centerpoint)
        board.draw_wire(wirepath1)
        cross_points = board.find_crosses(wirepath2)
        
        smallest_manhattan = sys.maxsize
        for point in cross_points[1:]:
            print(point.stringme())
            if abs(point.x - centerpoint.x) + abs(point.y - centerpoint.y) < smallest_manhattan:
                smallest_manhattan = abs(point.x - centerpoint.x) + abs(point.y - centerpoint.y)
        
        return smallest_manhattan
        

def find_dimensions(wirepath, lowestx, highestx, lowesty, highesty):
  
    point1 = Point(0, 0)
    for instruction in wirepath:
        direction = instruction[0]
        distance = int(instruction[1:])
        if direction == 'U':
            point2 = Point(point1.x, point1.y + distance)
        elif direction == 'R':
            point2 = Point(point1.x + distance, point1.y)
        elif direction == 'D':
            point2 = Point(point1.x, point1.y - distance)
        elif direction == 'L':
            point2 = Point(point1.x - distance, point1.y)
        else:
            point2 = Point(0, 0)
            print("oohhh noooo")
            exit(1)
            
        if point2.x < lowestx:
            lowestx = point2.x
            
        if point2.x > highestx:
            highestx = point2.x
            
        if point2.y < lowesty:
            lowesty = point2.y
            
        if point2.y > highesty:
            highesty = point2.y

        point1 = point2
        
    return lowestx, highestx, lowesty, highesty


def tests_day3puzzle1():
    return True


def main():
    if tests_day3puzzle1():
        print("Day 3 Puzzle 1 answer: ", solve_day3puzzle1())


if __name__ == "__main__":
    main()
