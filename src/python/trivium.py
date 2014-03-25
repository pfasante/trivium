from collections import deque
from itertools import repeat


class Trivium:
    def __init__(self, key, iv):
        """in the beginning we need to transform the key as well as the IV.
        Afterwards we initialize the state."""
        self.register = None
        self.counter = 0
        self.key = self._setLength(key)
        self.iv = self._setLength(iv)

        # Initialize state
        init_list = list(map(int, list(self.key)))
        init_list += list(repeat(0, 13))
        init_list += list(map(int, list(self.iv)))
        init_list += list(repeat(0, 4))
        init_list += list(repeat(0, 108))
        init_list += list([1, 1, 1])
        self.register = deque(init_list)

        # Do 4 full cycles, drop output
        for i in range(4*288):
            self._gen_keystream()

    def encrypt(self, message):
        """To be implemented?"""
        pass

    def decrypt(self, cipher):
        """To be implemented"""
        pass

    def keystream(self):
        """output keystream"""
        while self.counter < 2**64:
            self.counter += 1
            yield self._gen_keystream()

    def _setLength(self, input_data):
        """we cut off after 80 bits, alternatively we pad these with zeros."""
        input_data = "{0:080b}".format(input_data)
        if len(input_data) > 80:
            input_data = input_data[:(len(input_data)-81):-1]
        else:
            input_data = input_data[::-1]
        return input_data

    def _gen_keystream(self):
        """this method generates triviums keystream"""
        t_1 = self.register[65] ^ self.register[92]
        t_2 = self.register[161] ^ self.register[176]
        t_3 = self.register[242] ^ self.register[287]

        out = t_1 ^ t_2 ^ t_3

        t_1 = t_1 ^ (self.register[90] & self.register[91]) ^ self.register[170]
        t_2 = t_2 ^ (self.register[174] & self.register[175]) ^ self.register[263]
        t_3 = t_3 ^ (self.register[285] & self.register[287]) ^ self.register[68]

        self.register.rotate(1)

        self.register[0] = t_3
        self.register[93] = t_1
        self.register[177] = t_2

        return out


def main():

    KEY = 0xFFFFFFFFFFFFFFFFFFF0
    IV = 0xFFFFFFFFFFFFFFFFFFFF
    trivium = Trivium(IV, KEY)

    for i in range(8*4):
        print(trivium.keystream().next())

if __name__ == "__main__":
    main()
