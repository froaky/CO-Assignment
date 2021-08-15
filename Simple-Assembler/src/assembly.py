def translateToBinary(instructions, line_count):
    output = []
    halt_flag = 0
    for instruction in instructions:
        if instruction[-1] == 'F':
            halt_flag += 1
            output.append(instruction[-2])
        else: 
            l = instruction[-2]
            binary = instruction[l + 2]
        
            if instruction[-1] == 'A':
                binary += "00"

            if instruction[-1] == 'E':
                binary += "000"

            if instruction[-1] == 'C':
                binary += "00000"

            binary += instruction[l + 3]
            
            if instruction[-1] != 'E':
                binary += instruction[l + 4]

            if instruction[-1] == 'A':
                binary += instruction[l + 5]

            output.append(binary)
    
    if halt_flag == 1:
        for b in output:
            print(b)
    else:
        print("Line", line_count, "Syntax Error: Missing halt instruction")