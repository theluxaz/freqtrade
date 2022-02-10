import sys, os

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QComboBox, QLabel, QCheckBox, QScrollBar
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, \
    QPlainTextEdit, QDateEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QDate, QDateTime
from PyQt5 import QtCore, QtWidgets
from importlib import reload
from main import main
import json
import time
import datetime
import math

from importlib import reload, import_module

## use __ autopep8 __ formatter for the whole project (apart from this file)
## --in-place --aggressive --ignore E402 $FilePath$




computer_processing_power = 1.3  # 0.00001 to.. 2.0

balance_per_pair=1000

stake_amount=800

strategy_json = [{"DEV": "DevLukas15min"},
                 {"PROD": "ProdLukas15min"},
                 {"HIGH": "BuyerDevHigh"},
                 {"MID": "BuyerDevMid"},
                 {"LOW": "BuyerDevLow"},
                 {"LONG UPTREND": "BuyerDevLongUptrend"},
                 {"SLOW DOWNTREND": "BuyerDevSlowDowntrend"},
                 {"LONG DOWNTREND": "BuyerDevLongDowntrend"},
                 {"DOWNTREND UPSWING": "BuyerDevDowntrendUpswing"},
                 {"DANGER ZONE": "BuyerDevDangerZone"},
                 {"UPPER DANGER ZONE": "BuyerDevUpperDangerZone"},
                 {"BUY 1": "x_Buy1"},
                 {"BUY 2": "x_Buy2"},
                 {"BUY 3": "x_Buy3"},
                 {"BUY 4": "x_Buy4"},
                 {"BUY 5": "x_Buy5"},
                 {"SELL 1": "x_Sell1"},
                 {"SELL 2": "x_Sell2"},
                 {"SELL 3": "x_Sell3"},
                 {"SELL 4": "x_Sell4"},
                 {"SELL 5": "x_Sell5"}
                 ]

timeframes_json = [
                    {"6": 1644278400000},  # 8 february 2022
                    {"5": 1638835200000},  # 7 december 2021
                   {"4": 1631232000000},  # 10 september 2021
                   {"3": 1625097600000},  # 1 july 2021
                   {"2": 1617235200000},  # 1 april 2021
                   {"1": 1609464867000},  # 1 january 2021
                   {"0": 1600312000000}  # 17 september 2020
                   ]

configs_json = ["normal", "nostalgia", "nostalgia-other", "older-classic"]

hyperopt_loss_functions = ["ShortTradeDurHyperOptLoss", "OnlyProfitHyperOptLoss", "SharpeHyperOptLoss",
                           "SharpeHyperOptLossDaily", "SortinoHyperOptLoss",
                           "SortinoHyperOptLossDaily", "MaxDrawDownHyperOptLoss"]

indicators1_solo_trends = [{"5": "Upper Danger Zone"},
                           # {"4":"Huge Fall Turnaround"},
                           {"3": "Long Uptrend"},
                           {"2": "Downtrend Upswing"},
                           # {"1":"Small Upswing"},
                           {"0": "Normal"},
                           {"-1": "Slow Downtrend"},
                           {"-2": "Long Downtrend"},
                           {"-3": "Danger Zone"},
                           ]


MODULE_LIST = ["BUY_SIGNALS.LOW","BUY_TRENDS.BUYER_LOW","LOW","BUY_SIGNALS.MID","BUY_TRENDS.BUYER_MID", "MID", "BUY_SIGNALS.HIGH","BUY_TRENDS.BUYER_HIGH","HIGH",
                            "BUY_SIGNALS.LONG_UPTREND","BUY_TRENDS.BUYER_LONG_UPTREND","LONG_UPTREND","BUY_SIGNALS.LONG_DOWNTREND","BUY_TRENDS.BUYER_LONG_DOWNTREND","LONG_DOWNTREND",
                            "BUY_SIGNALS.SLOW_DOWNTREND","BUY_TRENDS.BUYER_SLOW_DOWNTREND","SLOW_DOWNTREND","BUY_SIGNALS.DOWNTREND_UPSWING","BUY_TRENDS.BUYER_DOWNTREND_UPSWING","DOWNTREND_UPSWING",
                            "BUY_SIGNALS.DANGER_ZONE","BUY_TRENDS.BUYER_DANGER_ZONE","DANGER_ZONE","BUY_SIGNALS.UPPER_DANGER_ZONE","BUY_TRENDS.BUYER_UPPER_DANGER_ZONE","UPPER_DANGER_ZONE",
                            "BUY_xCOMMON.COMMON_BUYERS","BUY_xCOMMON.COMMON_BUYERS_LOW", "BUY_xCOMMON.COMMON_BUYERS_MID", "BUY_xCOMMON.COMMON_BUYERS_HIGH",

                            "SELL_SIGNALS.SELLER_LOW","SELL_SIGNALS.SELLER_MID","SELL_SIGNALS.SELLER_HIGH","SELL_SIGNALS.SELLER_LONG_DOWNTREND","SELL_SIGNALS.SELLER_SLOW_DOWNTREND",
                            "SELL_SIGNALS.SELLER_LONG_UPTREND","SELL_SIGNALS.SELLER_DOWNTREND_UPSWING", "SELL_SIGNALS.SELLER_DANGER_ZONE","SELL_SIGNALS.SELLER_UPPER_DANGER_ZONE",
                            "COMMON_SELL.COMMON_SELLERS", "COMMON_SELL.COMMON_SELLERS_LOW","COMMON_SELL.COMMON_SELLERS_MID","COMMON_SELL.COMMON_SELLERS_HIGH",

                            "COMMON.COMMON_FUNCTIONS", "COMMON.CONSTANTS","COMMON.TA_FUNCTIONS","COMMON.POPULATE_INDICATORS",
                            "COMMON_FUNCTIONS", "CONSTANTS","TA_FUNCTIONS","POPULATE_INDICATORS",

                            "DevLukas15min",
                            "Buy1","Buy2","Buy3","Buy4","Buy5","Sell1","Sell2","Sell3","Sell4","Sell5",

                            "Common","CommonBuyerLOW","CommonBuyerMID","CommonBuyerHIGH","Constants",
                            ]

data_loading_time_ms = 905000000


indicators1_default = ['sma50', 'sma200', 'sma400', 'sma10k']

config_file = "run-configuration.json"

fiat_currency = "USDT"

# date_until_gap = 5259492000 # 2 months
date_until_gap = 7889238000  # 3 months
# date_until_gap = 9289238000  # 3.5 months


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Freqtrade Strategy Tester'
        self.left = 15
        self.top = 20
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

        # Set solo trends
        self.solo_trends = []
        self.solo_trends_label = []
        for pair in indicators1_solo_trends:
            for key, value in pair.items():
                self.solo_trends.append(key)
                self.solo_trends_label.append(value)

        # Set configs
        self.configs = configs_json

        f = open(config_file)
        self.data = json.load(f)
        f.close()

        # app.aboutToQuit.connect(self.on_click_save_json)

        self.backtesting_clicked = False
        self.show_plot_clicked = False
        self.hyperopt_clicked = False

        self.backtest_data_enabled = False
        self.backtest_data_issues_display = ""

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
        self.indicator1_textbox.resize(150, 20)
        self.indicator1_textbox.setText(self.data["indicators1"]["text"])
        self.indicator1_textbox.editingFinished.connect(self.on_textchange_indicators1)
        if (self.data["indicators1"]["enabled"] == True):
            self.indicator1_textbox.setEnabled(True)
        else:
            self.indicator1_textbox.setEnabled(False)

        # Checkbox Indicators 1 Enable
        self.indicator1_checkbox = QCheckBox(self)
        self.indicator1_checkbox.move(250, 82)
        self.indicator1_checkbox.setChecked(self.data["indicators1"]["enabled"])
        self.indicator1_checkbox.stateChanged.connect(self.checkbox_indicators1)

        # Label Indicators 2
        self.indicator2_label = QLabel(self)
        self.indicator2_label.setText('Indicators 2:')
        self.indicator2_label.move(20, 134)
        # Textbox Indicator 2
        self.indicator2_textbox = QLineEdit(self)
        self.indicator2_textbox.move(90, 132)
        self.indicator2_textbox.resize(150, 20)
        self.indicator2_textbox.setText(self.data["indicators2"]["text"])
        self.indicator2_textbox.editingFinished.connect(self.on_textchange_indicators2)
        if (self.data["indicators2"]["enabled"] == True):
            self.indicator2_textbox.setEnabled(True)
        else:
            self.indicator2_textbox.setEnabled(False)
        # Checkbox Indicators 2 Enable
        self.indicator2_checkbox = QCheckBox(self)
        self.indicator2_checkbox.move(250, 136)
        self.indicator2_checkbox.setChecked(self.data["indicators2"]["enabled"])
        self.indicator2_checkbox.stateChanged.connect(self.checkbox_indicators2)

        # Label Indicators 3
        self.indicator3_label = QLabel(self)
        self.indicator3_label.setText('Indicators 3:')
        self.indicator3_label.move(20, 164)
        # Textbox Indicator 3
        self.indicator3_textbox = QLineEdit(self)
        self.indicator3_textbox.move(90, 162)
        self.indicator3_textbox.resize(150, 20)
        self.indicator3_textbox.setText(self.data["indicators3"]["text"])
        self.indicator3_textbox.editingFinished.connect(self.on_textchange_indicators3)
        if (self.data["indicators3"]["enabled"] == True):
            self.indicator3_textbox.setEnabled(True)
        else:
            self.indicator3_textbox.setEnabled(False)
        # Checkbox Indicators 3 Enable
        self.indicator3_checkbox = QCheckBox(self)
        self.indicator3_checkbox.move(250, 166)
        self.indicator3_checkbox.setChecked(self.data["indicators3"]["enabled"])
        self.indicator3_checkbox.stateChanged.connect(self.checkbox_indicators3)

        # Label Indicators extra Main
        self.indicator_extra_label_main = QLabel(self)
        self.indicator_extra_label_main.setText('Main:')
        self.indicator_extra_label_main.move(20, 106)
        # Checkbox Indicators extra Main
        self.indicator_extra_checkbox_main = QCheckBox(self)
        self.indicator_extra_checkbox_main.move(50, 107)
        self.indicator_extra_checkbox_main.setChecked(self.data["indicators_extra"]["main"])
        self.indicator_extra_checkbox_main.stateChanged.connect(self.checkbox_indicators_extra_main)
        # Label Indicators extra Solo
        self.indicator_extra_label_solo = QLabel(self)
        self.indicator_extra_label_solo.setText('Solo Trend:')
        self.indicator_extra_label_solo.move(75, 106)
        # Checkbox Indicators extra Solo
        self.indicator_extra_checkbox_solo = QCheckBox(self)
        self.indicator_extra_checkbox_solo.move(132, 107)
        self.indicator_extra_checkbox_solo.setChecked(self.data["indicators_extra"]["solo"])
        self.indicator_extra_checkbox_solo.stateChanged.connect(self.checkbox_indicators_extra_solo)
        # Dropdown Indicators extra Solo Trend
        self.indicator_extra_dropdown_solo = QComboBox(self)
        self.indicator_extra_dropdown_solo.setGeometry(162, 104, 100, 20)
        self.indicator_extra_dropdown_solo.addItems(self.solo_trends_label)
        self.indicator_extra_dropdown_solo.setCurrentIndex(self.data["indicators_extra"]["solo_trend"])
        self.indicator_extra_dropdown_solo.currentIndexChanged.connect(self.on_select_solo_trend)
        if (self.data["indicators_extra"]["solo"] != True or self.data["indicators_extra"]["main"] == True):
            self.indicator_extra_dropdown_solo.hide()
        # Label Indicators extra Default
        self.indicator_extra_label_default = QLabel(self)
        self.indicator_extra_label_default.setText('Default:')
        self.indicator_extra_label_default.move(35, 189)
        # Checkbox Indicators extra Default
        self.indicator_extra_checkbox_default = QCheckBox(self)
        self.indicator_extra_checkbox_default.move(78, 190)
        self.indicator_extra_checkbox_default.setChecked(self.data["indicators_extra"]["default"])
        self.indicator_extra_checkbox_default.stateChanged.connect(self.checkbox_indicators_extra_default)
        # Label Indicators extra Volatility
        self.indicator_extra_label_volatility = QLabel(self)
        self.indicator_extra_label_volatility.setText('Volatility:')
        self.indicator_extra_label_volatility.move(103, 189)
        # Checkbox Indicators extra Volatility
        self.indicator_extra_checkbox_volatility = QCheckBox(self)
        self.indicator_extra_checkbox_volatility.move(151, 190)
        self.indicator_extra_checkbox_volatility.setChecked(self.data["indicators_extra"]["volatility"])
        self.indicator_extra_checkbox_volatility.stateChanged.connect(self.checkbox_indicators_extra_volatility)
        # Label Indicators extra Uptrend
        self.indicator_extra_label_uptrend = QLabel(self)
        self.indicator_extra_label_uptrend.setText('Uptrend:')
        self.indicator_extra_label_uptrend.move(176, 189)
        # Checkbox Indicators extra Uptrend
        self.indicator_extra_checkbox_uptrend = QCheckBox(self)
        self.indicator_extra_checkbox_uptrend.move(222, 190)
        self.indicator_extra_checkbox_uptrend.setChecked(self.data["indicators_extra"]["uptrend"])
        self.indicator_extra_checkbox_uptrend.stateChanged.connect(self.checkbox_indicators_extra_uptrend)
        # Label Indicators extra UptrendSmall
        self.indicator_extra_label_uptrendsmall = QLabel(self)
        self.indicator_extra_label_uptrendsmall.setText('Small Uptrend:')
        self.indicator_extra_label_uptrendsmall.move(150, 212)
        # Checkbox Indicators extra UptrendSmall
        self.indicator_extra_checkbox_uptrendsmall = QCheckBox(self)
        self.indicator_extra_checkbox_uptrendsmall.move(222, 212)
        self.indicator_extra_checkbox_uptrendsmall.setChecked(self.data["indicators_extra"]["uptrendsmall"])
        self.indicator_extra_checkbox_uptrendsmall.stateChanged.connect(self.checkbox_indicators_extra_uptrendsmall)
        # Label Indicators extra Sec Trend
        self.indicator_extra_label_sec_trend = QLabel(self)
        self.indicator_extra_label_sec_trend.setText('Sec.Trend:')
        self.indicator_extra_label_sec_trend.move(20, 212)
        # Checkbox Indicators extra Sec Trend
        self.indicator_extra_checkbox_sec_trend = QCheckBox(self)
        self.indicator_extra_checkbox_sec_trend.move(78, 212)
        self.indicator_extra_checkbox_sec_trend.setChecked(self.data["indicators_extra"]["sec_trend"])
        self.indicator_extra_checkbox_sec_trend.stateChanged.connect(self.checkbox_indicators_extra_sec_trend)

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
        self.time_from_calendar = QDateEdit(self, calendarPopup=True)
        self.time_from_calendar.setGeometry(310, 30, 150, 30)
        self.time_from_calendar.setDateTime(QDateTime.fromMSecsSinceEpoch(self.data["time"]["time_from"]))
        self.time_from_calendar.dateChanged.connect(self.on_select_from_date)
        self.time_from_calendar.hide()
        if (self.data["time"]["time_from_date"] == True):
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
        self.time_from_final_date_label.setText(unix_to_datetime(self.data["time"]["time_from"], True, True))
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
        self.time_until_calendar = QDateEdit(self, calendarPopup=True)
        self.time_until_calendar.setGeometry(510, 30, 150, 30)
        self.time_until_calendar.setDateTime(QDateTime.fromMSecsSinceEpoch(self.data["time"]["time_until"]))
        self.time_until_calendar.dateChanged.connect(self.on_select_until_date)
        self.time_until_calendar.setMaximumDateTime(
            QDateTime.fromMSecsSinceEpoch(self.data["download"]["latest_update"]))
        self.time_until_calendar.setMinimumDateTime(QDateTime.fromMSecsSinceEpoch(self.data["time"]["time_from"]))
        self.time_until_calendar.hide()
        if (self.data["time"]["time_until_date"] == True):
            self.time_until_calendar.show()
            self.time_until_dropdown.hide()
        # Time Until Checkbox
        self.time_until_checkbox = QCheckBox(self)
        self.time_until_checkbox.move(667, 37)
        self.time_until_checkbox.setChecked(True)
        self.time_until_checkbox.setChecked(self.data["time"]["time_until_enabled"])
        self.time_until_checkbox.stateChanged.connect(self.checkbox_time_until)
        if (self.data["time"]["time_until_enabled"] == False):
            self.time_until_checkbox_date.setEnabled(False)
            if (self.data["time"]["time_until_date"] == True):
                self.time_until_calendar.setEnabled(False)
            else:
                self.time_until_dropdown.setEnabled(False)
        # Time From final date label
        self.time_until_final_date_label = QLabel(self)
        self.time_until_final_date_label.setText(unix_to_datetime(self.data["time"]["time_until"], True, True))
        self.time_until_final_date_label.move(504, 72)
        # Time difference label
        self.time_difference_label = QLabel(self)
        self.time_difference_label.setText(
            "Days: " + str(days_between_timestamps(self.data["time"]["time_from"], self.data["time"]["time_until"])))
        self.time_difference_label.move(610, 72)

        # Download Data absolute latest label
        self.label_download_data_abs_latest = QLabel(self)
        self.label_download_data_abs_latest.setText(
            'Abs Latest:   ' + unix_to_datetime(self.data["download"]["absolute_latest_update"], True, True))
        self.label_download_data_abs_latest.move(695, 40)
        # Download Data
        self.download_data_button = QPushButton('Download Data', self)
        self.download_data_button.setToolTip('Download 15m and 1h data for the selected pairs')
        self.download_data_button.move(695, 12)
        self.download_data_button.clicked.connect(self.on_click_download_data)
        # # Download Data 1h
        # self.download_1h_button=QPushButton('1h',self)
        # self.download_1h_button.setToolTip('Download 1h data for the selected pairs')
        # self.download_1h_button.move(760, 32)
        # self.download_1h_button.clicked.connect(self.on_click_1h)
        # Download Data days textbox
        self.textbox_download_days = QLineEdit(self)
        self.textbox_download_days.move(782, 15)
        self.textbox_download_days.resize(45, 18)
        self.textbox_download_days.setText(str(self.data["download"]["days_to_download"]))
        self.textbox_download_days.textChanged.connect(self.on_textchange_download_days)

        # Download Data latest from pairlist label
        self.label_download_data_latest = QLabel(self)
        self.label_download_data_latest.setText(
            'Latest: ' + unix_to_datetime(self.data["download"]["latest_update"], True, True))
        self.label_download_data_latest.move(675, 160)
        # Download Data days from pairlist label
        self.label_download_days_latest = QLabel(self)
        self.label_download_days_latest.setText(str(self.data["download"]["latest_days"]) + " days")
        self.label_download_days_latest.move(795, 160)
        # Download Data clashes label
        self.label_download_data_clashes = QLabel(self)
        self.label_download_data_clashes.setText("Latest Date Clash...")
        self.label_download_data_clashes.move(683, 186)
        self.label_download_data_clashes.hide()
        # Download Data check button
        self.check_downloaded_data_button = QPushButton('Check', self)
        self.check_downloaded_data_button.setToolTip('Check downloaded data for the selected pairs')
        self.check_downloaded_data_button.move(792, 180)
        self.check_downloaded_data_button.resize(50, 25)
        self.check_downloaded_data_button.clicked.connect(self.on_click_check_download_data)
        # Download Data textfields view
        self.download_data_details_textbox = QPlainTextEdit(self)
        self.download_data_details_textbox.move(850, 10)
        self.download_data_details_textbox.resize(190, 360)
        self.download_data_details_textbox.setEnabled(False)
        # self.download_data_details_textbox.setPlainText(self.data["pairs1"])
        # self.download_data_details_textbox.textChanged.connect(self.on_textchange_pairs1)

        # Label Pairs 1
        self.pairs1_label = QLabel(self)
        self.pairs1_label.setText('Pairs:')
        self.pairs1_label.move(320, 100)
        # Textbox Pairs 1
        self.pairs1_textbox = QPlainTextEdit(self)
        self.pairs1_textbox.move(355, 100)
        self.pairs1_textbox.resize(60, 246)
        self.pairs1_textbox.setPlainText(self.data["pairs1"])
        self.pairs1_textbox.textChanged.connect(self.on_textchange_pairs1)

        # Label Cache Pairs 2
        self.pairs2_label = QLabel(self)
        self.pairs2_label.setText('Cache:')
        self.pairs2_label.move(470, 100)
        # Textbox Cache Pairs 2
        self.pairs2_textbox = QPlainTextEdit(self)
        self.pairs2_textbox.move(510, 100)
        self.pairs2_textbox.resize(60, 246)
        self.pairs2_textbox.setPlainText(self.data["pairs2"])
        self.pairs2_textbox.textChanged.connect(self.on_textchange_pairs2)

        # Label All Pairs 3
        self.pairs3_label = QLabel(self)
        self.pairs3_label.setText('All:')
        self.pairs3_label.move(580, 100)
        # Textbox All Pairs 3
        self.pairs3_textbox = QPlainTextEdit(self)
        self.pairs3_textbox.move(600, 100)
        self.pairs3_textbox.resize(60, 246)
        self.pairs3_textbox.setPlainText(self.data["pairs3"])
        self.pairs3_textbox.textChanged.connect(self.on_textchange_pairs3)

        self.addHyperopt()

        # Button backtest
        self.backtest_button = QPushButton('Backtest', self)
        self.backtest_button.setToolTip('Backtest Data')
        self.backtest_button.move(670, 324)
        self.backtest_button.clicked.connect(self.on_click_backtest)

        # Button Show Plot
        self.plot_button = QPushButton('Show Plot', self)
        self.plot_button.setToolTip('Create A plot for the selected pair')
        self.plot_button.move(765, 324)
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
        self.checkbox_config_default.move(720, 100)
        self.checkbox_config_default.setChecked(self.data["config_default"])
        self.checkbox_config_default.stateChanged.connect(self.checkbox_config)
        # Config dropdown
        self.dropdown_config = QComboBox(self)
        self.dropdown_config.setGeometry(750, 96, 85, 20)
        self.dropdown_config.addItems(self.configs)
        self.dropdown_config.setCurrentIndex(self.data["config_selection"])
        self.dropdown_config.currentIndexChanged.connect(self.on_select_config)
        if (self.data["config_default"]):
            self.dropdown_config.hide()

        # Button load config pairs
        self.backtest_button = QPushButton('Config Pairs', self)
        self.backtest_button.move(750, 120)
        self.backtest_button.clicked.connect(self.load_config_pairs)

        # # Plot Pair label
        # self.label_plot_pair = QLabel(self)
        # self.label_plot_pair.setText('Plot Pair:')
        # self.label_plot_pair.move(705, 300)
        # Plot Pair dropdown
        self.dropdown_plot_pair = QComboBox(self)
        self.dropdown_plot_pair.setGeometry(766, 297, 73, 20)
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
        self.label_backtest_process.move(667, 289)
        self.get_backtest_processing_power()
        # Processing Plot  label
        self.label_plot_process = QLabel(self)
        self.label_plot_process.move(667, 305)
        self.get_plot_processing_power()
        # Processing Hyperopt  label
        self.label_hyperopt_process = QLabel(self)
        self.label_hyperopt_process.move(250, 300)
        self.get_hyperopt_processing_power()

        # Profit plot label
        self.display_profit_label = QLabel(self)
        self.display_profit_label.setText('Profit')
        self.display_profit_label.move(789, 275)
        # Profit plot Checkbox
        self.display_profit_checkbox = QCheckBox(self)
        self.display_profit_checkbox.move(820, 275)
        self.display_profit_checkbox.setChecked(self.data["plot_profit"])
        self.display_profit_checkbox.stateChanged.connect(self.checkbox_profit)

        # Label Run Command args
        self.run_command_args_label = QLabel(self)

        self.run_command_args_label.setText(self.data["command"])
        self.run_command_args_label.move(18, 356)

        self.update_download_data_labels()
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)
        self.update_display_dates()
        self.show()
        self.update_hyperopt()

    def addHyperopt(self):

        # Label Separator
        self.hyperopt_label = QLabel(self)
        self.hyperopt_label.setText('--------------------------------------------------------------------------------')
        self.hyperopt_label.move(20, 227)

        # Label Hyperopt
        self.hyperopt_label = QLabel(self)
        self.hyperopt_label.setText('Hyperopt:')
        self.hyperopt_label.move(20, 260)

        # Checkbox hyperopt
        self.hyperopt_checkbox = QCheckBox(self)
        self.hyperopt_checkbox.move(71, 261)
        self.hyperopt_checkbox.setChecked(self.data["hyperopt"]["hyperopt"])
        self.hyperopt_checkbox.stateChanged.connect(self.checkbox_hyperopt)

        # # Label Search Space:
        # self.search_space_label = QLabel(self)
        # self.search_space_label.setText('Search Space')
        # self.search_space_label.move(190, 230)

        # Label Epochs
        self.label_epochs = QLabel(self)
        self.label_epochs.setText('Epochs:')
        self.label_epochs.move(144, 300)
        # Textbox Epochs
        self.textbox_epochs = QLineEdit(self)
        self.textbox_epochs.move(187, 298)  # x was 170
        self.textbox_epochs.resize(30, 18)
        self.textbox_epochs.setText(self.data["hyperopt"]["epochs"])
        self.textbox_epochs.textChanged.connect(self.on_textchange_epochs)

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
        self.hyperopt_button = QPushButton('Hyperopt', self)
        self.hyperopt_button.move(255, 323)
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
        if self.data["hyperopt"]["hyperopt"] == True:
            # self.search_space_label.show()
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
            self.label_hyperopt_process.show()
            self.label_epochs.show()
            self.textbox_epochs.show()
        else:
            # self.search_space_label.hide()
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
            self.label_hyperopt_process.hide()
            self.label_epochs.hide()
            self.textbox_epochs.hide()

    def update_onclick_triggers(self):
        self.backtesting_clicked = False
        self.show_plot_clicked = False
        self.hyperopt_clicked = False

    def update_display_dates(self):
        # print("Updating display dates")
        self.time_from_final_date_label.setText(unix_to_datetime(self.data["time"]["time_from"], True, True))
        self.time_from_final_date_label.adjustSize()
        self.time_until_final_date_label.setText(unix_to_datetime(self.data["time"]["time_until"], True, True))
        self.time_until_final_date_label.adjustSize()
        self.time_difference_label.setText(
            "Days: " + str(days_between_timestamps(self.data["time"]["time_from"], self.data["time"]["time_until"])))
        self.time_difference_label.adjustSize()
        self.get_backtest_processing_power()
        self.get_plot_processing_power()
        self.get_hyperopt_processing_power()
        self.time_until_calendar.setMaximumDateTime(
            QDateTime.fromMSecsSinceEpoch(self.data["download"]["latest_update"]))
        # if(self.data["time"]["time_until_enabled"]):
        #     if(not self.data["time"]["time_until_date"]):
        #         index_limit = 0
        #         # for i in range(len(self.timeframes)):
        #         #    # i = len(self.timeframes)-i
        #         #     if(i > self.data["time"]["time_from_index"]):
        #         #         index_limit = i
        #         #         break
        #         print("index_limit "+str(self.data["time"]["time_from_index"]))
        #         # TODO what happens if index = 0
        #         # if(index_limit > 1):
        #         #     self.time_until_dropdown.setEnabled(True)
        #         #     self.time_until_dropdown.setMaxCount(index_limit-1)
        #         # else:
        #         self.time_until_dropdown.setMaxCount(self.data["time"]["time_from_index"])
        #         #self.time_until_dropdown.setEnabled(False)

    def update_download_data_labels(self):
        self.update_days_download_data_label()
        self.update_latest_date_download_data_label()
        self.check_for_issues_downloaded_data()

    @pyqtSlot()
    def on_click_save_json(self):
        # print("Saving data to JSON")
        try:
            with open(config_file, 'w') as file:
                json.dump(self.data, file)
        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_click_backtest(self):
        if (self.backtesting_clicked):

            main(self.command_list)
            self.backtesting_clicked = False
            self.show_plot_clicked = False
            self.hyperopt_clicked = False
        else:
            self.update_config_pairs()
            self.on_click_save_json()
            self.get_backtest_processing_power()
            time_until = ""
            if (self.data["time"]["time_until_enabled"]):
                time_until = self.data["time"]["time_until"]

            command_list = ["backtesting", "--config", "user_data/" + self.data["config"], "--timeframe", "15m","--cache","none",
                            "--strategy", self.strategies[self.data["strategy"]], "--export", "trades",
                            "--timerange=" + str(self.data["time"]["time_from"]-data_loading_time_ms) + "-" + str(time_until)]

            print(command_list)
            self.command_list = command_list
            self.data["command"] = ' '.join(command_list)
            self.run_command_args_label.setText(self.data["command"])
            self.hyperopt_clicked = False
            self.backtesting_clicked = True
            self.show_plot_clicked = False
            self.reload_imports()

    @pyqtSlot()
    def on_click_plot(self):
        if (self.show_plot_clicked):
            main(self.command_list)
            # commands = "main.py " +' '.join(self.command_list)
            # os.system('cmd /c python ' + commands)
            # Opens the plot in the default browser
            if (self.data["plot_profit"] == False):
                pair = self.data["pairs1"].split()[self.data["plot_pair"]]
                url = file_dir + "/user_data/plot/freqtrade-plot-" + pair + "_" + fiat_currency + '-15m.html'
            else:
                url = file_dir + '/user_data/plot/freqtrade-profit-plot.html'
            os.system('cmd /c start ' + url)
            self.backtesting_clicked = False
            self.show_plot_clicked = False
            self.hyperopt_clicked = False
        else:
            self.update_config_pairs()
            self.on_click_save_json()
            self.get_plot_processing_power()
            time_until = ""
            if (self.data["time"]["time_until_enabled"]):
                time_until = self.data["time"]["time_until"]

            pair = self.data["pairs1"].split()[self.data["plot_pair"]]

            command = "plot-dataframe"
            if (self.data["plot_profit"]):
                command = "plot-profit"

            indicators1_temp = []
            indicators1 = []
            indicators2 = []
            indicators3 = []
            if self.data["plot_profit"] == False:

                if (self.data["indicators_extra"]["main"]):
                    indicators1_temp.append("main")
                if (self.data["indicators_extra"]["solo"]):
                    indicators1_temp.append(
                        "solo-" + str(self.solo_trends[self.data["indicators_extra"]["solo_trend"]]))
                if (self.data["indicators_extra"]["default"]):
                    for item in indicators1_default:
                        indicators1_temp.append(item)
                if (self.data["indicators_extra"]["volatility"]):
                    indicators1_temp.append("volatility")
                if (self.data["indicators_extra"]["uptrend"]):
                    indicators1_temp.append("uptrend")
                if (self.data["indicators_extra"]["uptrendsmall"]):
                    indicators1_temp.append("uptrendsmall")
                if (self.data["indicators_extra"]["sec_trend"]):
                    indicators1_temp.append("sec_trend")
                if (self.data["indicators1"]["enabled"]):
                    if (self.data["indicators1"]["text"] and len(self.data["indicators1"]["text"]) > 2):
                        for item in self.data["indicators1"]["text"].split():
                            indicators1_temp.append(item)
                if (len(indicators1_temp) >= 0):
                    indicators1 = ["--indicators1"]
                    for indicator in indicators1_temp:
                        indicators1.append(indicator)

            if (self.data["indicators2"]["enabled"]):
                indicators2 = ["--indicators2"]
                for item in self.data["indicators2"]["text"].split():
                    indicators2.append(item)
            if (self.data["indicators3"]["enabled"]):
                indicators3 = ["--indicators3"]
                for item in self.data["indicators3"]["text"].split():
                    indicators3.append(item)

            command_list = [command, "--config", "user_data/" + self.data["config"], "--strategy",
                            self.strategies[self.data["strategy"]], "-p", pair + "/" + fiat_currency,
                            "--timerange=" + str(self.data["time"]["time_from"]-data_loading_time_ms) + "-" + str(time_until)]

            if (len(indicators1) > 0):
                command_list.extend(indicators1)
            if (len(indicators2) > 0):
                command_list.extend(indicators2)
            if (len(indicators3) > 0):
                command_list.extend(indicators3)

            print(command_list)
            self.command_list = command_list
            self.data["command"] = ' '.join(command_list)
            self.run_command_args_label.setText(self.data["command"])
            self.hyperopt_clicked = False
            self.backtesting_clicked = False
            self.show_plot_clicked = True
            self.reload_imports()

    @pyqtSlot()
    def on_click_hyperopt(self):
        if (self.data["hyperopt"]["hyperopt"]):
            if (self.hyperopt_clicked):
                main(self.command_list)
                self.backtesting_clicked = False
                self.show_plot_clicked = False
                self.hyperopt_clicked = False
            else:
                self.update_config_pairs()
                self.on_click_save_json()
                self.get_hyperopt_processing_power()
                time_until = ""
                if (self.data["time"]["time_until_enabled"]):
                    time_until = self.data["time"]["time_until"]

                search_spaces = ["--spaces"]
                if (self.data["hyperopt"]["search_space_all"]):
                    search_spaces.append("all")
                if (self.data["hyperopt"]["search_space_default"]):
                    search_spaces.append("default")
                if (self.data["hyperopt"]["search_space_buy"]):
                    search_spaces.append("buy")
                if (self.data["hyperopt"]["search_space_sell"]):
                    search_spaces.append("sell")
                if (self.data["hyperopt"]["search_space_roi"]):
                    search_spaces.append("roi")
                if (self.data["hyperopt"]["search_space_stoploss"]):
                    search_spaces.append("stoploss")
                if (self.data["hyperopt"]["search_space_trailing"]):
                    search_spaces.append("trailing")
                if (self.data["hyperopt"]["search_space_protect"]):
                    search_spaces.append("protect")

                command_list = ["hyperopt", "--config", "user_data/" + self.data["config"], "--timeframe", "15m",
                                "--strategy", self.strategies[self.data["strategy"]], "-e",
                                self.data["hyperopt"]["epochs"],
                                "--timerange=" + str(self.data["time"]["time_from"]-data_loading_time_ms) + "-" + str(time_until),
                                "--hyperopt-loss", hyperopt_loss_functions[self.data["hyperopt"]["loss_function"]],
                                "--print-all"]

                if (len(search_spaces) > 1):
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
                self.reload_imports()
        else:
            print("Hyperopt is disabled")

    @pyqtSlot()
    def on_click_download_data(self):
        self.update_config_pairs()
        self.on_click_save_json()

        pairs = self.data["pairs1"].split()
        datetime_now = datetime.datetime.now() - datetime.timedelta(hours=2)
        timestamp = int(datetime_to_unix(datetime_now, False))
        if (timestamp > self.data["download"]["absolute_latest_update"]):
            self.data["download"]["absolute_latest_update"] = timestamp
        days = self.data["download"]["days"]
        self.data["download"]["days"] = int(days)
        for pair in pairs:
            found = False
            for item in self.data["download"]["pairs"]:
                if item["name"] == pair:
                    found = True
                    item["latest_update"] = timestamp
                    item["days"] = days
            if (found == False):
                pair_object = {"name": pair,
                               "latest_update": timestamp,
                               "days": int(days)}
                self.data["download"]["pairs"].append(pair_object)

        if self.backtest_data_enabled == True:
            self.hide_download_data_details()
        self.update_download_data_labels()
        self.on_click_save_json()
        print("Downloading data for 15m")
        main(["download-data", "-t", "15m"])
        print("Downloading data for 1h")
        main(["download-data", "-t", "1h"])
        print("FINISHED DOWNLOADING DATA")

    # @pyqtSlot()
    # def on_click_1h(self):
    #     self.update_config_pairs()
    #     self.on_click_save_json()
    #     main(["download-data", "-t" , "1h"])

    @pyqtSlot()
    def checkbox_indicators1(self):
        if (self.data["indicators1"]["enabled"] == True):
            self.data["indicators1"]["enabled"] = False
            self.indicator1_textbox.setEnabled(False)
        else:
            self.data["indicators1"]["enabled"] = True
            self.indicator1_textbox.setEnabled(True)

    @pyqtSlot()
    def checkbox_indicators2(self):
        if (self.data["indicators2"]["enabled"] == True):
            self.data["indicators2"]["enabled"] = False
            self.indicator2_textbox.setEnabled(False)
        else:
            self.data["indicators2"]["enabled"] = True
            self.indicator2_textbox.setEnabled(True)

    @pyqtSlot()
    def checkbox_indicators3(self):
        if (self.data["indicators3"]["enabled"] == True):
            self.data["indicators3"]["enabled"] = False
            self.indicator3_textbox.setEnabled(False)
        else:
            self.data["indicators3"]["enabled"] = True
            self.indicator3_textbox.setEnabled(True)

    @pyqtSlot()
    def checkbox_indicators_extra_main(self):
        if (self.data["indicators_extra"]["main"] == True):
            self.data["indicators_extra"]["main"] = False
        else:
            self.data["indicators_extra"]["main"] = True
            if (self.data["indicators_extra"]["solo"] == True):
                self.indicator_extra_checkbox_solo.setChecked(False)
            self.indicator_extra_dropdown_solo.hide()

    @pyqtSlot()
    def checkbox_indicators_extra_solo(self):
        if (self.data["indicators_extra"]["solo"] == True):
            self.data["indicators_extra"]["solo"] = False
            self.indicator_extra_dropdown_solo.hide()
        else:
            self.data["indicators_extra"]["solo"] = True
            if (self.data["indicators_extra"]["main"] == True):
                self.indicator_extra_checkbox_main.setChecked(False)
            self.indicator_extra_dropdown_solo.show()

    @pyqtSlot()
    def checkbox_indicators_extra_default(self):
        if (self.data["indicators_extra"]["default"] == True):
            self.data["indicators_extra"]["default"] = False
        else:
            self.data["indicators_extra"]["default"] = True

    @pyqtSlot()
    def checkbox_indicators_extra_volatility(self):
        if (self.data["indicators_extra"]["volatility"] == True):
            self.data["indicators_extra"]["volatility"] = False
        else:
            self.data["indicators_extra"]["volatility"] = True

    @pyqtSlot()
    def checkbox_indicators_extra_uptrend(self):
        if (self.data["indicators_extra"]["uptrend"] == True):
            self.data["indicators_extra"]["uptrend"] = False
        else:
            self.data["indicators_extra"]["uptrend"] = True

    @pyqtSlot()
    def checkbox_indicators_extra_uptrendsmall(self):
        if (self.data["indicators_extra"]["uptrendsmall"] == True):
            self.data["indicators_extra"]["uptrendsmall"] = False
        else:
            self.data["indicators_extra"]["uptrendsmall"] = True

    @pyqtSlot()
    def checkbox_indicators_extra_sec_trend(self):
        if (self.data["indicators_extra"]["sec_trend"] == True):
            self.data["indicators_extra"]["sec_trend"] = False
        else:
            self.data["indicators_extra"]["sec_trend"] = True

    def on_select_solo_trend(self, i):
        self.data["indicators_extra"]["solo_trend"] = i

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
        if self.backtest_data_enabled == True:
            self.hide_download_data_details()
        self.data["pairs1"] = self.pairs1_textbox.toPlainText().upper()
        self.dropdown_plot_pair.clear()
        self.dropdown_plot_pair.addItems(self.data["pairs1"].split())
        self.label_pairs_no.setText("Pairs: " + str(len(self.data["pairs1"].split())))
        self.data["max_open_trades"] = len(self.data["pairs1"].split())
        self.label_pairs_no.adjustSize()
        self.get_backtest_processing_power()
        self.get_hyperopt_processing_power()
        self.update_download_data_labels()
        self.update_onclick_triggers()

    @pyqtSlot()
    def on_textchange_pairs2(self):
        self.data["pairs2"] = self.pairs2_textbox.toPlainText().upper()

    @pyqtSlot()
    def on_textchange_pairs3(self):
        self.data["pairs3"] = self.pairs3_textbox.toPlainText().upper()

    @pyqtSlot()
    def checkbox_hyperopt(self):
        if (self.data["hyperopt"]["hyperopt"] == True):
            self.data["hyperopt"]["hyperopt"] = False
        else:
            self.data["hyperopt"]["hyperopt"] = True
        self.update_hyperopt()

    @pyqtSlot()
    def on_textchange_epochs(self):
        self.data["hyperopt"]["epochs"] = self.textbox_epochs.text()
        self.textbox_epochs.setText(self.data["hyperopt"]["epochs"])

    @pyqtSlot()
    def on_textchange_download_days(self):
        self.data["download"]["days_to_download"] = int(self.textbox_download_days.text())

    @pyqtSlot()
    def checkbox_search_space_all(self):
        if (self.data["hyperopt"]["search_space_all"] == True):
            self.data["hyperopt"]["search_space_all"] = False
        else:
            self.data["hyperopt"]["search_space_all"] = True

    @pyqtSlot()
    def checkbox_search_space_default(self):
        if (self.data["hyperopt"]["search_space_default"] == True):
            self.data["hyperopt"]["search_space_default"] = False
        else:
            self.data["hyperopt"]["search_space_default"] = True

    @pyqtSlot()
    def checkbox_search_space_buy(self):
        if (self.data["hyperopt"]["search_space_buy"] == True):
            self.data["hyperopt"]["search_space_buy"] = False
        else:
            self.data["hyperopt"]["search_space_buy"] = True

    @pyqtSlot()
    def checkbox_search_space_sell(self):
        if (self.data["hyperopt"]["search_space_sell"] == True):
            self.data["hyperopt"]["search_space_sell"] = False
        else:
            self.data["hyperopt"]["search_space_sell"] = True

    @pyqtSlot()
    def checkbox_search_space_roi(self):
        if (self.data["hyperopt"]["search_space_roi"] == True):
            self.data["hyperopt"]["search_space_roi"] = False
        else:
            self.data["hyperopt"]["search_space_roi"] = True

    @pyqtSlot()
    def checkbox_search_space_stoploss(self):
        if (self.data["hyperopt"]["search_space_stoploss"] == True):
            self.data["hyperopt"]["search_space_stoploss"] = False
        else:
            self.data["hyperopt"]["search_space_stoploss"] = True

    @pyqtSlot()
    def checkbox_search_space_trailing(self):
        if (self.data["hyperopt"]["search_space_trailing"] == True):
            self.data["hyperopt"]["search_space_trailing"] = False
        else:
            self.data["hyperopt"]["search_space_trailing"] = True

    @pyqtSlot()
    def checkbox_search_space_protect(self):
        if (self.data["hyperopt"]["search_space_protect"] == True):
            self.data["hyperopt"]["search_space_protect"] = False
        else:
            self.data["hyperopt"]["search_space_protect"] = True

    @pyqtSlot()
    def checkbox_time_from_date(self):
        if (self.data["time"]["time_from_date"] == True):
            self.data["time"]["time_from_date"] = False
            self.time_from_dropdown.show()
            self.time_from_calendar.hide()
            best_index = self.timeframes[0]
            for x in range(len(self.timeframes)):
                x= len(self.timeframes)-1-x
                closeness = self.timeframes[x] - self.data["time"]["time_from"]
                if closeness < 0:
                    best_index = x
            self.time_from_dropdown.setCurrentIndex(best_index)
        else:
            self.data["time"]["time_from_date"] = True
            self.time_from_calendar.setDateTime(QDateTime.fromMSecsSinceEpoch(self.data["time"]["time_from"]))
            self.time_from_calendar.show()
            self.time_from_dropdown.hide()

    @pyqtSlot()
    def checkbox_time_until_date(self):
        if (self.data["time"]["time_until_date"] == True):
            self.data["time"]["time_until_date"] = False
            self.time_until_dropdown.show()
            self.time_until_calendar.hide()
            best_index = self.timeframes[len(self.timeframes)-1]
            for x in range(len(self.timeframes)):
                closeness = self.timeframes[x] - self.data["time"]["time_until"]
                if closeness > 0:
                    best_index = x
            self.time_until_dropdown.setCurrentIndex(best_index)
        else:
            self.data["time"]["time_until_date"] = True
            self.time_until_calendar.setDateTime(QDateTime.fromMSecsSinceEpoch(self.data["time"]["time_until"]))
            self.time_until_calendar.show()
            self.time_until_dropdown.hide()

    @pyqtSlot()
    def date_to_dropdown_switch(self):
        best_index = self.timeframes[len(self.timeframes)-1]
        for x in range(len(self.timeframes)):
            closeness = abs(self.timeframes[x] - self.data["time"]["time_until"])
            if closeness > 0:
                best_index = x
                break



    @pyqtSlot()
    def checkbox_time_until(self):
        if (self.data["time"]["time_until_enabled"] == True):
            self.data["time"]["time_until_enabled"] = False
            self.time_until_checkbox_date.setEnabled(False)
            self.data["time"]["time_until"] = self.data["download"]["latest_update"]
            self.update_display_dates()
            if (self.data["time"]["time_until_date"] == True):
                self.time_until_calendar.setEnabled(False)
            else:
                self.time_until_dropdown.setEnabled(False)
        else:
            self.data["time"]["time_until_enabled"] = True
            self.time_until_calendar.setEnabled(True)
            self.time_until_dropdown.setEnabled(True)
            self.time_until_checkbox_date.setEnabled(True)
            self.time_until_calendar.setDateTime(QDateTime.fromMSecsSinceEpoch(self.data["time"]["time_until"]))

    @pyqtSlot()
    def checkbox_profit(self):
        if (self.data["plot_profit"] == True):
            self.data["plot_profit"] = False
        else:
            self.data["plot_profit"] = True

    @pyqtSlot()
    def checkbox_config(self):
        if (self.data["config_default"] == True):
            self.data["config_default"] = False
            self.dropdown_config.show()
        else:
            self.data["config"] = "config.json"
            self.data["config_default"] = True
            self.dropdown_config.hide()

    def on_select_strategy(self, i):
        self.data["strategy"] = i

    def on_select_loss_function(self, i):
        self.data["hyperopt"]["loss_function"] = i

    def on_select_time_from(self, i):
        if (i <= self.data["time"]["time_until_index"]):
            self.data["time"]["time_from_index"] = i
            timestamp = self.timeframes[i]

            # update time_until if lower time_from selected
            if (self.data["time"]["time_until_enabled"]):
                if (self.data["time"]["time_until_date"]):
                    print("doing date")
                    if (timestamp >= self.data["time"]["time_until"]):
                        if ((timestamp + date_until_gap) > self.data["download"]["latest_update"]):
                            self.data["time"]["time_until"] = self.data["download"]["latest_update"]
                        else:
                            self.data["time"]["time_until"] = (timestamp + date_until_gap)
                        self.time_until_calendar.setDateTime(
                            QDateTime.fromMSecsSinceEpoch(self.data["time"]["time_until"]))
                else:

                    if (timestamp >= self.data["time"]["time_until"]):
                        if (i > 0 and i < len(self.timeframes)):
                            self.data["time"]["time_until_index"] = i - 1
                            self.time_until_dropdown.setCurrentIndex(self.data["time"]["time_until_index"])
                            self.time_until_dropdown.setMaxVisibleItems(self.data["time"]["time_from_index"])
        else:
            self.data["time"]["time_from_index"] = i
            timestamp = self.timeframes[i]
            self.time_until_dropdown.setMaxVisibleItems(self.data["time"]["time_from_index"])
            self.time_until_dropdown.hide()
            self.time_until_dropdown.show()
        if(self.data["time"]["time_until_date"]):
            self.time_until_calendar.setMinimumDateTime(QDateTime.fromMSecsSinceEpoch(timestamp))
        self.data["time"]["time_from"] = timestamp
        self.update_display_dates()

    def on_select_time_until(self, i):
        self.data["time"]["time_until_index"] = i
        timestamp = self.timeframes[i]
        self.data["time"]["time_until"] = timestamp
        self.update_display_dates()

    def on_select_config(self, i):
        self.data["config_selection"] = i
        config = self.configs[i]
        self.data["config"] = "config-" + str(config) + ".json"

    def on_select_plot_pair(self, i):
        self.data["plot_pair"] = i

    def on_click_check_download_data(self):
        if self.backtest_data_enabled == False:
            self.check_downloaded_data_button.setText("Hide")
            self.backtest_data_enabled = True
            self.width = 1050
            self.setFixedWidth(1050)
            self.generate_download_data_table()
            self.show()
        else:
            self.hide_download_data_details()

    def hide_download_data_details(self):
        self.check_downloaded_data_button.setText("Check")
        self.backtest_data_enabled = False
        self.width = 850
        self.setFixedWidth(850)
        self.show()

    ## Generates ands updates data for downloaded data for pairs in the textfield
    def generate_download_data_table(self):
        highest = 0
        highest_days = 1
        pairs_present = self.data["pairs1"].split()
        display_string = ""
        for pairname in pairs_present:
            for pair in self.data["download"]["pairs"]:
                lower = False
                lower_days = False
                if (pair["name"] == pairname):
                    if (pair["latest_update"] > highest):
                        highest = pair["latest_update"]
                    elif pair["latest_update"] < highest:
                        lower = True

                    if (pair["days"] > highest_days):
                        highest_days = pair["days"]
                    elif (pair["days"] < highest_days - highest_days / 100 * 5 and pair["latest_update"] != int(
                            highest)):
                        lower_days = True

                    if (lower == True and lower_days == True):
                        display_string += ("BAD    " + str(pair["name"]) + "   Days: " + str(
                            pair["days"]) + "   " + unix_to_datetime(pair["latest_update"], True, True) + "\n")
                    elif (lower == True):
                        display_string += ("OLD    " + str(pair["name"]) + "   Days: " + str(
                            pair["days"]) + "   " + unix_to_datetime(pair["latest_update"], True, True) + "\n")
                    elif (lower_days == True):
                        display_string += ("SHORT  " + str(pair["name"]) + "   Days: " + str(
                            pair["days"]) + "   " + unix_to_datetime(pair["latest_update"], True, True) + "\n")
                    else:
                        display_string += ("------   " + str(pair["name"]) + "   Days: " + str(
                            pair["days"]) + "   " + unix_to_datetime(pair["latest_update"], True, True) + "\n")

        self.backtest_data_issues_display = display_string
        self.download_data_details_textbox.setPlainText(self.backtest_data_issues_display)

    ## Generates ands updates data for downloaded data for pairs in the textfield
    def check_for_issues_downloaded_data(self):
        highest = 0
        highest_days = 1
        pairs_present = self.data["pairs1"].split()
        lower = False
        type_days = False
        for pairname in pairs_present:
            if (lower == False):
                for pair in self.data["download"]["pairs"]:

                    if (pair["name"] == pairname):

                        if (highest == 0):
                            highest = pair["latest_update"]
                        elif (pair["latest_update"] > highest):
                            lower = True
                            break
                        elif pair["latest_update"] < highest:
                            lower = True
                            break

                        if (highest_days == 1):
                            highest_days = pair["days"]
                        elif (pair["days"] - highest_days / 100 * 5 > highest_days):
                            lower = True
                            type_days = True
                            break
                        elif pair["days"] < highest_days - highest_days / 100 * 5:
                            lower = True
                            type_days = True
                            break

        if type_days:
            self.label_download_data_clashes.setText("Data Days Clash...  ")
        else:
            self.label_download_data_clashes.setText("Latest Date Clash...")

        if (lower == True):
            self.label_download_data_clashes.show()
        else:
            self.label_download_data_clashes.hide()

    def update_days_download_data_label(self):
        lowest = 0
        pairs_present = self.data["pairs1"].split()
        for pairname in pairs_present:
            for pair in self.data["download"]["pairs"]:
                if (pair["name"] == pairname):
                    if (lowest == 0):
                        lowest = pair["latest_update"]
                    if (pair["days"] < lowest):
                        lowest = pair["days"]
        self.data["download"]["latest_days"] = lowest
        self.label_download_days_latest.setText(str(self.data["download"]["latest_days"]) + " days")

    def update_latest_date_download_data_label(self):
        lowest = 0
        pairs_present = self.data["pairs1"].split()
        for pairname in pairs_present:
            for pair in self.data["download"]["pairs"]:
                if (pair["name"] == pairname):
                    if (lowest == 0):
                        lowest = pair["latest_update"]
                    if (pair["latest_update"] < lowest):
                        lowest = pair["latest_update"]

        self.data["download"]["latest_update"] = lowest
        self.label_download_data_latest.setText('Latest: ' + unix_to_datetime(lowest, True, True))

    def on_select_from_date(self, date):
        if(self.data["time"]["time_from_date"]):
            py_date = date.toPyDate()
            final_date = datetime.datetime(
                year=py_date.year,
                month=py_date.month,
                day=py_date.day,
            )
            final_timestamp = int(final_date.timestamp() * 1000)
            # updates date until by 2+ months
            if (self.data["time"]["time_until_enabled"]):
                if (self.data["time"]["time_until_date"]):
                    if (final_timestamp > self.data["time"]["time_from"]):
                        if ((final_timestamp + date_until_gap) > self.data["download"]["latest_update"]):
                            self.data["time"]["time_until"] = self.data["download"]["latest_update"]
                        else:
                            self.data["time"]["time_until"] = (final_timestamp + date_until_gap)
                        self.time_until_calendar.setDateTime(QDateTime.fromMSecsSinceEpoch(self.data["time"]["time_until"]))
                else:
                    if (final_timestamp > self.data["time"]["time_until"]):
                        if (self.data["time"]["time_until_index"] > 0):
                            self.data["time"]["time_until_index"] = self.data["time"]["time_until_index"] - 1
                            timestamp = self.timeframes[self.data["time"]["time_until_index"]]
                            self.data["time"]["time_until"] = timestamp
                            self.time_until_dropdown.setCurrentIndex(self.data["time"]["time_until_index"])
                    best_index = 0
                    for x in range(len(self.timeframes)):
                        x= len(self.timeframes)-1-x
                        closeness =  self.timeframes[x] - self.data["time"]["time_from"]
                        if closeness < 0 and x >0:
                            best_index = x-1
                    self.time_until_dropdown.setMaxVisibleItems(best_index)
            self.time_until_calendar.setMinimumDateTime(QDateTime.fromMSecsSinceEpoch(self.data["time"]["time_from"]))
            self.data["time"]["time_from"] = final_timestamp
            self.update_display_dates()

    def on_select_until_date(self, date):
        if(self.data["time"]["time_until_date"]):
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
        # print(self.data["config"])
        config_url = file_dir + "/user_data/" + self.data["config"]
        # print(config_url)
        f = open(config_url)
        config_json = json.load(f)
        f.close()

        pairs = self.data["pairs1"].split()
        processed_pairs = []
        for pair in pairs:
            processed_pairs.append(pair + "/" + fiat_currency)

        config_json["exchange"]["pair_whitelist"] = processed_pairs
        config_json["max_open_trades"] = self.data["max_open_trades"]
        config_json = update_config_funds(config_json)
        try:
            with open(config_url, 'w') as file:
                json.dump(config_json, file)
        except Exception as e:
            print(e)

        self.update_onclick_triggers()

    # Loads the pairlist from config to the GUI
    def load_config_pairs(self):
        config_url = file_dir + "/user_data/" + self.data["config"]
        f = open(config_url)
        config_json = json.load(f)
        f.close()

        processed_pair_text = ""

        for pair in config_json["exchange"]["pair_whitelist"]:
            processed_pair = pair.strip("/" + fiat_currency)
            processed_pair_text += (processed_pair + "/n")
        self.data["pairs1"] = processed_pair_text
        self.pairs1_textbox.setPlainText(self.data["pairs1"])
        self.label_pairs_no.setText("Pairs: " + str(len(config_json["exchange"]["pair_whitelist"])))
        self.label_pairs_no.adjustSize()
        self.get_backtest_processing_power()
        self.get_hyperopt_processing_power()
        if self.backtest_data_enabled == True:
            self.hide_download_data_details()
        self.update_download_data_labels()
        self.update_onclick_triggers()

    def get_pairlist_length(self):
        pairs = self.data["pairs1"].split()
        if (pairs):
            return "Pairs: " + str(len(pairs))
        else:
            return "0"

    def get_backtest_processing_power(self):
        time = 0.1
        days = days_between_timestamps(self.data["time"]["time_from"], self.data["time"]["time_until"])
        pairs = len(self.data["pairs1"].split())
        if (pairs <= 6):
            days_from_25 = days / 50
            days_ratio = (1 + (0.135 * (days_from_25)))
            pair_time = pairs * 1.8
            pair_time = pair_time + (0.4 * math.pow(1.22, pair_time))
            time = (pair_time * (days_ratio))
            time += 2.5
        else:
            days_from_25 = days / 50
            days_ratio = (1 + (0.135 * (days_from_25)))
            pair_time = pairs * 2.0
            pair_time = pair_time + (0.10 * math.pow(1.16, pair_time))
            time = (pair_time * (days_ratio))
            time += 2.0
        time = round(time + ((time / 2 * ((computer_processing_power - 1.0) * -1))), 1)
        self.label_backtest_process.setText('Backtest-Pw: ' + str(time) + "s")

    def get_plot_processing_power(self):
        days = days_between_timestamps(self.data["time"]["time_from"], self.data["time"]["time_until"])
        time1 = 5
        time1 = time1 + (days * 0.075)
        time2 = (0.16 * math.pow(1.05, days / 5))
        final_time = time1 + time2
        final_time = round(final_time + ((final_time / 2 * ((computer_processing_power - 1.0) * -1))), 1)
        self.label_plot_process.setText('Plotting-Pw:  ' + str(final_time) + "s")

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
        self.label_hyperopt_process.setText('Hyperopt-Pw: ' + "??" + "s")



    # RESETS ALL IMPORTS BEFORE RUNNING ANY COMMANDS
    def reload_imports(self):
        modules_copy =    sys.modules.copy()
        for item  in modules_copy:
            if(item in MODULE_LIST):
                reload(sys.modules[item])
        return True


    def closeEvent(self, event):
        self.on_click_save_json()
        sys.exit(0)


    # Updates the balance and order size for the config


def update_config_funds(config_json):
    config_json["dry_run_wallet"] = len(config_json["exchange"]["pair_whitelist"]) * balance_per_pair
    config_json["stake_amount"] = stake_amount
    return config_json


def unix_to_datetime(timestamp, to_string, to_simple):
    if (to_string):
        from_date_s = datetime.datetime.fromtimestamp(timestamp / 1000)
        if (to_simple):
            return from_date_s.strftime("%d %b %Y")
        else:
            return from_date_s.strftime("%d %b %Y %H:%M:%S")
    else:
        return datetime.datetime.fromtimestamp(timestamp / 1000)


def datetime_to_unix(date, from_string):
    if (from_string):
        date_obj = datetime.datetime.strptime(date, "%d %b %Y %H:%M:%S")
        return date_obj.timestamp() * 1000
    else:
        return date.timestamp() * 1000


def days_between_timestamps(from_timestamp, until_timestamp):
    difference = until_timestamp - from_timestamp
    difference = difference / 1000
    days = int(difference // (24 * 3600))
    return days

def run_commands(command_list):
    main(command_list)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
