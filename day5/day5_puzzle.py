from enum import IntEnum
from abc import ABC, abstractmethod


class Intcode:
    def __init__(self, program, input_id=5):
        self.program = program
        self.input_id = input_id

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
                self.program[address] = self.input_id
                
                instruction_code_index += 2
            elif instruction.opcode == Opcode.OUTPUT:
                address = self.program[instruction_code_index + 1]
                print("Diagnostic test result: ", self.program[address], " at address ", address)
                
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
                print("Halting")
                return self.program
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
    
    #@abstractmethod
    #def execute(self):
    #    pass
  
  
"""
class Add(Instruction):
    def __init__(self, instruction_code):
        Instruction.__init__(self, instruction_code)
        
    def execute(self):
        return
"""


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
    
    
def solve_day5puzzle1():
    with open("day5_data.txt", 'r') as f:
        diagnostic_program = list(map(int, f.readline().split(',')))

        intcode = Intcode(diagnostic_program)
        finished_intcode = intcode.run()
        
        return


def tests_day5puzzle1():
    return True


def main():
    if tests_day5puzzle1():
        print("Day 5 Puzzle 1 answer: ", solve_day5puzzle1())


if __name__ == "__main__":
    main()
