from sys import stdin
import matplotlib.pyplot as plt

string = ''
c = 0
for s in stdin:
    c += 1
    if s == "":
        break
    string += s

string = string.splitlines()

TypeA = ['00000', '00001', '00110', '01010', '01011', '01100']
TypeB = ['00010', '01000', '01001']
TypeC = ['00011', '00111', '01101', '01110']
TypeD = ['00100', '00101']
TypeE = ['01111', '10000', '10001', '10010']

reg_add = {'000': 'R0', '001': 'R1', '010': 'R2', '011': 'R3', '100': 'R4', '101': 'R5', '110': 'R6', '111': 'FLAGS'}
reg_value = {'R0': 0, 'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0, 'R5': 0, 'R6': 0, 'FLAGS': 0}

mem_add = []  # memory
for i in range(256):
    mem_add.append('0' * 16)

variables = {}
labels = {}
V = 0
L = 0
G = 0
E = 0


def addition(r1, r2, r3):
    global V
    reg_value[reg_add[r1]] = reg_value[reg_add[r2]] + reg_value[reg_add[r3]]
    if reg_value[reg_add[r1]] >= 65536:
        V = 1
        reg_value[reg_add[r1]] %= 65536


def subtraction(r1, r2, r3):
    global V
    reg_value[reg_add[r1]] = reg_value[reg_add[r2]] - reg_value[reg_add[r3]]
    if reg_value[reg_add[r1]] < 0:
        V = 1
        reg_value[reg_add[r1]] = 0


def multiplication(r1, r2, r3):
    global V
    reg_value[reg_add[r1]] = reg_value[reg_add[r2]] * reg_value[reg_add[r3]]
    if reg_value[reg_add[r1]] >= 65536:
        V = 1
        reg_value[reg_add[r1]] %= 65536


def division(r1, r2):
    if reg_value[reg_add[r2]] == 0:
        print('Zero division error')
        quit()
    reg_value['R0'] = (reg_value[reg_add[r1]]) // (reg_value[reg_add[r2]])
    reg_value['R1'] = (reg_value[reg_add[r1]]) % (reg_value[reg_add[r2]])


def movimm(r1, a):
    reg_value[reg_add[r1]] = int(a, 2)


def movreg(r1, r2):
    reg_value[reg_add[r1]] = reg_value[reg_add[r2]]


def rs(r1, a):
    reg_value[reg_add[r1]] = reg_value[reg_add[r1]] >> int(a, 2)


def ls(r1, a):
    reg_value[reg_add[r1]] = reg_value[reg_add[r1]] << int(a, 2)


def load(r1, x):
    x = int(x, 2)
    reg_value[reg_add[r1]] = int(mem_add[x], 2)  # convert binary to integer


def store(r1, x):
    x = int(x, 2)
    mem_add[x] = f'{reg_value[reg_add[r1]]:016b}'  # convert integer to 16bit binary


def compare(r1, r2):
    global L
    global G
    global E
    if reg_value[reg_add[r1]] == reg_value[reg_add[r2]]:
        E = 1
    elif reg_value[reg_add[r1]] < reg_value[reg_add[r2]]:
        L = 1
    elif reg_value[reg_add[r1]] > reg_value[reg_add[r2]]:
        G = 1


def xor(r1, r2, r3):
    # reg_value[reg_add[r1]] = reg_value[reg_add[r2]] ^ reg_value[reg_add[r3]]
    a = str(f'{reg_value[reg_add[r2]]:016b}')
    b = str(f'{reg_value[reg_add[r3]]:016b}')
    c = ''
    for i in range(16):
        if a[i] == b[i]:
            c += '0'
        else:
            c += '1'
    reg_value[reg_add[r1]] = int(c, 2)


def Or(r1, r2, r3):
    reg_value[reg_add[r1]] = reg_value[reg_add[r2]] or reg_value[reg_add[r3]]


def And(r1, r2, r3):
    reg_value[reg_add[r1]] = reg_value[reg_add[r2]] and reg_value[reg_add[r3]]


def invert(r1, r2):
    # reg_value[reg_add[r1]] = ~ reg_value[reg_add[r2]]
    a = str(f'{reg_value[reg_add[r2]]:016b}')
    c = ''
    for i in range(16):
        if a[i] == '0':
            c += '1'
        else:
            c += '0'
    reg_value[reg_add[r1]] = int(c, 2)


def jmp(add):
    return add


def jlt(add):
    return add


def jgt(add):
    return add


def je(add):
    return add


x = []
y = []
c = 0
pc = 0  # program counter
for i in string:
    x.append(c)
    y.append(pc)

    mem_add[pc] = string[pc]
    pc += 1
    if i[0:5] in TypeA:

        if i[0:5] == "00000":
            V, L, G, E = 0, 0, 0, 0
            addition(i[7:10], i[10:13], i[13:16])
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(f'{pc - 1:08b}', f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')
        elif i[0:5] == "00001":
            V, L, G, E = 0, 0, 0, 0
            subtraction(i[7:10], i[10:13], i[13:16])
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(f'{pc - 1:08b}', f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')
        elif i[0:5] == "00110":
            V, L, G, E = 0, 0, 0, 0
            multiplication(i[7:10], i[10:13], i[13:16])
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(f'{pc - 1:08b}', f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')
        elif i[0:5] == "01010":
            V, L, G, E = 0, 0, 0, 0
            xor(i[7:10], i[10:13], i[13:16])
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(f'{pc - 1:08b}', f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')
        elif i[0:5] == "01011":
            V, L, G, E = 0, 0, 0, 0
            Or(i[7:10], i[10:13], i[13:16])
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(f'{pc - 1:08b}', f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')
        elif i[0:5] == "01100":
            V, L, G, E = 0, 0, 0, 0
            And(i[7:10], i[10:13], i[13:16])
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(f'{pc - 1:08b}', f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')
    if i[0:5] in TypeD:

        if i[0:5] == "00100":
            V, L, G, E = 0, 0, 0, 0
            load(i[5:8], i[8:16])
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(f'{pc - 1:08b}', f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')
        elif i[0:5] == "00101":
            V, L, G, E = 0, 0, 0, 0
            store(i[5:8], i[8:16])
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(f'{pc - 1:08b}', f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')
    if i[0:5] in TypeB:

        if i[0:5] == "00010":
            V, L, G, E = 0, 0, 0, 0
            movimm(i[5:8], i[8:16])
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(f'{pc - 1:08b}', f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')
        elif i[0:5] == "01000":
            V, L, G, E = 0, 0, 0, 0
            rs(i[5:8], i[8:16])
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(f'{pc - 1:08b}', f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')
        elif i[0:5] == "01001":
            V, L, G, E = 0, 0, 0, 0
            ls(i[5:8], i[8:16])
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(f'{pc - 1:08b}', f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')
    if i[0:5] in TypeC:

        if i[0:5] == "00011":
            V, L, G, E = 0, 0, 0, 0
            movreg(i[10:13], i[13:])
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(f'{pc - 1:08b}', f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')
        elif i[0:5] == "00111":
            V, L, G, E = 0, 0, 0, 0
            division(i[10:13], i[13:])
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(f'{pc - 1:08b}', f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')
        elif i[0:5] == "01101":
            V, L, G, E = 0, 0, 0, 0
            invert(i[10:13], i[13:])
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(f'{pc - 1:08b}', f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')
        elif i[0:5] == "01110":
            V, L, G, E = 0, 0, 0, 0
            compare(i[10:13], i[13:])
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(f'{pc - 1:08b}', f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')

    if i[0:5] in TypeE:

        if i[0:5] == '01111':
            a = jmp(i[8:16])
            b = int(a, 2) - 1
            a = f'{b:08b}'
            x.append(c)
            y.append(b)
            V, L, G, E = 0, 0, 0, 0
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(a, f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')
        elif i[0:5] == '10000':
            a = jlt(i[8:16])
            b = int(a, 2) - 1
            a = f'{b:08b}'
            x.append(c)
            y.append(b)
            V, L, G, E = 0, 0, 0, 0
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(a, f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')
        elif i[0:5] == '10001':
            a = jgt(i[8:16])
            b = int(a, 2) - 1
            a = f'{b:08b}'
            x.append(c)
            y.append(b)
            V, L, G, E = 0, 0, 0, 0
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(a, f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')
        elif i[0:5] == '10010':
            a = je(i[8:16])
            b = int(a, 2) - 1
            a = f'{b:08b}'
            x.append(c)
            y.append(b)
            V, L, G, E = 0, 0, 0, 0
            reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
            print(a, f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
                  f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
                  f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')

    if i == '1001100000000000':
        V, L, G, E = 0, 0, 0, 0
        reg_value["FLAGS"] = (V * 8) + (4 * L) + (2 * G) + (1 * E)
        print(f'{pc - 1:08b}', f'{reg_value["R0"]:016b}', f'{reg_value["R1"]:016b}',
              f'{reg_value["R2"]:016b}', f'{reg_value["R3"]:016b}', f'{reg_value["R4"]:016b}',
              f'{reg_value["R5"]:016b}', f'{reg_value["R6"]:016b}', f'{reg_value["FLAGS"]:016b}')
    c += 1
for i in mem_add:
    print(i)
plt.scatter(x, y, )
plt.savefig('dha.png')
plt.show()
