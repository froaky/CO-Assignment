import data

def mem_addr(n):
    return ((8 - len(bin(n)[2:])) * "0") + bin(n)[2:]

def isValidName(name, variables, labels):
    if name in data.registers.keys() or name == "FLAGS":
        return name + " is predefined for a register"
    if name in variables.keys():
        return name + " has already been defined as a variable name"
    if name in labels.keys():
        return name + " has already been defined as a label name"
    if name in data.instructions.keys():
        return "Operation name cannot be used as a label/variable"
    
    else:
        for i in name:
            a = ord(i)
            if not ((a >= 65 and a <= 90)   
                or  (a >= 97 and a <= 122)  
                or  (a >= 48 and a <= 57)   
                or  (a == 95)):             
                
                return False
        return True    
    
def isLabel(label, variables, labels):
    if label[-1] == ':':
        is_valid_name = isValidName(label[0:-1], variables, labels)
        if is_valid_name == True and label[-1] == ':':
            return True
        elif is_valid_name == False and label[-1] == ':':
            return False
        else:
            return is_valid_name
    return False
    
def check(i_flag, line, variables, labels):
    
    if line[0] == "var":
        if len(line) == 2:
            if i_flag == 0:
                is_valid_name = isValidName(line[1], variables, labels)
                if is_valid_name == True:
                    return "variable"
                elif is_valid_name == False: 
                    return "Variable names can only contain letters, numbers and underscores"
                else:
                    return is_valid_name      
            else:
                return "Variables must be declared at the beginning"
        elif len(line) < 2:
            return "Syntax Error: No variable name provided"
        elif len(line) > 2:
            return "Syntax Error: Variable names cannot contain spaces"
    else:
        l_flag = 0

        if isLabel(line[0], variables, labels) and len(line) == 1:
            return "Label must be followed by instruction"
        elif isLabel(line[0], variables, labels) and len(line) >= 1:
            l_flag = 1

        
        if line[l_flag] in data.instructions.keys() or line[l_flag] == "mov":
            return ("label: " * l_flag) + "instruction"
        else:
            return line[l_flag] + " is an invalid operation name"