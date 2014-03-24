import collections
import binascii
import itertools


reg_1 = None
reg_2 = None
reg_3 = None

def output():
    pass


def update_state():
    global reg_1
    global reg_2
    global reg_3

    t_1 = reg_1[65] ^ reg_1[92]
    t_2 = reg_2[67] ^ reg_2[82]
    t_3 = reg_3[64] ^ reg_3[109]
    
    out = t_1 ^ t_2 ^ t_3

    t_1 = t_1 ^ (reg_1[90] & reg_1[91]) ^ reg_2[76]
    t_2 = t_2 ^ (reg_2[80] & reg_2[81]) ^ reg_3[85]
    t_3 = t_3 ^ (reg_3[107] & reg_3[108]) ^ reg_1[68]

    # Shift by one to MSB
    reg_1.rotate(1)
    reg_2.rotate(1)
    reg_3.rotate(1)

    reg_1[0] = t_3
    reg_2[0] = t_1
    reg_3[0] = t_2

    return out


def init():
    global reg_1
    global reg_2
    global reg_3

    for i in range(4*288):
        update_state()


def main():
    global reg_1
    global reg_2
    global reg_3

    KEY = 0xFFFFFFFFFFFFFFFFFFF0
    use_key = bin(KEY)[2:82] # Cut off for 80 Bit
    use_key = use_key[::-1]  # Invert string
    IV = 0xFFFFFFFFFFFFFFFFFFFF
    use_iv = bin(IV)[2:82]
    use_iv = use_iv[::-1]
    # Transform key to binary list and append 13 Zeros
    reg_1 = collections.deque(map(int,list(use_key)) + list(itertools.repeat(0, 13))) #len 93
    reg_2 = collections.deque(map(int,list(use_iv)) + list(itertools.repeat(0, 4)))  # len 84
    reg_3 = collections.deque(list(itertools.repeat(0, 108)) + list([1,1,1]))  # len 111
    init()

    print reg_3
    print reg_2
    # Use /dev/urandom later

    for i in range(15):
        print update_state()

if __name__ == "__main__":
    main()