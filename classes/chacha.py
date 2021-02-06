from binaryfunctions.binoperations import *
from mchacha.chacha_operations import *

class ChachaEncrypt():
    def __init__(self, key, nonce=[generate_key(32+i-i) for i in range(0,3)]):
        self.m_constant = [generate_key(32+n-n) for n in range(0,4)]
        self.key = key
        self.nonce = nonce
        self.counter = '0b'+'0'*32
        self.chacha_M = generate_chacha_matrix(self.key,self.counter,self.nonce[0],
                                               self.nonce[1],self.nonce[2], self.m_constant[0],
                                               self.m_constant[1],self.m_constant[2],self.m_constant[3])
        self.encrypted_chacha_M = []
        self.n_round = 0

    def __str__(self):
        print(self.chacha_M)

    def generate_round(self):
        self.encrypted_chacha_M = chacha_round(self.chacha_M)

        for i in range(0,10):
            self.encrypted_chacha_M = chacha_round(self.encrypted_chacha_M)
        return self.encrypted_chacha_M

    def get_encrypted_matrix(self):
        return self.encrypted_chacha_M

    def get_chacha_matrix(self):
        return self.chacha_M

    def get_status(self):
        print("")