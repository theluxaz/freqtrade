import sys,os
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QComboBox, QLabel, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox,QPlainTextEdit,QDateEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot,QDate, QDateTime
from PyQt5 import QtCore,QtWidgets
from main import main
import json
import time
import datetime
import math
from collections import OrderedDict


computer_processing_power = 1.3   # 0.00001 to.. 2.0

strategy_json = [{"DEV":"DevLukas15min"},
                 {"PROD":"ProdLukas15min"},
                  {"BUYER HIGH":"BuyerDevHigh"},
                   {"BUYER MID":"BuyerDevMid"},
                    {"BUYER LOW":"BuyerDevLow"},
                     {"BUYER LONG UPTREND":"BuyerDevLongUptrend"},
                      {"BUYER SLOW DOWNTREND":"BuyerDevSlowDowntrend"},
                       {"BUYER LONG DOWNTREND":"BuyerDevLongDowntrend"},
                        {"BUYER DOWNTREND UPSWING":"BuyerDevDowntrendUpswing"}
                 ]


timeframes_json = [{"4":1631232000000},# 10 september 2021
                    {"3":1625097600000},# 1 july 2021
                 {"2":1617235200000},
                  {"1":1609464867000},
                   {"0":1600312000000}
                    # {"5":"BuyerDevLow"},
                    #  {"6":"BuyerDevLongUptrend"},
                    #   {"7":"BuyerDevSlowDowntrend"},
                    #    {"8":"BuyerDevLongDowntrend"},
                    #     {"0":"BuyerDevDowntrendUpswing"}
                 ]

configs_json = ["normal","nostalgia","nostalgia-other","older-classic"]

hyperopt_loss_functions = ["ShortTradeDurHyperOptLoss","OnlyProfitHyperOptLoss","SharpeHyperOptLoss","SharpeHyperOptLossDaily","SortinoHyperOptLoss",
              "SortinoHyperOptLossDaily","MaxDrawDownHyperOptLoss"]

indicators1_default = ['volatility', 'uptrend', 'uptrendsmall', 'sma50', 'sma200', 'sma400', 'sma10k']

config_file = "run-configuration.json"

fiat_currency="USDT"

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Freqtrade Strategy Tester'
        self.left = 300
        self.top = 200
        self.width = 850
        self.height = 380

        # Set strategies
        self.strategies = []
        self.strategies_label = []
        for pair in strategy_json:
            for key, value in pair.items():
                self.strategies_label.append(key)
                self.strategies.append(value)

        # Set timeframes
        self.timeframes = []
        self.timeframes_label = []
        for pair in timeframes_json:
            for key, value in pair.items():
                self.timeframes_label.append(key)
                self.timeframes.append(value)

        # Set configs
        self.configs = configs_json

        f = open(config_file)
        self.data = json.load(f)
        f.close()

        app.aboutToQuit.connect(self.on_click_save_json)

        self.backtesting_clicked = False
        self.show_plot_clicked = False
        self.hyperopt_clicked = False
        self.command_list = []

        self.processing_power = 0


        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.command = self.data["command"]


        # Label strategy
        self.label_strategy = QLabel(self)
        self.label_strategy.setText('Strategy:')
        self.label_strategy.move(25, 10)
        # Dropdown strategy
        self.combobox_strategy = QComboBox(self)
        self.combobox_strategy.setGeometry(20, 30, 220, 30)
        self.combobox_strategy.addItems(self.strategies_label)
        self.combobox_strategy.setCurrentIndex(self.data["strategy"])
        self.combobox_strategy.currentIndexChanged.connect(self.on_select_strategy)

        # Label Indicators 1
        self.indicator1_label = QLabel(self)
        self.indicator1_label.setText('Indicators 1:')
        self.indicator1_label.move(20, 80)
        # Textbox Indicator 1
        self.indicator1_textbox = QLineEdit(self)
        self.indicator1_textbox.move(90, 78)
        self.indicator1_textbox.resize(150,20)
        self.indicator1_textbox.setText(self.data["indicators1"]["text"])
        self.indicator1_textbox.editingFinished.connect(self.on_textchange_epochs)
        # Label Indicators 1 Default?
        self.indicator1_default_label = QLabel(self)
        self.indicator1_default_label.setText('Default:')
        self.indicator1_default_label.move(20, 100)

        # Checkbox Indicators 1 Default?
        self.indicator1_checkbox_default = QCheckBox(self)
        self.indicator1_checkbox_default.move(63, 101)
        self.indicator1_checkbox_default.setChecked(self.data["indicators1"]["default"])
        self.indicator1_checkbox_default.stateChanged.connect(self.checkbox_indicators1_default)
        # Checkbox Indicators 1 Enable
        self.indicator1_checkbox = QCheckBox(self)
        self.indicator1_checkbox.move(250, 82)
        self.indicator1_checkbox.setChecked(self.data["indicators1"]["enabled"])
        self.indicator1_checkbox.stateChanged.connect(self.checkbox_indicators1)


        # Label Indicators 2
        self.indicator2_label = QLabel(self)
        self.indicator2_label.setText('Indicators 2:')
        self.indicator2_label.move(20, 130)
        # Textbox Indicator 2
        self.indicator2_textbox = QLineEdit(self)
        self.indicator2_textbox.move(90, 128)
        self.indicator2_textbox.resize(150,20)
        self.indicator2_textbox.setText(self.data["indicators2"]["text"])
        self.indicator2_textbox.editingFinished.connect(self.on_textchange_indicators2)
        # Checkbox Indicators 2 Enable
        self.indicator2_checkbox = QCheckBox(self)
        self.indicator2_checkbox.move(250, 132)
        self.indicator2_checkbox.setChecked(self.data["indicators2"]["enabled"])
        self.indicator2_checkbox.stateChanged.connect(self.checkbox_indicators2)

        # Label Indicators 3
        self.indicator3_label = QLabel(self)
        self.indicator3_label.setText('Indicators 3:')
        self.indicator3_label.move(20, 160)
        # Textbox Indicator 3
        self.indicator3_textbox = QLineEdit(self)
        self.indicator3_textbox.move(90, 158)
        self.indicator3_textbox.resize(150,20)
        self.indicator3_textbox.setText(self.data["indicators3"]["text"])
        self.indicator3_textbox.editingFinished.connect(self.on_textchange_indicators3)
        # Checkbox Indicators 3 Enable
        self.indicator3_checkbox = QCheckBox(self)
        self.indicator3_checkbox.move(250, 162)
        self.indicator3_checkbox.setChecked(self.data["indicators3"]["enabled"])
        self.indicator3_checkbox.stateChanged.connect(self.checkbox_indicators3)


        # Time From label
        self.time_from_label = QLabel(self)
        self.time_from_label.setText('Time From:')
        self.time_from_label.move(310, 12)
        # Time From Dropdown
        self.time_from_dropdown = QComboBox(self)
        self.time_from_dropdown.setGeometry(310, 30, 150, 30)
        self.time_from_dropdown.addItems(self.timeframes_label)
        self.time_from_dropdown.setCurrentIndex(self.data["time"]["time_from_index"])
        self.time_from_dropdown.currentIndexChanged.connect(self.on_select_time_from)
        # Time From Calendar
        self.time_from_calendar = QDateEdit(self,calendarPopup=True)
        self.time_from_calendar.setGeometry(310, 30, 150, 30)
        self.time_from_calendar.setDateTime(QtCore.QDateTime.currentDateTime())
        self.time_from_calendar.dateChanged.connect(self.on_select_from_date)
        self.time_from_calendar.hide()
        if(self.data["time"]["time_from_date"] == True):
            self.time_from_calendar.show()
            self.time_from_dropdown.hide()
        # Time From label checkbox
        self.time_from_date_label = QLabel(self)
        self.time_from_date_label.setText('Date')
        self.time_from_date_label.move(420, 12)
        # Time From Checkbox Date
        self.time_from_checkbox_date = QCheckBox(self)
        self.time_from_checkbox_date.move(446, 13)
        self.time_from_checkbox_date.setChecked(self.data["time"]["time_from_date"])
        self.time_from_checkbox_date.stateChanged.connect(self.checkbox_time_from_date)
        # Time From label
        self.time_from_final_date_label = QLabel(self)
        self.time_from_final_date_label.setText(unix_to_datetime(self.data["time"]["time_from"],True,True))
        self.time_from_final_date_label.move(404, 72)

        ## ^ ^ WHEN THIS ONE IS UPDATED, UPDATE THE TIME UNTIL TO THE NEXT NUMBER AUTOMATICALLY


        # Time From to Util arrows label
        self.time_arrow_label = QLabel(self)
        self.time_arrow_label.setText('----->')
        self.time_arrow_label.move(470, 36)
        self.time_arrow_lower_label = QLabel(self)
        self.time_arrow_lower_label.setText('---->')
        self.time_arrow_lower_label.move(470, 72)


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
        self.time_until_checkbox_date.setChecked(self.data["time"]["time_until_date"])
        self.time_until_checkbox_date.stateChanged.connect(self.checkbox_time_until_date)
        # Time Until Dropdown
        self.time_until_dropdown = QComboBox(self)
        self.time_until_dropdown.setGeometry(510, 30, 150, 30)
        self.time_until_dropdown.addItems(self.timeframes_label)
        self.time_until_dropdown.setCurrentIndex(self.data["time"]["time_until_index"])
        self.time_until_dropdown.currentIndexChanged.connect(self.on_select_time_until)
        # Time Until Calendar
        self.time_until_calendar = QDateEdit(self,calendarPopup=True)
        self.time_until_calendar.setGeometry(510, 30, 150, 30)
        self.time_until_calendar.setDateTime(QtCore.QDateTime.currentDateTime())
        self.time_until_calendar.dateChanged.connect(self.on_select_until_date)
        self.time_until_calendar.hide()
        if(self.data["time"]["time_until_date"] == True):
            self.time_until_calendar.show()
            self.time_until_dropdown.hide()
        # Time Until Checkbox
        self.time_until_checkbox = QCheckBox(self)
        self.time_until_checkbox.move(667, 37)
        self.time_until_checkbox.setChecked(True)
        self.time_until_checkbox.setChecked(self.data["time"]["time_until_enabled"])
        self.time_until_checkbox.stateChanged.connect(self.checkbox_time_until)
        if(self.data["time"]["time_until_enabled"] == False):
            self.time_until_checkbox_date.setEnabled(False)
            if(self.data["time"]["time_until_date"] == True):
                self.time_until_calendar.setEnabled(False)
            else:
                self.time_until_dropdown.setEnabled(False)
        # Time From final date label
        self.time_until_final_date_label = QLabel(self)
        self.time_until_final_date_label.setText(unix_to_datetime(self.data["time"]["time_until"],True,True))
        self.time_until_final_date_label.move(504, 72)
        # Time difference label
        self.time_difference_label = QLabel(self)
        self.time_difference_label.setText("Days: " + str(days_between_timestamps(self.data["time"]["time_from"],self.data["time"]["time_until"])))
        self.time_difference_label.move(610, 72)



        # Download Data label
        self.label_download_data = QLabel(self)
        self.label_download_data.setText('Download data:')
        self.label_download_data.move(726, 12)
        # Download Data 15m
        self.backtest_button=QPushButton('15m',self)
        self.backtest_button.setToolTip('Download 15m data for the selected pairs')
        self.backtest_button.move(690, 32)
        self.backtest_button.clicked.connect(self.on_click_15m)
        # Download Data 1h
        self.backtest_button=QPushButton('1h',self)
        self.backtest_button.setToolTip('Download 1h data for the selected pairs')
        self.backtest_button.move(760, 32)
        self.backtest_button.clicked.connect(self.on_click_1h)



         # Label Pairs 1
        self.pairs1_label = QLabel(self)
        self.pairs1_label.setText('Pairs:')
        self.pairs1_label.move(320, 100)
        # Textbox Pairs 1
        self.pairs1_textbox = QPlainTextEdit(self)
        self.pairs1_textbox.move(355, 100)
        self.pairs1_textbox.resize(60,246)
        self.pairs1_textbox.setPlainText(self.data["pairs1"])
        self.pairs1_textbox.textChanged.connect(self.on_textchange_pairs1)

         # Label Cache Pairs 2
        self.pairs2_label = QLabel(self)
        self.pairs2_label.setText('Cache:')
        self.pairs2_label.move(470, 100)
        # Textbox Cache Pairs 2
        self.pairs2_textbox = QPlainTextEdit(self)
        self.pairs2_textbox.move(510, 100)
        self.pairs2_textbox.resize(60,246)
        self.pairs2_textbox.setPlainText(self.data["pairs2"])
        self.pairs2_textbox.textChanged.connect(self.on_textchange_pairs2)

         # Label All Pairs 3
        self.pairs3_label = QLabel(self)
        self.pairs3_label.setText('All:')
        self.pairs3_label.move(580, 100)
        # Textbox All Pairs 3
        self.pairs3_textbox = QPlainTextEdit(self)
        self.pairs3_textbox.move(600, 100)
        self.pairs3_textbox.resize(60,246)
        self.pairs3_textbox.setPlainText(self.data["pairs3"])
        self.pairs3_textbox.textChanged.connect(self.on_textchange_pairs3)



        # Label Hyperopt
        self.hyperopt_label = QLabel(self)
        self.hyperopt_label.setText('Hyperopt:')
        self.hyperopt_label.move(20, 220)

        # Checkbox hyperopt
        self.hyperopt_checkbox = QCheckBox(self)
        self.hyperopt_checkbox.move(71, 221)
        self.hyperopt_checkbox.setChecked(self.data["hyperopt"]["hyperopt"])
        self.hyperopt_checkbox.stateChanged.connect(self.checkbox_hyperopt)


        self.addSearchSpace()


        # Button backtest
        self.backtest_button=QPushButton('Backtest',self)
        self.backtest_button.setToolTip('Backtest Data')
        self.backtest_button.move(670,324)
        self.backtest_button.clicked.connect(self.on_click_backtest)

        # Button Show Plot
        self.plot_button=QPushButton('Show Plot',self)
        self.plot_button.setToolTip('Create A plot for the selected pair')
        self.plot_button.move(760,324)
        self.plot_button.clicked.connect(self.on_click_plot)



        # Config  label
        self.label_config = QLabel(self)
        self.label_config.setText('Config:')
        self.label_config.move(735, 72)
        # Config Default label
        self.label_config_default = QLabel(self)
        self.label_config_default.setText('Default:')
        self.label_config_default.move(675, 100)
        # Config Default checkbox
        self.checkbox_config_default = QCheckBox(self)
        self.checkbox_config_default.move(720,100)
        self.checkbox_config_default.setChecked(self.data["config_default"])
        self.checkbox_config_default.stateChanged.connect(self.checkbox_config)
        # Config dropdown
        self.dropdown_config = QComboBox(self)
        self.dropdown_config.setGeometry(750, 96, 85, 20)
        self.dropdown_config.addItems(self.configs)
        self.dropdown_config.setCurrentIndex(self.data["config_selection"])
        self.dropdown_config.currentIndexChanged.connect(self.on_select_config)
        if(self.data["config_default"]):
            self.dropdown_config.hide()

        # Button load config pairs
        self.backtest_button=QPushButton('Config Pairs',self)
        self.backtest_button.move(750,120)
        self.backtest_button.clicked.connect(self.load_config_pairs)


        # # Plot Pair label
        # self.label_plot_pair = QLabel(self)
        # self.label_plot_pair.setText('Plot Pair:')
        # self.label_plot_pair.move(705, 300)
        # Plot Pair dropdown
        self.dropdown_plot_pair = QComboBox(self)
        self.dropdown_plot_pair.setGeometry(761, 300, 73, 20)
        self.dropdown_plot_pair.addItems(self.data["pairs1"].split())
        self.dropdown_plot_pair.setCurrentIndex(self.data["plot_pair"])
        self.dropdown_plot_pair.currentIndexChanged.connect(self.on_select_plot_pair)



        # Pairs no label
        self.label_pairs_no = QLabel(self)
        self.label_pairs_no.setText(self.get_pairlist_length())
        self.label_pairs_no.move(690, 126)
        self.label_pairs_no.adjustSize()
        # Processing Backtest  label
        self.label_backtest_process = QLabel(self)
        self.label_backtest_process.move(690, 155)
        self.get_backtest_processing_power()
        # Processing Plot  label
        self.label_plot_process = QLabel(self)
        self.label_plot_process.move(690, 175)
        self.get_plot_processing_power()
        # Processing Hyperopt  label
        self.label_hyperopt_process = QLabel(self)
        self.label_hyperopt_process.move(690, 195)
        self.get_hyperopt_processing_power()


        # Profit plot label
        self.display_profit_label = QLabel(self)
        self.display_profit_label.setText('Profit')
        self.display_profit_label.move(789,275)
        # Profit plot Checkbox Date
        self.display_profit_checkbox = QCheckBox(self)
        self.display_profit_checkbox.move(820,275)
        self.display_profit_checkbox.setChecked(self.data["plot_profit"])
        self.display_profit_checkbox.stateChanged.connect(self.checkbox_profit)

        # Label Run Command args
        self.run_command_args_label = QLabel(self)

        self.run_command_args_label.setText(self.data["command"])
        self.run_command_args_label.move(18,356)


        self.show()
        self.update_hyperopt()

    def addSearchSpace(self):


        # Label Search Space:
        self.search_space_label = QLabel(self)
        self.search_space_label.setText('Search Space')
        self.search_space_label.move(190, 230)


        # Label Epochs
        self.label_epochs = QLabel(self)
        self.label_epochs.setText('Epochs:')
        self.label_epochs.move(50, 250)
        # Textbox Epochs
        self.textbox_epochs = QLineEdit(self)
        self.textbox_epochs.move(54, 266)
        self.textbox_epochs.resize(30,18)
        self.textbox_epochs.setText(self.data["hyperopt"]["epochs"])
        self.textbox_epochs.editingFinished.connect(self.on_textchange_epochs)


        # Label Loss Function
        self.label_loss_function = QLabel(self)
        self.label_loss_function.setText('Loss function:')
        self.label_loss_function.move(20, 300)
        # Dropdown Loss Function
        self.combobox_loss_function = QComboBox(self)
        self.combobox_loss_function.setGeometry(17, 320, 200, 30)
        self.combobox_loss_function.addItems(hyperopt_loss_functions)
        self.combobox_loss_function.setCurrentIndex(self.data["hyperopt"]["loss_function"])
        self.combobox_loss_function.currentIndexChanged.connect(self.on_select_loss_function)

        # Button Hyperopt
        self.hyperopt_button=QPushButton('Hyperopt',self)
        self.hyperopt_button.move(255,323)
        self.hyperopt_button.setToolTip('Start Hyperopting')
        self.hyperopt_button.clicked.connect(self.on_click_hyperopt)

        # Label ALL Search Space:
        self.search_space_all_label = QLabel(self)
        self.search_space_all_label.setText('All:')
        self.search_space_all_label.move(100, 250)
        # Checkbox ALL Search Space
        self.search_space_all_checkbox = QCheckBox(self)
        self.search_space_all_checkbox.move(118, 251)
        self.search_space_all_checkbox.setChecked(self.data["hyperopt"]["search_space_all"])
        self.search_space_all_checkbox.stateChanged.connect(self.checkbox_search_space_all)

        # Label DEFAULT Search Space:
        self.search_space_default_label = QLabel(self)
        self.search_space_default_label.setText('Default:')
        self.search_space_default_label.move(150, 250)
        # Checkbox DEFAULT Search Space
        self.search_space_default_checkbox = QCheckBox(self)
        self.search_space_default_checkbox.move(191, 251)
        self.search_space_default_checkbox.setChecked(self.data["hyperopt"]["search_space_default"])
        self.search_space_default_checkbox.stateChanged.connect(self.checkbox_search_space_default)

        # Label BUY Search Space:
        self.search_space_buy_label = QLabel(self)
        self.search_space_buy_label.setText('Buy:')
        self.search_space_buy_label.move(230, 250)
        # Checkbox BUY Search Space
        self.search_space_buy_checkbox = QCheckBox(self)
        self.search_space_buy_checkbox.move(254, 251)
        self.search_space_buy_checkbox.setChecked(self.data["hyperopt"]["search_space_buy"])
        self.search_space_buy_checkbox.stateChanged.connect(self.checkbox_search_space_buy)

        # Label SELL Search Space:
        self.search_space_sell_label = QLabel(self)
        self.search_space_sell_label.setText('Sell:')
        self.search_space_sell_label.move(290, 250)
        # Checkbox SELL Search Space
        self.search_space_sell_checkbox = QCheckBox(self)
        self.search_space_sell_checkbox.move(312, 251)
        self.search_space_sell_checkbox.setChecked(self.data["hyperopt"]["search_space_sell"])
        self.search_space_sell_checkbox.stateChanged.connect(self.checkbox_search_space_sell)

        # Label ROI Search Space:
        self.search_space_roi_label = QLabel(self)
        self.search_space_roi_label.setText('Roi:')
        self.search_space_roi_label.move(100, 270)
        # Checkbox ROI Search Space
        self.search_space_roi_checkbox = QCheckBox(self)
        self.search_space_roi_checkbox.move(120, 271)
        self.search_space_roi_checkbox.setChecked(self.data["hyperopt"]["search_space_roi"])
        self.search_space_roi_checkbox.stateChanged.connect(self.checkbox_search_space_roi)

        # Label STOPLOSS Search Space:
        self.search_space_stoploss_label = QLabel(self)
        self.search_space_stoploss_label.setText('Stoploss:')
        self.search_space_stoploss_label.move(150, 270)
        # Checkbox STOPLOSS Search Space
        self.search_space_stoploss_checkbox = QCheckBox(self)
        self.search_space_stoploss_checkbox.move(195, 271)
        self.search_space_stoploss_checkbox.setChecked(self.data["hyperopt"]["search_space_stoploss"])
        self.search_space_stoploss_checkbox.stateChanged.connect(self.checkbox_search_space_stoploss)

        # Label TRAILING Search Space:
        self.search_space_trailing_label = QLabel(self)
        self.search_space_trailing_label.setText('Trailing:')
        self.search_space_trailing_label.move(230, 270)
        # Checkbox TRAILING Search Space
        self.search_space_trailing_checkbox = QCheckBox(self)
        self.search_space_trailing_checkbox.move(269, 271)
        self.search_space_trailing_checkbox.setChecked(self.data["hyperopt"]["search_space_trailing"])
        self.search_space_trailing_checkbox.stateChanged.connect(self.checkbox_search_space_trailing)

        # Label PROTECTIONS Search Space:
        self.search_space_protections_label = QLabel(self)
        self.search_space_protections_label.setText('Protect:')
        self.search_space_protections_label.move(290, 270)
        # Checkbox PROTECTIONS Search Space
        self.search_space_protections_checkbox = QCheckBox(self)
        self.search_space_protections_checkbox.move(330, 271)
        self.search_space_protections_checkbox.setChecked(self.data["hyperopt"]["search_space_protect"])
        self.search_space_protections_checkbox.stateChanged.connect(self.checkbox_search_space_protect)


    def update_hyperopt(self):
        if self.data["hyperopt"]["hyperopt"]== True:
            self.search_space_label.show()
            self.label_loss_function.show()
            self.combobox_loss_function.show()
            self.hyperopt_button.show()
            self.search_space_all_label.show()
            self.search_space_all_checkbox.show()
            self.search_space_default_label.show()
            self.search_space_default_checkbox.show()
            self.search_space_buy_label.show()
            self.search_space_buy_checkbox.show()
            self.search_space_sell_label.show()
            self.search_space_sell_checkbox.show()
            self.search_space_roi_label.show()
            self.search_space_roi_checkbox.show()
            self.search_space_stoploss_label.show()
            self.search_space_stoploss_checkbox.show()
            self.search_space_trailing_label.show()
            self.search_space_trailing_checkbox.show()
            self.search_space_protections_label.show()
            self.search_space_protections_checkbox.show()
            self.label_epochs.show()
            self.textbox_epochs.show()
        else:
            self.search_space_label.hide()
            self.label_loss_function.hide()
            self.combobox_loss_function.hide()
            self.hyperopt_button.hide()
            self.search_space_all_label.hide()
            self.search_space_all_checkbox.hide()
            self.search_space_default_label.hide()
            self.search_space_default_checkbox.hide()
            self.search_space_buy_label.hide()
            self.search_space_buy_checkbox.hide()
            self.search_space_sell_label.hide()
            self.search_space_sell_checkbox.hide()
            self.search_space_roi_label.hide()
            self.search_space_roi_checkbox.hide()
            self.search_space_stoploss_label.hide()
            self.search_space_stoploss_checkbox.hide()
            self.search_space_trailing_label.hide()
            self.search_space_trailing_checkbox.hide()
            self.search_space_protections_label.hide()
            self.search_space_protections_checkbox.hide()
            self.label_epochs.hide()
            self.textbox_epochs.hide()


    def update_display_dates(self):
        print("Updating display dates")
        self.time_from_final_date_label.setText(unix_to_datetime(self.data["time"]["time_from"],True,True))
        self.time_from_final_date_label.adjustSize()
        self.time_until_final_date_label.setText(unix_to_datetime(self.data["time"]["time_until"],True,True))
        self.time_until_final_date_label.adjustSize()
        self.time_difference_label.setText("Days: " + str(days_between_timestamps(self.data["time"]["time_from"],self.data["time"]["time_until"])))
        self.time_difference_label.adjustSize()
        self.get_backtest_processing_power()
        self.get_plot_processing_power()
        self.get_hyperopt_processing_power()


    @pyqtSlot()
    def on_click_save_json(self):
        print("Saving data to JSON")
        try:
            with open(config_file, 'w') as file:
                json.dump(self.data, file)
        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_click_backtest(self):
        if(self.backtesting_clicked):
            main(self.command_list)
            self.backtesting_clicked = False
            self.show_plot_clicked = False
            self.hyperopt_clicked = False
        else:
            self.update_config_pairs()
            self.on_click_save_json()
            self.get_backtest_processing_power()
            time_until = ""
            if(self.data["time"]["time_until_enabled"]):
                time_until = self.data["time"]["time_until"]


            command_list = ["backtesting","--config", "user_data/"+self.data["config"], "--timeframe" , "15m", "--strategy",self.strategies[self.data["strategy"]],"--export","trades","--timerange="+str(self.data["time"]["time_from"])+"-"+str(time_until)]

            print(command_list)
            self.command_list = command_list
            self.data["command"] = ' '.join(command_list)
            self.run_command_args_label.setText(self.data["command"])
            self.hyperopt_clicked = False
            self.backtesting_clicked = True
            self.show_plot_clicked = False

    @pyqtSlot()
    def on_click_plot(self):
        if(self.show_plot_clicked):
            main(self.command_list)
            self.backtesting_clicked = False
            self.show_plot_clicked = False
            self.hyperopt_clicked = False
        else:
            self.update_config_pairs()
            self.on_click_save_json()
            self.get_plot_processing_power()
            print("1")
            time_until = ""
            if(self.data["time"]["time_until_enabled"]):
                time_until = self.data["time"]["time_until"]

            pair = self.data["pairs1"].split()[self.data["plot_pair"]]

            command = "plot-dataframe"
            if(self.data["plot_profit"]):
                command = "plot-profit"

            print("2")

            indicators1 = []
            indicators2 = []
            indicators3 = []
            if(self.data["indicators1"]["default"] and self.data["plot_profit"]==False):
                indicators1 = ["--indicators1"]
                for item in indicators1_default:
                    indicators1.append(item)
            if(self.data["indicators1"]["enabled"] and self.data["plot_profit"]==False):
                if(len(indicators1) <= 0):
                    indicators1 = ["--indicators1"]
                for item in self.data["indicators1"]["text"].split():
                    indicators1.append(item)

            if(self.data["indicators2"]["enabled"] and self.data["plot_profit"]==False):
                indicators2 = ["--indicators2"]
                for item in self.data["indicators2"]["text"].split():
                    indicators2.append(item)
            if(self.data["indicators3"]["enabled"] and self.data["plot_profit"]==False):
                indicators3 = ["--indicators3"]
                for item in self.data["indicators3"]["text"].split():
                    indicators3.append(item)

            print("3")
            command_list = [command,"--config", "user_data/"+self.data["config"], "--strategy", self.strategies[self.data["strategy"]],"-p",pair+"/"+fiat_currency,"--timerange="+str(self.data["time"]["time_from"])+"-"+str(time_until)]

            if(len(indicators1)>0):
                command_list.extend(indicators1)
            if(len(indicators2)>0):
                command_list.extend(indicators2)
            if(len(indicators3)>0):
                command_list.extend(indicators3)

            print(command_list)
            self.command_list = command_list
            self.data["command"] = ' '.join(command_list)
            self.run_command_args_label.setText(self.data["command"])
            self.hyperopt_clicked = False
            self.backtesting_clicked = False
            self.show_plot_clicked = True

    @pyqtSlot()
    def on_click_hyperopt(self):
        if(self.data["hyperopt"]["hyperopt"]):
            if(self.hyperopt_clicked):
                main(self.command_list)
                self.backtesting_clicked = False
                self.show_plot_clicked = False
                self.hyperopt_clicked = False
            else:
                self.update_config_pairs()
                self.on_click_save_json()
                self.get_hyperopt_processing_power()
                time_until = ""
                if(self.data["time"]["time_until_enabled"]):
                    time_until = self.data["time"]["time_until"]

                search_spaces = ["--spaces"]
                if(self.data["hyperopt"]["search_space_all"]):
                    search_spaces.append("all")
                if(self.data["hyperopt"]["search_space_default"]):
                    search_spaces.append("default")
                if(self.data["hyperopt"]["search_space_buy"]):
                    search_spaces.append("buy")
                if(self.data["hyperopt"]["search_space_sell"]):
                    search_spaces.append("sell")
                if(self.data["hyperopt"]["search_space_roi"]):
                    search_spaces.append("roi")
                if(self.data["hyperopt"]["search_space_stoploss"]):
                    search_spaces.append("stoploss")
                if(self.data["hyperopt"]["search_space_trailing"]):
                    search_spaces.append("trailing")
                if(self.data["hyperopt"]["search_space_protect"]):
                    search_spaces.append("protect")




                command_list = ["hyperopt","--config", "user_data/"+self.data["config"], "--timeframe" , "15m", "--strategy", self.strategies[self.data["strategy"]],"-e",self.data["hyperopt"]["epochs"],"--timerange="+str(self.data["time"]["time_from"])+"-"+str(time_until),"--hyperopt-loss",hyperopt_loss_functions[self.data["hyperopt"]["loss_function"]], "--print-all"]

                if(len(search_spaces)>1):
                    command_list.extend(search_spaces)
                else:
                    print("At least one search space should be selected!")

                print(command_list)
                self.command_list = command_list
                self.data["command"] = ' '.join(command_list)
                self.run_command_args_label.setText(self.data["command"])
                self.hyperopt_clicked = True
                self.backtesting_clicked = False
                self.show_plot_clicked = False
        else:
            print("Hyperopt is disabled")

    @pyqtSlot()
    def on_click_15m(self):
        self.update_config_pairs(self)
        self.on_click_save_json()
        main(["download-data", "-t" , "15m"])

    @pyqtSlot()
    def on_click_1h(self):
        self.update_config_pairs(self)
        self.on_click_save_json()
        main(["download-data", "-t" , "1h"])

    @pyqtSlot()
    def checkbox_indicators1(self):
        if(self.data["indicators1"]["enabled"] == True):
            self.data["indicators1"]["enabled"] = False
            self.indicator1_textbox.setEnabled(False)
        else:
            self.data["indicators1"]["enabled"] = True
            self.indicator1_textbox.setEnabled(True)

    @pyqtSlot()
    def checkbox_indicators1_default(self):
        if(self.data["indicators1"]["default"] == True):
            self.data["indicators1"]["default"] = False
        else:
            self.data["indicators1"]["default"] = True

    @pyqtSlot()
    def checkbox_indicators2(self):
        if(self.data["indicators2"]["enabled"] == True):
            self.data["indicators2"]["enabled"] = False
            self.indicator2_textbox.setEnabled(False)
        else:
            self.data["indicators2"]["enabled"] = True
            self.indicator2_textbox.setEnabled(True)

    @pyqtSlot()
    def checkbox_indicators3(self):
        if(self.data["indicators3"]["enabled"] == True):
            self.data["indicators3"]["enabled"] = False
            self.indicator3_textbox.setEnabled(False)
        else:
            self.data["indicators3"]["enabled"] = True
            self.indicator3_textbox.setEnabled(True)

    @pyqtSlot()
    def on_textchange_indicators1(self):
        self.data["indicators1"]["text"] = self.indicator1_textbox.text()
    @pyqtSlot()
    def on_textchange_indicators2(self):
        self.data["indicators2"]["text"] = self.indicator2_textbox.text()
    @pyqtSlot()
    def on_textchange_indicators3(self):
        self.data["indicators3"]["text"] = self.indicator3_textbox.text()


    @pyqtSlot()
    def on_textchange_pairs1(self):
        self.data["pairs1"] = self.pairs1_textbox.toPlainText().upper()
        self.dropdown_plot_pair.clear()
        self.dropdown_plot_pair.addItems(self.data["pairs1"].split())
        self.label_pairs_no.setText("Pairs: "+str(len(self.data["pairs1"].split())))
        self.label_pairs_no.adjustSize()
        self.get_backtest_processing_power()
        self.get_hyperopt_processing_power()
    @pyqtSlot()
    def on_textchange_pairs2(self):
        self.data["pairs2"] = self.pairs2_textbox.toPlainText().upper()
    @pyqtSlot()
    def on_textchange_pairs3(self):
        self.data["pairs3"] = self.pairs3_textbox.toPlainText().upper()



    @pyqtSlot()
    def checkbox_hyperopt(self):
        if(self.data["hyperopt"]["hyperopt"] == True):
            self.data["hyperopt"]["hyperopt"] = False
        else:
            self.data["hyperopt"]["hyperopt"] = True
        self.update_hyperopt()

    @pyqtSlot()
    def on_textchange_epochs(self):
        self.data["hyperopt"]["epochs"] = self.textbox_epochs.text()

    @pyqtSlot()
    def checkbox_search_space_all(self):
        if(self.data["hyperopt"]["search_space_all"] == True):
            self.data["hyperopt"]["search_space_all"] = False
        else:
            self.data["hyperopt"]["search_space_all"] = True
    @pyqtSlot()
    def checkbox_search_space_default(self):
        if(self.data["hyperopt"]["search_space_default"] == True):
            self.data["hyperopt"]["search_space_default"] = False
        else:
            self.data["hyperopt"]["search_space_default"] = True
    @pyqtSlot()
    def checkbox_search_space_buy(self):
        if(self.data["hyperopt"]["search_space_buy"] == True):
            self.data["hyperopt"]["search_space_buy"] = False
        else:
            self.data["hyperopt"]["search_space_buy"] = True
    @pyqtSlot()
    def checkbox_search_space_sell(self):
        if(self.data["hyperopt"]["search_space_sell"] == True):
            self.data["hyperopt"]["search_space_sell"] = False
        else:
            self.data["hyperopt"]["search_space_sell"] = True
    @pyqtSlot()
    def checkbox_search_space_roi(self):
        if(self.data["hyperopt"]["search_space_roi"] == True):
            self.data["hyperopt"]["search_space_roi"] = False
        else:
            self.data["hyperopt"]["search_space_roi"] = True
    @pyqtSlot()
    def checkbox_search_space_stoploss(self):
        if(self.data["hyperopt"]["search_space_stoploss"] == True):
            self.data["hyperopt"]["search_space_stoploss"] = False
        else:
            self.data["hyperopt"]["search_space_stoploss"] = True
    @pyqtSlot()
    def checkbox_search_space_trailing(self):
        if(self.data["hyperopt"]["search_space_trailing"] == True):
            self.data["hyperopt"]["search_space_trailing"] = False
        else:
            self.data["hyperopt"]["search_space_trailing"] = True
    @pyqtSlot()
    def checkbox_search_space_protect(self):
        if(self.data["hyperopt"]["search_space_protect"] == True):
            self.data["hyperopt"]["search_space_protect"] = False
        else:
            self.data["hyperopt"]["search_space_protect"] = True


    @pyqtSlot()
    def checkbox_time_from_date(self):
        if(self.data["time"]["time_from_date"] == True):
            self.data["time"]["time_from_date"] = False
            self.time_from_dropdown.show()
            self.time_from_calendar.hide()
        else:
            self.data["time"]["time_from_date"] = True
            self.time_from_calendar.show()
            self.time_from_dropdown.hide()

    @pyqtSlot()
    def checkbox_time_until_date(self):
        if(self.data["time"]["time_until_date"] == True):
            self.data["time"]["time_until_date"] = False
            self.time_until_dropdown.show()
            self.time_until_calendar.hide()
        else:
            self.data["time"]["time_until_date"] = True
            self.time_until_calendar.show()
            self.time_until_dropdown.hide()

    @pyqtSlot()
    def checkbox_time_until(self):
        if(self.data["time"]["time_until_enabled"] == True):
            self.data["time"]["time_until_enabled"] = False
            self.time_until_checkbox_date.setEnabled(False)
            if(self.data["time"]["time_until_date"] == True):
                self.time_until_calendar.setEnabled(False)
            else:
                self.time_until_dropdown.setEnabled(False)
        else:
            self.data["time"]["time_until_enabled"] = True
            self.time_until_checkbox_date.setEnabled(True)
            if(self.data["time"]["time_until_date"] == True):
                self.time_until_calendar.setEnabled(True)
            else:
                self.time_until_dropdown.setEnabled(True)

    @pyqtSlot()
    def checkbox_profit(self):
        if(self.data["plot_profit"] == True):
            self.data["plot_profit"] = False
        else:
            self.data["plot_profit"] = True

    @pyqtSlot()
    def checkbox_config(self):
        if(self.data["config_default"] == True):
            self.data["config_default"] = False
            self.dropdown_config.show()
        else:
            self.data["config"] = "config.json"
            self.data["config_default"] = True
            self.dropdown_config.hide()

    def on_select_strategy(self,i):
        self.data["strategy"] = i
    def on_select_loss_function(self,i):
        self.data["hyperopt"]["loss_function"] = i

    def on_select_time_from(self,i):
        self.data["time"]["time_from_index"] = i
        timestamp = self.timeframes[i]
        self.data["time"]["time_from"] = timestamp
        self.update_display_dates()

    def on_select_time_until(self,i):
        self.data["time"]["time_until_index"] = i
        timestamp = self.timeframes[i]
        self.data["time"]["time_until"] = timestamp
        self.update_display_dates()

    def on_select_config(self,i):
        self.data["config_selection"] = i
        config = self.configs[i]
        self.data["config"] = "config-"+str(config)+".json"

    def on_select_plot_pair(self,i):
        self.data["plot_pair"] = i


    def on_select_from_date(self,date):
        print("Changing from date")
        py_date = date.toPyDate()
        final_date = datetime.datetime(
            year=py_date.year,
            month=py_date.month,
            day=py_date.day,
            )
        final_timestamp = final_date.timestamp() * 1000
        self.data["time"]["time_from"] = int(final_timestamp)
        self.update_display_dates()


    def on_select_until_date(self,date):
        print("Changing until date")
        py_date = date.toPyDate()
        final_date = datetime.datetime(
            year=py_date.year,
            month=py_date.month,
            day=py_date.day,
            )
        final_timestamp = final_date.timestamp() * 1000
        self.data["time"]["time_until"] = int(final_timestamp)
        self.update_display_dates()



    # Updates chosen chosen with pairs from GUI
    def update_config_pairs(self):
        config_url = file_dir+"/user_data/"+self.data["config"]
        print(config_url)
        f = open(config_url)
        config_json = json.load(f)
        f.close()

        pairs = self.data["pairs1"].split()
        processed_pairs =[]
        for pair in pairs:
            processed_pairs.append(pair+"/"+fiat_currency)



        config_json["exchange"]["pair_whitelist"] = processed_pairs
        config_json = update_config_funds(config_json)
        try:
            with open(config_url, 'w') as file:
                json.dump(config_json, file)
        except Exception as e:
            print(e)

    # Loads the pairlist from config to the GUI
    def load_config_pairs(self):
        config_url = file_dir+"/user_data/"+self.data["config"]
        f = open(config_url)
        config_json = json.load(f)
        f.close()

        processed_pair_text=""

        for pair in config_json["exchange"]["pair_whitelist"]:
            processed_pair = pair.strip("/"+fiat_currency)
            processed_pair_text += (processed_pair+"/n")
        self.data["pairs1"] = processed_pair_text
        self.label_pairs_no.setText("Pairs: "+str(len(config_json["exchange"]["pair_whitelist"])))
        self.label_pairs_no.adjustSize()
        self.get_backtest_processing_power()
        self.get_hyperopt_processing_power()


    def get_pairlist_length(self):
        pairs = self.data["pairs1"].split()
        if(pairs):
            return "Pairs: "+str(len(pairs))
        else:
            return "0"

    def get_backtest_processing_power(self):
        time=0.1
        days = days_between_timestamps(self.data["time"]["time_from"],self.data["time"]["time_until"])
        pairs = len(self.data["pairs1"].split())
        if(pairs <= 6):
            days_from_25 = days / 50
            days_ratio = (1+(0.135 *(days_from_25)))
            pair_time= pairs *1.8
            pair_time = pair_time  + (0.4*math.pow( 1.22, pair_time ))
            time = (pair_time * (days_ratio) )
            time += 2.5
        else:
            days_from_25 = days / 50
            days_ratio = (1+(0.135 *(days_from_25)))
            pair_time= pairs *2.0
            pair_time = pair_time  + (0.10*math.pow( 1.16, pair_time ))
            time = (pair_time * (days_ratio) )
            time += 2.0
        time = round(time +  ((time/2 *((computer_processing_power-1.0)*-1))),1)
        self.label_backtest_process.setText('Backtest-Pw: '+str(time)+"s")

    def get_plot_processing_power(self):
        days = days_between_timestamps(self.data["time"]["time_from"],self.data["time"]["time_until"])
        time1 = 5
        time1= time1 + (days *0.075)
        time2 = (0.16*math.pow( 1.05, days/5 ))
        final_time= time1 + time2
        final_time = round(final_time +  ((final_time/2 *((computer_processing_power-1.0)*-1))),1)
        self.label_plot_process.setText('Plotting-Pw:  '+str(final_time)+"s")

    ##TO FINISH LATER
    def get_hyperopt_processing_power(self):
        # time=0.1
        # days = days_between_timestamps(self.data["time"]["time_from"],self.data["time"]["time_until"])
        # pairs = len(self.data["pairs1"].split())
        # if(pairs <= 6):
        #     days_from_25 = days / 50
        #     days_ratio = (1+(0.135 *(days_from_25)))
        #     pair_time= pairs *1.8
        #     pair_time = pair_time  + (0.4*math.pow( 1.22, pair_time ))
        #     time = (pair_time * (days_ratio) )
        #     time += 2.5
        # else:
        #     days_from_25 = days / 50
        #     days_ratio = (1+(0.135 *(days_from_25)))
        #     pair_time= pairs *2.0
        #     pair_time = pair_time  + (0.10*math.pow( 1.16, pair_time ))
        #     time = (pair_time * (days_ratio) )
        #     time += 2.0
        # time = round(time +  ((time/2 *((computer_processing_power-1.0)*-1))),1)
        self.label_hyperopt_process.setText('Hyperopt-Pw: '+"??"+"s")


    def closeEvent(self, event):
        self.on_click_save_json()
        sys.exit(0)

    # Updates the balance and order size for the config
def update_config_funds(config_json):
    config_json["dry_run_wallet"] = len(config_json["exchange"]["pair_whitelist"])*1000
    config_json["stake_amount"] = 900
    return config_json

def unix_to_datetime(timestamp,to_string,to_simple):
    if(to_string):
        from_date_s = datetime.datetime.fromtimestamp(timestamp/1000)
        if(to_simple):
            return from_date_s.strftime("%d %b %Y")
        else:
            return from_date_s.strftime("%d %b %Y %H:%M:%S")
    else:
        return datetime.datetime.fromtimestamp(timestamp/1000)

def datetime_to_unix(date,from_string):
    if(from_string):
        date_obj = datetime.datetime.strptime(date, "%d %b %Y %H:%M:%S")
        return date_obj.timestamp() * 1000
    else:
        return date.timestamp() * 1000

def days_between_timestamps(from_timestamp,until_timestamp):
    difference = until_timestamp - from_timestamp
    difference = difference /1000
    days = int(difference // (24 * 3600))
    return days


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

