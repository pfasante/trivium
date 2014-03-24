from collections import deque
from itertools import repeat


register = None
counter = 0


def output():
    pass


def trivium(iv, key):
    global register
    global counter

    use_key = "{0:080b}".format(key)  # print key in binary
    if len(use_key) > 80:  # reverse string and cut off 80b
        use_key = use_key[:(len(use_key)-81):-1]
    else:
        use_key = use_key[::-1]

    use_iv = "{0:080b}".format(iv)  # print iv in binary
    if len(use_iv) > 80:  # reverse string and cut off 80b
        use_iv = use_iv[:(len(use_iv)-81):-1]
    else:
        use_iv = use_iv[::-1]

    # len 93
    init_list = list(map(int, list(use_key)))
    init_list += list(repeat(0, 13))
    init_list += list(map(int, list(use_iv)))
    init_list += list(repeat(0, 4))
    init_list += list(repeat(0, 108))
    init_list += list([1, 1, 1])
    register = deque(init_list)

    # init state
    for i in range(4*288):
        t_1 = register[65] ^ register[92]
        t_2 = register[161] ^ register[176]
        t_3 = register[242] ^ register[287]

        t_1 = t_1 ^ (register[90] & register[91]) ^ register[170]
        t_2 = t_2 ^ (register[174] & register[175]) ^ register[263]
        t_3 = t_3 ^ (register[285] & register[287]) ^ register[68]

        register.rotate(1)

        register[0] = t_3
        register[93] = t_1
        register[177] = t_2

    # output keystream
    while counter < 2**64:
        t_1 = register[65] ^ register[92]
        t_2 = register[161] ^ register[176]
        t_3 = register[242] ^ register[287]

        out = t_1 ^ t_2 ^ t_3

        t_1 = t_1 ^ (register[90] & register[91]) ^ register[170]
        t_2 = t_2 ^ (register[174] & register[175]) ^ register[263]
        t_3 = t_3 ^ (register[285] & register[287]) ^ register[68]

        register.rotate(1)

        register[0] = t_3
        register[93] = t_1
        register[177] = t_2

        yield out


def main():

    KEY = 0xFFFFFFFFFFFFFFFFFFF0
    IV = 0xFFFFFFFFFFFFFFFFFFFF
    keystream = trivium(IV, KEY)

    for i in range(8*4):
        print(keystream.__next__())

if __name__ == "__main__":
    main()
