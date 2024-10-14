def flip_bit(binary, index):
    return binary[:index] + ('1' if binary[index] == '0' else '0') + binary[index+1:]

def bin2hex(binary):
    return hex(int(binary,2))[2:]

def hex2bin(msg):
    return bin(int(msg, 16))[2:]

def bit_count(length):
    i = 0
    while (1 << i) - 1 < i + length:
        i += 1
    return i

def add_bit(index, encoded):
    output = 0
    for i in range(1, len(encoded) + 1):
        if (i >> (index - 1)) & 1: 
            output ^= int(encoded[i - 1])
    return output

def flipped_bit(encoded):
    binary = encoded[::-1]
    length = len(binary)
    parity_count = bit_count(length)
    flipped = 0
    for p in range(parity_count):
        bit = add_bit(p + 1, binary)
        flipped |= bit << p
    return flipped-1

r = eval(open("output.txt", "r").read())

flag = ""
for arr in r:
    temp, cek = arr
    flipped = flipped_bit(hex2bin(temp))
    if flipped == cek:
        flag += "1"
    else: 
        flag += "0"

print(bytes.fromhex(hex(int(flag,2))[2:]))

    