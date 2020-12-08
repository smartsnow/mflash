# -*- coding: UTF-8 -*-
# Date    : 2018/08/07
# Author  : Snow Yang
# Mail    : yangsw@mxchip.com

import os
import sys
import argparse

from .progressbar import ProgressBar
from .version import *
from .mflash import MFlash, CalledProcessError

long_description = '''
author  : %s
email   : %s
version : %s

usage: mflash <chip> <command> [<args>] [<optinons>]

chip:
    mx1270
    mx1290
    mx1300
    mx1310
    mx1350
    rtl8720c

command:
    read    -f <file> -a <address> -s <size>    read data from flash to file
    write   -f <file> -a <address>              write data from file to flash
    erase   -a <address> -s <size>              erase flash
    unlock                                      unlock flash
    mac                                         read mac address of chip
''' % (author, email, version)


def main():
    parser = argparse.ArgumentParser(description=long_description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('chip', type=str, help='chip name')
    parser.add_argument('command', type=str, help='command')
    parser.add_argument('-f', '--file', type=str, help='file name')
    parser.add_argument('-a', '--address', type=str, help='flash address')
    parser.add_argument('-s', '--size', type=str, help='size')
    args = parser.parse_args()

    pbar = ProgressBar(0)
    def progress_handler(out):
            if '%' in out:
                pos = int(out[:-1], 0)
                pbar.update(int(pos * pbar.step))
    mflash = MFlash(args.chip, progress_handler)
    try:
        if args.command == 'mac':
            print(mflash.mac())
        elif args.command == 'erase':
            mflash.erase(int(args.address, 0), int(args.size, 0))
        elif args.command == 'write':
            filename = args.file.replace('\\', '/')
            pbar.max_value = os.path.getsize(filename)
            pbar.step = pbar.max_value / 100
            mflash.write(filename, int(args.address, 0))
        elif args.command == 'read':
            filename = args.file.replace('\\', '/')
            pbar.max_value = int(args.size, 0)
            pbar.step = pbar.max_value / 100
            mflash.read(filename, int(args.address, 0), int(args.size, 0))
    except CalledProcessError as e:
        print(e.cmd)
        print(e.stdout)
        print(e.stderr)

if __name__ == "__main__":
    main()
