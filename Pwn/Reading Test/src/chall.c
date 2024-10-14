// gcc -no-pie -fno-stack-protector -o chall chall.c

#include <unistd.h>

int main()
{
    long l = 0x18;
    read(0, &l, l);
    return 0;
}
