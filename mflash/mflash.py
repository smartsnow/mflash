import os
import sys
import collections
from time import sleep
from subprocess import Popen, run, CalledProcessError, PIPE, STDOUT, DEVNULL


class MFlash():
    def __init__(self, chip, progress, debugger='jlink_swd', id=0):
        self.progress = progress
        hostos = 'osx' if sys.platform == 'darwin' else 'Linux64' if sys.platform == 'linux2' else 'win'
        cwd = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        openocd = '%s/openocd/%s/openocd_mxos' % (cwd, hostos)
        self._cmd_hdr = ' '.join([
            openocd,
            '-s %s' % cwd,
            '-f interface/%s.cfg' % debugger,
            '-f targets/%s.cfg' % chip,
            '-f flashloader/scripts/flash.tcl',
            '-f flashloader/scripts/cmd.tcl',
            '-c "gdb_port disabled"',
            '-c "tcl_port disabled"',
            '-c "telnet_port disabled"',
            '-c init',
            '-c mflash_pre_init',
            '-c "mflash_init flashloader/ramcode/%s.elf"' % chip])
        self.logfile = os.path.join(cwd, '.mflash-%d.log' % id).replace('\\', '/')

    def _construct_cmdline(self, cmds):
        cmds.append('shutdown')
        cmdline = ' '.join([self._cmd_hdr, ' '.join('-c "%s"' % cmd for cmd in cmds)])
        return cmdline

    def _run(self, cmds, progress=True):
        cmdline = self._construct_cmdline(cmds)
        cmdline += ' -l %s' % self.logfile
        p = Popen(cmdline, shell=True, universal_newlines=True, stdout=PIPE, stderr=DEVNULL)
        out = ''
        while True:
            o = p.stdout.readline().strip()
            if o:
                out += o
                if progress:
                    self.progress(o)
            if p.poll() != None:
                if p.poll():
                    lines = collections.deque(open(self.logfile), 10)
                    raise CalledProcessError(1, cmdline, out, ''.join(lines))
                return out

    def justrun(self):
        cmdline = self._construct_cmdline([])
        run(cmdline, shell=True, check=True, stdout=DEVNULL, stderr=DEVNULL)

    def connect(self):
        while True:
            try:
                self.justrun()
                sleep(0.1)
                self.justrun()
                break
            except CalledProcessError:
                sleep(0.5)

    def disconnect(self):
        while True:
            try:
                self.justrun()
            except CalledProcessError:
                sleep(0.1)
                try:
                    self.justrun()
                except CalledProcessError:
                    break
            sleep(0.5)

    def mac(self):
        return self._run(['mflash_mac'], progress=False)

    def write(self, file, addr):
        self._run(['mflash_unlock', 'mflash_erase %s %d' % (
            addr, os.path.getsize(file)), 'mflash_write %s %s' % (file, addr)])

    def erase(self, addr, size):
        self._run(['mflash_unlock', 'mflash_erase %s %d' % (addr, size)])

    def read(self, file, addr, size):
        self._run(['mflash_read %s %s %s' % (file, addr, size)])


if __name__ == '__main__':

    helpdoc = '''
python3 mflash.py <chip> <mflash_read/mflash_write/mflash_erase/mflash_mac/mflash_unlock> [arguments]
- mflash_read <file> <address> <size>: read data from chip to file.
- mflash_write <file> <address>: write data from file to chip.
- mflash_erase <address> <size>: write data from file to chip.
- mflash_mac: read mac address of chip.
- mflash_unlock: unlock flash of chip.
'''

    argv = sys.argv
    argc = len(sys.argv)
    if argc < 3:
        print(helpdoc)
        exit(0)

    mflash = MFlash(argv[1], lambda out: print('out:', out))

    cmd = argv[2]

    try:
        if cmd == 'mflash_read':
            if argc >= 5:
                mflash.connect()
                mflash.read(argv[3].replace('\\', '/'), argv[4], argv[5])
                exit(0)
        elif cmd == 'mflash_write':
            if argc >= 4:
                mflash.connect()
                mflash.write(argv[3].replace('\\', '/'), argv[4])
                exit(0)
        elif cmd == 'mflash_mac':
            mflash.connect()
            print(mflash.mac())
            exit(0)
    except CalledProcessError as e:
        print(e.cmd)
        print(e.stdout)
        print(e.stderr)
        exit(1)

    print(helpdoc)
    exit(1)
