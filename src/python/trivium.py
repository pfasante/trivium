from collections import deque
from itertools import repeat
from sys import version_info


class Trivium:
    def __init__(self, key, iv):
        """in the beginning we need to transform the key as well as the IV.
        Afterwards we initialize the state."""
        self.state = None
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
        self.state = deque(init_list)

        # Do 4 full cycles, drop output
        for i in range(4*288):
            self._gen_keystream()

    def encrypt(self, message):
        """To be implemented"""
        pass

    def decrypt(self, cipher):
        """To be implemented"""
        pass

    def keystream(self):
        """output keystream
        only use this when you know what you are doing!!"""
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
        t_1 = self.state[65] ^ self.state[92]
        t_2 = self.state[161] ^ self.state[176]
        t_3 = self.state[242] ^ self.state[287]

        out = t_1 ^ t_2 ^ t_3

        t_1 = t_1 ^ (self.state[90] & self.state[91]) ^ self.state[170]
        t_2 = t_2 ^ (self.state[174] & self.state[175]) ^ self.state[263]
        t_3 = t_3 ^ (self.state[285] & self.state[286]) ^ self.state[68]

        self.state.rotate(1)

        self.state[0] = t_3
        self.state[93] = t_1
        self.state[177] = t_2

        return out


def main():

    KEY = 0xFFFFFFFFFFFFFFFFFFF0
    IV = 0xFFFFFFFFFFFFFFFFFFFF
    trivium = Trivium(IV, KEY)

    for i in range(8*4):
        if version_info[0] == 3:
            print(trivium.keystream().__next__())
        elif version_info[0] == 2:
            print(trivium.keystream().next())


if __name__ == "__main__":
    main()
