#!/usr/bin/env python3
import regex
import glob
import sys

exception_groups = (Warning, SystemExit, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError, KeyboardInterrupt, ConnectionError, ResourceWarning, TypeError, BytesWarning, OverflowError, TabError, InterruptedError, RuntimeError, TimeoutError, FileNotFoundError, UserWarning, GeneratorExit, PermissionError, KeyError, AssertionError, UnicodeDecodeError, IsADirectoryError, ZeroDivisionError, FileExistsError, BlockingIOError, SystemError, OSError, EOFError, EncodingWarning, StopIteration, UnicodeWarning, ImportWarning, SyntaxWarning, LookupError, AttributeError, ImportError, ArithmeticError, EnvironmentError, ChildProcessError, UnicodeTranslateError, UnicodeEncodeError, RecursionError, StopAsyncIteration, RuntimeWarning, IndentationError, ValueError, ModuleNotFoundError, DeprecationWarning, BufferError, FutureWarning, ReferenceError, MemoryError, UnicodeError, PendingDeprecationWarning, NotADirectoryError, IOError, FloatingPointError, ProcessLookupError, NameError, NotImplementedError, UnboundLocalError, BrokenPipeError, IndexError)
secret_of_trades = glob.glob('flags/*')

re_pattern = regex.compile(r'[ad-z]+\(((?R)|)\)')
user_input = input('>>> ')

sys.stderr = sys.stdout
sys.stdout = None
sys.stdin = None

if re_pattern.fullmatch(user_input):
    try:
        exec(user_input)
    except exception_groups as e:
        pass
