######################################################################################################################
# Binary oparations particulary made to use in chacha algorihtm ######################################################
# Made by: Carlos Keleanderson Pereira da Silva ######################################################################
# Federal University of Rio de Janeiro ###############################################################################
######################################################################################################################

import random
def generate_key(n_bits):
    """This function return a key of n_bits bit"""
    number = ''  # aux vector to save all bits

    # Generates all key's bits
    for i in range(0, n_bits):
        number = number + str(random.randrange(0, 2))
    return '0b' + number

def shift_left(number, shift):
    """The function receive a binary number such as a=bin(12) and compute a left shift in this number by the value
    of a shift parameter.
    number: an integer number
    shift: number of bits shifted to the left
    """

    # A verification if the type is binary type and if yes tranform it into integer type to aplicate the shift function
    if type(number) is str:
        n = int(number, 2)  # transforms into integer type
    else:
        n = number

    # If the shift is bigger than the lenght of the binary number ( without the '0b' prefix) we must see the equivalent
    # shift by using module function in python
    shift = shift % len(bin(n)[2:])

    # Now we apply the shift and after tranform into binary number
    n1 = bin(n << shift)
    number = '0b' + n1[2 + shift:-shift] + n1[2:2 + shift]
    # print(len(number))

    if len(number) == 34:
        return number
    else:
        diff = abs(len(number) - 34)
        return '0b' + '0' * diff + number[2:]

def shift_right(number, shift):
    """The function receive a binary number such as a=bin(12) and compute a right shift in this number by the value
    of a shift parameter.
    number: an integer number
    shift: number of bits shifted to the right.
    """

    # A verification if the type is binary type and if yes tranform it into integer type to aplicate the shift function
    if type(number) is str:
        n = int(number, 2)  # transforms into integer type
    else:
        n = number

    # If the shift is bigger than the lenght of the binary number ( without the '0b' prefix) we must see the equivalent
    # shift by using module function in python
    shift = shift % len(bin(n)[2:])

    # If shift is zero then return the number istself
    if not shift:
        return bin(n)
    # create an auxiliar matrix to store the bits will arase when apply n>>shift
    n_aux = bin(n)[-shift:]
    n1 = bin(n >> shift)[2:]

    # return the binary of shift bilding
    return '0b' + n_aux + n1


def xor(n1, n2):
    if type(n1) is str:
        n1 = int(n1, 2)
    else:
        n1 = n1
    if type(n2) is str:
        n2 = int(n2, 2)
    else:
        n2 = n2

    number = bin(n1 ^ n2)

    # print("numero binario e tamanho ")
    # print(number, len(number))
    # print("n1 e n2")
    # print(n1,n2)

    if len(number) == 34:
        return number
    else:
        diff = abs(len(number) - 34)
        return '0b' + '0' * diff + number[2:]


def bit_sum(n1, n2):
    # verifiying if is a bit class
    if type(n1) is str:
        n1 = n1
    else:
        n1 = bin(n1)
    if type(n2) is str:
        n2 = n2
    else:
        n2 = bin(n2)

    number = ''  # create a list to add the binary number
    carry = 0  # carry to use in the bit addition

    for i, j in zip(n1[2:][::-1], n2[2:][::-1]):
        soma = int(i) + int(j) + carry
        if soma % 2 == 0:
            carry = 1
            number = number + str(0)
        elif soma % 3 == 0:
            carry = 1
            number = number + str(1)
        else:
            carry = 0
            number = number + str(1)
    if len(number) == len(n1[2:]):
        pass
    else:
        number = number[:-2]

    return '0b' + number[::-1]