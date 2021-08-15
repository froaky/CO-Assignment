from sys import stdin
import syntax
import assembly

def main():
    line_count = 0
    instruction_count = 0
    labels = {}
    variables = {}
    var_count = 0
    temp = []
    program = []

    for line in stdin:
        if line == '':
            break    
        temp.append(line.split())

    for t in temp:
        line_count += 1
        if len(t) == 1 and t[0] != "hlt":
            print("Line", line_count, "-> Syntax Error: Typo in instruction name")
            return
        else:
            instruction = [line_count, instruction_count]

            if t[0] == "var":
                if len(t) == 2:
                    if syntax.isName(t[1]):
                        if instruction_count == 0:
                            variables[t[1]] = var_count
                            var_count += 1
                        else:
                            print("Line", line_count, "-> Syntax Error: Variable not declared at the beginning")
                            return
                    else:
                        print("Line", line_count, "-> Syntax Error: Variable name invalid")
                        return
                else:
                    print("Line", line_count, "-> General Syntax Error")
                    return
            
            elif syntax.isLabel(t[0]):
                labels[t[0][0:-1]] = syntax.mem_addr(instruction_count)
                instruction.extend(t)
                program.append(instruction)
                instruction_count += 1

            else:
                instruction.extend(t)
                program.append(instruction)
                instruction_count += 1

    for variable in variables:
        variables[variable] += instruction_count
        variables[variable] = syntax.mem_addr(variables[variable])
    
    for instruction in program:
        if syntax.isInstruction(instruction, labels, variables, line_count) == False:
            return
    
    assembly.translateToBinary(program, line_count)
                
if __name__ == "__main__":
    main()