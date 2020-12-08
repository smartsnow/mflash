import os
import time
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from threading import Thread

from .version import *
from .mflash import MFlash, CalledProcessError

root = Tk()
root.title('mfash tools')
root.resizable(0, 0)

config = LabelFrame(root, labelanchor=N, text='Configure', borderwidth=2)
config.grid(column=0, row=0, pady=2, padx=2, ipadx=2, ipady=2, sticky=E+W)

Label(config, text='Chip').grid(column=0, row=0, pady=2, padx=2, sticky=E+W)
chipvar = StringVar()
chip = Combobox(config, textvariable=chipvar, width=10)
chip['values'] = ('mx1270', 'mx1290', 'mx1310')
chip.current(0)
chip.grid(column=1, row=0, pady=2, padx=2, sticky=E+W)

Label(config, text='Debugger').grid(
    column=2, row=0, pady=2, padx=2, sticky=E+W)
dbg = Combobox(config, width=10)
dbg['values'] = ('jlink_swd', 'jlink', 'stlink-v2-1')
dbg.current(0)
dbg.grid(column=3, row=0, pady=2, padx=2, sticky=E+W)

info = LabelFrame(root, labelanchor=N, text='Information', borderwidth=2)
info.grid(column=0, row=1, pady=2, padx=2, ipadx=2, ipady=2, sticky=E+W)

Label(info, text='MAC', borderwidth=5).grid(
    column=0, row=0, pady=2, padx=2, sticky=E+W)
macval = StringVar()
Entry(info, textvariable=macval, width=14).grid(
    column=1, row=0, pady=2, padx=2, sticky=E+W)

cmd = LabelFrame(root, labelanchor=N, text='Flash Command', borderwidth=2)
cmd.grid(column=0, row=2, pady=2, padx=2, ipadx=2, ipady=2, sticky=E+W)

Label(cmd, text='Command', borderwidth=5, relief="solid", anchor=CENTER).grid(
    column=0, row=0, pady=2, padx=2, sticky=E+W)
Label(cmd, text='Address', borderwidth=5, relief="solid", anchor=CENTER).grid(
    column=1, row=0, pady=2, padx=2, sticky=E+W)
Label(cmd, text='Size', borderwidth=5, relief="solid", anchor=CENTER).grid(
    column=2, row=0, pady=2, padx=2, sticky=E+W)
Label(cmd, text='File', borderwidth=5, relief="solid", anchor=CENTER).grid(
    column=3, row=0, pady=2, padx=2, sticky=E+W)


class FlashCmd():
    def __init__(self, row, name, addr, size, file):
        self.handler = None

        def handler_thread():
            thread = Thread(target=self.handler, daemon=True)
            thread.start()
        self.btn = Button(cmd, text=name, command=handler_thread)
        self.btn.grid(column=0, row=row, pady=2, padx=2, sticky=E+W)
        if addr:
            self.addrvar = IntVar()
            self.addr = Entry(cmd, textvariable=self.addrvar, width=10)
            self.addr.grid(column=1, row=row, pady=2, padx=2, sticky=E+W)
        if size:
            self.sizevar = IntVar()
            self.size = Entry(cmd, textvariable=self.sizevar, width=10)
            self.size.grid(column=2, row=row, pady=2, padx=2, sticky=E+W)
        if file:
            self.fileval = StringVar()
            self.filename = Entry(cmd, textvariable=self.fileval, width=32)
            self.filename.grid(column=3, row=row, pady=2, padx=2, sticky=E+W)

            def clicked():
                if file == 'r':
                    name = filedialog.asksaveasfilename(
                        initialdir=os.path.dirname(__file__))
                else:
                    name = filedialog.askopenfilename(
                        initialdir=os.path.dirname(__file__))
                self.fileval.set(name)
            self.filechoose = Button(cmd, text='...', command=clicked, width=3)
            self.filechoose.grid(column=4, row=row)


erase = FlashCmd(1, 'Erase', True, True, False)
write = FlashCmd(2, 'Write', True, False, 'w')
read = FlashCmd(3, 'Read', True, True, 'r')

pbarval = IntVar()
pbar = Progressbar(cmd, variable=pbarval)
pbar.grid(row=4, column=0, columnspan=5, pady=2, padx=2, sticky=E+W)


def progress_handler(out):
    if '%' in out:
        pos = int(out[:-1], 0)
        pbarval.set(pos)


def read_handler():
    mflash = MFlash(chipvar.get(), progress_handler)
    macval.set(mflash.mac())
    mflash.read(read.fileval.get(), read.addrvar.get(), read.sizevar.get())


read.handler = read_handler

root.mainloop()
