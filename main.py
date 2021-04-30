from mchacha.chacha_operations import *
from mchacha.constants import *


# Funcionando
def generate_key_stream(matrix):
    """ :param: The first matrix
        :return: The key stream based on chacha algorithm
    """
    M = matrix
    for i in range(0, 10):
        M = chacha_round(M)

    return M, [key for l in M for key in l]


# Funcionando
def my_join(x):
    """
    :param x: -> the list desired to join
    :return:
    """
    return ''.join(x)


# Funcionando
def counter_update(counter):
    c = counter
    add = bin(int(c, 2) + 1)
    diff = abs(len(add) - 34)
    c = '0b' + '0' * diff + add[2:]
    return c


# Funcionando
def generate_initial_keystream(key=None, nonce=None):
    """
    :param key:
    :param nonce:
    :return: The initial keystream
    """

    # verifying if key is None
    if key is None:
        if key is None:
            key1 = KEY
        else:
            key1 = key

    # verifiying if nonce is None
    if nonce is None:
        n0, n1, n2 = NONCE0, NONCE1, NONCE2
    else:
        n0, n1, n2 = nonce[0], nonce[1], nonce[1]

    # setting counter
    local_counter = '0b' + '0' * 32
    # keystream variable
    keystream = ''

    for i in range(0, 3):
        # generate initial matrix
        m_1 = generate_chacha_matrix(key1, local_counter, n0, n1, n2, C0, C1, C2, C3)

        # generate keystream matrix
        k1 = generate_key_stream(m_1)[0]

        # concatenate all elements of matrix
        keystream = keystream + ''.join(list(map(my_join, k1))).replace("0b", "")
        local_counter = counter_update(local_counter)

    return '0b' + keystream


# FALTA FAZER UMA ATUALIZAÇÃO DE CHAVE
def update_key(current_key, counter, nonce=None, c0=None, c1=None, c2=None, c3=None):
    return 0


# Funcionando aparentemente
def event_cd(u0, u1, k, ep=None, en=None, cd=True):
    """
    Entrega os eventos no processo de encriptação decriptação
    :param ep: evento proibido
    :param u0:-> leitura anterior
    :param u1:-> leitura atual
    :param k: -> chave atual
    :param e_n: -> evento nulo
    :param cd: -> escolhe o modo de cifragem ou decifragem
    :return: tupla (evento em binário e evento em forma de lista)
    """
    if en is None:
        en = [0, 0, 0, 0, 0]
    if ep is None:
        ep = [1, 1, 1, 1, 1]

    u_0 = '0b' + ''.join(map(str, u0))
    u_1 = '0b' + ''.join(map(str, u1))
    e_p = '0b' + ''.join(map(str, ep))
    e_n = '0b' + ''.join(map(str, en))

    if not cd:
        aux = e_p
        e_p = e_n
        e_n = aux

    if u_0 == u_1:
        return [0] * len(u0), '0b' + ''.join(map(str, [0] * len(u0)))

    # definindo evento de entrada
    e_0 = xor(u_0, u_1)  # vemos a mudança na leitura dos sensores
    print('evento 0', e_0)
    e_1 = xor(e_0, k)  # evento cifrado
    if e_n == e_1:
        return list(map(int, xor(e_p, k)[-len(u0):])), '0b' + xor(e_p, k)[-len(u0):]
    else:
        return list(map(int, e_1[-len(u0):])), '0b' + e_1[-len(u0):]


# Funcionando aparentemente
def get_cipher(u0, u1, c0, k, ep=None, en=None):
    c_0 = '0b' + ''.join(map(str, c0))
    if en is None:
        en = [0, 0, 0, 0, 0]
    if ep is None:
        ep = [1, 1, 1, 1, 1]
    e_cif = event_cd(u0, u1, k, ep, en)[1]
    print('e_cif', e_cif)
    return [list(map(int, xor(e_cif, c_0)[-len(u0):])), '0b' + xor(e_cif, c_0)[-len(u0):]]


# Funcionando aparentemente
def get_plain(u0, u1, c0, k, ep=None, en=None):
    c_0 = '0b' + ''.join(map(str, c0))
    if en is None:
        en = [0, 0, 0, 0, 0]
    if ep is None:
        ep = [1, 1, 1, 1, 1]
    e_cif = event_cd(u0, u1, k, ep, en,cd=False)[1]
    print('e_cif', e_cif)
    return [list(map(int, xor(e_cif, c_0)[-len(u0):])), '0b' + xor(e_cif, c_0)[-len(u0):]]


if __name__ == "__main__":
    ks = generate_initial_keystream()
    counter1 = bit_sum(1, 2)
    print(ks)
    print(len(ks[2:]))

    U0 = [1, 0, 1, 1, 1]
    U1 = [1, 1, 0, 0, 1]

    cipher = get_cipher(U0, U1, U0, ks[:7])
    print(cipher)
    plain = get_plain(U0,[1,0,1,1,0],U0,ks[:7])
    print(plain)
