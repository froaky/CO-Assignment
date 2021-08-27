registerStates = {
                    "000"   :   "0000000000000000",
                    "001"   :   "0000000000000000",
                    "010"   :   "0000000000000000",
                    "011"   :   "0000000000000000",
                    "100"   :   "0000000000000000",
                    "101"   :   "0000000000000000",
                    "110"   :   "0000000000000000",
                    "111"   :   "0000000000000000"
                }

def getRegisterStates():
    output = ''
    for key in registerStates.keys():
        output += registerStates[key] + ' '
    return output