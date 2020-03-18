/**
 * @author  snow yang
 * @email   snowyang.iot@gmail.com
 * @date    2020-03-17 14:26:56
 */

#include <stdio.h>
#include <stdint.h>

#include "mloader_conf.h"
#include "mloader.h"

typedef struct
{
    void *entry;
    uint32_t bufsize;
    volatile int rdy;
    volatile int cmd;
    volatile int ret;
    volatile uint32_t addr;
    volatile uint32_t size;
    volatile uint8_t buf[DATA_BUF_SIZE];
} mloader_t;

extern mloader_cmd_t mloader_cmds[];

mloader_t mloader = {
    .entry = ENTRY_FUNC,
    .bufsize = DATA_BUF_SIZE,
    .rdy = 0,
};

void mloader_loop(void)
{
    while (1)
    {
        while (mloader.rdy == 0)
            ;
        mloader.ret = mloader_cmds[mloader.cmd](mloader.addr, mloader.size, (uint8_t *)mloader.buf);
        mloader.rdy = 0;
    }
}
