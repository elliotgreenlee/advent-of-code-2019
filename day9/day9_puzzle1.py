from queue import Queue
from enum import IntEnum
from abc import ABC, abstractmethod
import sys
import itertools


class Intcode:
    def __init__(self, program, input_queue, instruction_code_index=0):
        self.program = program
        self.input_queue = input_queue
        self.output_queue = []
        self.instruction_code_index = instruction_code_index
        self.relative_base = 0
    
    def run(self):
        while True:
            instruction_code = self.program[self.instruction_code_index]
            instruction = Instruction(instruction_code, self.program, self.instruction_code_index, self.relative_base)
            
            if instruction.opcode == Opcode.ADD:
                parameters = instruction.determine_read_parameters(2)
                write_location = instruction.determine_write_location(write_parameter_index=2)
                
                self.program[write_location] = parameters[0] + parameters[1]
                
                self.instruction_code_index += 4
            elif instruction.opcode == Opcode.MULTIPLY:
                parameters = instruction.determine_read_parameters(2)
                write_location = instruction.determine_write_location(write_parameter_index=2)
                
                self.program[write_location] = parameters[0] * parameters[1]
                
                self.instruction_code_index += 4
            elif instruction.opcode == Opcode.INPUT:
                if not self.input_queue.empty():
                    write_location = instruction.determine_write_location(write_parameter_index=0)
                    self.program[write_location] = self.input_queue.get()
                    self.instruction_code_index += 2
                else:
                    return self.program, self.instruction_code_index, True, self.output_queue
            
            elif instruction.opcode == Opcode.OUTPUT:
                parameters = instruction.determine_read_parameters(num_parameters=1)
                self.output_queue.append(parameters[0])
                
                self.instruction_code_index += 2
            elif instruction.opcode == Opcode.JUMP_IF_TRUE:
                parameters = instruction.determine_read_parameters(2)
                
                if parameters[0]:
                    self.instruction_code_index = parameters[1]
                else:
                    self.instruction_code_index += 3
            elif instruction.opcode == Opcode.JUMP_IF_FALSE:
                parameters = instruction.determine_read_parameters(2)
                
                if not parameters[0]:
                    self.instruction_code_index = parameters[1]
                else:
                    self.instruction_code_index += 3
            elif instruction.opcode == Opcode.LESS_THAN:
                parameters = instruction.determine_read_parameters(num_parameters=2)
                write_location = instruction.determine_write_location(write_parameter_index=2)
                
                if parameters[0] < parameters[1]:
                    self.program[write_location] = 1
                else:
                    self.program[write_location] = 0
                
                self.instruction_code_index += 4
            elif instruction.opcode == Opcode.EQUALS:
                parameters = instruction.determine_read_parameters(num_parameters=2)
                write_location = instruction.determine_write_location(write_parameter_index=2)
                
                if parameters[0] == parameters[1]:
                    self.program[write_location] = 1
                else:
                    self.program[write_location] = 0
                
                self.instruction_code_index += 4
            elif instruction.opcode == Opcode.ADJUST_RELATIVE_BASE:
                parameters = instruction.determine_read_parameters(1)
                    
                self.relative_base += parameters[0]
                
                self.instruction_code_index += 2
            elif instruction.opcode == Opcode.STOP:
                return self.program, self.instruction_code_index, False, self.output_queue
            else:
                print("ohhhh nooooo")
                exit(1)


class Instruction(ABC):
    def __init__(self, instruction_code, program, instruction_code_index, relative_base):
        self.instruction_code = instruction_code
        self.program = program
        self.instruction_code_index = instruction_code_index
        self.relative_base = relative_base
        self.opcode = self.determine_opcode()
        self.parameter_modes = self.determine_parameter_modes()
        self.parameters = []
        
    def determine_opcode(self):
        return self.instruction_code % 100
    
    def determine_parameter_modes(self):
        leading_added = "{:03}".format(self.instruction_code // 100)
        listed = list(map(int, leading_added))
        return [listed[2], listed[1], listed[0]]
    
    def determine_read_parameters(self, num_parameters):
        self.parameters = []
        for parameter_index in range(0, num_parameters):
            if self.parameter_modes[parameter_index] == ParameterMode.POSITION:
                parameter = self.program[self.program[self.instruction_code_index + parameter_index + 1]]
            elif self.parameter_modes[parameter_index] == ParameterMode.IMMEDIATE:
                parameter = self.program[self.instruction_code_index + parameter_index + 1]
            elif self.parameter_modes[parameter_index] == ParameterMode.RELATIVE:
                parameter = self.program[self.program[self.instruction_code_index + parameter_index + 1] + self.relative_base]
            else:
                parameter = None
                print("bad first parameter mode")
                exit(1)
                
            self.parameters.append(parameter)
        return self.parameters
    
    def determine_write_location(self, write_parameter_index):
        if self.parameter_modes[write_parameter_index] == ParameterMode.POSITION:
            write_location = self.program[self.instruction_code_index + write_parameter_index + 1]
        elif self.parameter_modes[write_parameter_index] == ParameterMode.RELATIVE:
            write_location = self.program[self.instruction_code_index + write_parameter_index + 1] + self.relative_base
        else:
            write_location = None
            print("bad first parameter mode")
            print(self.instruction_code_index, self.program)
            exit(1)
            
        return write_location


class ParameterMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class Opcode(IntEnum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    ADJUST_RELATIVE_BASE = 9
    STOP = 99


def solve_day9puzzle1():
    with open("day9_data.txt", 'r') as f:
        program = list(map(int, f.readline().strip().split(',')))
        program += [0] * 10000
        input_queue = Queue()
        input_queue.put(1)
        intcode = Intcode(program, input_queue)
        program, instruction_code_index, not_finished, output_list = intcode.run()
        return output_list[0]
        

def tests_day9puzzle1():
    intcode = Intcode([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99] + [0] * 1000, Queue())
    program, instruction_code_index, not_finished, output_list = intcode.run()
    if output_list != [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]:
        return False
    return True


def main():
    if tests_day9puzzle1():
        print("Day 9 Puzzle 1 answer: ", solve_day9puzzle1())


if __name__ == "__main__":
    main()
