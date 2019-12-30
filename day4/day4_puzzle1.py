def solve_day4puzzle1():
    with open("day4_data.txt", 'r') as f:
        inputs = list(map(int, f.readline().split('-')))
        lower_limit = inputs[0]
        upper_limit = inputs[1]
        
        valids = 0
        for password in range(lower_limit, upper_limit):
            if check_password(str(password)):
                valids += 1
                
        return valids


def check_password(password):
    if check_doubles(password) and check_increasing(password):
        return True
    else:
        return False


def check_doubles(password):
    doubles = False
    for index in range(0, len(password) - 1):
        if password[index] is password[index + 1]:
            doubles = True
    return doubles


def check_increasing(password):
    increasing = True
    for index in range(0, len(password) - 1):
        if password[index] > password[index + 1]:
            increasing = False
    
    return increasing


def tests_day4puzzle1():
    if not check_password("111111"):
        print("111111: not valid and should be")
        return False
    
    if not check_password("122345"):
        print("122345: not valid and should be")
        return False
    
    if check_password("223450"):
        print("223450: valid and shouldn't be")
        return False
    
    if check_password("123789"):
        print("123789: valid and shouldn't be")
        return False
    
    return True


def main():
    if tests_day4puzzle1():
        print("Day 4 Puzzle 1 answer: ", solve_day4puzzle1())


if __name__ == "__main__":
    main()
