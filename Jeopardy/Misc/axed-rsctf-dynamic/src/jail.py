#!/usr/bin/env python2.7
import re

code = raw_input('>>> ')
banned = '!"#$%&\'+*-/\\;<>?@^`~=|}{()0123456789'

if re.findall('(print)|(exec)|[%s]' % re.escape(banned), code):
    exit('try again')
assert code.islower()

try:
    __builtins__.__dict__.clear()
    _global = {'__builtins__': None, '_': __builtins__}
    exec(code, _global, _global)
except:
    pass
