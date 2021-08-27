import data

def mem_addr(n):
    return ((8 - len(bin(n)[2:])) * "0") + bin(n)[2:]

def isInt(n):
    try:
        int(n[1:])
        return True
    except:
        return False        

class Command:
    halt_flag = 0

    def __init__(self, line, instruction = '', arg1 = '', arg2 = '', arg3 = ''):
        self.line = line
        self.instruction = instruction
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.t_flag = 0
        self.e_flag = 0
        self.args = ''
        self.args_code = ''
        self.unused_bits = ''
        self.type = ''


    def setType(self, variables, labels):
        if (self.instruction == "ld" or self.instruction == "st") and self.arg1 in data.registers.keys() and self.arg3 == '':
            if self.arg2 not in variables.keys():
                self.e_flag = 1
                if self.arg2 in labels.keys():
                    self.error = "Line " + str(self.line) + " -> Error: Use of label as variable"
                else:
                    self.error = "Line " + str(self.line) + " -> Error: Use of undefined variable"
                return
            
        
        elif (self.instruction == "je" or self.instruction == "jgt" or self.instruction == "jlt") and self.arg2 == '' and self.arg3 == '':
            if self.arg1 not in labels.keys():
                self.e_flag = 1
                if self.arg1 in variables.keys():
                    self.error = "Line " + str(self.line) + " -> Error: Use of variable as label"
                else:
                    self.error = "Line " + str(self.line) + " -> Error: Use of undefined label"
                return

        for argument in [self.arg1, self.arg2, self.arg3]:
            if argument in data.registers.keys():
                self.args += 'R'
                self.args_code += data.registers[argument]

            elif argument == "FLAGS":
                self.args += 'F'
                self.args_code += "111"
            
            elif argument in variables.keys():
                self.args += 'V'
                self.args_code += variables[argument]
            
            elif argument in labels.keys():
                self.args += 'L'
                self.args_code += labels[argument]
            
            elif argument == '':
                continue
            
            elif len(argument) >= 2 and argument[0] == '$' and isInt(argument):
                self.args += 'I'
                self.args_code += mem_addr(int(argument[1:]))
                
            else:
                self.e_flag == 1
                self.args += 'E'
                
        if self.e_flag != 0:
            self.error = "Line " + str(self.line) + " -> General Syntax Error: " + self.instruction + " does not support given arguments"
            return

        if self.instruction == "mov" and self.args == 'RF':
            self.type = 'C'
            self.unused_bits = "00000"
        
        elif 'F' in self.args and self.instruction != "mov":
            self.e_flag += 1
            self.error = "Line " + str(self.line) + " -> Error: Illegal use of flags register"
        
        elif self.args == 'RRR':
            self.type = 'A'
            self.unused_bits = "00"
        
        elif self.args == 'RI':
            self.type = 'B'
            if int(self.arg2[1:]) < 0:
                self.e_flag += 1
                self.error = "Line " + str(self.line) + " -> Error: Illegal immediate value (less than 0)"
            if int(self.arg2[1:]) > 255:
                self.e_flag += 1
                self.error = "Line " + str(self.line) + " -> Error: Illegal immediate value (more than 255)"
        
        elif self.args == 'RR':
            self.type = 'C'
            self.unused_bits = "00000"
        
        elif self.args == 'RV':
            self.type = 'D'
        
        elif self.args == 'L':
            self.type = 'E'
            self.unused_bits ="000"
        
        elif self.args == '':
            self.type = 'F'
            self.unused_bits = "00000000000"
        
        if self.type in ['A','B','C','D','E','F']:
            self.t_flag += 1