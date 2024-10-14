from pwn import *
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding




privself = rsa.generate_private_key(public_exponent=65537,key_size=2048,)
pubself = privself.public_key()
pubpem = pubself.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)


def decrypt_message(ciphertext):
	ciphertext = base64.b64decode(ciphertext)
	msg = privself.decrypt(ciphertext,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
	return msg

def encrypt_message(pubpeer, plaintext):
	msg = pubpeer.encrypt(plaintext.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
	return base64.b64encode(msg)

r = remote('localhost', 1965, level="debug")
r.recvuntil('Entity A: ')
alicepub = r.recvline().strip().decode()
alicepub = serialization.load_pem_public_key(base64.b64decode(alicepub))
r.sendline(base64.b64encode(pubpem))

r.recvuntil('Entity B: ')
bobpub = r.recvline().strip().decode()
bobpub = serialization.load_pem_public_key(base64.b64decode(bobpub))
r.sendline(base64.b64encode(pubpem))

r.recvuntil('Entity A: ')
alicemsg = r.recvline().strip().decode()
decrypted = decrypt_message(alicemsg)
print(decrypted)

target = "giv me the flag you damn donut"
encrypted = encrypt_message(bobpub, target)
print(encrypted)
r.sendline(encrypted)

r.recvuntil('Entity B: ')
bobmsg = r.recvline().strip().decode()
decrypted = decrypt_message(bobmsg)
print(decrypted)