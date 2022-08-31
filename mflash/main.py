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

def flasher(curdir, mcu, file_name, addr, debugger):

    hostos = 'osx' if sys.platform == 'darwin' else 'Linux64' if sys.platform == 'linux2' else 'win'
    pbar = ProgressBar(os.path.getsize(file_name), marker=MARKER[hostos], fill=FILL[hostos])
    openocd = os.path.join(curdir, 'openocd', hostos, 'openocd_mxos')

    cmd_line = openocd + \
        ' -s ' + curdir + \
        ' -f ' + os.path.join(curdir, 'interface', debugger + '.cfg') + \
        ' -f ' + os.path.join(curdir, 'targets', mcu + '.cfg') + \
        ' -f ' + os.path.join(curdir, 'flashloader', 'scripts', 'flash.tcl') + \
        ' -f ' + os.path.join(curdir, 'flashloader', 'scripts', 'cmd.tcl') + \
        ' -c init' + \
        ' -c flash_alg_pre_init' + \
        ' -c "flash_alg_init ' + os.path.join(curdir, 'flashloader', 'ramcode', mcu + '.elf').replace('\\', '/') + '"' + \
        ' -c "erase ' + addr + ' ' + '%d'%os.path.getsize(file_name) + '"' + \
        ' -c "write ' + file_name.replace('\\', '/') + ' ' + addr + '" -c shutdown'
    proc = Popen(cmd_line, shell=True, universal_newlines=True, stderr=PIPE)
    logtext = ''

    while True:
        out = proc.stderr.readline().strip()
        logtext += out + '\r\n'
        if proc.poll() != None:
            if proc.poll():
                print(logtext)
            return
        else:
            if out[:prefix_len] == PREFIX:
                pos = int(out[prefix_len:], 0)
                pbar.update(pos)

long_description = '''MXCHIP Flash Tool.

Author  : Snow Yang
Mail    : yangsw@mxchip.com
Version : 1.3.0
'''

def main():
    parser = argparse.ArgumentParser(description=long_description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-m', '--mcu', type=str, required=True, help='mcu name')
    parser.add_argument('-f', '--file', type=str, required=True, help='file name')
    parser.add_argument('-a', '--addr', type=str, required=True, help='address')
    parser.add_argument('-d', '--debugger', type=str, required=False, default='jlink_swd', help='address')

    curdir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    args = parser.parse_args(sys.argv[1:])

    flasher(curdir, args.mcu, args.file, args.addr, args.debugger)

def interactive():
    print(long_description)

    if len(sys.argv) == 1:
        print('mflashi <file name>')
        return 1
    curdir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    mcu_list = []
    for root, dirs, files in os.walk(os.path.join(curdir, 'targets')):
        for name in files:
            if name.endswith('.cfg'):
                mcu_list.append(os.path.splitext(name)[0])
    _file = sys.argv[1]
    print('MCU list:')
    for i, name in enumerate(mcu_list):
        print(' %d - %s'%(i, name))
    mcu = mcu_list[int(input('MCU Number: '))]
    addr = input('Download Address: ')

    flasher(curdir, mcu, _file, addr)

    input('Press any key to exit: ')

if __name__ == "__main__":
    main()