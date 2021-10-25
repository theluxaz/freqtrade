import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QComboBox, QLabel, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

strategies = ["DevLukas15min","ProdLukas15min","BuyerDevHigh","BuyerDevMid""BuyerDevLow",
              "BuyerDevLongUptrend","BuyerDevSlowDowntrend","BuyerDevLongDowntrend","BuyerDevDowntrendUpswing"]

timesteps = ["1","2","3","4""5"]

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
        # self.textbox = QLineEdit(self)
        # self.textbox.move(20, 70)
        # self.textbox.resize(150,20)

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

        # Label Indicators 1
        self.indicator1_label = QLabel(self)
        self.indicator1_label.setText('Indicators 1:')
        self.indicator1_label.move(20, 80)
        # Textbox Indicator 1
        self.indicator1_textbox = QLineEdit(self)
        self.indicator1_textbox.move(90, 78)
        self.indicator1_textbox.resize(150,20)
        # Label Indicators 1 Default?
        self.indicator1_default_label = QLabel(self)
        self.indicator1_default_label.setText('Default:')
        self.indicator1_default_label.move(20, 100)
        # Checkbox Indicators 1 Default?
        self.indicator1_checkbox_default = QCheckBox(self)
        self.indicator1_checkbox_default.move(63, 101)
        self.indicator1_checkbox_default.setChecked(True)
        #self.indicator1_checkbox_default.stateChanged.connect(self.clickBox)
        # Checkbox Indicators 1 Enable
        self.indicator1_checkbox = QCheckBox(self)
        self.indicator1_checkbox.move(250, 82)
        #self.indicator1_checkbox.stateChanged.connect(self.clickBox)


        # Label Indicators 2
        self.indicator2_label = QLabel(self)
        self.indicator2_label.setText('Indicators 2:')
        self.indicator2_label.move(20, 130)
        # Textbox Indicator 2
        self.indicator2_textbox = QLineEdit(self)
        self.indicator2_textbox.move(90, 128)
        self.indicator2_textbox.resize(150,20)
        # Checkbox Indicators 2 Enable
        self.indicator2_checkbox = QCheckBox(self)
        self.indicator2_checkbox.move(250, 132)
        #self.indicator2_checkbox.stateChanged.connect(self.clickBox)

        # Label Indicators 3
        self.indicator3_label = QLabel(self)
        self.indicator3_label.setText('Indicators 3:')
        self.indicator3_label.move(20, 160)
        # Textbox Indicator 3
        self.indicator3_textbox = QLineEdit(self)
        self.indicator3_textbox.move(90, 158)
        self.indicator3_textbox.resize(150,20)
        # Checkbox Indicators 3 Enable
        self.indicator3_checkbox = QCheckBox(self)
        self.indicator3_checkbox.move(250, 162)
        #self.indicator3_checkbox.stateChanged.connect(self.clickBox)


        # Time From label
        self.time_from_label = QLabel(self)
        self.time_from_label.setText('Time From:')
        self.time_from_label.move(310, 12)
        # Time From Dropdown
        self.time_from_dropdown = QComboBox(self)
        self.time_from_dropdown.setGeometry(310, 30, 150, 30)
        self.time_from_dropdown.addItems(timesteps)
        # Time From label checkbox
        self.time_from_label = QLabel(self)
        self.time_from_label.setText('Date')
        self.time_from_label.move(420, 12)
        # Time From Checkbox Date
        self.time_from_checkbox_date = QCheckBox(self)
        self.time_from_checkbox_date.move(446, 13)
        #self.time_from_checkbox_date.stateChanged.connect(self.clickBox)

        ## ^ ^ WHEN THIS ONE IS UPDATED, UPDATE THE TIME UNTIL TO THE NEXT NUMBER AUTOMATICALLY


        # Time From to Util arrows label
        self.time_until_label = QLabel(self)
        self.time_until_label.setText('----->')
        self.time_until_label.move(470, 36)


        # Time Until label
        self.time_until_label = QLabel(self)
        self.time_until_label.setText('Time Until:')
        self.time_until_label.move(510, 12)
        # Time Until label checkbox
        self.time_until_label_checkbox = QLabel(self)
        self.time_until_label_checkbox.setText('Date')
        self.time_until_label_checkbox.move(620, 12)
        # Time Until Checkbox Date
        self.time_until_checkbox_date = QCheckBox(self)
        self.time_until_checkbox_date.move(646, 13)
        #self.time_until_checkbox_date.stateChanged.connect(self.clickBox)
        # Time Until Dropdown
        self.time_until_dropdown = QComboBox(self)
        self.time_until_dropdown.setGeometry(510, 30, 150, 30)
        self.time_until_dropdown.addItems(timesteps)
        # Time Until Checkbox
        self.time_until_checkbox = QCheckBox(self)
        self.time_until_checkbox.move(667, 37)
        #self.time_until_checkbox.stateChanged.connect(self.clickBox)




        #         # Label strategy
        # self.label_strategy = QLabel(self)
        # self.label_strategy.setText('Strategy:')
        # self.label_strategy.move(25, 10)
        # # Dropdown strategy
        # self.combo_box = QComboBox(self)
        # self.combo_box.setGeometry(20, 30, 150, 30)
        # self.combo_box.addItems(strategies)
        #
        #
        # #self.selection, okPressed = QInputDialog.getItem(self, "Select Basic or Advanced", "", strategies, 0, False)
        #
        # if self.combo_box == strategies[0]:
        #     print('DevLukas15min')
        # if self.combo_box == strategies[1]:
        #     print('ProdLukas15min')
        # # connect button to function on_click
        # #self.button.clicked.connect(self.on_click)
        #
        #
        # button=QPushButton('Backtest',self)
        # button.setToolTip('Thank you for thinking about me')
        # button.move(100,100)
        # button.clicked.connect(self.on_click)
        #
        #
        # button_plot=QPushButton('Show graph',self)
        # button_plot.setToolTip('Thank you for thinking about me')
        # button_plot.move(200,140)

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