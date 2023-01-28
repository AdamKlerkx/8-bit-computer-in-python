import time as t

BIN = {
    "D0": "0000",
    "D1": "0110",
    "D2": "0000",
    "D3": "0000",
    "D4": "0000",
    "D5": "0000",
    "D6": "0000",
    "D7": "0000",
    "D8": "0000",
    "D9": "0000",
    "DA": "0000",
    "DB": "0000",
    "DC": "0000",
    "DD": "0000",
    "DE": "0000",
    "DF": "0000",
    "A0": "0000",
    "A1": "0000",
    "A2": "0000",
    "A3": "0000",
    "A4": "0000",
    "A5": "0000",
    "A6": "0000",
    "A7": "0000",
    "A8": "0000",
    "A9": "0000",
    "AA": "0000",
    "AB": "0000",
    "AC": "0000",
    "AD": "0000",
    "AE": "0000",
    "AF": "0000"
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

# ---------------------------
RA = "0000"
RB = "0000"
carry = "0"
prgcnt = 0
count = 0
prgstp = 32

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
    print("JMP -> " + ADDRESS)
    prgcnt = int(ADDRESS, 2)

def JC(ADDRESS):
    if carry == "1":
        JMP(ADDRESS)

def JZ(ADDRESS):
    if RA == "0000":
        JMP(ADDRESS)

def OUT(RA):
    print("OUT to display: " + RA)

# ----------------------------------- oparations --------------------------------

def execute(DATA, ADDRESS):
    global RA
    global carry
    if DATA == "0000":
        print("nothing")
        return ("skip")
    if DATA == "0001":
        RA = LDA(ADDRESS)
        print("[ad] -> RA")
        return ("continue")
    if DATA == "0010":
        RA, carry = ADD(ADDRESS)
        print("ADD RA + [ad]")
        print("RA " + RA)
        print("RB " + RB)
        print("carry " + str(carry))
        return ("continue")
    if DATA == "0011":
        RA, carry = SUB(ADDRESS)
        print("SUB RA - [ad] ")
        print("RA " + RA)
        print("RB " + RB)
        print("carry " + str(carry))
        return ("continue")
    if DATA == "0100":
        STA(ADDRESS)
        print("RA -> [AD]")
        return ("continue")
    if DATA == "0101":
        RA = LDI(ADDRESS)
        print("VA -> RA")
        return ("continue")
    if DATA == "0110":
        JMP(ADDRESS)
        return ("jump")
    if DATA == "0111":
        print("JMP if carry = 0")
        JC(ADDRESS)
        return ("jump")
    if DATA == "1000":
        print("JMP if RA = 0")
        JZ(ADDRESS)
        return ("jump")
    if DATA == "1110":
        print("print RA")
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
    manuel = False
    while True:
        if manuel == False:
            if input("do you want manuel Y or N: ").lower() == "y":
                manuel = True
            else:
                manuel = False
        print("----------------------")
        prgcnt += 1
        count += 1
        print("program count: " + str(HEX[prgcnt]))
        DATACODE = BIN["D" + HEX[prgcnt]]
        ADDRESSCODE = BIN["A" + HEX[prgcnt]]
        print(DATACODE, ADDRESSCODE)
        exrt = execute(DATACODE, ADDRESSCODE)
        if exrt == "continue":
            print("next")
            t.sleep(0.5)
        if exrt == "skip":
            print("skip")
        if exrt == "jump":
            print("jump")
            t.sleep(0.5)
        if exrt == "stop":
            print("stopping program: stop")
            break
        if count == prgstp:
            print("stopping program: count")
            break
        if prgcnt == 16:
            print("stopping program: prgcnt")
            break

runprg()