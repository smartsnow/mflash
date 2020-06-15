import os
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

window = Tk()
window.title('mflash tool')

lbl_chip = Label(window, text='Chip')
lbl_chip.grid(column=0, row=0, sticky=W)
combo_chip = Combobox(window, width=8)
combo_chip['values'] = ('mx1270', 'mx1290', 'mx1310')
combo_chip.current(0)
combo_chip.grid(column=1, row=0, sticky=W)

lbl_debugger = Label(window, text='Debugger')
lbl_debugger.grid(column=0, row=1, sticky=W)
combo_debugger = Combobox(window, width=8)
combo_debugger['values'] = ('jlink_swd', 'jlink', 'stlink')
combo_debugger.current(0)
combo_debugger.grid(column=1, row=1, sticky=W)


def clicked():
    # lbl.insert(0, text=combo_chip.get())
    pass


btn_mac = Button(window, text='Read MAC', command=clicked)
btn_mac.grid(column=0, row=2, sticky=W)
lbl_mac = Label(window, text='')
lbl_mac.grid(column=1, row=2, sticky=W)

lbl_address = Label(window, text='Address')
lbl_address.grid(column=1, row=3, sticky=W)
lbl_size = Label(window, text='Size')
lbl_size.grid(column=2, row=3, sticky=W)
lbl_file = Label(window, text='File')
lbl_file.grid(column=3, row=3, sticky=W)


class Flash():
    def __init__(self, master, row, name, addr, size, file):
        self.btn = Button(master, text=name, command=None)
        self.btn.grid(column=0, row=row, sticky=W)
        if addr:
            self.addr = Entry(master, width=10)
            self.addr.grid(column=1, row=row, sticky=W)
        if size:
            self.size = Entry(master, width=10)
            self.size.grid(column=2, row=row, sticky=W)
        if file:
            strval = StringVar()
            self.filename = Entry(master, textvariable=strval, width=32)
            self.filename.grid(column=3, row=row, sticky=W)

            def clicked():
                if file == 'r':
                    name = filedialog.asksaveasfilename(
                        initialdir=os.path.dirname(__file__))
                else:
                    name = filedialog.askopenfilename(
                        initialdir=os.path.dirname(__file__))
                strval.set(name)
            self.filechoose = Button(
                master, text='...', command=clicked, width=3)
            self.filechoose.grid(column=4, row=row)


flash_erase = Flash(window, 4, 'Erase', True, True, False)
flash_write = Flash(window, 5, 'Write', True, False, 'w')
flash_read = Flash(window, 6, 'Read', True, True, 'r')

bar = Progressbar(window, style='black.Horizontal.TProgressbar')
bar['value'] = 70
bar.grid(column=0, row=7, columnspan=10, sticky=E+W)

window.mainloop()
