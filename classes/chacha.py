from binaryfunctions.binoperations import *
from mchacha.chacha_operations import *


class ChachaEncrypt:
    def __init__(self, key, nonce=None):

        # constants and relevant things for matrix formation
        if nonce is None:
            nonce = [generate_key(32 + i - i) for i in range(0, 3)]
        self.m_constant = [generate_key(32 + n - n) for n in range(0, 4)]  # Top matrix constants (magic numbers)
        self.key = key  # The algorithm key
        self.nonce = nonce  # o nonce
        self.counter = '0b' + '0' * 32  # the counter
        self.key_order = [0, 0]  # the ith,jth element of encrypted matrix

        # The pre round matrix
        self.chacha_M = generate_chacha_matrix(self.key, self.counter, self.nonce[0],
                                               self.nonce[1], self.nonce[2], self.m_constant[0],
                                               self.m_constant[1], self.m_constant[2], self.m_constant[3])
        self.encrypted_chacha_M = []

        # To storage cipher texts
        self.present_cipher = ''
        self.historical_cipher = []

        self.n_matrix = 0

    def __str__(self):
        return str(self.chacha_M)

    def encrypt(self, plain_text):
        """
        :param: plain_text: a binary entry in str format '0b001' or '010100101'
        :return: ciphertext in binary base
        """

        # The case when plaintext <= 32bits
        # verifying if plain text is a python bin form
        if plain_text[:2] == '0b':
            diff = abs(34 - len(plain_text))  # diff variable to add zeros if necessary
            p_text = '0b' + '0' * diff + plain_text[2:]  # to mount plaintext in binary
        else:  # if the input is in the form 0111010101101
            diff = abs(32 - len(str(plain_text)))  # the difference between the input and 32 bits
            p_text = '0b' + '0' * diff + str(plain_text)  # mount a plaintext in binary

        self.present_cipher = xor(p_text, self.encrypted_chacha_M[self.key_order[0]][self.key_order[1]])
        self.historical_cipher.append(self.present_cipher)

        return self.present_cipher

    def generate_encrypted_matrix(self):
        # first chacha round
        self.encrypted_chacha_M = chacha_round(self.get_chacha_matrix())
        # range for remainig rounds
        for i in range(0, 10):
            self.encrypted_chacha_M = chacha_round(self.encrypted_chacha_M)
        # update the counter
        self.counter_update()
        # return encrypted matrix
        return self.encrypted_chacha_M

    def counter_update(self):
        add = bin(int(self.counter, 2) + 1)
        diff = abs(len(add) - 34)
        self.counter = '0b' + '0' * diff + add[2:]
        return self.counter

    def get_encrypted_matrix(self):
        return self.encrypted_chacha_M

    def get_chacha_matrix(self):
        """
        :return: The Matrix ready to chacha round (ready to generate a encrypted matrix from it) if the counter was
        updated it will be consider in this matrix
        """
        self.chacha_M = generate_chacha_matrix(self.key, self.counter, self.nonce[0],
                                               self.nonce[1], self.nonce[2], self.m_constant[0],
                                               self.m_constant[1], self.m_constant[2], self.m_constant[3])
        return self.chacha_M

    def get_status(self):
        print("Número da matrix encriptada gerada: ", self.n_matrix)
        print("Número de chaves que foram usadas da matrix atual")
        print("Encriptações feitas: ")
