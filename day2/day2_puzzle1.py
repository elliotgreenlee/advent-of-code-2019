from enum import Enum
OPCODE_STEP_LENGTH = 4


class Opcode(Enum):
    ADD = 1
    MULTIPLY = 2
    STOP = 99


def solve_day2puzzle1():
    with open("day2_data.txt", 'r') as f:
        for line in f:
            intcode = line.split(',')
            intcode = list(map(int, intcode))
        
        intcode = alarm_state(intcode)
        finished_intcode = intcode_run(intcode)
        
        return finished_intcode[0]


def alarm_state(intcode):
    intcode[1] = 12
    intcode[2] = 2
    return intcode


def intcode_run(intcode):
    for i in range(0, (int(len(intcode) / OPCODE_STEP_LENGTH)) + 1):
        opcode_index = i * 4
        opcode = intcode[opcode_index]
        
        value1_index = i * 4 + 1
        value2_index = i * 4 + 2
        result_index = i * 4 + 3
        
        if opcode == 1:
            value1 = intcode[intcode[value1_index]]
            value2 = intcode[intcode[value2_index]]
            result = value1 + value2
            intcode[intcode[result_index]] = result
        elif opcode == 2:
            value1 = intcode[intcode[value1_index]]
            value2 = intcode[intcode[value2_index]]
            result = value1 * value2
            intcode[intcode[result_index]] = result
        elif opcode == 99:
            return intcode
        else:
            print("ohhhh nooooo")
            exit(1)


def tests_day2puzzle1():
    if intcode_run([1, 0, 0, 0, 99]) != [2, 0, 0, 0, 99]:
        return False
    
    if intcode_run([2, 3, 0, 3, 99]) != [2, 3, 0, 6, 99]:
        return False
    
    if intcode_run([2, 4, 4, 5, 99, 0]) != [2, 4, 4, 5, 99, 9801]:
        return False
    
    if intcode_run([1, 1, 1, 4, 99, 5, 6, 0, 99]) != [30, 1, 1, 4, 2, 5, 6, 0, 99]:
        return False
    
    return True


def main():
    if tests_day2puzzle1():
        print("Day 2 Puzzle 1 answer: ", solve_day2puzzle1())


if __name__ == "__main__":
    main()
