import registerFile

def xBitBinary(x, n):
    return ((x - len(bin(n)[2:])) * "0") + bin(n)[2:]

def checkOverflow(n):
    if n < 0:
        registerFile.registerStates["111"] = '0' * 12 + "1000"
        return 0
    elif n > 65535:
        registerFile.registerStates["111"] = '0' * 12 + "1000"
        return int(bin(n)[2:][-16:], 2)
    return n

def updateRegisterStates(memory, program_counter):

    if memory[program_counter][0:5] in ["00000", "00001", "00110", "01010", "01011", "01100"]:
        registerFile.registerStates["111"] = '0' * 16
        operand1 = int(registerFile.registerStates[memory[program_counter][10:13]], 2)
        operand2 = int(registerFile.registerStates[memory[program_counter][13:]], 2)
        result = int()

        if memory[program_counter][0:5] == "00000":
            result = checkOverflow(operand1 + operand2)

        elif memory[program_counter][0:5] == "00001":
            result = checkOverflow(operand1 - operand2)

        elif memory[program_counter][0:5] == "00110":
            result = checkOverflow(operand1 * operand2)

        elif memory[program_counter][0:5] == "01010":
            result = operand1 ^ operand2

        elif memory[program_counter][0:5] == "01011":
            result = operand1 | operand2

        elif memory[program_counter][0:5] == "01100":
            result = operand1 & operand2
    
        registerFile.registerStates[memory[program_counter][7:10]] = xBitBinary(16, result)

    elif memory[program_counter][0:5] == "00010":
        registerFile.registerStates["111"] = '0' * 16
        registerFile.registerStates[memory[program_counter][5:8]] = "0" * 8 + memory[program_counter][8:]
    
    elif memory[program_counter][0:5] == "00011":
        if memory[program_counter][13:] == "111": 
            registerFile.registerStates[memory[program_counter][10:13]] = registerFile.registerStates[memory[program_counter][13:]]
            registerFile.registerStates["111"] = '0' * 16
        else:
            registerFile.registerStates["111"] = '0' * 16
            registerFile.registerStates[memory[program_counter][10:13]] = registerFile.registerStates[memory[program_counter][13:]]

    elif memory[program_counter][0:5] == "00100":
        registerFile.registerStates["111"] = '0' * 16
        registerFile.registerStates[memory[program_counter][5:8]] = memory[int(memory[program_counter][8:], 2)]
    
    elif memory[program_counter][0:5] == "00101":
        registerFile.registerStates["111"] = '0' * 16
        memory[int(memory[program_counter][8:], 2)] = registerFile.registerStates[memory[program_counter][5:8]]
    
    elif memory[program_counter][0:5] in ["00111", "01110"]:
        registerFile.registerStates["111"] = '0' * 16
        operand1 = int(registerFile.registerStates[memory[program_counter][10:13]], 2)
        operand2 = int(registerFile.registerStates[memory[program_counter][13:]], 2)

        if memory[program_counter][0:5] == "00111":
            quotient = operand1 // operand2
            remainder = operand1 % operand2
            registerFile.registerStates["000"] = xBitBinary(16, quotient)
            registerFile.registerStates["001"] = xBitBinary(16, remainder)
        
        elif memory[program_counter][0:5] == "01110":
            if operand1 == operand2:
                registerFile.registerStates["111"] = '0' * 12 + "0001"
            elif operand1 > operand2:
                registerFile.registerStates["111"] = '0' * 12 + "0010"
            elif operand1 < operand2:
                registerFile.registerStates["111"] = '0' * 12 + "0100"

    elif memory[program_counter][0:5] in ["01000", "01001"]:
        registerFile.registerStates["111"] = '0' * 16
        operand1 = int(registerFile.registerStates[memory[program_counter][5:8]], 2)
        operand2 = int(memory[program_counter][8:], 2)
        result = int()

        if memory[program_counter][0:5] == "01000":
            result = operand1 >> operand2
        
        elif memory[program_counter][0:5] == "01001":
            result = operand1 << operand2
        
        registerFile.registerStates[memory[program_counter][5:8]] = xBitBinary(16, result)
    
    elif memory[program_counter][0:5] == "01101":
        registerFile.registerStates["111"] = '0' * 16
        operand = registerFile.registerStates[memory[program_counter][13:]]
        inversion = ''
        for index in range(len(operand)):
            if operand[index] == '1':
                inversion += '0'
            if operand[index] == '0':
                inversion += '1'

        registerFile.registerStates[memory[program_counter][10:13]] = inversion

    elif memory[program_counter][0:5] == "01111":
        registerFile.registerStates["111"] = '0' * 16
        return int(memory[program_counter][8:], 2)
    
    elif memory[program_counter][0:5] == "10000":
        if registerFile.registerStates["111"][-3] == '1':
            registerFile.registerStates["111"] = '0' * 16
            return int(memory[program_counter][8:], 2)
        else:
            registerFile.registerStates["111"] = '0' * 16
            return program_counter + 1
    
    elif memory[program_counter][0:5] == "10001":
        if registerFile.registerStates["111"][-2] == '1':
            registerFile.registerStates["111"] = '0' * 16
            return int(memory[program_counter][8:], 2)
        else:
            registerFile.registerStates["111"] = '0' * 16
            return program_counter + 1

    elif memory[program_counter][0:5] == "10010":
        if registerFile.registerStates["111"][-1] == '1':
            registerFile.registerStates["111"] = '0' * 16
            return int(memory[program_counter][8:], 2)
        else:
            registerFile.registerStates["111"] = '0' * 16
            return program_counter + 1
        
    return program_counter + 1