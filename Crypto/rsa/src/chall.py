from Crypto.Util.number import *
from secret import flag
z = 567
p = getPrime(1024)
q = getPrime(1024)
n = p*q
c = pow(bytes_to_long(flag), 65537, n)
tot = (p-1) * (q-1)
d = int(pow(65537, -1, tot))
dinv = int(pow(d, -1, n))

h = int(dinv >> z)
hpq = (int((p+q)>> z))

with open('out.txt', 'w+') as f:
    f.write(f'{n=}\n')
    f.write(f'{h=}\n')
    f.write(f'{hpq=}\n')
    f.write(f'{c=}\n')
