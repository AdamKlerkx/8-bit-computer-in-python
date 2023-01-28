BIN = {
    "D0": "0101", "A0": "0001",
    "D1": "0100", "A1": "1111",
    "D2": "0101", "A2": "0000",
    "D3": "0010", "A3": "1111",
    "D4": "1110", "A4": "0000",
    "D5": "0110", "A5": "0011",
    "D6": "0000", "A6": "0000",
    "D7": "0000", "A7": "0000",
    "D8": "0000", "A8": "0000",
    "D9": "0000", "A9": "0000",
    "DA": "0000", "AA": "0000",
    "DB": "0000", "AB": "0000",
    "DC": "0000", "AC": "0000",
    "DD": "0000", "AD": "0000",
    "DE": "0000", "AE": "0000",
    "DF": "0000", "AF": "0000"
}

HEX = {
    1: "0",
    2: "1",
    3: "2",
    4: "3",
    5: "4",
    6: "5",
    7: "6",
    8: "7",
    9: "8",
    10: "9",
    11: "A",
    12: "B",
    13: "C",
    14: "D",
    15: "E",
    16: "F"
}

comands = {
    "NOP": "0000",
    "LDA": "0001",
    "ADD": "0010",
    "SUB": "0011",
    "STA": "0100",
    "LDI": "0101",
    "JMP": "0110",
    "JC":  "0111",
    "JZ":  "1000",
    "JN":  "1001",
    "OUT": "1110",
    "HLT": "1111"
}


def print_BIN ():
    print("N D    A")
    for key, value in HEX.items():
        temp_hex = HEX[key]
        print(f"{temp_hex} {BIN['D' + str(temp_hex)]} {BIN['A' + str(temp_hex)]}")


def make_file(name):
    print("in " + name + ".txt: ")
    with open(name + ".txt", "w") as f:
        print("N D    A")
        f.write("N D    A\n")
        for key, value in HEX.items():
            temp_hex = HEX[key]
            print(f"{temp_hex} {BIN['D' + str(temp_hex)]} {BIN['A' + str(temp_hex)]}")
            f.write(f"{temp_hex} {BIN['D' + str(temp_hex)]} {BIN['A' + str(temp_hex)]}\n")
    f.close()



# --------------------------------- translate ----------------------

def binary_value(binary_value):
    value = 0
    count = 0
    for caracters in binary_value[::-1]:
        count += 1
        if caracters == "1":
            value = value + pow(2, (count - 1))
        else:
            pass
    return value

def value_binary(value):
    value = HEX_value(value)
    binary = ""
    while int(value) > 0:
        remainder = value % 2
        binary = str(remainder) + binary
        value = value // 2
    while len(binary) < 4:
        binary = "0" + binary
    return binary

def HEX_value(value):
    if value in ("A", "B", "C", "D", "E", "F"):
        for key, val in HEX.items():
            if val == value:
                return (key - 1)
    else:
        return int(value)


# ---------------------------------- logic -------------------------

def find_binary(input):
    operation, _, value = input.partition(" ")
    operation = comands[str(operation)]
    value = value_binary(int(HEX_value(value)))

    return operation, value

def find_value(input):
    operation, _, value = input.partition(" ")
    for key, val in comands.items():
        if val == value:
            operation = key
    value = str(binary_value(value))
    return operation, value

# ----------------------------- interface --------------------------

def compile():
    global program
    program = {}
    print("just write your program: ")
    for key, value in HEX.items():
        inp = input(value + ": ")
        if inp == "":
            pass
        else:
            operasion, address = find_binary(inp)
            BIN["D" + value] = operasion
            BIN["A" + value] = address
    print("here is your program compiled: ")
    print_BIN()

def decode():
    global program
    print("here is your program decoded: ")
    for key, value in HEX.items():
        DATA = BIN["D" + value]
        ADDRESS = BIN["A" + value]
        for comand, binary in comands.items():
            if binary == DATA:
                DATA = comand
        print(DATA + " " + HEX[binary_value(ADDRESS) + 1])


decode()
# compile()

# if statments for les wrong imputs
# i want to also be able to input binary instead of numbers or leters
# make it so i can see what comands are sent when the program is running








