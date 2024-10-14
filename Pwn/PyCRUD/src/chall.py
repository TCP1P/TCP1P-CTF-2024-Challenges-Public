#!/usr/bin/env python3

import ctypes
import sys

MAX_NOTES = 16
libc = ctypes.CDLL("libc.so.6")
notes = [0 for _ in range(MAX_NOTES)]


def create_note():
    index = int(input("Index: "))
    print("Content: ", end="", flush=True)
    data = sys.stdin.buffer.readline()[:-1]
    size = len(data)
    content = ctypes.create_string_buffer(data, size)
    notes[index] = libc.malloc(size)
    ctypes.memmove(notes[index], content, size)


def view_note():
    index = int(input("Index: "))
    if notes[index] == 0:
        print("Note does not exist")
        return
    sys.stdout.buffer.write(ctypes.string_at(notes[index]))
    print()


def edit_note():
    index = int(input("Index: "))
    if notes[index] == 0:
        print("Note does not exist")
        return
    print("Content: ", end="", flush=True)
    data = sys.stdin.buffer.readline()[:-1]
    size = len(data)
    content = ctypes.create_string_buffer(data, size)
    ctypes.memmove(notes[index], content, size)


def delete_note():
    index = int(input("Index: "))
    if notes[index] == 0:
        print("Note does not exist")
        return
    libc.free(notes[index])
    notes[index] = 0


if __name__ == "__main__":
    while True:
        print("1. Create note")
        print("2. Edit note")
        print("3. View note")
        print("4. Delete note")
        print("5. Exit")
        option = int(input(">> "))
        if option == 1:
            create_note()
        elif option == 2:
            edit_note()
        elif option == 3:
            view_note()
        elif option == 4:
            delete_note()
        elif option == 5:
            break
