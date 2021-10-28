import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QComboBox, QLabel, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox,QPlainTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

strategies = ["DevLukas15min","ProdLukas15min","BuyerDevHigh","BuyerDevMid""BuyerDevLow",
              "BuyerDevLongUptrend","BuyerDevSlowDowntrend","BuyerDevLongDowntrend","BuyerDevDowntrendUpswing"]

hyperopt_loss_functions = ["ShortTradeDurHyperOptLoss","OnlyProfitHyperOptLoss","SharpeHyperOptLoss","SharpeHyperOptLossDaily","SortinoHyperOptLoss",
              "SortinoHyperOptLossDaily","MaxDrawDownHyperOptLoss"]

timesteps = ["1","2","3","4""5"]

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Freqtrade Strategy Tester'
        self.left = 300
        self.top = 200
        self.width = 850
        self.height = 380
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
        self.time_until_checkbox.setChecked(True)
        #self.time_until_checkbox.stateChanged.connect(self.clickBox)


         # Label Pairs 1
        self.pairs1_label = QLabel(self)
        self.pairs1_label.setText('Pairs:')
        self.pairs1_label.move(320, 100)
        # Textbox Pairs 1
        self.pairs1_textbox = QPlainTextEdit(self)
        self.pairs1_textbox.move(355, 100)
        self.pairs1_textbox.resize(60,246)

         # Label Cache Pairs 2
        self.pairs2_label = QLabel(self)
        self.pairs2_label.setText('Cache:')
        self.pairs2_label.move(470, 100)
        # Textbox Cache Pairs 2
        self.pairs2_textbox = QPlainTextEdit(self)
        self.pairs2_textbox.move(510, 100)
        self.pairs2_textbox.resize(60,246)

         # Label All Pairs 3
        self.pairs3_label = QLabel(self)
        self.pairs3_label.setText('All:')
        self.pairs3_label.move(580, 100)
        # Textbox All Pairs 3
        self.pairs3_textbox = QPlainTextEdit(self)
        self.pairs3_textbox.move(600, 100)
        self.pairs3_textbox.resize(60,246)



        # Label Hyperopt
        self.hyperopt_label = QLabel(self)
        self.hyperopt_label.setText('Hyperopt:')
        self.hyperopt_label.move(20, 220)

        # Checkbox hyperopt
        self.hyperopt_checkbox = QCheckBox(self)
        self.hyperopt_checkbox.move(71, 221)
        self.hyperopt_checkbox.setChecked(False)
        #self.indicator1_checkbox_default.stateChanged.connect(self.clickBox)


        self.addSearchSpace()


        # Button backtest
        self.backtest_button=QPushButton('Backtest',self)
        self.backtest_button.setToolTip('Thank you for thinking about me')
        self.backtest_button.move(670,324)
        #self.backtest_button.clicked.connect(self.on_click)


        # Button Show Plot
        self.plot_button=QPushButton('Show Plot',self)
        self.plot_button.setToolTip('Thank you for thinking about me')
        self.plot_button.move(760,324)
        #self.plot_button.clicked.connect(self.on_click)

        # Profit plot label
        self.display_profit_label = QLabel(self)
        self.display_profit_label.setText('Profit')
        self.display_profit_label.move(789,302)
        # Time Until Checkbox Date
        self.display_profit_checkbox = QCheckBox(self)
        self.display_profit_checkbox.move(820,302)
        #self.display_profit_checkbox.stateChanged.connect(self.clickBox)


        # Label Run Command args
        self.run_command_args_label = QLabel(self)
        self.run_command_args_label.setText('--Indicator1 test test2 test3 --Indicator2 sma10k rsi macd rsi100')
        self.run_command_args_label.move(18,356)


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

    def addSearchSpace(self):


        # Label Search Space:
        self.search_space_label = QLabel(self)
        self.search_space_label.setText('Search Space')
        self.search_space_label.move(190, 230)


        # # Label Hyperopt
        # self.label_strategy = QLabel(self)
        # self.label_strategy.setText('Hyperopt:')
        # self.label_strategy.move(20, 300)
        # # Dropdown strategy
        # self.combo_box = QComboBox(self)
        # self.combo_box.setGeometry(15, 320, 150, 30)
        # self.combo_box.addItems(strategies)


        # Label Loss Function
        self.label_strategy = QLabel(self)
        self.label_strategy.setText('Loss function:')
        self.label_strategy.move(20, 300)
        # Dropdown Loss Function
        self.combo_box = QComboBox(self)
        self.combo_box.setGeometry(17, 320, 200, 30)
        self.combo_box.addItems(hyperopt_loss_functions)


        # Button Hyperopt
        self.hyperopt_button=QPushButton('Hyperopt',self)
        self.hyperopt_button.move(255,323)
        #self.hyperopt_button.clicked.connect(self.on_click)


        # Label ALL Search Space:
        self.search_space_all_label = QLabel(self)
        self.search_space_all_label.setText('All:')
        self.search_space_all_label.move(100, 250)
        # Checkbox ALL Search Space
        self.search_space_all_checkbox = QCheckBox(self)
        self.search_space_all_checkbox.move(118, 251)
        self.search_space_all_checkbox.setChecked(False)
        #self.search_space_all_checkbox.stateChanged.connect(self.clickBox)

        # Label DEFAULT Search Space:
        self.search_space_default_label = QLabel(self)
        self.search_space_default_label.setText('Default:')
        self.search_space_default_label.move(150, 250)
        # Checkbox DEFAULT Search Space
        self.search_space_default_checkbox = QCheckBox(self)
        self.search_space_default_checkbox.move(191, 251)
        self.search_space_default_checkbox.setChecked(False)
        #self.search_space_default_checkbox.stateChanged.connect(self.clickBox)

        # Label BUY Search Space:
        self.search_space_buy_label = QLabel(self)
        self.search_space_buy_label.setText('Buy:')
        self.search_space_buy_label.move(230, 250)
        # Checkbox BUY Search Space
        self.search_space_buy_checkbox = QCheckBox(self)
        self.search_space_buy_checkbox.move(254, 251)
        self.search_space_buy_checkbox.setChecked(False)
        #self.search_space_buy_checkbox.stateChanged.connect(self.clickBox)

        # Label SELL Search Space:
        self.search_space_sell_label = QLabel(self)
        self.search_space_sell_label.setText('Sell:')
        self.search_space_sell_label.move(290, 250)
        # Checkbox SELL Search Space
        self.search_space_sell_checkbox = QCheckBox(self)
        self.search_space_sell_checkbox.move(312, 251)
        self.search_space_sell_checkbox.setChecked(False)
        #self.search_space_sell_checkbox.stateChanged.connect(self.clickBox)

        # Label ROI Search Space:
        self.search_space_roi_label = QLabel(self)
        self.search_space_roi_label.setText('Roi:')
        self.search_space_roi_label.move(100, 270)
        # Checkbox ROI Search Space
        self.search_space_roi_checkbox = QCheckBox(self)
        self.search_space_roi_checkbox.move(120, 271)
        self.search_space_roi_checkbox.setChecked(False)
        #self.search_space_roi_checkbox.stateChanged.connect(self.clickBox)

        # Label STOPLOSS Search Space:
        self.search_space_stoploss_label = QLabel(self)
        self.search_space_stoploss_label.setText('Stoploss:')
        self.search_space_stoploss_label.move(150, 270)
        # Checkbox STOPLOSS Search Space
        self.search_space_stoploss_checkbox = QCheckBox(self)
        self.search_space_stoploss_checkbox.move(195, 271)
        self.search_space_stoploss_checkbox.setChecked(False)
        #self.search_space_stoploss_checkbox.stateChanged.connect(self.clickBox)

        # Label TRAILING Search Space:
        self.search_space_trailing_label = QLabel(self)
        self.search_space_trailing_label.setText('Trailing:')
        self.search_space_trailing_label.move(230, 270)
        # Checkbox TRAILING Search Space
        self.search_space_trailing_checkbox = QCheckBox(self)
        self.search_space_trailing_checkbox.move(269, 271)
        self.search_space_trailing_checkbox.setChecked(False)
        #self.search_space_trailing_checkbox.stateChanged.connect(self.clickBox)

        # Label PROTECTIONS Search Space:
        self.search_space_protections_label = QLabel(self)
        self.search_space_protections_label.setText('Protect:')
        self.search_space_protections_label.move(290, 270)
        # Checkbox PROTECTIONS Search Space
        self.search_space_protections_checkbox = QCheckBox(self)
        self.search_space_protections_checkbox.move(330, 271)
        self.search_space_protections_checkbox.setChecked(False)
        #self.search_space_protections_checkbox.stateChanged.connect(self.clickBox)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

