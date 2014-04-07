from collections import deque
from itertools import repeat
from sys import version_info


class Trivium:
    def __init__(self, key, iv):
        """in the beginning we need to transform the key as well as the IV.
        Afterwards we initialize the state."""
        self.state0 = None
        self.state1 = None
        self.state2 = None
        self.counter = 0
        self.key = key  # self._setLength(key)
        self.iv = iv  # self._setLength(iv)

        # Initialize state
        init_list = list(map(int, list(self.key)))
        init_list += list(repeat(0, 20))
        self.state0 = deque(init_list)

        init_list = list(map(int, list(self.iv)))
        init_list += list(repeat(0, 4))
        self.state1 = deque(init_list)

        init_list = list(repeat(0, 108))
        init_list += list([1, 1, 1])
        self.state2 = deque(init_list)

        print(self.state0, len(self.state0))
        print(self.state1, len(self.state1))
        print(self.state2, len(self.state2))
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

        a_1 = self.state0[90] & self.state0[91]
        a_2 = self.state1[81] & self.state1[82]
        a_3 = self.state2[108] & self.state2[109]

        t_1 = self.state0[65] ^ self.state0[92]
        t_2 = self.state1[68] ^ self.state1[83]
        t_3 = self.state2[65] ^ self.state2[110]

        out = t_1 ^ t_2 ^ t_3

        s_1 = a_3 ^ self.state0[68] ^ t_3
        s_2 = a_1 ^ self.state1[77] ^ t_1
        s_3 = a_2 ^ self.state2[86] ^ t_2

        self.state0.rotate(1)
        self.state1.rotate(1)
        self.state2.rotate(1)

        self.state0[0] = s_1
        self.state1[0] = s_2
        self.state2[0] = s_3

        return out


def main():
    KEY = hex_to_bits("0F62B5085BAE0154A7FA")[::-1]
    IV = hex_to_bits("288FF65DC42B92F960C7")[::-1]
    trivium = Trivium(KEY, IV)

    # Check python version
    if version_info[0] == 2:
        next_key_bit = trivium.keystream().next
    elif version_info[0] == 3:
        next_key_bit = trivium.keystream().__next__
    else:
        print("invalid python version")
        return

    for i in range(1):
        keystream = []
        for j in range(128):
            keystream.append(next_key_bit())
        print(bits_to_hex(keystream))

# Convert strings of hex to strings of bytes and back, little-endian style
_allbytes = dict([("%02X" % i, i) for i in range(256)])


def _hex_to_bytes(s):
    return [_allbytes[s[i:i+2].upper()] for i in range(0, len(s), 2)]


def hex_to_bits(s):
    return [(b >> i) & 1 for b in _hex_to_bytes(s)
            for i in range(8)]


def bits_to_hex(b):
    return "".join(["%02X" % sum([b[i + j] << j for j in range(8)])
                    for i in range(0, len(b), 8)])


if __name__ == "__main__":
    main()
