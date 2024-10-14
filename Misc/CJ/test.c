# include <stdio.h>
# include <stdlib.h>
# include <seccomp.h>
# include <unistd.h>
# include <fcntl.h>

void install_seccomp() {
    scmp_filter_ctx ctx;

    ctx = seccomp_init(SCMP_ACT_ALLOW);
    if (ctx == NULL) {
        perror("seccomp_init");
        exit(EXIT_FAILURE);
    }

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

typedef int (*open_t)(const char*, int);

int callOpen(open_t openFunc, const char* path, int flags) {
    return openFunc(path, flags);
}

int callOpens(open_t openFunc[], const char* path, int flags) {
    return openFunc[0](path, flags);
}

void run() {
// #define callFunc(a, b, params) a##b params
//     int fd = callFunc(o,pen, ("/etc/passwd", O_RDONLY));
//     char buffer[512];
//     callFunc(re,ad, (fd, buffer, sizeof(buffer)));
//     puts(buffer);
//     callFunc(cl,ose,(fd));

    // void* openX = (void *)open;
    // typedef int (*openX)(const char*, int);
    // openX open2 = (openX)open;
    // ((int (*)(const char*, int))open2)("/etc/passwd", O_RDONLY);

    // int fd = callOpen((open_t)open, "/etc/passwd", O_RDONLY);
    // printf("fd: %d\n", fd);

    int fd = o##pen("/etc/passwd", O_RDONLY);
    char buffer[512];
    re##ad(fd, buffer, sizeof(buffer));
    puts(buffer);
    cl##ose(fd);

}

int main() {
    install_seccomp();
    run();
    return 0;
}