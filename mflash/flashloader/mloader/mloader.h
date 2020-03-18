/**
 * @author  snow yang
 * @email   snowyang.iot@gmail.com
 * @date    2020-03-17 14:27:02
 */

#ifndef _MLOADER_H_
#define _MLOADER_H_

#include <stdint.h>

enum
{
    READ,
    WRITE,
    ERASE,
    MAC,
};

typedef int (*mloader_cmd_t)(uint32_t addr, uint32_t size, uint8_t *buf);
void mloader_loop(void);

#endif