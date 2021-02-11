# criar a matrix do chacha
from binaryfunctions.binoperations import *
def generate_chacha_matrix(key, counter, n0, n1, n2, c0, c1, c2, c3, elements=0):
    try:
        x0 = c0
        x1 = c1
        x2 = c2
        x3 = c3
        x4 = key[:34]
        x5 = '0b' + key[34:66]
        x6 = '0b' + key[66:98]
        x7 = '0b' + key[98:130]
        x8 = '0b' + key[130:162]
        x9 = '0b' + key[162:194]
        x10 = '0b' + key[194:226]
        x11 = '0b' + key[226:]
        x12 = counter
        x13 = n0
        x14 = n1
        x15 = n2
    except:
        raise Exception(" the key has not 256 or some of the inputs are not allowed")

    if elements:
        return [x0, x1, x2, x3, x4, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15]
    else:
        return [[x0, x1, x2, x3], [x4, x5, x6, x7], [x8, x9, x10, x11], [x12, x13, x14, x15]]


def quarter_round(a, b, c, d):
    a = bit_sum(a, b)
    d = xor(d, a)
    d = shift_left(d, 16)
    c = bit_sum(c, d)
    b = xor(b, c)
    b = shift_left(b, 12)
    a = bit_sum(a, b)
    d = xor(d, a)
    d = shift_left(d, 8)
    c = bit_sum(c, d)
    b = xor(b, c)
    b = shift_left(b, 7)

    return a, b, c, d


def chacha_round(matrix):
    M = matrix
    # Column Round
    M[0][0], M[1][0], M[2][0], M[3][0] = quarter_round(M[0][0], M[1][0], M[2][0], M[3][0])
    M[0][1], M[1][1], M[2][1], M[3][1] = quarter_round(M[0][1], M[1][1], M[2][1], M[3][1])
    M[0][2], M[1][2], M[2][2], M[3][2] = quarter_round(M[0][2], M[1][2], M[2][2], M[3][2])
    M[0][3], M[1][3], M[2][3], M[3][3] = quarter_round(M[0][3], M[1][3], M[2][3], M[3][3])
    # Diagonal Round
    M[0][0], M[1][1], M[2][2], M[3][3] = quarter_round(M[0][0], M[1][1], M[2][2], M[3][3])
    M[0][1], M[1][2], M[2][3], M[3][0] = quarter_round(M[0][1], M[1][2], M[2][3], M[3][0])
    M[0][2], M[1][3], M[2][0], M[3][1] = quarter_round(M[0][2], M[1][3], M[2][0], M[3][1])
    M[0][3], M[1][0], M[2][1], M[3][2] = quarter_round(M[0][3], M[1][0], M[2][1], M[3][2])

    return M