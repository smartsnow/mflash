# -*- coding: UTF-8 -*-
# Date    : 2018/08/07
# Author  : Snow Yang
# Mail    : yangsw@mxchip.com

import os
import sys
import shlex
import struct
import argparse
from subprocess import Popen, CalledProcessError, PIPE
from .progressbar import ProgressBar

MARKER = {'osx': '█', 'win': '#'}
FILL = {'osx': '░', 'win': '-'}

PREFIX = '-->'
prefix_len = len(PREFIX)

def flasher(curdir, mcu, file_name, addr):

    hostos = 'osx' if sys.platform == 'darwin' else 'Linux64' if sys.platform == 'linux2' else 'win'
    pbar = ProgressBar(os.path.getsize(file_name), marker=MARKER[hostos], fill=FILL[hostos])
    openocd = os.path.join(curdir, 'openocd', hostos, 'openocd_mxos')

    cmd_line = openocd + \
        ' -s ' + curdir + \
        ' -f ' + os.path.join(curdir, 'interface', 'jlink_swd.cfg') + \
        ' -f ' + os.path.join(curdir, 'targets', mcu + '.cfg') + \
        ' -f ' + os.path.join(curdir, 'flashloader', 'scripts', 'flash.tcl') + \
        ' -f ' + os.path.join(curdir, 'flashloader', 'scripts', 'cmd.tcl') + \
        ' -c init' + \
        ' -c flash_alg_pre_init' + \
        ' -c "flash_alg_init ' + os.path.join(curdir, 'flashloader', 'ramcode', mcu + '.elf') + '"' + \
        ' -c "write ' + file_name + ' ' + addr + '" -c shutdown'
    proc = Popen(shlex.split(cmd_line), universal_newlines=True, stderr=PIPE)
    logtext = ''

    while True:
        out = proc.stderr.readline().strip()
        logtext += out
        if proc.poll() != None:
            if proc.poll():
                print(logtext)
            return
        else:
            if out[:prefix_len] == PREFIX:
                pos = int(out[prefix_len:], 0)
                pbar.update(pos)

def main():
    parser = argparse.ArgumentParser(description='Download binary file to flash')
    parser.add_argument('-m', '--mcu', type=str, required=True, help='mcu name')
    parser.add_argument('-f', '--file', type=str, required=True, help='file name')
    parser.add_argument('-a', '--addr', type=str, required=True, help='address')

    curdir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    args = parser.parse_args(sys.argv[1:])

    flasher(curdir, args.mcu, args.file, args.addr)

if __name__ == "__main__":
    main()