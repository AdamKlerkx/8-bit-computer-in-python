import time as t
import re as r

BIN = {
    "D0": "0000", "A0": "0000",
    "D1": "0000", "A1": "0000",
    "D2": "0000", "A2": "0000",
    "D3": "0000", "A3": "0000",
    "D4": "0000", "A4": "0000",
    "D5": "0000", "A5": "0000",
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
    "OUT": "1110",
    "HLT": "1111"
}

# < -----------------------------------------      stuff   ---------------------------------------->

#math stuff
RA = "00000000"
RB = "0000"
carry = "0"
prgcnt = 0
count: int = 0
prgstp = 32
time = 0.5
#ui stuff
stop = False
responce = ""
screen_with = 75
# comand names
ctr_quit = "q"
ctr_print = "p"
ctr_run = "r"
ctr_change = "c"
ctr_compile = "co"
ctr_decode = "d"
ctr_select  = "s"
ctr_file = "f"
ctr_load = "l"
ctr_count = "cc"
ctr_time = "t"
#regex
safecheck = r.compile("^[0-1]{4}|[0-9,a-f,A-F]|1[0-5]$")
isbinary = r.compile("^[0-1]{4}$")
# key = "D5"

# <---------------------------------------------    cool shit   ----------------------------------->

def select_BIN (change):
    BIN_type = input("choose a bin: ").lower()
    if len(BIN_type) == 1:
        print(BIN["D" + BIN_type] + " " + BIN["A" + BIN_type])
        if change == True:
            choose = input("which one do you want to change? D or A ").lower()
            if choose == "a":
                return ("A" + BIN_type)
            if choose == "d":
                return ("D" + BIN_type)
    if len(BIN_type) == 2 and "d" or "a" in BIN_type:
        print(BIN[BIN_type])
        return (BIN_type)
    if len(BIN_type) > 2:
        print("sorry mate")
        select_BIN(change)

def change_BIN (key):
    change = input("to what do you want to change " + str(key) + ": ")
    if len(change) == 4 and str(change).isdigit():
        BIN[key] = change
        print(key + " was successfully changed to: " + BIN[key])
    else:
        print("no can do")
        change_BIN(key)

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

def load_file(name):
    f = open(name + ".txt","r")
    inhoud = f.readline(20).rstrip()
    for key, value in HEX.items():
        # print(HEX[key])
        inhoud = f.readline(20).rstrip().replace(HEX[key], "", 1).replace(" ", "", 1)
        # print(inhoud)
        part1, _, part2 = inhoud.partition(" ")
        BIN["D" + HEX[key]] = part1
        BIN["A" + HEX[key]] = part2
        # print("P1 " + part1)
        # print("P2 " + part2)

# ----------------------------------------- binary logic -----------------------------------

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

# ----------------------------------------- decode logic -----------------------------------

def find_binary(input):
    operation, _, value = input.partition(" ")
    if len(value) == 4:
        value = binary_value(value)
    if value == "":
        value = "0"
    value = value_binary(int(HEX_value(value)))
    operation = comands[str(operation)]
    return operation, value

def find_value(input):
    operation, _, value = input.partition(" ")
    for key, val in comands.items():
        if val == value:
            operation = key
    value = str(binary_value(value))
    return operation, value

# ------------------------------------------- compile and decode ------------------------------

def compile():
    print("just write your program: ")
    for key, value in HEX.items():
        inp = input(value + ": ").upper()
        print(inp)
        if inp == "":
            pass
        if r.match(safecheck, inp):
            inp = "NOP " + inp
            operasion, address = find_binary(inp)
            BIN["D" + value] = operasion
            BIN["A" + value] = address
        else:
            operasion, address = find_binary(inp)
            BIN["D" + value] = operasion
            BIN["A" + value] = address
    print("here is your program compiled: ")
    print_BIN()

def decode():
    print("here is your program decoded: ")
    for key, value in HEX.items():
        DATA = BIN["D" + value]
        ADDRESS = BIN["A" + value]
        for comand, binary in comands.items():
            if binary == DATA:
                DATA = comand
        print(DATA + " " + HEX[binary_value(ADDRESS) + 1])

# <----------------------------------------   menu shit ---------------------------------------->

def print_top():
    print("+" + "-" * screen_with + "+")

def print_line(tekst="", uitlijn="<"):
    print(("| = {:" + uitlijn + str(screen_with - 4) + "} |").format(tekst))

def print_menu_line(tekst="", uitlijn="<"):
    print(("| {:" + uitlijn + str(screen_with - 2) + "} |").format(tekst))

def print_menu():
    print_top()
    print_menu_line(ctr_quit + " - to quit")
    print_menu_line(ctr_print + " - to print bin")
    print_menu_line(ctr_count + " - change max program count")
    print_menu_line(ctr_time + " - to change the time of the program")
    print_menu_line(ctr_run + " - to run simulation")
    print_menu_line(ctr_compile + " - to compile your own program")
    print_menu_line(ctr_decode + " - to decode your program")
    print_menu_line(ctr_change + " - to change bin")
    print_menu_line(ctr_select + " - to select")
    print_menu_line(ctr_file + " - to make a file")
    print_menu_line(ctr_load + " - to load file")
    print_top()
    Input = input("just say what you want: ")
    return Input

# ---------------------------- logic ---------------------------------

def ALU(A, B, C): #ALU logic
    if A + B + C == 0:
        return (0, 0)
    if A + B + C == 1:
        return (1, 0)
    if A + B + C == 2:
        return (0, 1)
    if A + B + C == 3:
        return (1, 1)

def INV(value): #this inverts the value given
    invertedvalue = ""
    for caracter in value:
        if caracter == "0":
            caracter = "1"
            invertedvalue += caracter
            continue
        if caracter == "1":
            caracter = "0"
            invertedvalue += caracter
    return (invertedvalue)

def ATV(ADDRESS):   #address to value
    ADDRESS = "A" + HEX[int(ADDRESS, 2) + 1]
    value = BIN[ADDRESS]
    return value

# ------------------------------ external --------------------------------

def LDA(ADDRESS):
    global RA
    RA = ATV(ADDRESS)
    return RA

def ADD(ADDRESS):
    RB = ATV(ADDRESS)
    carry  = 0
    output = ""
    for i in range(len(RA)):
        A = RA[3 - i]
        B = RB[3 - i]
        anser, carry = ALU(int(A), int(B), carry)
        output = output + str(anser)
    output = output[::-1]
    return output, str(carry)

def SUB(ADDRESS):
    carry  = 1
    output = ""
    RB = INV(ATV(ADDRESS))
    for i in range(len(RA)):
        A = RA[3 - i]
        B = RB[3 - i]
        anser, carry = ALU(int(A), int(B), carry)
        output = output + str(anser)
    output = output[::-1]
    return output, str(carry)

def STA(ADDRESS):
    ADDRESS = "A" + HEX[int(ADDRESS, 2) + 1]
    BIN[ADDRESS] = RA
    return BIN[ADDRESS]

def LDI(VALUE):
    RA = VALUE
    return RA

def JMP(ADDRESS):
    global prgcnt
    print_line("JMP -> " + ADDRESS)
    prgcnt = int(ADDRESS, 2)

def JC(ADDRESS):
    if carry == "1":
        JMP(ADDRESS)

def JZ(ADDRESS):
    if RA == "0000":
        JMP(ADDRESS)

def OUT(RA):
    print_line("OUT to display: " + RA + "       output = " + str(int(RA, 2)))


# ----------------------------------- oparations --------------------------------

def execute(DATA, ADDRESS):
    global RA
    global carry
    if DATA == "0000":
        print_line("nothing")
        return ("skip")
    if DATA == "0001":
        RA = LDA(ADDRESS)
        print_line("[ad] -> RA")
        return ("continue")
    if DATA == "0010":
        RA, carry = ADD(ADDRESS)
        print_line("ADD RA + [ad]")
        print_line("anser " + RA)
        print_line("carry " + str(carry))
        return ("continue")
    if DATA == "0011":
        RA, carry = SUB(ADDRESS)
        print_line("SUB RA - [ad] ")
        print_line("anser " + RA)
        print_line("carry " + str(carry))
        return ("continue")
    if DATA == "0100":
        STA(ADDRESS)
        print_line("RA -> [AD]")
        return ("continue")
    if DATA == "0101":
        RA = LDI(ADDRESS)
        print_line("VA -> RA")
        return ("continue")
    if DATA == "0110":
        JMP(ADDRESS)
        return ("jump")
    if DATA == "0111":
        print_line("JMP if carry = 0")
        JC(ADDRESS)
        return ("jump")
    if DATA == "1000":
        print_line("JMP if RA = 0")
        JZ(ADDRESS)
        return ("jump")
    if DATA == "1110":
        print_line("print RA")
        OUT(RA)
        return ("continue")
    if DATA == "1111":
        return ("stop")
    else:
        return ("stop")


def runprg():
    global count
    global prgcnt
    global prgstp
    global time
    manuel = False
    count = 0
    prgcnt = 0
    while True:
        if manuel == False:
            if input("do you want manuel Y or N: ").lower() == "y":
                manuel = True
            else:
                manuel = False
        print_top()
        prgcnt += 1
        count += 1
        print_line("program count: " + str(HEX[prgcnt]))
        DATACODE = BIN["D" + HEX[prgcnt]]
        ADDRESSCODE = BIN["A" + HEX[prgcnt]]
        print_line("input: " + str(DATACODE) + " " +str(ADDRESSCODE))
        exrt = execute(DATACODE, ADDRESSCODE)
        if exrt == "continue":
            print_line("next")
            t.sleep(time)
        if exrt == "skip":
            print_line("skip")
        if exrt == "jump":
            print_line("jump")
            t.sleep(time)
        if exrt == "stop":
            print_line("stopping program: stop")
            break
        if count == int(prgstp):
            print_line("stopping program: count")
            break
        if prgcnt == 16:
            print_line("stopping program: prgcnt")
            break

# --------------------------------------- prog -------------------------------

while (responce := print_menu().lower()) != ctr_quit:
    # print(responce)
    if responce == ctr_print:
        print_BIN()
    if responce == ctr_change:
        key = select_BIN(True)
        change_BIN(key)
    if responce == ctr_select:
        select_BIN(False)
    if responce == ctr_file:
        make_file(input("what do want the name to be: "))
    if responce == ctr_load:
        load_file(input("what file do you want to load: "))
    if responce == ctr_run:
        runprg()
    if responce == ctr_compile:
        compile()
    if responce == ctr_decode:
        decode()
    if responce == ctr_count:
        prgstp = input("this is the curent max program count: " + str(prgstp) + " to what do you want to change the maximum program count: ")
    if responce == ctr_time:
        time = int(input("what do you want the time to be: "))