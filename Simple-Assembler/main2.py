# CO ASSIGNMENT
# ASSEMBLER

from sys import stdin

string = ''
c = 0
for s in stdin:
    c += 1
    if s == "":
        break
    string += s

string = string.splitlines()

hc = 0
for i in string:
    sub = i.split(' ')
    if 'hlt' in sub:
        hc += 1

if hc < 1:
    print('Missing hlt instruction')
    quit()
if hc > 1:
    print('Excess use of hlt instruction.')
    quit()
if 'hlt' not in string[-1]:
    print('hlt is not used as last instruction')
    quit()

typeA = ['add', 'sub', 'mul', 'xor', 'or', 'and']
typeB = ['mov', 'rs', 'ls']
typeC = ['mov', 'div', 'not', 'cmp']
typeD = ['ld', 'st']
typeE = ['jmp', 'jlt', 'jgt', 'je']
typeF = ['hlt']

complete_list = ['add', 'sub', 'mul', 'xor', 'or', 'and', 'mov', 'rs', 'ls', 'div', 'not', 'cmp', 'ld', 'st', 'jmp',
                 'jlt', 'jgt', 'je', 'hlt', 'var']

reg_add = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110', 'FLAGS': '111'}

variables = {}
labels = {}


def type_A(s, r1, r2, r3):
    if s == 'add':
        print(addition(r1, r2, r3))
    elif s == 'sub':
        print(subtraction(r1, r2, r3))
    elif s == 'mul':
        print(multiplication(r1, r2, r3))
    elif s == 'xor':
        print(xor(r1, r2, r3))
    elif s == 'or':
        print(Or(r1, r2, r3))
    elif s == 'and':
        print(And(r1, r2, r3))


def type_B(s, r1, imm):
    if s == 'mov':
        print(mov(r1, imm))
    elif s == 'rs':
        print(rs(r1, imm))
    elif s == 'ls':
        print(ls(r1, imm))


def type_C(s, r1, r2):
    if s == 'mov':
        print(mov(r1, r2))
    elif s == 'div':
        print(division(r1, r2))
    elif s == 'not':
        print(Not(r1, r2))
    elif s == 'cmp':
        print(compr(r1, r2))


def type_D(s, r1, count):
    if s == 'ld':
        print(load(r1, count))
    elif s == 'st':
        print(store(r1, count))


def type_E(s, count):
    if s == 'jmp':
        print(jmp(count))
    elif s == 'jlt':
        print(jlt(count))
    elif s == 'jgt':
        print(jgt(count))
    elif s == 'je':
        print(je(count))


def addition(r1, r2, r3):
    ans = '0000000' + reg_add[r1] + reg_add[r2] + reg_add[r3]
    return ans


def subtraction(r1, r2, r3):
    ans = '0000100' + reg_add[r1] + reg_add[r2] + reg_add[r3]
    return ans


def multiplication(r1, r2, r3):
    ans = '0011000' + reg_add[r1] + reg_add[r2] + reg_add[r3]
    return ans


def division(r1, r2):
    ans = '0011100000' + reg_add[r1] + reg_add[r2]
    return ans


def mov(r1, r2):
    if r2[0] == '$':
        a = int(r2[1:])
        if a in range(0, 256):
            ans = '00010' + reg_add[r1] + f'{a:08b}'
            return ans
        else:
            print("Illegal Immediate values")
    else:
        ans = '0001100000' + reg_add[r1] + reg_add[r2]
        return ans


def load(r1, count):
    ans = '00100' + reg_add[r1] + f'{count:08b}'
    return ans


def store(r1, count):
    ans = '00101' + reg_add[r1] + f'{count:08b}'
    return ans


def xor(r1, r2, r3):
    ans = '0101000' + reg_add[r1] + reg_add[r2] + reg_add[r3]
    return ans


def Or(r1, r2, r3):
    ans = '0101100' + reg_add[r1] + reg_add[r2] + reg_add[r3]
    return ans


def And(r1, r2, r3):
    ans = '0110000' + reg_add[r1] + reg_add[r2] + reg_add[r3]
    return ans


def Not(r1, r2):
    ans = '0110100000' + reg_add[r1] + reg_add[r2]
    return ans


def compr(r1, r2):
    ans = '0111000000' + reg_add[r1] + reg_add[r2]
    return ans


def rs(r1, imm):
    a = int(imm[1:])
    if a in range(0, 256):
        ans = '01000' + reg_add[r1] + f'{a:08b}'
        return ans
    else:
        print("Illegal Immediate values")


def ls(r1, imm):
    a = int(imm[1:])
    if a in range(0, 256):
        ans = '01001' + reg_add[r1] + f'{a:08b}'
        return ans
    else:
        print("Illegal Immediate values")


def jmp(count):
    a = int(count)
    ans = '01111000' + f'{a:08b}'
    return ans


def jlt(count):
    a = int(count)
    ans = "10000000" + f'{a:08b}'
    return ans


def jgt(count):
    a = int(count)
    ans = "10001000" + f'{a:08b}'
    return ans


def je(count):
    a = int(count)
    ans = '10010000' + f'{a:08b}'
    return ans


def halt():
    ans = '1001100000000000'
    return ans


c = 0
for i in string:
    sub = i.split()
    if len(sub)>0:
        if sub[0] == '':  # c
            continue
        if sub[0] != 'var':
            c += 1
        if sub[0][-1] == ':':  # c
            for h in sub[0][:-1]:  # c
                if not (h.isalnum()) and h != "_":
                    print("error")
                    quit()
            labels[sub[0][:-1]] = c - 1

n = 0
v = 0
for i in string:

    sub = i.split()
    if len(sub)>0:
        if sub[0] == '':  # c
            continue  # c
        if sub[0] == 'var':
            if len(sub) == 2:
                v += 1  # c
                variables[sub[1]] = v  # line number of variable
            else:
                print('Variable error.')
                quit()

        if sub[0][:-1] in labels.keys():
            sub = sub[1:]

        n += 1
        if sub[0] in typeA:
            if len(sub) == 4:
                type_A(sub[0], sub[1], sub[2], sub[3])
            else:
                print("general syntax error at line", n)

        elif sub[0] in typeB:
            if len(sub) == 3:
                type_B(sub[0], sub[1], sub[2])
            else:
                print("general syntax error at line", n)

        elif sub[0] in typeC:
            if len(sub) == 3:
                type_C(sub[0], sub[1], sub[2])
            else:
                print("general syntax error at line", n)

        elif sub[0] in typeD:
            if sub[2] not in variables.keys():
                print('Use of undefined variables at line', n)
                quit()
            count = n - 1 + variables[sub[2]]
            type_D(sub[0], sub[1], count)

        elif sub[0] in typeE:
            if sub[1] not in labels.keys():
                print('Use of undefined labels at line', n)
                quit()
            count = labels[sub[1]]
            type_E(sub[0], count)

        elif sub[0] == 'hlt':
            print(halt())
            quit()

        elif (sub[0] not in complete_list) and sub[0][-1] != ':':

            print('typo error at line', n)
            quit()
