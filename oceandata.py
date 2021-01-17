import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtGui import QIcon
from threading import Thread
from datetime import datetime

import processing


class OceanDataProcess:

    def __init__(self):
        self.ui = uic.loadUi("ui/ocean_data.ui")
        self.ui.clearButton.clicked.connect(self.clearConsole)
        self.ui.pathButton.clicked.connect(self.getFilePath)
        self.ui.outputButton.clicked.connect(self.outputFile)
        self.consoleOutputInfoIn = ''
        self.consoleOutputInfoOut = ''

    def clearConsole(self):
        self.ui.console.clear()

    def getFilePath(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "选取文件", ".", "HAR文件 (*.har)")
        self.ui.pathEdit.setText(file_path)

    def outputFile(self):
        file_path = self.ui.pathEdit.text()
        file_type = self.ui.typeComboBox.currentText()
        self.consoleOutputInfoIn = ('===========================start==========================\n' +
                                    f'{datetime.now().strftime("%Y-%m-%d ** %H:%M:%S")}\n\n' +
                                    f'har文件路径 : {file_path}\n\n导出文件格式 : {file_type}\n' +
                                    '\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n'
                                    )
        self.ui.console.append(self.consoleOutputInfoIn)
        od = processing.OceanData(file_path, file_type)
        thread = Thread(target=self.processThread, args=[od])
        thread.start()

    def processThread(self, od):
        od.dataProcessing()
        self.consoleOutputInfoOut = (od.getOutput() +
                                     '\n===========================end===========================\n'
                                     )
        self.ui.console.append(self.consoleOutputInfoOut)
        self.ui.console.ensureCursorVisible()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('img/ocean.jpeg'))
    MainWindow = OceanDataProcess()
    MainWindow.ui.show()
    sys.exit(app.exec_())
