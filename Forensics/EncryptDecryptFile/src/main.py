import argparse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

key = bytes.fromhex('00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff')
iv = bytes.fromhex('0102030405060708090a0b0c0d0e0f10')

BLOCK_SIZE = 16

def encrypt_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        plaintext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)

    padded_plaintext = pad(plaintext, BLOCK_SIZE)
    ciphertext = cipher.encrypt(padded_plaintext)

    with open(output_file, 'wb') as f:
        f.write(ciphertext)

    print(f'File encrypted successfully and saved as {output_file}')

def decrypt_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted_data = cipher.decrypt(ciphertext)
    plaintext = unpad(decrypted_data, BLOCK_SIZE)

    with open(output_file, 'wb') as f:
        f.write(plaintext)

    print(f'File decrypted successfully and saved as {output_file}')

def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt a file using AES-256-CBC.")
    parser.add_argument('--encrypt', action='store_true', help="Encrypt the file.")
    parser.add_argument('--decrypt', action='store_true', help="Decrypt the file.")
    parser.add_argument('--input', type=str, required=True, help="Input file path.")
    parser.add_argument('--output', type=str, required=True, help="Output file path.")

    args = parser.parse_args()

    if args.encrypt:
        encrypt_file(args.input, args.output)
    elif args.decrypt:
        decrypt_file(args.input, args.output)
    else:
        print("Please specify --encrypt or --decrypt.")

if __name__ == "__main__":
    main()
