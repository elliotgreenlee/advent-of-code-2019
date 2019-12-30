def solve_day4puzzle2():
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
    if check_doubles_only(password) and check_increasing(password):
        return True
    else:
        return False


def check_doubles_only(password):
    password = password + 'a'
    doubles_only = False
    index = 0
    while index < len(password) - 1:
        in_group = True
        index2 = index
        group_number = password[index]
        group_size = 1
        while in_group:
            index2 += 1
            if password[index2] is group_number:
                group_size += 1
            else:
                in_group = False
        if group_size == 2:
            doubles_only = True
        index = index2
        
    return doubles_only


def check_increasing(password):
    increasing = True
    for index in range(0, len(password) - 1):
        if password[index] > password[index + 1]:
            increasing = False
    
    return increasing


def tests_day4puzzle2():
    if check_password("111111"):
        print("111111: valid and shouldn't be")
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
    
    if check_password("123444"):
        print("123444: valid and shouldn't be")
        return False
    
    if not check_password("111122"):
        print("111122: not valid and should be")
        return False
    
    if not check_password("112233"):
        print("112233: not valid and should be")
        return False
    
    return True


def main():
    if tests_day4puzzle2():
        print("Day 4 Puzzle 2 answer: ", solve_day4puzzle2())


if __name__ == "__main__":
    main()
