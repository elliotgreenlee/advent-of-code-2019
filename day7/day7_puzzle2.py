# https://docs.python.org/3/library/threading.html#threading.Condition.wait_for
# https://docs.python.org/3/library/queue.html

from queue import Queue
from enum import IntEnum
from abc import ABC, abstractmethod
import sys
import itertools


class Intcode:
    def __init__(self, program, input_queue, instruction_code_index):
        self.program = program
        self.input_queue = input_queue
        self.output_queue = []
        self.instruction_code_index = instruction_code_index
    
    def run(self):
        while True:
            instruction_code = self.program[self.instruction_code_index]
            instruction = Instruction(instruction_code)
            
            if instruction.opcode == Opcode.ADD:
                if instruction.parameter_modes.first == ParameterMode.POSITION:
                    value1 = self.program[self.program[self.instruction_code_index + 1]]
                elif instruction.parameter_modes.first == ParameterMode.IMMEDIATE:
                    value1 = self.program[self.instruction_code_index + 1]
                else:
                    value1 = None
                    print("ADD: bad first parameter mode.")
                    exit(1)
                
                if instruction.parameter_modes.second == ParameterMode.POSITION:
                    value2 = self.program[self.program[self.instruction_code_index + 2]]
                elif instruction.parameter_modes.second == ParameterMode.IMMEDIATE:
                    value2 = self.program[self.instruction_code_index + 2]
                else:
                    value2 = None
                    print("ADD: bad second parameter mode.")
                    exit(1)
                
                self.program[self.program[self.instruction_code_index + 3]] = value1 + value2
                
                self.instruction_code_index += 4
            elif instruction.opcode == Opcode.MULTIPLY:
                if instruction.parameter_modes.first == ParameterMode.POSITION:
                    value1 = self.program[self.program[self.instruction_code_index + 1]]
                elif instruction.parameter_modes.first == ParameterMode.IMMEDIATE:
                    value1 = self.program[self.instruction_code_index + 1]
                else:
                    value1 = None
                    print("Multiply: bad first parameter mode.")
                    exit(1)
                
                if instruction.parameter_modes.second == ParameterMode.POSITION:
                    value2 = self.program[self.program[self.instruction_code_index + 2]]
                elif instruction.parameter_modes.second == ParameterMode.IMMEDIATE:
                    value2 = self.program[self.instruction_code_index + 2]
                else:
                    value2 = None
                    print("Multiply: bad second parameter mode.")
                    exit(1)
                
                self.program[self.program[self.instruction_code_index + 3]] = value1 * value2
                
                self.instruction_code_index += 4
            elif instruction.opcode == Opcode.INPUT:
                if not self.input_queue.empty():
                    address = self.program[self.instruction_code_index + 1]
                    self.program[address] = self.input_queue.get()
                    self.instruction_code_index += 2
                else:
                    return self.program, self.instruction_code_index, True, self.output_queue
            
            elif instruction.opcode == Opcode.OUTPUT:
                address = self.program[self.instruction_code_index + 1]
                self.output_queue.append(self.program[address])
                
                self.instruction_code_index += 2
            elif instruction.opcode == Opcode.JUMP_IF_TRUE:
                if instruction.parameter_modes.first == ParameterMode.POSITION:
                    value1 = self.program[self.program[self.instruction_code_index + 1]]
                elif instruction.parameter_modes.first == ParameterMode.IMMEDIATE:
                    value1 = self.program[self.instruction_code_index + 1]
                else:
                    value1 = None
                    print("Jump If True: bad first parameter mode.")
                    exit(1)
                
                if instruction.parameter_modes.second == ParameterMode.POSITION:
                    value2 = self.program[self.program[self.instruction_code_index + 2]]
                elif instruction.parameter_modes.second == ParameterMode.IMMEDIATE:
                    value2 = self.program[self.instruction_code_index + 2]
                else:
                    value2 = None
                    print("Jump If True: bad second parameter mode.")
                    exit(1)
                
                if value1:
                    self.instruction_code_index = value2
                else:
                    self.instruction_code_index += 3
            elif instruction.opcode == Opcode.JUMP_IF_FALSE:
                if instruction.parameter_modes.first == ParameterMode.POSITION:
                    value1 = self.program[self.program[self.instruction_code_index + 1]]
                elif instruction.parameter_modes.first == ParameterMode.IMMEDIATE:
                    value1 = self.program[self.instruction_code_index + 1]
                else:
                    value1 = None
                    print("Jump If False: bad first parameter mode.")
                    exit(1)
                
                if instruction.parameter_modes.second == ParameterMode.POSITION:
                    value2 = self.program[self.program[self.instruction_code_index + 2]]
                elif instruction.parameter_modes.second == ParameterMode.IMMEDIATE:
                    value2 = self.program[self.instruction_code_index + 2]
                else:
                    value2 = None
                    print("Jump If False: bad second parameter mode.")
                    exit(1)
                
                if not value1:
                    self.instruction_code_index = value2
                else:
                    self.instruction_code_index += 3
            elif instruction.opcode == Opcode.LESS_THAN:
                if instruction.parameter_modes.first == ParameterMode.POSITION:
                    value1 = self.program[self.program[self.instruction_code_index + 1]]
                elif instruction.parameter_modes.first == ParameterMode.IMMEDIATE:
                    value1 = self.program[self.instruction_code_index + 1]
                else:
                    value1 = None
                    print("Less Than: bad first parameter mode.")
                    exit(1)
                
                if instruction.parameter_modes.second == ParameterMode.POSITION:
                    value2 = self.program[self.program[self.instruction_code_index + 2]]
                elif instruction.parameter_modes.second == ParameterMode.IMMEDIATE:
                    value2 = self.program[self.instruction_code_index + 2]
                else:
                    value2 = None
                    print("Less Than: bad second parameter mode.")
                    exit(1)
                
                if value1 < value2:
                    self.program[self.program[self.instruction_code_index + 3]] = 1
                else:
                    self.program[self.program[self.instruction_code_index + 3]] = 0
                
                self.instruction_code_index += 4
            elif instruction.opcode == Opcode.EQUALS:
                if instruction.parameter_modes.first == ParameterMode.POSITION:
                    value1 = self.program[self.program[self.instruction_code_index + 1]]
                elif instruction.parameter_modes.first == ParameterMode.IMMEDIATE:
                    value1 = self.program[self.instruction_code_index + 1]
                else:
                    value1 = None
                    print("Equals: bad first parameter mode.")
                    exit(1)
                
                if instruction.parameter_modes.second == ParameterMode.POSITION:
                    value2 = self.program[self.program[self.instruction_code_index + 2]]
                elif instruction.parameter_modes.second == ParameterMode.IMMEDIATE:
                    value2 = self.program[self.instruction_code_index + 2]
                else:
                    value2 = None
                    print("Equals: bad second parameter mode.")
                    exit(1)
                
                if value1 == value2:
                    self.program[self.program[self.instruction_code_index + 3]] = 1
                else:
                    self.program[self.program[self.instruction_code_index + 3]] = 0
                
                self.instruction_code_index += 4
            elif instruction.opcode == Opcode.STOP:
                return self.program, self.instruction_code_index, False, self.output_queue
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
    amp_a_diagnostic = diagnostic_program[:]
    amp_b_diagnostic = diagnostic_program[:]
    amp_c_diagnostic = diagnostic_program[:]
    amp_d_diagnostic = diagnostic_program[:]
    amp_e_diagnostic = diagnostic_program[:]
    amp_a_running = True
    amp_b_running = True
    amp_c_running = True
    amp_d_running = True
    amp_e_running = True
    amp_a_input_queue = Queue()
    amp_a_input_queue.put(phases[0])
    amp_a_input_queue.put(0)
    amp_b_input_queue = Queue()
    amp_b_input_queue.put(phases[1])
    amp_c_input_queue = Queue()
    amp_c_input_queue.put(phases[2])
    amp_d_input_queue = Queue()
    amp_d_input_queue.put(phases[3])
    amp_e_input_queue = Queue()
    amp_e_input_queue.put(phases[4])
    amp_a_instruction_code_index = 0
    amp_b_instruction_code_index = 0
    amp_c_instruction_code_index = 0
    amp_d_instruction_code_index = 0
    amp_e_instruction_code_index = 0
    while amp_a_running and amp_b_running and amp_c_running and amp_d_running and amp_e_running:
        amp_a_intcode = Intcode(amp_a_diagnostic, amp_a_input_queue, amp_a_instruction_code_index)
        amp_a_diagnostic, amp_a_instruction_code_index, amp_a_running, amp_a_output_queue = amp_a_intcode.run()
        for output in amp_a_output_queue:
            amp_b_input_queue.put(output)
        
        amp_b_intcode = Intcode(amp_b_diagnostic, amp_b_input_queue, amp_b_instruction_code_index)
        amp_b_diagnostic, amp_b_instruction_code_index, amp_b_running, amp_b_output_queue = amp_b_intcode.run()
        for output in amp_b_output_queue:
            amp_c_input_queue.put(output)
        
        amp_c_intcode = Intcode(amp_c_diagnostic, amp_c_input_queue, amp_c_instruction_code_index)
        amp_c_diagnostic, amp_c_instruction_code_index, amp_c_running, amp_c_output_queue = amp_c_intcode.run()
        for output in amp_c_output_queue:
            amp_d_input_queue.put(output)
        
        amp_d_intcode = Intcode(amp_d_diagnostic, amp_d_input_queue, amp_d_instruction_code_index)
        amp_d_diagnostic, amp_d_instruction_code_index, amp_d_running, amp_d_output_queue = amp_d_intcode.run()
        for output in amp_d_output_queue:
            amp_e_input_queue.put(output)
        
        amp_e_intcode = Intcode(amp_e_diagnostic, amp_e_input_queue, amp_e_instruction_code_index)
        amp_e_diagnostic, amp_e_instruction_code_index, amp_e_running, amp_e_output_queue = amp_e_intcode.run()
        for output in amp_e_output_queue:
            amp_a_input_queue.put(output)
    
    return amp_a_input_queue.get()


def find_max_thruster_signal_and_phases(diagnostic_program, phase_options):
    phases_permutations = list(itertools.permutations(phase_options))
    
    max_thruster_signal = -sys.maxsize - 1
    max_phases = (-1, -1, -1, -1, -1)
    for phases in phases_permutations:
        thruster_signal = run_diagnostic_for_phases(diagnostic_program, phases)
        if thruster_signal > max_thruster_signal:
            max_thruster_signal = thruster_signal
            max_phases = phases
    return max_thruster_signal, max_phases


def solve_day7puzzle2():
    with open("day7_data.txt", 'r') as f:
        diagnostic_program = list(map(int, f.readline().split(',')))
        max_thruster_signal, max_phases = find_max_thruster_signal_and_phases(diagnostic_program, [5, 6, 7, 8, 9])
        return max_thruster_signal


def tests_day7puzzle2():
    if find_max_thruster_signal_and_phases([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0], [0, 1, 2, 3, 4]) != \
            (43210, (4, 3, 2, 1, 0)):
        return False
    
    if find_max_thruster_signal_and_phases(
            [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0], [0, 1, 2, 3, 4]) != \
            (54321, (0, 1, 2, 3, 4)):
        return False
    
    if find_max_thruster_signal_and_phases(
            [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32,
             31, 31, 4, 31, 99, 0, 0, 0], [0, 1, 2, 3, 4]) != \
            (65210, (1, 0, 4, 3, 2)):
        return False
    
    if find_max_thruster_signal_and_phases(
            [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99,
             0, 0, 5], [5, 6, 7, 8, 9]) != \
            (139629729, (9, 8, 7, 6, 5)):
        return False
    
    if find_max_thruster_signal_and_phases(
            [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5, 54, 1105, 1,
             12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56, 1005, 56, 6,
             99, 0, 0, 0, 0, 10], [5, 6, 7, 8, 9]) != \
            (18216, (9, 7, 8, 5, 6)):
        return False
    
    return True


def main():
    if tests_day7puzzle2():
        print("Day 7 Puzzle 2 answer: ", solve_day7puzzle2())


if __name__ == "__main__":
    main()
