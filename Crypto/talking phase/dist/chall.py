import random
import time
import base64
from messages import *
from secret import flag
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class Entity:
	def __init__(self, name):
		self.name = name
		self.privself = None
		self.pubself = None
		self.pubpeer = None
		self.crypt_init()

	def checkflag(self, message):
		if message == b"giv me the flag you damn donut":
			return True
		else:
			return False

	def crypt_init(self):
		self.privself = rsa.generate_private_key(public_exponent=65537,key_size=2048,)
		self.pubself = self.privself.public_key()

	def send_key(self, receiver):
		pubpem = base64.b64encode(self.pubself.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)).decode()
		receiver.receive_key(self, pubpem)

	def send_key_too(self, receiver):
		pubpem = base64.b64encode(self.pubself.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)).decode()
		receiver.receive_key_too(self, pubpem)

	def receive_key(self, sender, key):
		try:
			self.pubpeer = serialization.load_pem_public_key(base64.b64decode(key))
			self.send_key_too(sender)
		except:
			print("[!] Error, Shutting down...")
			exit()

	def receive_key_too(self, sender, key):
		try:
			self.pubpeer = serialization.load_pem_public_key(base64.b64decode(key))
			return
		except:
			print("[!] Error, Shutting down...")
			exit()

	def encrypt_message(self, plaintext):
		msg = self.pubpeer.encrypt(plaintext.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
		return base64.b64encode(msg)


	def decrypt_message(self, ciphertext):
		ciphertext = base64.b64decode(ciphertext)
		msg = self.privself.decrypt(ciphertext,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
		return msg

	def send_message(self, receiver, message):
		time.sleep(random.uniform(0.5, 1.5))
		encrypted_message = self.encrypt_message(message).decode()
		receiver.receive_message(self, encrypted_message)

	def receive_message(self, sender, message):
		try:
			decrypted_message = self.decrypt_message(message)
			if self.checkflag(decrypted_message):
				msg_sent = flag
			else:
				msg_sent = random.choice(message_choice)

			self.send_message(sender, msg_sent)
		except:
			print("[!] Error, Shutting down...")
			exit()


class Attacker:
	def __init__(self, entityone, entitytwo):
		self.entityone = entityone
		self.entitytwo = entitytwo

	def relay_message(self, receiver, message):
		receiver.receive_message(self, message)

	def receive_message(self, sender, message):
		print(f"{sender.name}: {message}")
		tamp = input(f"{sender.name} (tamper): ")
		if tamp == "fwd":
			msg_sent = message
		else:
			msg_sent = tamp.encode()

		if sender == self.entityone:
			self.relay_message(self.entitytwo, msg_sent)
		elif sender == self.entitytwo:
			self.relay_message(self.entityone, msg_sent)

	
	def relay_key(self, receiver, key):
		receiver.receive_key(self, key)

	def relay_key_too(self, receiver, key):
		receiver.receive_key_too(self, key)

	def receive_key(self, sender, key):
		print(f"{sender.name}: {key}")
		tamp = input(f"{sender.name} (tamper): ")
		if tamp == "fwd":
			key_sent = key
		else:
			key_sent = tamp.encode()

		if sender == self.entityone:
			self.relay_key(self.entitytwo, key_sent)
		elif sender == self.entitytwo:
			self.relay_key(self.entityone, key_sent)

	def receive_key_too(self, sender, key):
		print(f"{sender.name}: {key}")
		tamp = input(f"{sender.name} (tamper): ")
		if tamp == "fwd":
			key_sent = key
		else:
			key_sent = tamp

		if sender == self.entityone:
			self.relay_key_too(self.entitytwo, key_sent)
		elif sender == self.entitytwo:
			self.relay_key_too(self.entityone, key_sent)


entity_a = Entity("Entity A")
entity_b = Entity("Entity B")
entity_c = Attacker(entity_a, entity_b)


def begin_communication():
	while True:
		entity_a.send_key(entity_c)
		entity_a.send_message(entity_c, random.choice(message_choice))

begin_communication()