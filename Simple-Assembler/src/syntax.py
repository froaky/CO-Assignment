import data

def isInt(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


def mem_addr(n):
    return ((8 - len(bin(n)[2:])) * "0") + bin(n)[2:]

def isName(name):
    for i in name:
        a = ord(i)
        if ((a >= 65 and a <= 90)   
        or  (a >= 97 and a <= 122)  
        or  (a >= 48 and a <= 57)   
        or  (a == 95)):             
            return True

    return False

def isLabel(label):
    if isName(label[0:-1]) and label[-1] == ":": 
        return True
    return False

def isRegister(instruction, index):
    for register in data.registers:
        if instruction[index] == register["name"]:
            instruction[index] = register["address"]
            return True
    return False

def isImmediate(immediate):
    try:
        return immediate[0] == '$' and int(immediate[1:]) >= 0 and int(immediate[1:]) <= 255
    except ValueError:
        return False
    
def isInstruction(instruction, labels, variables, line_count):
    l_flag = 0

    if isLabel(instruction[2]):
        l_flag += 1 
    instruction.append(l_flag)
    
    index = 2 + l_flag

    if (instruction[index] == "add" or instruction[index] == "sub" or instruction[index] == "mul" or instruction[index] == "or" or instruction[index] == "xor" or instruction[index] == "xor") and (len(instruction) == 7 + l_flag):
        if isRegister(instruction, index + 1) and isRegister(instruction, index + 2) and isRegister(instruction, index + 3):
            instruction.append('A')
            instruction[index] = data.operations[instruction[index]]
            return True
        elif instruction[index + 1] == 'FLAGS' or instruction[index + 2] == 'FLAGS' or instruction[index + 3] == 'FLAGS':
            print("Line", instruction[0], "-> Syntax Error: Illegal use of flags register")
            return False
        else:
            print("Line", instruction[0], "-> Syntax Error: Typos in register name")
            return False

    elif instruction[index] == "hlt" and (len(instruction) == 4 + l_flag):
        if instruction[0] == line_count:
            instruction.append("1001100000000000")
            instruction.append('F')
            return True
        else:
            print("Line", instruction[0], "-> Syntax Error: hlt not being used as the last instruction")
            return False

    elif (instruction[index] == "rs" or instruction[index] == "ls") and len(instruction) == 6 + l_flag:
        if isRegister(instruction, index + 1): 
            if isImmediate(instruction[index + 2]):
                instruction.append('B')
                instruction[index] = data.operations[instruction[index]]
                return True
            elif instruction[4 + l_flag][0] == '$' and isInt(instruction[index + 2][1:]):
                print("Line", instruction[0], "-> Syntax Error: Illegal immediate value")
                return False
            else:
                print("Line", instruction[0], "-> General Syntax Error")
                return False
        elif instruction[index + 1] == 'FLAGS':
            print("Line", instruction[0], "-> Syntax Error: Illegal use of flags register")
            return False
        else:
            print("Line", instruction[0], "-> Syntax Error: Typos in register name")
            return False
        
    elif instruction[index] == "mov" and len(instruction) == 6 + l_flag: 
        if isRegister(instruction, index + 1):
            if isRegister(instruction, 4 + l_flag):
                instruction.append('C')
                instruction[index] = "00011"
            elif instruction[4 + l_flag] == "FLAGS":
                instruction.append('C')
                instruction[index] = "00011"
                instruction[4 + l_flag] = "111"
            elif isImmediate(instruction[4 + l_flag]):
                instruction.append('B')
                instruction[index] = "00010"
                instruction[index + 2] = mem_addr(int(instruction[index + 2][1:]))
            elif instruction[4 + l_flag][0] == '$' and isInt(instruction[4 + l_flag][1:]):
                print("Line", instruction[0], "-> Syntax Error: Illegal immediate value")
                return False
            else:
                print("Line", instruction[0], "-> General Syntax Error")
                return False
        elif instruction[index + 1] == 'FLAGS':
            print("Line", instruction[0], "-> Syntax Error: Illegal use of flags register")
            return False
        else:
            print("Line", instruction[0], "-> Syntax Error: Typos in register name")
            return False

    elif (instruction[index] == "div" or instruction[index] == "cmp" or instruction[index] == "not") and len(instruction) == 6 + l_flag:
        if isRegister(instruction, index + 1) and isRegister(instruction, index + 2):
            instruction.append('C')
            instruction[index] = data.operations[instruction[index]]          
            return True
        elif instruction[index + 1] == 'FLAGS' or instruction[index + 2] == 'FLAGS':
            print("Line", instruction[0], "-> Syntax Error: Illegal use of flags register")
            return False
    
    elif (instruction[index] == "ld" or instruction[index] == "st") and len(instruction) == 6 + l_flag:
        if isRegister(instruction, index + 1):
            if instruction[index + 2] in variables.keys():
                instruction[index + 2] = variables[instruction[index + 2]]
                instruction.append('D')
                instruction[index] = data.operations[instruction[index]]
                return True 
            elif instruction[index + 2] in labels.keys():
                print("Line", instruction[0], "-> Syntax Error: Misuse of label as variable")
                return False
            else:
                print("Line", instruction[0], "-> Syntax Error: Use of undefined variable")
                return False
            
        elif instruction[index + 1] == 'FLAGS':
            print("Line", instruction[0], "-> Syntax Error: Illegal use of flags register")
            return False
            
    elif (instruction[index] == "jmp" or instruction[index] == "jlt" or instruction[index] == "jgt" or instruction[index] == "je") and len(instruction) == 5 + l_flag:
        if instruction[index + 1] in labels.keys():
            instruction[index + 1] = labels[instruction[index + 1]]
            instruction.append('E')
            instruction[index] = data.operations[instruction[index]]
            return True
        elif instruction[index + 1] in variables.keys():
                print("Line", instruction[0], "-> Syntax Error: Misuse of variable as label")
                return False
        else:
            print("Line", instruction[0], "-> Syntax Error: Use of undefined label")
            return False
    
    else:
        print("Line", instruction[0], "-> Syntax Error: Typo in instruction name")
        return False