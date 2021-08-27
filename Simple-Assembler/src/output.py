import data

def translateToBinary(program, line_count, variables, labels):
    output = []
    halt_flag = 0
    for command in program:
        command.setType(variables, labels)

        if command.e_flag == 1:
            print(command.error)
            return

        binary_code = ''
        
        if command.instruction == "mov":
            if command.args == 'RI':
                binary_code += "00010"
                binary_code += command.args_code
                output.append(binary_code)
                continue
            elif command.args == 'RF' or command.args == 'RR':
                binary_code += "00011"
                binary_code += "00000"
                binary_code += command.args_code
                output.append(binary_code)
                continue
            else:
                print("Line", command.line, "-> General Syntax Error: mov does not support given arguments")
                return

        elif command.t_flag == 1:
            if command.type == data.instructions[command.instruction][1]:
                if command.instruction == "hlt":
                    if command.line != line_count:
                        print("Line", command.line, "-> Error: hlt not used as the last instruction")
                        return
                    else:
                        halt_flag += 1
        
                binary_code += data.instructions[command.instruction][0]
                binary_code += command.unused_bits
                binary_code += command.args_code
                output.append(binary_code)
                continue
        
            else:
                print("Line", command.line, "-> Error: Type '" + data.instructions[command.instruction][1] + "' instruction cannot be used as type '" + command.type + "'")
                return

    if halt_flag == 0:
        print("Line", line_count + 1, "-> Error: Missing hlt statement at the end")
        return

    elif halt_flag == 1:
        for code in output:
            print(code)

    
    



