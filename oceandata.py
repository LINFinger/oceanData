import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtGui import QIcon

import processing


class OceanDataProcess:

    def __init__(self):
        self.ui = uic.loadUi("ui/ocean_data.ui")
        self.ui.clearButton.clicked.connect(self.clearConsole)
        self.ui.pathButton.clicked.connect(self.getFilePath)
        self.ui.outputButton.clicked.connect(self.outputFile)

    def clearConsole(self):
        self.ui.console.clear()

    def getFilePath(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "选取文件", ".", "HAR文件 (*.har)")
        self.ui.pathEdit.setText(file_path)

    def outputFile(self):
        self.ui.console.append(
            '==================================start==================================')
        file_path = self.ui.pathEdit.text()
        file_type = self.ui.typeComboBox.currentText()
        self.ui.console.append(f'har文件路径 : {file_path}\n\n导出文件格式 : {file_type}')
        self.ui.console.append('\n--------------------------------------------------------------------------\n')
        od = processing.OceanData(file_path, file_type)
        od.dataProcessing()
        self.ui.console.append(od.getOutput())
        self.ui.console.append(
            '===================================end===================================\n')
        self.ui.console.ensureCursorVisible()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('img/ocean.jpeg'))
    MainWindow = OceanDataProcess()
    MainWindow.ui.show()
    sys.exit(app.exec_())
