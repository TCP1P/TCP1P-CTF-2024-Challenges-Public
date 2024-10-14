#!/usr/bin/python3
from pycparser import c_parser, c_ast, plyparser
from base64 import b64decode

import re
import os
import hashlib
import subprocess

BLACKLIST = [
    # I/O Operations
    "open", "openat", "fopen", "fopen64", "freopen", "freopen64",
    "read", "pread", "readv", "preadv", "write", "pwrite", "writev", "pwritev",
    "fgets", "fgetws", "fread", "fwrite", "fscanf", "fwscanf", "scanf", "wscanf",
    "sscanf", "swscanf", "getline", "getdelim", "fread_unlocked", "fwrite_unlocked",
    "getchar", "putchar", "getwc", "putwc", "memcpy", "strcpy", "strncpy", "strcat",
    "strncat", "sprintf", "snprintf", "truncate", "ftruncate", "chdir", "mkdir",
    "rmdir", "readdir", "link", "symlink", "readlink", "mknod",
    "fdatasync", "sync", "rename", "renameat", "renameat2",
    "fallocate", "posix_fadvise", "readlinkat", "faccessat", "faccessat2",
    "sendfile", "splice", "tee", "vmsplice", "copy_file_range",
    "preadv", "pwritev", "preadv2", "pwritev2",
    "statx", "name_to_handle_at", "open_by_handle_at",
    "openat2", "close_range",
    "nftw", "ftw",
    
    # Process Management
    "fork", "vfork", "execve", "execvp", "execv", "execl", "execle", "clone", "clone3",
    "setsid", "setpgid", "setpgrp", "kill", "wait", "waitpid", "waitid",
    "prlimit", "prlimit64",
    "sched_setscheduler", "sched_setparam", "setresuid", "setreuid", "setresgid",
    "setregid", "setrlimit", "getrlimit", "getpid", "getppid", "getuid", "geteuid",
    "getgid", "getegid", "sysinfo", "uname", "ptrace", "popen", "killpg",
    "prctl", "nice", "setpriority", "sched_yield", "sched_get_priority_max",
    "sched_get_priority_min", "sched_rr_get_interval",
    "sched_setaffinity", "sched_getaffinity", "sched_setscheduler", "sched_getscheduler",
    "sched_setparam", "sched_getparam",
    "getrusage", "times", "getitimer", "setitimer",
    "exit_group", "set_tid_address", "gettid",
    "sched_setattr", "sched_getattr",
    "pidfd_open", "pidfd_send_signal", "pidfd_getfd", "process_mrelease",
    "execveat",
    
    # Memory Management
    "mmap", "mprotect", "munmap", "brk", "sbrk", "mlock", "munlock", "madvise",
    "shmat", "shmdt", "shmctl", "shmget", "semctl", "semget", "semop",
    "remap_file_pages", "mremap", "mincore", "mlock2",
    "pkey_mprotect", "pkey_alloc", "pkey_free",
    "mbind", "set_mempolicy", "get_mempolicy", "migrate_pages",
    "process_madvise", "userfaultfd", "membarrier",
    "process_vm_readv", "process_vm_writev",
    
    # Network and IPC
    "socket", "bind", "listen", "accept", "connect", "send", "recv", "sendto",
    "recvfrom", "sendmsg", "recvmsg", "getsockopt", "setsockopt", "ioctl",
    "epoll_ctl", "epoll_wait", "eventfd", "socketpair", "mkfifo",
    "sethostname", "setdomainname", "gethostname", "getdomainname",
    "msgget", "msgsnd", "msgrcv", "msgctl",
    "accept4", "recvmmsg", "sendmmsg", "ethernet_multicast_join", "ethernet_multicast_leave",
    
    # System Calls and Kernel Interfaces
    "syscall", "io_submit", "io_getevents", "syslog", "system",
    "seccomp_init", "seccomp_rule_add", "seccomp_load", "seccomp_release",
    "sysctl", "sysfs",
    "reboot", "acct", "iopl", "ioperm", "modify_ldt", "create_module",
    "get_kernel_syms", "query_module", "nfsservctl", "getpmsg", "putpmsg",
    "afs_syscall", "tuxcall", "security",
    "init_module", "finit_module", "delete_module",
    "kexec_load", "kexec_file_load",
    "bpf", "perf_event_open",
    
    # File Descriptors and I/O
    "dup", "dup2", "dup3", "fcntl", "fileno", "flock", "lseek",
    "pread64", "pwrite64", "readahead", "sync_file_range",
    "io_setup", "io_destroy", "io_submit", "io_cancel", "io_getevents",
    "epoll_create1", "timerfd_create", "timerfd_settime", "timerfd_gettime",
    "io_uring_setup", "io_uring_enter", "io_uring_register",
    
    # Environment and Security
    "setenv", "unsetenv", "putenv", "getenv", "chroot",
    "capset", "capget",
    "seccomp",
    "cap_get_proc", "cap_set_proc", "cap_from_text", "cap_to_text",
    "security_getenforce", "security_setenforce",
    
    # Signal Handling
    "signal", "sigaction", "sigprocmask", "sigpending", "sigsuspend",
    "tgkill", "tkill", "sigqueue", "sigtimedwait", "sigwaitinfo",
    "rt_sigaction", "rt_sigprocmask", "rt_sigpending", "rt_sigsuspend", "rt_sigtimedwait",
    "rt_sigqueueinfo", "rt_tgsigqueueinfo",
    "sigaltstack", "rt_sigreturn",
    
    # User and Group Management
    "setuid", "setgid", "seteuid", "setegid", "setgroups", "getgroups",
    "setresuid", "setresgid", "setregid", "initgroups", "getresuid", "getresgid",
    
    # Dynamic Loading
    "dlopen", "dlsym", "dlclose", "dlerror", "dlinfo",
    
    # Time-related functions
    "settimeofday", "adjtimex", "clock_settime", "clock_gettime", "clock_getres",
    "clock_nanosleep", "timer_create", "timer_settime", "timer_gettime", "timer_delete",
    "timer_getoverrun",
    
    # Namespace manipulation
    "unshare", "setns",
    
    # Audit system
    "audit_write", "audit_read",
    
    # Extended attributes
    "setxattr", "lsetxattr", "fsetxattr", "getxattr", "lgetxattr", "fgetxattr",
    "listxattr", "llistxattr", "flistxattr", "removexattr", "lremovexattr", "fremovexattr",
    
    # File system operations
    "mount", "umount", "umount2", "pivot_root", "swapon", "swapoff",
    "syncfs", "fsmount", "fsopen", "fsconfig", "fspick",
    "open_tree", "move_mount",
    
    # Tracing and debugging
    "strace", "ltrace",
    
    # Asynchronous I/O
    "aio_read", "aio_write", "lio_listio",
    
    # Shared memory
    "shm_open", "shm_unlink",
    
    # Message queues
    "mq_open", "mq_close", "mq_unlink", "mq_send", "mq_receive", "mq_getattr", "mq_setattr",
    "mq_notify", "mq_timedreceive", "mq_timedsend",
    
    # Keyring functions
    "add_key", "request_key", "keyctl",
    
    # Filesystem quotas
    "quotactl", "quotactl_fd",
    
    # Lightweight process (thread) operations
    "set_robust_list", "get_robust_list", "futex", "futex_waitv", "futex_wake",
    
    # Virtualization-related calls
    "kvm", "vfio",
    
    # Extended Berkeley Packet Filter (eBPF) related
    "bpf_map_create", "bpf_map_lookup_elem", "bpf_map_update_elem", "bpf_map_delete_elem",
    "bpf_prog_load", "bpf_object__open", "bpf_object__load",
    
    # Newer IPC mechanisms
    "memfd_create", "memfd_secret",
    
    # File change monitoring
    "inotify_init", "inotify_add_watch", "inotify_rm_watch", "fanotify_init", "fanotify_mark",
    
    # Miscellaneous
    "getcpu", "kcmp", "getrandom",
    "rseq", "io_pgetevents",
    "cgroup_init", "cgroup_create_cgroup", "cgroup_delete_cgroup",
    "gethostbyname", "gethostbyaddr", "gethostbyname2", "getservbyname", "getservbyport",
    "getprotobyname", "getprotobynumber", "getnetbyname", "getnetbyaddr",
    "cachestat", "fchmodat2", "map_shadow_stack",
    
    # Container and namespace related
    "mount_setattr",
    
    # Landlock LSM
    "landlock_create_ruleset", "landlock_add_rule", "landlock_restrict_self",
    
    # Memory policy
    "set_mempolicy_home_node",
    
    # Architecture-specific calls (x86)
    "vm86",

    # ASM Inline
    "asm", "__asm__", "_asm",
]

def md5(s):
    return hashlib.md5(s.encode()).hexdigest()

def clean(s):
    return s.replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '').replace('\x0b', '').replace('\x0c', '')

def even_more_clean(s):
    return re.sub(r'[^a-zA-Z0-9.]', '', s)

def check_for_inline_assembly(code):
    if re.search(r'(__asm__|asm)(\s+volatile)?\s*\(', code):
        return True
    
    if re.search(r':\s*"=\w+"', code):
        return True
    
    if re.search(r'\b(?:__asm|_asm|asm)\s*{', code):
        return True
    
    return False

class SandboxVisitor(c_ast.NodeVisitor):
    def __init__(self, blacklist):
        self.blacklist = set(blacklist)

    def visit_ID(self, node):
        if node.name in self.blacklist:
            print(f"No!")
            exit()

code = input("Enter C code (in base64): ").encode()
try:
    code = b64decode(code).decode().replace('\r', '')
except:
    print("Invalid base64 code!")
    exit()

if len(code) > 512:
    print("Code is too long!")
    exit()

print()

if check_for_inline_assembly(code):
    print("No!")
    exit()

preprocessor_directives_count = 0
parsed_code = ""
for line in code.split("\n"):
    line = clean(line)

    if 'flag.txt' in even_more_clean(line):
        print(f"No!")
        exit()
    else:
        if '#' in line:
            for blacklisted in BLACKLIST:
                if blacklisted in line:
                    print(f"No!")
                    exit()
            preprocessor_directives_count += 1
        else:
            parsed_code += line + "\n"

if preprocessor_directives_count > 1:
    print("Too many preprocessor directive!")
    exit()

parsed_code = """
int run() {
""" + parsed_code + """
    return 0;
}"""

parser = c_parser.CParser()
try:
    ast = parser.parse(parsed_code)

    visitor = SandboxVisitor(BLACKLIST)
    visitor.visit(ast)

    final_code = """// CJ Generated Code
#include <stdio.h>
#include <stdlib.h>
#include <seccomp.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/prctl.h>

void init() {
    scmp_filter_ctx ctx;

    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) == -1) {
        perror("prctl(PR_SET_NO_NEW_PRIVS)");
        exit(EXIT_FAILURE);
    }

    ctx = seccomp_init(SCMP_ACT_ALLOW);
    if (ctx == NULL) {
        perror("seccomp_init");
        exit(EXIT_FAILURE);
    }

    seccomp_arch_add(ctx, SCMP_ARCH_NATIVE);

    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execveat), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(fork), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(vfork), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(clone), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(ptrace), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(socket), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(connect), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(accept), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(accept4), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(bind), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(listen), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(mmap), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(mprotect), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(openat), 1,
                     SCMP_A2(SCMP_CMP_MASKED_EQ, O_CREAT, O_CREAT));
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(open), 1,
                     SCMP_A2(SCMP_CMP_MASKED_EQ, O_CREAT, O_CREAT));

    if (seccomp_load(ctx) < 0) {
        perror("seccomp_load");
        seccomp_release(ctx);
        exit(EXIT_FAILURE);
    }

    seccomp_release(ctx);
}

int run() {
""" + code + """
    return 0;
}

int main() {
    init();
    run();
    return 0;
}
    """

    hash_code = md5(code)

    with open("/tmp/" + hash_code + ".c", "w") as f:
        f.write(final_code)

    try:
        result = subprocess.run(
            ["gcc", "/tmp/" + hash_code + ".c", "-o", "/tmp/" + hash_code, "-lseccomp"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        if result.stdout:
            print(result.stdout.decode('latin1'), end='')
        
        if result.stderr:
            print(result.stderr.decode('latin1'), end='')
        
        os.chmod("/tmp/" + hash_code, 0o777)
        
        result = subprocess.run(
            ["/tmp/" + hash_code],
            check=True,
            timeout=1,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        if result.stdout:
            print(result.stdout.decode('latin1'), end='')
        
        if result.stderr:
            print(result.stderr.decode('latin1'), end='')
    except subprocess.CalledProcessError as e:
        if e.stderr:
            print(e.stderr.decode('latin1'))
        exit()

    os.remove("/tmp/" + hash_code + ".c")
    os.remove("/tmp/" + hash_code)

    exit()
except plyparser.ParseError as e:
    print(f"Parsing error: {e}")
