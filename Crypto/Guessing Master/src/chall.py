import math
import os
from Crypto.Random import random

def bin2hex(binary):
    return hex(int(binary,2))[2:]

def hex2bin(msg):
    return bin(int(msg, 16))[2:]

def count_bit(data_length):
    i = 0
    while (1 << i) - 1 < i + data_length:
        i += 1
    return i

def flip_bit(binary, index):
    return binary[:index] + ('1' if binary[index] == '0' else '0') + binary[index+1:]

def add_bit(index, data):
    output = 0
    length = len(data) + count_bit(len(data)) + 1
    for i in range(1, length):
        if (i & (i - 1)) != 0 and (i >> (index - 1)) & 1:
            output ^= int(data[i - math.ceil(math.log2(i)) - 1])
    return str(output)

def random_flip(binary):
    binary = binary[::-1]
    length = len(binary) + count_bit(len(binary)) + 1
    encoded = ""
    index = 0
    for i in range(1, length):
        if math.log2(i) % 1 == 0: 
            bit = add_bit(int(math.log2(i)) + 1, binary)
            encoded += bit
        else:
            encoded += binary[index]
            index += 1
    rand = random.randrange(0, len(encoded))
    flipped = flip_bit(encoded, rand)
    return flipped[::-1], rand

def main():
    flag = open("flag.txt", "rb").read()
    binarys = hex2bin(flag.hex())
    output = []
    for binary in binarys:
        temp = hex2bin(os.urandom(16).hex())
        encoded, rand = random_flip(temp)
        if int(binary):
            output.append([bin2hex(encoded), rand])
        else:
            output.append([bin2hex(encoded), random.randrange(0, len(encoded))])
    print(output)

if __name__ == "__main__":
    main()