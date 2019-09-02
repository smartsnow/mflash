import os
import sys
import qdarkstyle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from subprocess import Popen, CalledProcessError, PIPE


class UserWidget(QWidget):

    def __init__(self):
        super().__init__()
        # self.resize(200, 200)
        self.setWindowTitle('MXCHIP Flash Tool')
        curdir = os.path.join(os.path.dirname(os.path.abspath(__file__)))

        vLayout = QVBoxLayout(self)
        h0Layout = QHBoxLayout()
        vLayout.addLayout(h0Layout)
        self.fileNameLineEdit = QLineEdit()
        h0Layout.addWidget(self.fileNameLineEdit)
        self.fileNameLineEdit.setReadOnly(True)
        self.helpButton = QPushButton(QIcon(os.path.join(curdir, 'resources/help.png')), '')
        h0Layout.addWidget(self.helpButton)
        h1Layout = QHBoxLayout()
        vLayout.addLayout(h1Layout)
        self.comboBox = QComboBox()
        h1Layout.addWidget(self.comboBox)
        self.lineEdit = QLineEdit()
        h1Layout.addWidget(self.lineEdit)
        self.button = QPushButton(QIcon(os.path.join(curdir, 'resources/download.png')), '')
        self.button.setToolTip('Download')
        h1Layout.addWidget(self.button)
        h2Layout = QHBoxLayout()
        vLayout.addLayout(h2Layout)
        self.progressBar = QProgressBar()
        h2Layout.addWidget(self.progressBar)
        self.showHideLogButton = QPushButton(QIcon(os.path.join(curdir, 'resources/log.png')), '')
        self.showHideLogButton.setToolTip('Show/Hide log')
        h2Layout.addWidget(self.showHideLogButton)
        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.hide()
        vLayout.addWidget(self.plainTextEdit)
        self.plainTextEdit.setReadOnly(True)

PREFIX = '-->'
prefix_len = len(PREFIX)

infoText = '''MXCHIP Flash Tool.

Author : Snow Yang
Mail : yangsw@mxchip.com
Version : 1.2.2
'''

helpText = '''FLASH MAP
--------------------------------
MX1270
Bootloader : 0x00
Application : 0xA000
ATE : 0x100000
--------------------------------
'''

errorLogReasonDict = {
"in procedure 'ocd_bouncer'": 'Please check JTAG/SWD connection.',
'LIBUSB_ERROR_NOT_FOUND.': 'Please download "Zadig", and replace J-Link driver with "WinUSB".',
'Error: No J-Link device found.':'Please check J-Link USB connection.'
}

class Worker(QThread):

    signalProgressBar = pyqtSignal(int)
    signalPlainTextEdit = pyqtSignal(str)
    signalMessageBox = pyqtSignal(str)

    def __init__(self, widget):
        super().__init__()
        self.curdir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self.mculist = []
        for _root, _dirs, files in os.walk(os.path.join(self.curdir, 'targets')):
            for name in files:
                if name.endswith('.cfg'):
                    self.mculist.append(os.path.splitext(name)[0])

        self.widget = widget
        self.widget.comboBox.addItems(self.mculist)

        hostos = 'osx' if sys.platform == 'darwin' else 'Linux64' if sys.platform == 'linux2' else 'win'
        self.openocd = os.path.join(self.curdir, 'openocd', hostos, 'openocd_mxos')

        self.semaphore = QSemaphore()
        self.widget.button.clicked.connect(self.download)
        self.logShow = False
        self.widget.showHideLogButton.clicked.connect(self.showHideLog)
        self.widget.helpButton.clicked.connect(self.showHelp)
        self.signalProgressBar.connect(lambda value: self.widget.progressBar.setValue(value))
        self.signalPlainTextEdit.connect(lambda text: self.widget.plainTextEdit.appendPlainText(text))
        self.signalMessageBox.connect(lambda text: QMessageBox.critical(self.widget, '', text, QMessageBox.Yes, QMessageBox.Yes))

        self.filename = self.widget.fileNameLineEdit.text()
        self.widget.progressBar.setMinimum(0)
        self.widget.progressBar.setMaximum(os.path.getsize(self.filename))

    def showHelp(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Help')
        msgBox.setText(infoText)
        msgBox.setInformativeText(helpText)
        msgBox.exec()

    def showHideLog(self):
        if self.logShow:
            self.widget.plainTextEdit.hide()
            self.logShow = False
        else:
            self.widget.plainTextEdit.show()
            self.logShow = True
        self.widget.adjustSize()

    def download(self):
        self.widget.comboBox.setEnabled(False)
        self.widget.lineEdit.setEnabled(False)
        self.widget.button.setEnabled(False)
        self.semaphore.release()

    def run(self):
        self.semaphore.acquire()
        mcu = self.widget.comboBox.currentText()
        addr = self.widget.lineEdit.text()
        cmd_line = self.openocd + \
            ' -s ' + self.curdir + \
            ' -f ' + os.path.join(self.curdir, 'interface', 'jlink_swd.cfg') + \
            ' -f ' + os.path.join(self.curdir, 'targets', mcu + '.cfg') + \
            ' -f ' + os.path.join(self.curdir, 'flashloader', 'scripts', 'flash.tcl') + \
            ' -f ' + os.path.join(self.curdir, 'flashloader', 'scripts', 'cmd.tcl') + \
            ' -c init' + \
            ' -c flash_alg_pre_init' + \
            ' -c "flash_alg_init ' + os.path.join(self.curdir, 'flashloader', 'ramcode', mcu + '.elf').replace('\\', '/') + '"' + \
            ' -c "write ' + \
            self.filename.replace('\\', '/') + ' ' + addr + '" -c shutdown'
        proc = Popen(cmd_line, shell=True, universal_newlines=True, stderr=PIPE)

        log = ''
        while True:
            out = proc.stderr.readline().strip()
            log += out
            self.signalPlainTextEdit.emit(out)
            if proc.poll() != None:
                break
            else:
                if out[:prefix_len] == PREFIX:
                    self.signalProgressBar.emit(int(out[prefix_len:], 0))

        if proc.poll():
            reason = 'Unkown Reason'
            for errorLog in errorLogReasonDict:
                if errorLog in log:
                    reason = errorLogReasonDict[errorLog]
                    break
            self.signalMessageBox.emit('Download Failed!\r\n\r\nReason:\r\n%s' % (reason))

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Calibri"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    curdir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    app.setWindowIcon(QIcon(os.path.join(curdir, 'resources/flash.png')))
    widget = UserWidget()
    widget.fileNameLineEdit.setText(sys.argv[1])
    widget.show()
    worker = Worker(widget)
    worker.start()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
