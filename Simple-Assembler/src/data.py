operations = {"add" : "00000",
              "sub" : "00001",
              "ld"  : "00100",
              "st"  : "00101",
              "mul"  : "00110",
              "div"  : "00111",
              "rs"  : "01000",
              "ls"  : "01001",
              "je"  : "10010",
              "jlt"  : "10000",
              "jgt"  : "10001",
              "jmp"  : "01111",
              "cmp"  : "01110",
              "and"  : "01100",
              "not"  : "01101",
              "or"  : "01011",
              "xor"  : "01010",
}

registers = [
                {
                    "name"     : "R0",
                    "address"  : "000"
                },

                {
                    "name"     : "R1",
                    "address"  : "001"
                },

                {
                    "name"     : "R2",
                    "address"  : "010"
                },

                {
                    "name"     : "R3",
                    "address"  : "011"
                },

                {
                    "name"     : "R4",
                    "address"  : "100"
                },

                {
                    "name"     : "R5",
                    "address"  : "101"
                },

                {
                    "name"     : "R6",
                    "address"  : "110"
                }
]