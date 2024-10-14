#!/usr/bin/env python2.7
from string import letters, digits, whitespace

banned = letters + digits + whitespace + '!"#$&+./;=>?@\\^_{|}'
code = raw_input('>>> ')

for char in set(code):
    if char in banned:
        exit()

assert len(code) < 12000
__builtins__.__dict__.clear()

try:
    _global = {'__builtins__': None}
    exec('exec %s' % code, _global, _global)
except:
    pass
