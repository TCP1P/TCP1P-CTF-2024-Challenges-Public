from sage.all import *
from math import gcd
from pwn import xor
import time
from hashlib import sha512

n = 0x1cec7c3ff93ca538e71f334e83d905eabd894729a1b515b89dc2392036bc7e5d59fad2c35dbb0a8903c8bb2e9cd5e4779a92d3f361eb1ce9fa2530c47881a8719763f828360138373ffa2ce627f8ccad08e9b5ead178c614f7899adc6a14fa33aa2216c463a04041e78cffa2c68963c6ff422a076bedd32236282eb3bd1b7ba870a3b1c8f639cd536cba329b10a6cf7b4ef78bd11052ff8a0d432fb6d3b221742aa1da6914876e94aca5abdaeef30acdfc90cbc621245ad288a634e8bdf4152ea8ed0062c872ace7b4011dc5743fa9c424413f4e3e8fa5c5513fd4a711141f2ef68c01177f78945db623ac6cc762a6813f11cc278a143ea657bf309e281ef59048a29f279c9ad8b37f221ac06242f577bba985a2aaec051d95391a9681f905472f4e7d1322da492639ee4a5ac776a476cece55f9dfb782c1ef869deed2226691d3157fbb6b131968ebfb1fe5bc1e44a158f1e2321c001355cc9cb3344f6b09b78d965a807cd60d58a9efbab8c6d4f75c8e5ac7c9cf0e5409b55bb2133129272685913be02166c6bffe3747ccd186b6c26fc9f09
ct = "43edcf6275293ce97d716f49875c4bdba37f6ab30f15a53f09b72bf3816edf6b92618fb56d569d911b2f6fe7a36d4a854022dddf671dc89b4800bc1605822aab72d3" 
x = -51 
start_time = time.time()
xs = Mod(x, n).nth_root(51, all=True)
end_time = time.time()
print(end_time-start_time)
for x in xs:
    L = Matrix([[n, 0], [Integer(x), 1]])
    L = L.LLL()
    a = abs(L[0][0]) 
    b = abs(L[0][1])
    if gcd(51*b, a**51 + 51*b**51) == 1 and a**51 + 51*b**51 == n:
        print(a,b)
        print(xor(bytes.fromhex(ct),sha512((str(a)+str(b)).encode()).digest()))

