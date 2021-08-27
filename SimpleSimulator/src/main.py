from sys import stdin
import matplotlib.pyplot as plt
import numpy as np
import registerFile
import executionEngine

def main():
    memory = ['0'*16] * 256
    cycle = 0
    program_counter = 0
    index = 0
    halt_flag = 0
    output = []

    for line in stdin:
        if line == '':
            break
        memory[index] = line[:-1]
        index += 1
    memory[index - 1] = "1001100000000000"    

    x = np.array([])
    y = np.array([])

    while halt_flag != 1:
        mem_addr_1 = program_counter
        if memory[program_counter][0:5] == "10011":
            halt_flag += 1
        next = executionEngine.updateRegisterStates(memory, program_counter)
        program_counter = executionEngine.xBitBinary(8, program_counter)
        cycle += 1
        x = np.append(x, cycle)
        y = np.append(y, mem_addr_1)
        if memory[mem_addr_1][0:5] in ["00100", "00101"]:
            mem_addr_2 = int(memory[mem_addr_1][8:], 2)
            x = np.append(x, cycle)
            y = np.append(y, mem_addr_2)
        register_states = registerFile.getRegisterStates()
        output.append(program_counter + ' ' + register_states)
        program_counter = next

        
    for line in output:
        print(line)

    for line in memory:
        print(line)

    x = x.astype(int)
    y = y.astype(int)
    plt.xlabel("Cycle")
    plt.ylabel("Memory Address")
    plt.title("Cycles vs Memory Addresses")
    plt.plot(x, y, 'o')
    if np.size(y) < 25:
        plt.yticks(y[::1])
    else:
        i = np.size(y) // 25
        l = []
        for j in range(0, np.size(y), i):
            l.append(j)
        plt.yticks(l) 
    
    if np.size(x) < 15:
        plt.xticks(x[::1])
    else:
        i = np.size(x) // 15
        l = []
        for j in range(1, np.size(x), i):
            l.append(j)
        plt.xticks(l) 
    
    plt.savefig("pattern.png", format = "png")

if __name__ == "__main__":
    main()