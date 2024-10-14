from Crypto.Util.Padding import pad
from aes import AES
from secret import flag
import os

c = AES(os.urandom(16))

admin_id = os.urandom(8).hex().encode()
enc_id = c.encrypt(admin_id)

print(f"Encrypted ID: {enc_id.hex()}")

while True:
    print("1. Encrypt")
    print("2. Admin Login")
    print("3. Exit")
    choice = int(input(">> "))
    if choice == 1:
        msg = input("message: ").encode()
        msg = pad(msg, 16)
        msg_block = [msg[i:i+16] for i in range(0, len(msg), 16)]
        ct_block = []
        for m in msg_block:
            ct_block.append(c.encrypt(m))
        print("Encrypted:", b''.join(ct_block).hex())
    elif choice == 2:
        id = input("Enter ID: ")
        if id.encode() == admin_id:
            print("Welcome Admin!")
            print(flag)
        else:
            print("Invalid ID")
    elif choice == 3:
        break
    else:
        print("Invalid Choice")
