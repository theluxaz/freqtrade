import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QComboBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

strategies = ["DevLukas15min","ProdLukas15min","BuyerDevHigh","BuyerDevMid""BuyerDevLow",
              "BuyerDevLongUptrend","BuyerDevSlowDowntrend","BuyerDevLongDowntrend","BuyerDevDowntrendUpswing"]

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Freqtrade Strategy Tester'
        self.left = 300
        self.top = 200
        self.width = 850
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

                # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 70)
        self.textbox.resize(150,20)

        # Create a button in the window
        # self.button = QPushButton('Show text', self)
        # self.button.move(20,80)

        # Label strategy
        self.label_strategy = QLabel(self)
        self.label_strategy.setText('Strategy:')
        self.label_strategy.move(25, 10)
        # Dropdown strategy
        self.combo_box = QComboBox(self)
        self.combo_box.setGeometry(20, 30, 150, 30)
        self.combo_box.addItems(strategies)

                # Label strategy
        self.label_strategy = QLabel(self)
        self.label_strategy.setText('Strategy:')
        self.label_strategy.move(25, 10)
        # Dropdown strategy
        self.combo_box = QComboBox(self)
        self.combo_box.setGeometry(20, 30, 150, 30)
        self.combo_box.addItems(strategies)


        #self.selection, okPressed = QInputDialog.getItem(self, "Select Basic or Advanced", "", strategies, 0, False)

        if self.combo_box == strategies[0]:
            print('DevLukas15min')
        if self.combo_box == strategies[1]:
            print('ProdLukas15min')
        # connect button to function on_click
        #self.button.clicked.connect(self.on_click)


        button=QPushButton('Backtest',self)
        button.setToolTip('Thank you for thinking about me')
        button.move(100,100)
        button.clicked.connect(self.on_click)


        button_plot=QPushButton('Show graph',self)
        button_plot.setToolTip('Thank you for thinking about me')
        button_plot.move(200,140)

        self.show()

    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("BACKTESTIIING")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())