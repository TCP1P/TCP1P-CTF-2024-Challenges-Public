#!/usr/bin/env python3
code = '''
import sys
import posix

__builtins__ = sys._getframe(0).f_builtins

for _ in unsafe_builtins:
    del __builtins__[_]
unsafe_builtins.clear()

posix.__dict__.clear()
sys.modules.clear()
for _ in sys.__dict__:
    sys.__dict__[_] = None

del sys, posix
'''

unsafe_builtins = []
unsafe_chars = 'FT!"#$%&\'()*+-,/;<=>?@\\^`{|}~0123456789\t\n\v '

for _ in __builtins__.__dict__:
    if not isinstance(__builtins__.__dict__[_], type):
        unsafe_builtins.append(_)
    elif _.startswith('_'):
        unsafe_builtins.append(_)
    elif _[0].islower():
        unsafe_builtins.append(_)

user_input = input('Enter code: ').strip()
for c in set(user_input):
    if c in unsafe_chars:
        assert 0, 'Unsafe character detected!'

assert len(user_input.split('\r')) < 3
assert user_input.isascii()
exec(code + user_input, {'unsafe_builtins': unsafe_builtins}, {})
