#!/bin/bash
cd $(dirname $0)
exec timeout --foreground 300 qemu-system-x86_64 \
	-m 64M \
        -cpu kvm64,+smep,+smap \
        -nographic \
        -monitor /dev/null \
        -kernel bzImage \
        -initrd rootfs.cpio.gz \
	-no-reboot \
	-append "console=ttyS0 quiet kaslr panic=1 kpti=1 oops=panic" \
	-net user -net nic -device e1000 \
