from sys import stdin
import command
import syntax
import output

def main():
    line_count = 0
    var_count = 0
    i_flag = 0
    labels = {}
    variables = {}
    assembly = []
    program = []

    for line in stdin:
        if line == '':
            break
        assembly.append(tuple((line.split())))

    for line in assembly:
        line_count += 1
        
        check = syntax.check(i_flag, line, variables, labels)

        if check == "label: instruction":
            i_flag += 1
            if len(line[1:]) <= 4: 
                program.append(command.Command(line_count, *line[1:]))
                labels[line[0][0:-1]] = command.mem_addr(len(program) - 1)
            else:
                print("Line", line_count, "-> General Syntax Error: Too many arguments")
        
        elif check == "instruction":
            i_flag += 1
            if len(line) <= 4:
                program.append(command.Command(line_count, *line))
            else:
                print("Line", line_count, "-> General Syntax Error: Too many arguments")

        elif check == "variable":
            variables[line[1]] = var_count
            var_count += 1

        elif check == "empty line":
            continue

        else:
            print("Line", line_count, "-> Error:", check)
            return

    for variable in variables:
        variables[variable] += len(program)
        variables[variable] = command.mem_addr(variables[variable])

    output.translateToBinary(program, line_count, variables, labels)

if __name__ == "__main__":
    main()