from enum import IntEnum
from abc import ABC, abstractmethod
import sys
import itertools


class Intcode:
    def __init__(self, program, input_id_stack):
        self.program = program
        self.input_id_stack = input_id_stack

    def run(self):
        running = True
        instruction_code_index = 0
        while running:
            instruction_code = self.program[instruction_code_index]
            instruction = Instruction(instruction_code)
        
            if instruction.opcode == Opcode.ADD:
                if instruction.parameter_modes.first == ParameterMode.POSITION:
                    value1 = self.program[self.program[instruction_code_index + 1]]
                elif instruction.parameter_modes.first == ParameterMode.IMMEDIATE:
                    value1 = self.program[instruction_code_index + 1]
                else:
                    value1 = None
                    print("ADD: bad first parameter mode.")
                    exit(1)

                if instruction.parameter_modes.second == ParameterMode.POSITION:
                    value2 = self.program[self.program[instruction_code_index + 2]]
                elif instruction.parameter_modes.second == ParameterMode.IMMEDIATE:
                    value2 = self.program[instruction_code_index + 2]
                else:
                    value2 = None
                    print("ADD: bad second parameter mode.")
                    exit(1)
                    
                self.program[self.program[instruction_code_index + 3]] = value1 + value2
                
                instruction_code_index += 4
            elif instruction.opcode == Opcode.MULTIPLY:
                if instruction.parameter_modes.first == ParameterMode.POSITION:
                    value1 = self.program[self.program[instruction_code_index + 1]]
                elif instruction.parameter_modes.first == ParameterMode.IMMEDIATE:
                    value1 = self.program[instruction_code_index + 1]
                else:
                    value1 = None
                    print("Multiply: bad first parameter mode.")
                    exit(1)
    
                if instruction.parameter_modes.second == ParameterMode.POSITION:
                    value2 = self.program[self.program[instruction_code_index + 2]]
                elif instruction.parameter_modes.second == ParameterMode.IMMEDIATE:
                    value2 = self.program[instruction_code_index + 2]
                else:
                    value2 = None
                    print("Multiply: bad second parameter mode.")
                    exit(1)
    
                self.program[self.program[instruction_code_index + 3]] = value1 * value2
                
                instruction_code_index += 4
            elif instruction.opcode == Opcode.INPUT:
                address = self.program[instruction_code_index + 1]
                self.program[address] = self.input_id_stack.pop()
                
                instruction_code_index += 2
            elif instruction.opcode == Opcode.OUTPUT:
                address = self.program[instruction_code_index + 1]
                output = self.program[address]
                
                instruction_code_index += 2
            elif instruction.opcode == Opcode.JUMP_IF_TRUE:
                if instruction.parameter_modes.first == ParameterMode.POSITION:
                    value1 = self.program[self.program[instruction_code_index + 1]]
                elif instruction.parameter_modes.first == ParameterMode.IMMEDIATE:
                    value1 = self.program[instruction_code_index + 1]
                else:
                    value1 = None
                    print("Jump If True: bad first parameter mode.")
                    exit(1)
                
                if instruction.parameter_modes.second == ParameterMode.POSITION:
                    value2 = self.program[self.program[instruction_code_index + 2]]
                elif instruction.parameter_modes.second == ParameterMode.IMMEDIATE:
                    value2 = self.program[instruction_code_index + 2]
                else:
                    value2 = None
                    print("Jump If True: bad second parameter mode.")
                    exit(1)
                    
                if value1:
                    instruction_code_index = value2
                else:
                    instruction_code_index += 3
            elif instruction.opcode == Opcode.JUMP_IF_FALSE:
                if instruction.parameter_modes.first == ParameterMode.POSITION:
                    value1 = self.program[self.program[instruction_code_index + 1]]
                elif instruction.parameter_modes.first == ParameterMode.IMMEDIATE:
                    value1 = self.program[instruction_code_index + 1]
                else:
                    value1 = None
                    print("Jump If False: bad first parameter mode.")
                    exit(1)
    
                if instruction.parameter_modes.second == ParameterMode.POSITION:
                    value2 = self.program[self.program[instruction_code_index + 2]]
                elif instruction.parameter_modes.second == ParameterMode.IMMEDIATE:
                    value2 = self.program[instruction_code_index + 2]
                else:
                    value2 = None
                    print("Jump If False: bad second parameter mode.")
                    exit(1)
    
                if not value1:
                    instruction_code_index = value2
                else:
                    instruction_code_index += 3
            elif instruction.opcode == Opcode.LESS_THAN:
                if instruction.parameter_modes.first == ParameterMode.POSITION:
                    value1 = self.program[self.program[instruction_code_index + 1]]
                elif instruction.parameter_modes.first == ParameterMode.IMMEDIATE:
                    value1 = self.program[instruction_code_index + 1]
                else:
                    value1 = None
                    print("Less Than: bad first parameter mode.")
                    exit(1)
    
                if instruction.parameter_modes.second == ParameterMode.POSITION:
                    value2 = self.program[self.program[instruction_code_index + 2]]
                elif instruction.parameter_modes.second == ParameterMode.IMMEDIATE:
                    value2 = self.program[instruction_code_index + 2]
                else:
                    value2 = None
                    print("Less Than: bad second parameter mode.")
                    exit(1)
                
                if value1 < value2:
                    self.program[self.program[instruction_code_index + 3]] = 1
                else:
                    self.program[self.program[instruction_code_index + 3]] = 0
    
                instruction_code_index += 4
            elif instruction.opcode == Opcode.EQUALS:
                if instruction.parameter_modes.first == ParameterMode.POSITION:
                    value1 = self.program[self.program[instruction_code_index + 1]]
                elif instruction.parameter_modes.first == ParameterMode.IMMEDIATE:
                    value1 = self.program[instruction_code_index + 1]
                else:
                    value1 = None
                    print("Equals: bad first parameter mode.")
                    exit(1)
    
                if instruction.parameter_modes.second == ParameterMode.POSITION:
                    value2 = self.program[self.program[instruction_code_index + 2]]
                elif instruction.parameter_modes.second == ParameterMode.IMMEDIATE:
                    value2 = self.program[instruction_code_index + 2]
                else:
                    value2 = None
                    print("Equals: bad second parameter mode.")
                    exit(1)

                if value1 == value2:
                    self.program[self.program[instruction_code_index + 3]] = 1
                else:
                    self.program[self.program[instruction_code_index + 3]] = 0

                instruction_code_index += 4
            elif instruction.opcode == Opcode.STOP:
                return output
            else:
                print("ohhhh nooooo")
                exit(1)


class Instruction(ABC):
    def __init__(self, instruction_code):
        self.instruction_code = instruction_code
        self.opcode = self.determine_opcode()
        self.parameter_modes = self.determine_parameter_modes()
        
    def determine_opcode(self):
        return self.instruction_code % 100
    
    def determine_parameter_modes(self):
        leading_added = "{:03}".format(self.instruction_code // 100)
        listed = [0 if code == '0' else 1 for code in leading_added]
        return ParameterModes(listed[0], listed[1], listed[2])
    

class ParameterModes:
    def __init__(self, third, second, first):
        self.third = third
        self.second = second
        self.first = first


class ParameterMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1


class Opcode(IntEnum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    STOP = 99


def run_diagnostic_for_phases(diagnostic_program, phases):
    flowthrough_value = 0
    for phase in phases:
        intcode = Intcode(diagnostic_program, [flowthrough_value, phase])
        flowthrough_value = intcode.run()
        
    return flowthrough_value


def find_max_thruster_signal_and_phases(diagnostic_program):
    phases_permutations = list(itertools.permutations([0, 1, 2, 3, 4]))
    
    max_thruster_signal = -sys.maxsize - 1
    max_phases = (-1, -1, -1, -1, -1)
    for phases in phases_permutations:
        thruster_signal = run_diagnostic_for_phases(diagnostic_program, phases)
        if thruster_signal > max_thruster_signal:
            max_thruster_signal = thruster_signal
            max_phases = phases
    print(max_thruster_signal, max_phases)
    return max_thruster_signal, max_phases


def solve_day7puzzle1():
    with open("day7_data.txt", 'r') as f:
        diagnostic_program = list(map(int, f.readline().split(',')))
        max_thruster_signal, max_phases = find_max_thruster_signal_and_phases(diagnostic_program)
        return max_thruster_signal


def tests_day7puzzle1():
    if find_max_thruster_signal_and_phases([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]) !=\
            (43210, (4,3,2,1,0)):
        return False
    
    if find_max_thruster_signal_and_phases(
            [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]) !=\
            (54321, (0,1,2,3,4)):
        return False
    
    if find_max_thruster_signal_and_phases(
            [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]) !=\
            (65210, (1,0,4,3,2)):
        return False

    return True


def main():
    if tests_day7puzzle1():
        print("Day 7 Puzzle 1 answer: ", solve_day7puzzle1())


if __name__ == "__main__":
    main()
