import time as t
import re as r

BIN = {
    "D0": "0000", "A0": "0000",
    "D1": "0001", "A1": "0000",
    "D2": "0010", "A2": "0000",
    "D3": "0011", "A3": "0000",
    "D4": "0100", "A4": "0000",
    "D5": "0101", "A5": "0000",
    "D6": "0110", "A6": "0000",
    "D7": "0111", "A7": "0000",
    "D8": "1000", "A8": "0000",
    "D9": "1001", "A9": "0000",
    "DA": "1010", "AA": "0000",
    "DB": "1011", "AB": "0000",
    "DC": "1100", "AC": "0000",
    "DD": "1101", "AD": "0000",
    "DE": "1110", "AE": "0000",
    "DF": "1111", "AF": "0000"
}
HEX = {
    0: "0",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "A",
    11: "B",
    12: "C",
    13: "D",
    14: "E",
    15: "F"
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
ctr_file = "f"
ctr_load = "l"
ctr_count = "cc"
ctr_time = "t"
ctr_cheat = "a"
#regex
safecheck = r.compile("^[0-1]{4}|[0-9,a-f,A-F]|1[0-5]$")
isbinary = r.compile("^[0-1]{4}$")
ishex = r.compile("^[0-9,a-f,A-F]$")
isnumber = r.compile("^([0-9]|1[0-5])$")
choosebin = r.compile("^(a|d)*[0-9a-f]{2}$")
iscomand = r.compile("^(NOP|LDA|ADD|SUB|STA|LDI|JMP|JC |JZ |OUT|HLT).{0,3}")

# --------------------------------------------- input logic -----------------------------------

def isstandard(standard, inp):
    if r.fullmatch(isbinary, inp):
        if standard == "binary":
            return "stop"
        else:
            print("this is not a valid input " + standard + " is expected")
    elif r.fullmatch(isnumber, inp) or r.fullmatch(ishex, inp):
        if standard == "number":
            return "stop"
        else:
            print("this is not a valid input " + standard + " is expected")


def inputcheck(standard):
    while True:
        inp = input()
        if r.fullmatch(generalcheck, inp):
            if isstandard(standard, inp) == "stop":
                break
        else:
            print("this is not a valid input " + standard + " is expected")
    return inputtovalue(inp)

# <---------------------------------------------    cool shit   ----------------------------------->

def change_BIN ():
    print("this is the curent bin: ")
    print_BIN()
    key = input("choose what exact codinates you want to change: ").lower()
    if r.fullmatch(choosebin, key):
        inp = input("what do want to replace it with: ")
        BIN[key] = inputtovalue(inp)
    else:
        print("give the exact cordinates")
        change_BIN()

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
                return (key)
    else:
        return int(value)

def inputtovalue(inp):
    if r.match(isbinary, str(inp)):
        binaryvalue = binary_value(inp)
        return binaryvalue
    elif r.match(ishex, inp):
        hexvalue = HEX_value(inp)
        return hexvalue
    elif r.match(isnumber, inp):
        return inp

# ----------------------------------------- decode logic -----------------------------------

def find_binary(input):
    operation, _, value = input.partition(" ")
    if value == "":
        value = "0"
    value = value_binary(int(inputtovalue(value)))
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
        # print(inp)
        if inp == "":
            pass
        elif r.fullmatch(safecheck, inp):
            inp = "NOP " + inp
            operasion, address = find_binary(inp)
            BIN["D" + value] = operasion
            BIN["A" + value] = address
        elif r.fullmatch(iscomand, inp):
            print("joi")
            operasion, address = find_binary(inp)
            BIN["D" + value] = operasion
            BIN["A" + value] = address
        else:
            print("this is not a comand")
            pass
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
        print(HEX[key] + " " + DATA + " " + HEX[binary_value(ADDRESS)])

# <----------------------------------------   menu shit ---------------------------------------->

def print_top():
    print("+" + "-" * screen_with + "+")

def print_line(tekst="", uitlijn="<"):
    print(("| = {:" + uitlijn + str(screen_with - 4) + "} |").format(tekst))

def print_menu_line(tekst="", uitlijn="<"):
    print(("| {:" + uitlijn + str(screen_with - 2) + "} |").format(tekst))

def print_cheat():
    print_top()
    print_menu_line("NOP = " + comands["NOP"] + " this does nothing")
    print_menu_line("LDA = " + comands["LDA"] + " this loads value in address to register A")
    print_menu_line("ADD = " + comands["ADD"] + " this adds register A to value in address")
    print_menu_line("SUB = " + comands["SUB"] + " this will subtract register A to value in address")
    print_menu_line("STA = " + comands["STA"] + " this will load register A into address")
    print_menu_line("LDI = " + comands["LDI"] + " this will load value into register A")
    print_menu_line("JMP = " + comands["JMP"] + " this will the program jump to selected step")
    print_menu_line("JC  = " + comands["JC"] + " this will jump when carry is 1")
    print_menu_line("JZ  = " + comands["JZ"] + " this will jump when register A is 0000")
    print_menu_line("OUT = " + comands["OUT"] + " this will print value")
    print_menu_line("HLT = " + comands["HLT"] + " this will stop the program")
    print_top()

def print_menu():
    print_top()
    print_menu_line(ctr_quit + " - to quit")
    print_menu_line(ctr_cheat + " - to print cheat sheet")
    print_menu_line(ctr_print + " - to print bin")
    print_menu_line(ctr_count + " - change max program count")
    print_menu_line(ctr_time + " - to change the time of the program")
    print_menu_line(ctr_run + " - to run simulation")
    print_menu_line(ctr_compile + " - to compile your own program")
    print_menu_line(ctr_decode + " - to decode your program")
    print_menu_line(ctr_change + " - to change bin")
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
    ADDRESS = "A" + HEX[int(ADDRESS, 2)]
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
    ADDRESS = "A" + HEX[int(ADDRESS, 2)]
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
        change_BIN()
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
    if responce == ctr_cheat:
        print_cheat()
