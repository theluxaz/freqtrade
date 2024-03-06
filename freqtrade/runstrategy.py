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
import winsound
from importlib import reload, import_module
from pynput.keyboard import Key, Listener
# from pynput import keyboard

## use __ autopep8 __ formatter for the whole project (apart from this file)
## --in-place --aggressive --ignore E402 $FilePath$




computer_processing_power = 1.3  # 0.00001 to.. 2.0

balance_per_pair= 1000  #ADJUST BALANCE, WAS 2000, trying with 1000

stake_amount=800

fee_enable = True
fee_amount = 0.0025   #CHANGED TO 25 RECENTLY!!!! 3% fees or so amount to about 0.4% percent profit


#change spot to futures in config and change to use orderbook= true
#add GUI
futures = False

production_max_trades_enable = True
production_max_trades = 5

strategy_json = [{"MAIN": "AltcoinTrader15"},
                 {"HIGH": "BuyerDevHigh"},
                 {"MID": "BuyerDevMid"},
                 {"LOW": "BuyerDevLow"},
                 {"LONG UPTREND": "BuyerDevLongUptrend"},
                 {"SLOW DOWNTREND": "BuyerDevSlowDowntrend"},
                 {"LONG DOWNTREND": "BuyerDevLongDowntrend"},
                 {"DOWNTREND UPSWING": "BuyerDevDowntrendUpswing"},
                 {"DANGER ZONE": "BuyerDevDangerZone"},
                 {"UPPER DANGER ZONE": "BuyerDevUpperDangerZone"},
                 {"ANY": "BuyerDevAny"},
                 {"NOTREND": "BuyerDevNotrend"},
                 {"HIGH SELL": "SellerDevHigh"},
                 {"MID SELL": "SellerDevMid"},
                 {"LOW SELL": "SellerDevLow"},
                 {"LONG UPTREND SELL": "SellerDevLongUptrend"},
                 {"SLOW DOWNTREND SELL": "SellerDevSlowDowntrend"},
                 {"LONG DOWNTREND SELL": "SellerDevLongDowntrend"},
                 {"DANGER ZONE SELL": "SellerDevDangerZone"},
                 {"UPPER DANGER ZONE SELL": "SellerDevUpperDangerZone"},
                 {"ANY SELL": "SellerDevAny"},
                 {"NOTREND SELL": "SellerDevNotrend"},

                 # #DRAFT RULES
                 # {"BUY 1": "x_Buy1"},
                 # {"BUY 2": "x_Buy2"},
                 # {"BUY 3": "x_Buy3"},
                 # {"BUY 4": "x_Buy4"},
                 # {"BUY 5": "x_Buy5"},



                 #DRAFT RULES
                 {"Template Buy": "TemplateBuy"},
                 {"Template Buy NFI": "TemplateBuyNfi"},
                 {"Template Sell": "TemplateSellNfi"},
                 {"Template Sell NFI": "TemplateSellNfi"},



                 #LOW RULES
                 {"LOW BUY 1": "x_BUY_LOW1"},
                 {"LOW BUY 2": "x_BUY_LOW2"},
                 {"LOW BUY 3": "x_BUY_LOW3"},
                 {"LOW BUY 4": "x_BUY_LOW4"},
                 {"LOW BUY 5": "x_BUY_LOW5"},
                 {"LOW BUY 6": "x_BUY_LOW6"},
                 {"LOW BUY 7": "x_BUY_LOW7"},
                 {"LOW BUY 8": "x_BUY_LOW8"},
                 {"LOW BUY 9": "x_BUY_LOW9"},
                 {"LOW BUY 10": "x_BUY_LOW10"},
                 {"LOW BUY 11": "x_BUY_LOW11"},
                 {"LOW BUY 12": "x_BUY_LOW12"},
                 {"LOW BUY 13": "x_BUY_LOW13"},
                 {"LOW BUY 14": "x_BUY_LOW14"},
                 {"LOW BUY 15": "x_BUY_LOW15"},
                 {"LOW BUY 16": "x_BUY_LOW16"},
                 {"LOW BUY 17": "x_BUY_LOW17"},

                 #MID RULES
                 {"MID BUY 1": "x_BUY_MID1"},
                 {"MID BUY 2": "x_BUY_MID2"},
                 {"MID BUY 3": "x_BUY_MID3"},
                 {"MID BUY 4": "x_BUY_MID4"},
                 {"MID BUY 5": "x_BUY_MID5"},
                 {"MID BUY 6": "x_BUY_MID6"},
                 {"MID BUY 7": "x_BUY_MID7"},
                 {"MID BUY 8": "x_BUY_MID8"},
                 {"MID BUY 9": "x_BUY_MID9"},
                 {"MID BUY 10": "x_BUY_MID10"},
                 {"MID BUY 11": "x_BUY_MID11"},
                 {"MID BUY 12": "x_BUY_MID12"},
                 {"MID BUY 13": "x_BUY_MID13"},
                 {"MID BUY 14": "x_BUY_MID14"},
                 {"MID BUY 15": "x_BUY_MID15"},
                 {"MID BUY 16": "x_BUY_MID16"},
                 {"MID BUY 17": "x_BUY_MID17"},

                 #HIGH RULES
                 {"HIGH BUY 1": "x_BUY_HIGH1"},
                 {"HIGH BUY 2": "x_BUY_HIGH2"},
                 {"HIGH BUY 3": "x_BUY_HIGH3"},
                 {"HIGH BUY 4": "x_BUY_HIGH4"},
                 {"HIGH BUY 5": "x_BUY_HIGH5"},
                 {"HIGH BUY 6": "x_BUY_HIGH6"},
                 {"HIGH BUY 7": "x_BUY_HIGH7"},
                 {"HIGH BUY 8": "x_BUY_HIGH8"},
                 {"HIGH BUY 9": "x_BUY_HIGH9"},
                 {"HIGH BUY 10": "x_BUY_HIGH10"},
                 {"HIGH BUY 11": "x_BUY_HIGH11"},
                 {"HIGH BUY 12": "x_BUY_HIGH12"},
                 {"HIGH BUY 13": "x_BUY_HIGH13"},
                 {"HIGH BUY 14": "x_BUY_HIGH14"},
                 {"HIGH BUY 15": "x_BUY_HIGH15"},
                 {"HIGH BUY 16": "x_BUY_HIGH16"},
                 {"HIGH BUY 17": "x_BUY_HIGH17"},
                 {"HIGH BUY 18": "x_BUY_HIGH18"},
                 {"HIGH BUY 19": "x_BUY_HIGH19"},
                 {"HIGH BUY 20": "x_BUY_HIGH20"},

                 #LONG UPTREND RULES
                 {"LONG UPTREND BUY 1": "x_BUY_LONG_UPTREND1"},
                 {"LONG UPTREND BUY 2": "x_BUY_LONG_UPTREND2"},
                 {"LONG UPTREND BUY 3": "x_BUY_LONG_UPTREND3"},
                 {"LONG UPTREND BUY 4": "x_BUY_LONG_UPTREND4"},
                 {"LONG UPTREND BUY 5": "x_BUY_LONG_UPTREND5"},
                 {"LONG UPTREND BUY 6": "x_BUY_LONG_UPTREND6"},
                 {"LONG UPTREND BUY 7": "x_BUY_LONG_UPTREND7"},
                 {"LONG UPTREND BUY 8": "x_BUY_LONG_UPTREND8"},
                 {"LONG UPTREND BUY 9": "x_BUY_LONG_UPTREND9"},
                 {"LONG UPTREND BUY 10": "x_BUY_LONG_UPTREND10"},
                 {"LONG UPTREND BUY 11": "x_BUY_LONG_UPTREND11"},
                 {"LONG UPTREND BUY 12": "x_BUY_LONG_UPTREND12"},
                 {"LONG UPTREND BUY 13": "x_BUY_LONG_UPTREND13"},
                 {"LONG UPTREND BUY 14": "x_BUY_LONG_UPTREND14"},
                 {"LONG UPTREND BUY 15": "x_BUY_LONG_UPTREND15"},
                 {"LONG UPTREND BUY 16": "x_BUY_LONG_UPTREND16"},
                 {"LONG UPTREND BUY 17": "x_BUY_LONG_UPTREND17"},
                 {"LONG UPTREND BUY 18": "x_BUY_LONG_UPTREND18"},
                 {"LONG UPTREND BUY 19": "x_BUY_LONG_UPTREND19"},
                 {"LONG UPTREND BUY 20": "x_BUY_LONG_UPTREND20"},


                 #LONG DOWNTREND RULES
                 {"LONG DOWNTREND BUY 1, test DZ": "x_BUY_LONG_DOWNTREND1"},
                 {"LONG DOWNTREND BUY 2, test DZ": "x_BUY_LONG_DOWNTREND2"},
                 {"LONG DOWNTREND BUY 3, test DZ": "x_BUY_LONG_DOWNTREND3"},
                 {"LONG DOWNTREND BUY 4, test DZ": "x_BUY_LONG_DOWNTREND4"},
                 {"LONG DOWNTREND BUY 5, test DZ": "x_BUY_LONG_DOWNTREND5"},
                 {"LONG DOWNTREND BUY 6, test DZ": "x_BUY_LONG_DOWNTREND6"},
                 {"LONG DOWNTREND BUY 7, test DZ": "x_BUY_LONG_DOWNTREND7"},
                 {"LONG DOWNTREND BUY 8, test DZ": "x_BUY_LONG_DOWNTREND8"},
                 {"LONG DOWNTREND BUY 9, test DZ": "x_BUY_LONG_DOWNTREND9"},
                 {"LONG DOWNTREND BUY 10 ,test DZ": "x_BUY_LONG_DOWNTREND10"},
                 {"LONG DOWNTREND BUY 11 ,test DZ": "x_BUY_LONG_DOWNTREND11"},
                 {"LONG DOWNTREND BUY 12 ,test DZ": "x_BUY_LONG_DOWNTREND12"},
                 {"LONG DOWNTREND BUY 13 ,test DZ": "x_BUY_LONG_DOWNTREND13"},
                 {"LONG DOWNTREND BUY 14 ,test DZ": "x_BUY_LONG_DOWNTREND14"},
                 {"LONG DOWNTREND BUY 15 ,test DZ": "x_BUY_LONG_DOWNTREND15"},
                 {"LONG DOWNTREND BUY 16 ,test DZ": "x_BUY_LONG_DOWNTREND16"},
                 {"LONG DOWNTREND BUY 17 ,test DZ": "x_BUY_LONG_DOWNTREND17"},
                 {"LONG DOWNTREND BUY 18 ,test DZ": "x_BUY_LONG_DOWNTREND18"},
                 {"LONG DOWNTREND BUY 19 ,test DZ": "x_BUY_LONG_DOWNTREND19"},
                 {"LONG DOWNTREND BUY 20 ,test DZ": "x_BUY_LONG_DOWNTREND20"},


                 # DANGER ZONE RULES
                 {"DANGER ZONE BUY 1 ,test LD": "x_BUY_DANGER_ZONE1"},
                 {"DANGER ZONE BUY 2 ,test LD": "x_BUY_DANGER_ZONE2"},
                 {"DANGER ZONE BUY 3 ,test LD": "x_BUY_DANGER_ZONE3"},
                 {"DANGER ZONE BUY 4 ,test LD": "x_BUY_DANGER_ZONE4"},
                 {"DANGER ZONE BUY 5 ,test LD": "x_BUY_DANGER_ZONE5"},
                 {"DANGER ZONE BUY 6 ,test LD": "x_BUY_DANGER_ZONE6"},
                 {"DANGER ZONE BUY 7 ,test LD": "x_BUY_DANGER_ZONE7"},
                 {"DANGER ZONE BUY 8 ,test LD": "x_BUY_DANGER_ZONE8"},
                 {"DANGER ZONE BUY 9 ,test LD": "x_BUY_DANGER_ZONE9"},
                 {"DANGER ZONE BUY 10 ,test LD": "x_BUY_DANGER_ZONE10"},


                 #SLOW DOWNTREND RULES
                 {"SLOW DOWNTREND BUY 1": "x_BUY_SLOW_DOWNTREND1"},
                 {"SLOW DOWNTREND BUY 2": "x_BUY_SLOW_DOWNTREND2"},
                 {"SLOW DOWNTREND BUY 3": "x_BUY_SLOW_DOWNTREND3"},
                 {"SLOW DOWNTREND BUY 4": "x_BUY_SLOW_DOWNTREND4"},
                 {"SLOW DOWNTREND BUY 5": "x_BUY_SLOW_DOWNTREND5"},
                 {"SLOW DOWNTREND BUY 6": "x_BUY_SLOW_DOWNTREND6"},
                 {"SLOW DOWNTREND BUY 7": "x_BUY_SLOW_DOWNTREND7"},
                 {"SLOW DOWNTREND BUY 8": "x_BUY_SLOW_DOWNTREND8"},
                 {"SLOW DOWNTREND BUY 9": "x_BUY_SLOW_DOWNTREND9"},
                 {"SLOW DOWNTREND BUY 10": "x_BUY_SLOW_DOWNTREND10"},
                 {"SLOW DOWNTREND BUY 11": "x_BUY_SLOW_DOWNTREND11"},
                 {"SLOW DOWNTREND BUY 12": "x_BUY_SLOW_DOWNTREND12"},
                 {"SLOW DOWNTREND BUY 13": "x_BUY_SLOW_DOWNTREND13"},
                 {"SLOW DOWNTREND BUY 14": "x_BUY_SLOW_DOWNTREND14"},
                 {"SLOW DOWNTREND BUY 15": "x_BUY_SLOW_DOWNTREND15"},
                 # {"SLOW DOWNTREND BUY 16": "x_BUY_SLOW_DOWNTREND16"},
                 # {"SLOW DOWNTREND BUY 17": "x_BUY_SLOW_DOWNTREND17"},
                 # {"SLOW DOWNTREND BUY 18": "x_BUY_SLOW_DOWNTREND18"},
                 # {"SLOW DOWNTREND BUY 19": "x_BUY_SLOW_DOWNTREND19"},
                 # {"SLOW DOWNTREND BUY 20": "x_BUY_SLOW_DOWNTREND20"},

                 # ANY RULES
                 {"ANY BUY 1": "x_BUY_ANY1"},
                 {"ANY BUY 2": "x_BUY_ANY2"},
                 {"ANY BUY 3": "x_BUY_ANY3"},
                 {"ANY BUY 4": "x_BUY_ANY4"},
                 {"ANY BUY 5": "x_BUY_ANY5"},
                 {"ANY BUY 6": "x_BUY_ANY6"},
                 # {"ANY BUY 7": "x_BUY_ANY7"},
                 # {"ANY BUY 8": "x_BUY_ANY8"},
                 # {"ANY BUY 9": "x_BUY_ANY9"},
                 # {"ANY BUY 10": "x_BUY_ANY10"},

                 # NOTREND RULES
                 {"NOTREND BUY 1": "x_BUY_NOTREND1"},
                 {"NOTREND BUY 2": "x_BUY_NOTREND2"},
                 {"NOTREND BUY 3": "x_BUY_NOTREND3"},
                 {"NOTREND BUY 4": "x_BUY_NOTREND4"},
                 {"NOTREND BUY 5": "x_BUY_NOTREND5"},
                 {"NOTREND BUY 6": "x_BUY_NOTREND6"},
                 # {"NOTREND BUY 7": "x_BUY_NOTREND7"},
                 # {"NOTREND BUY 8": "x_BUY_NOTREND8"},
                 # {"NOTREND BUY 9": "x_BUY_NOTREND9"},
                 # {"NOTREND BUY 10": "x_BUY_NOTREND10"},





                 # #DRAFT SELL RULES
                 # {"SELL 1": "x_Sell1"},
                 # {"SELL 2": "x_Sell2"},
                 # {"SELL 3": "x_Sell3"},
                 # {"SELL 4": "x_Sell4"},
                 # {"SELL 5": "x_Sell5"},


                 # LOW SELL RULES
                 {"LOW SELL 1": "x_SELL_LOW1"},
                 {"LOW SELL 2": "x_SELL_LOW2"},
                 {"LOW SELL 3": "x_SELL_LOW3"},
                 {"LOW SELL 4": "x_SELL_LOW4"},
                 {"LOW SELL 5": "x_SELL_LOW5"},
                 {"LOW SELL 6": "x_SELL_LOW6"},
                 {"LOW SELL 7": "x_SELL_LOW7"},
                 {"LOW SELL 8": "x_SELL_LOW8"},
                 {"LOW SELL 9": "x_SELL_LOW9"},
                 {"LOW SELL 10": "x_SELL_LOW10"},

                 # MID SELL RULES
                 {"MID SELL 1": "x_SELL_MID1"},
                 {"MID SELL 2": "x_SELL_MID2"},
                 {"MID SELL 3": "x_SELL_MID3"},
                 {"MID SELL 4": "x_SELL_MID4"},
                 {"MID SELL 5": "x_SELL_MID5"},
                 {"MID SELL 6": "x_SELL_MID6"},
                 {"MID SELL 7": "x_SELL_MID7"},
                 {"MID SELL 8": "x_SELL_MID8"},
                 {"MID SELL 9": "x_SELL_MID9"},
                 {"MID SELL 10": "x_SELL_MID10"},

                 # HIGH SELL RULES
                 {"HIGH SELL 1": "x_SELL_HIGH1"},
                 {"HIGH SELL 2": "x_SELL_HIGH2"},
                 {"HIGH SELL 3": "x_SELL_HIGH3"},
                 {"HIGH SELL 4": "x_SELL_HIGH4"},
                 {"HIGH SELL 5": "x_SELL_HIGH5"},
                 {"HIGH SELL 6": "x_SELL_HIGH6"},
                 {"HIGH SELL 7": "x_SELL_HIGH7"},
                 {"HIGH SELL 8": "x_SELL_HIGH8"},
                 {"HIGH SELL 9": "x_SELL_HIGH9"},
                 {"HIGH SELL 10": "x_SELL_HIGH10"},

                 # LONG UPTREND SELL RULES
                 {"LONG UPTREND SELL 1": "x_SELL_LONG_UPTREND1"},
                 {"LONG UPTREND SELL 2": "x_SELL_LONG_UPTREND2"},
                 {"LONG UPTREND SELL 3": "x_SELL_LONG_UPTREND3"},
                 {"LONG UPTREND SELL 4": "x_SELL_LONG_UPTREND4"},
                 {"LONG UPTREND SELL 5": "x_SELL_LONG_UPTREND5"},
                 {"LONG UPTREND SELL 6": "x_SELL_LONG_UPTREND6"},
                 {"LONG UPTREND SELL 7": "x_SELL_LONG_UPTREND7"},
                 {"LONG UPTREND SELL 8": "x_SELL_LONG_UPTREND8"},
                 {"LONG UPTREND SELL 9": "x_SELL_LONG_UPTREND9"},
                 {"LONG UPTREND SELL 10": "x_SELL_LONG_UPTREND10"},
                 # {"LONG UPTREND SELL 11": "x_SELL_LONG_UPTREND11"},
                 # {"LONG UPTREND SELL 12": "x_SELL_LONG_UPTREND12"},
                 # {"LONG UPTREND SELL 13": "x_SELL_LONG_UPTREND13"},
                 # {"LONG UPTREND SELL 14": "x_SELL_LONG_UPTREND14"},
                 # {"LONG UPTREND SELL 15": "x_SELL_LONG_UPTREND15"},
                 # {"LONG UPTREND SELL 16": "x_SELL_LONG_UPTREND16"},
                 # {"LONG UPTREND SELL 17": "x_SELL_LONG_UPTREND17"},
                 # {"LONG UPTREND SELL 18": "x_SELL_LONG_UPTREND18"},
                 # {"LONG UPTREND SELL 19": "x_SELL_LONG_UPTREND19"},
                 # {"LONG UPTREND SELL 20": "x_SELL_LONG_UPTREND20"},

                 # LONG DOWNTREND SELL RULES
                 {"LONG DOWNTREND SELL 1": "x_SELL_LONG_DOWNTREND1"},
                 {"LONG DOWNTREND SELL 2": "x_SELL_LONG_DOWNTREND2"},
                 {"LONG DOWNTREND SELL 3": "x_SELL_LONG_DOWNTREND3"},
                 {"LONG DOWNTREND SELL 4": "x_SELL_LONG_DOWNTREND4"},
                 {"LONG DOWNTREND SELL 5": "x_SELL_LONG_DOWNTREND5"},
                 {"LONG DOWNTREND SELL 6": "x_SELL_LONG_DOWNTREND6"},
                 {"LONG DOWNTREND SELL 7": "x_SELL_LONG_DOWNTREND7"},
                 {"LONG DOWNTREND SELL 8": "x_SELL_LONG_DOWNTREND8"},
                 {"LONG DOWNTREND SELL 9": "x_SELL_LONG_DOWNTREND9"},
                 {"LONG DOWNTREND SELL 10": "x_SELL_LONG_DOWNTREND10"},
                 # {"LONG DOWNTREND SELL 11": "x_SELL_LONG_DOWNTREND11"},
                 # {"LONG DOWNTREND SELL 12": "x_SELL_LONG_DOWNTREND12"},
                 # {"LONG DOWNTREND SELL 13": "x_SELL_LONG_DOWNTREND13"},
                 # {"LONG DOWNTREND SELL 14": "x_SELL_LONG_DOWNTREND14"},
                 # {"LONG DOWNTREND SELL 15": "x_SELL_LONG_DOWNTREND15"},
                 # {"LONG DOWNTREND SELL 16": "x_SELL_LONG_DOWNTREND16"},
                 # {"LONG DOWNTREND SELL 17": "x_SELL_LONG_DOWNTREND17"},
                 # {"LONG DOWNTREND SELL 18": "x_SELL_LONG_DOWNTREND18"},
                 # {"LONG DOWNTREND SELL 19": "x_SELL_LONG_DOWNTREND19"},
                 # {"LONG DOWNTREND SELL 20": "x_SELL_LONG_DOWNTREND20"},

                 # SLOW DOWNTREND SELL RULES
                 {"SLOW DOWNTREND SELL 1": "x_SELL_SLOW_DOWNTREND1"},
                 {"SLOW DOWNTREND SELL 2": "x_SELL_SLOW_DOWNTREND2"},
                 {"SLOW DOWNTREND SELL 3": "x_SELL_SLOW_DOWNTREND3"},
                 {"SLOW DOWNTREND SELL 4": "x_SELL_SLOW_DOWNTREND4"},
                 {"SLOW DOWNTREND SELL 5": "x_SELL_SLOW_DOWNTREND5"},
                 {"SLOW DOWNTREND SELL 6": "x_SELL_SLOW_DOWNTREND6"},
                 {"SLOW DOWNTREND SELL 7": "x_SELL_SLOW_DOWNTREND7"},
                 {"SLOW DOWNTREND SELL 8": "x_SELL_SLOW_DOWNTREND8"},
                 {"SLOW DOWNTREND SELL 9": "x_SELL_SLOW_DOWNTREND9"},
                 {"SLOW DOWNTREND SELL 10": "x_SELL_SLOW_DOWNTREND10"},
                 # {"SLOW DOWNTREND SELL 11": "x_SELL_SLOW_DOWNTREND11"},
                 # {"SLOW DOWNTREND SELL 12": "x_SELL_SLOW_DOWNTREND12"},
                 # {"SLOW DOWNTREND SELL 13": "x_SELL_SLOW_DOWNTREND13"},
                 # {"SLOW DOWNTREND SELL 14": "x_SELL_SLOW_DOWNTREND14"},
                 # {"SLOW DOWNTREND SELL 15": "x_SELL_SLOW_DOWNTREND15"},
                 # {"SLOW DOWNTREND SELL 16": "x_SELL_SLOW_DOWNTREND16"},
                 # {"SLOW DOWNTREND SELL 17": "x_SELL_SLOW_DOWNTREND17"},
                 # {"SLOW DOWNTREND SELL 18": "x_SELL_SLOW_DOWNTREND18"},
                 # {"SLOW DOWNTREND SELL 19": "x_SELL_SLOW_DOWNTREND19"},
                 # {"SLOW DOWNTREND SELL 20": "x_SELL_SLOW_DOWNTREND20"},

                 # ANY SELL RULES
                 {"ANY SELL 1": "x_SELL_ANY1"},
                 {"ANY SELL 2": "x_SELL_ANY2"},
                 {"ANY SELL 3": "x_SELL_ANY3"},
                 {"ANY SELL 4": "x_SELL_ANY4"},
                 {"ANY SELL 5": "x_SELL_ANY5"},
                 {"ANY SELL 6": "x_SELL_ANY6"},
                 # {"ANY SELL 7": "x_SELL_ANY7"},
                 # {"ANY SELL 8": "x_SELL_ANY8"},
                 # {"ANY SELL 9": "x_SELL_ANY9"},
                 # {"ANY SELL 10": "x_SELL_ANY10"},

                 # NOTREND SELL RULES
                 {"NOTREND SELL 1": "x_SELL_NOTREND1"},
                 {"NOTREND SELL 2": "x_SELL_NOTREND2"},
                 {"NOTREND SELL 3": "x_SELL_NOTREND3"},
                 {"NOTREND SELL 4": "x_SELL_NOTREND4"},
                 {"NOTREND SELL 5": "x_SELL_NOTREND5"},
                 {"NOTREND SELL 6": "x_SELL_NOTREND6"},
                 # {"NOTREND SELL 7": "x_SELL_NOTREND7"},
                 # {"NOTREND SELL 8": "x_SELL_NOTREND8"},
                 # {"NOTREND SELL 9": "x_SELL_NOTREND9"},
                 # {"NOTREND SELL 10": "x_SELL_NOTREND10"},

                # DANGER ZONE SELL RULES
                 {"DANGER_ZONE SELL 1": "x_SELL_DANGER_ZONE1"},
                 {"DANGER_ZONE SELL 2": "x_SELL_DANGER_ZONE2"},
                 {"DANGER_ZONE SELL 3": "x_SELL_DANGER_ZONE3"},
                 {"DANGER_ZONE SELL 4": "x_SELL_DANGER_ZONE4"},
                 {"DANGER_ZONE SELL 5": "x_SELL_DANGER_ZONE5"},

                # UPPER DANGER ZONE SELL RULES
                 {"UPPER_DANGER_ZONE SELL 1": "x_SELL_UPPER_DANGER_ZONE1"},
                 {"UPPER_DANGER_ZONE SELL 2": "x_SELL_UPPER_DANGER_ZONE2"},
                 {"UPPER_DANGER_ZONE SELL 3": "x_SELL_UPPER_DANGER_ZONE3"},
                 {"UPPER_DANGER_ZONE SELL 4": "x_SELL_UPPER_DANGER_ZONE4"},
                 {"UPPER_DANGER_ZONE SELL 5": "x_SELL_UPPER_DANGER_ZONE5"},


                 ]

timeframes_json = [
                    {"14":1709215200000},  # 29 February 2023 11:59am GMT
                    {"13":1702526400000},  # 14 December  2023 4pm GMT
                    {"12":1695566238000},  # 24 September  2023 5pm GMT
                    {"11":1687941699000},  # 28 June  2023 8am GMT
                    {"10": 1679114962000},  # 18 March  2023 4am GMT
                    {"9": 1671667200000},  # 22 December 2022 midday
                    {"8": 1663750800000},  # 22 september 2022 midday
                    {"7": 1652514252769}, # 14 may 2022 12:00 midday - AFTER HUGE CRASH
                    # {"TEST END":1650073800000},#16 march 2022
                    # {"TEST START":1648600200000},#30 feb 2022
                    {"6": 1644278400000},  # 8 february 2022
                    {"5": 1638835200000},  # 7 december 2021
                   {"4": 1631232000000},  # 10 september 2021
                   {"3": 1625097600000},  # 1 july 2021
                   {"2": 1617235200000},  # 1 april 2021
                   {"1": 1609464867000},  # 1 january 2021
                   {"0": 1600312000000},  # 17 september 2020,
                   {"Notrend-old2": 1552348800000},  # 3 december 2019
                    {"Bear-old": 1515715200000},  # 12 january 2018
                    {"Bull-old": 1491177600000},  # 3 April 2017
                    {"Bitcoin Start": 1486080000000}  # 3 February 2017
                   ]

configs_json = ["config-production"]

hyperopt_loss_functions = ["ShortTradeDurHyperOptLoss", "OnlyProfitHyperOptLoss", "SharpeHyperOptLoss",
                           "SharpeHyperOptLossDaily", "SortinoHyperOptLoss",
                           "SortinoHyperOptLossDaily", "MaxDrawDownHyperOptLoss"]

indicators1_solo_trends = [{"5": "Upper Danger Zone"},
                           # {"4":"Huge Fall Turnaround"},
                           {"3": "Long Uptrend"},
                           # {"2": "Downtrend Upswing"},
                           # {"1":"Small Upswing"},
                           {"0": "Normal"},
                           {"-1": "Slow Downtrend"},
                           {"-2": "Long Downtrend"},
                           {"-3": "Danger Zone"},
                           ]

    #GET OTHER INDICATORS FROM PREVIOUS LAPTOP
indicators1_list  = [   {"---FAVORITES---":""},
                        {"SMA mix": "sma50 sma25 sma30k_1h sma10k sma100 sma200 sma400"},

                        {"---RESISTANCE/SUP---":""},
                        {"Resistance/Sup":"res_low sup_low"},
                        {"Resistance 1h":"res_low_1h res_mid_1h res_high_1h"},
                        {"Support 1h":"sup_low_1h sup_mid_1h sup_high_1h"},
                        {"Support 1d":"res_level_1d sup_level_1d"},

                        {"---MOVING AVG---":""},
                        {"Short SMA":"sma3 sma5 sma10 sma15 sma25 "},
                        {"Mid SMA":"sma30 sma50 sma75 sma100 sma200 sma400 "},
                        {"Long SMA":"sma10k sma13k sma200_1h sma20k_1h sma30_1h"},
                        {"Very Long SMA":"sma30_1d sma35_1d sma50_1d sma100_1d"},
                        {"Short EMA":"ema8 ema12 ema16 ema20 ema25"},
                        {"Mid EMA":"ema50 ema200 ema12_1h"},
                        {"Long EMA":"ema35_1h ema50_1h ema100_1h ema200_1h"},

                        {"---BOLINGER BANDS---":""},
                        {"Bollinger 20":"bb_lowerband20 bb_upperband20 bb_middleband20"},
                        {"Bollinger 50":"bb_lowerband50 bb_middleband50 bb_upperband50"},
                        {"Bollinger 100":"bb_lowerband100 bb_upperband100 bb_middleband100"},
                        {"Bollinger 175":"bb_lowerband175 bb_upperband175 bb_middleband175"},
                        {"Bollinger 1h 2000":"bb_lowerband2000_1h bb_upperband2000_1h bb_middleband2000_1h"},

                        {"SAR":"sar"},
                        # {"SUPtttttttttttt":"ttttttttttttttttt"},
                        # {"SUPtttttttttttt":"ttttttttttttttttt"},
                           ]

#GET OTHER INDICATORS FROM PREVIOUS LAPTOP
indicators2_list  = [   {"---FAVORITES---":""},
                        {"PPO mix":"ppo5 ppo10 ppo25 ppo50 ppo100 ppo200 ppo500"},#ppos
                        {"ROC candlesize mix":"candlesize roc roc2 "},
                        {"RSI":"rsi rsi5"},
                        {"MUL":"mul mul_conv"},

                        {"---RATE OF CHANGE---":""},
                        {"Short ROC":"roc roc2 roc10"},
                        {"Mid ROC":"roc25 roc50 roc50avg"},
                        {"Sma ROC":"roc50sma roc50smaavg roc200sma"},

                        {"---MOMENTUM---":""},
                        {"Short PPO":"ppo5 ppo10 ppo25 ppo50"},
                        {"Long PPO":"ppo100 ppo200 ppo500 ppo1000"},
                        {"Short RSI":"rsi5 rsi"},
                        {"Mid RSI":"rsi50 rsi_1h"},

                        {"ADX":"adx plus_di minus_di"},
                        {"Connors RSI":"crsi crsi_1h"},
                        {"Money Flow Index":"mfi"},
                        {"Ultimate Oscillator":"ult"},

                        {"R_Will":"r_14 r_480 r_480_1h"},
                        {"Fisher RSI":"fisher_rsi"},
                        {"Candlesize":"candlesize candleheight"},
                        {"Elliott Wave Osc":"ewo ewo_1h"},
                        {"Momentum Indicator":"cmf cmf_1h"},
                        {"Chaikin Money Flow":"mom"},

                        # {"Aroon":"aroon aroonosc"},
                        {"CCI":"cci"},
                        # {"MACD":"macd macdext macdfix"},
                        # {"STOCH":"stoch fastd fastk"},
                        # {"STOCHRSI":"stochrsi"},
                        {"NFI ones":"bb50_delta tail"},
                        # {"Range %Change 1h":"hl_pct_6_1h hl_pct_12_1h hl_pct_24_1h hl_pct_36_1h hl_pct_48_1h"},

                        # {"SUPtttttttttttt":"ttttttttttttttttt"},
                        # {"SUPtttttttttttt":"ttttttttttttttttt"},
               ]

indicators3_list  = [   {"---FAVORITES---":""},
                        {"Volatility":"vol50 vol100 vol175 vol250"},
                        {"Convergence":"convsmall convmedium"},
                        {"MUL":"mul mul_conv"},
                        {"BULL/BEAR":"BULL BEAR"},
                        {"Huge_pit_turn/Down_upswing":"HUGE_PIT_TURN DOWNTREND_UPSWING"},
                        {"---VOLATILITY---":""},
                        {"Volatility":"vol50 vol100 vol175 vol250"},
                        {"Mid Volatility":"vol500 vol1000 volultra"},
                        {"High Volatility":"volultra vol1000"},
                        {"Convergence":"convsmall convmedium"},
                        {"Long Convergence":"convmain convtotal"},
                        {"Mean Volume":"volume_mean_12 volume_mean_24"},
                        # {"Top %Change":"tpct_change_0 tpct_change_2 tpct_change_12 tpct_change_144"},

                        # {"SUPtttttttttttt":"ttttttttttttttttt"},
                        # {"SUPtttttttttttt":"ttttttttttttttttt"},
               ]


    #GET OTHER INDICATORS FROM PREVIOUS LAPTOP
indicators1_rare_list  = [  {"---FAVORITES---":""},

                            {"---MOVING AVG---":""},
                            {"High Price":"high50 high100 high1000"},
                            {"Low Price":"low50 low100 low1000"},
                            {"vwap short":"vwap vwap10 vwap50"},
                            {"vwap long":"vwap100 vwap500 vwap950"},
                            {"Conv vwap":"convwap"},
                            {"Zemas":"zema zema50 zema100 zema200"},

                            # {"SUPtttttttttttt":"ttttttttttttttttt"},
                            # {"SUPtttttttttttt":"ttttttttttttttttt"},
                           ]

indicators2_rare_list  = [  {"---FAVORITES---":""},

                            {"---RATE OF CHANGE---":""},
                            {"ROC":"roc roc2 "},
                            {"ROC LONG":"roc10 roc25 roc50"},
                            {"ROC SMA":"roc50sma"},

                            {"---MOMENTUM---":""},
                            {"RSI average":"rsi5avg rsiavg"},
                            {"ROC average":"roc10avg roc25avg"},
                            {"ADX50":"adx50 plus_di50 minus_di50 "},

                            {"Avg Directional Move I":"adxr"},
                            {"Absolute Price Osc":"apo"},
                            {"Balance Of Power":"bop"},
                            {"Chande Mom. Osc":"cmo"},
                            {"Directional Move I":"dx"},

                            {"Plus-Minus DM":"minus_dm plus_dm"},
                            {"ROC variants":"rocp rocr rocr100"},
                            {"TRIX":"trix"},
                            {"MODERI":"moderi_32"},

                            {"Awesome Oscillator":"ao"},
                            {"Bias":"bias"},
                            {"Brar":"brar"},
                            {"Coppock Curve":"coppock"},
                            {"Efficiency Ratio":"er"},

                            {"Vortex KDJ":"kdj"},
                            {"Pretty Good Oscillator":"pgo"},
                            {"Pretty Good Oscillator":"psl"},
                            {"Percentage Volume Osc":"pvo"},

                            {"Slope":"slope"},
                            {"Smi Ergodic":"smi"},
                            {"Squeeze":"squeeze squeeze_pro"},
                            {"True strength index":"tsi"},

                            {"---CYCLE---":""},
                            {"Hillbert Transform":"ht_dcperiod ht_dcphase ht_phasor ht_sine ht_trendmode"},

               ]

indicators3_rare_list  = [  {"---FAVORITES---":""},

                            {"---DISTANCE---":""},
                            {"Distance":"dist50 dist200 dist400 dist10k"},
                            {"Boll Distance":"dist_upbol50 dist_upbol100 dist_lowbol50 dist_lowbol100"},
                            {"Distance Convergence":"convdist"},

                            {"---VOLATILITY---":""},
                            {"Mean Volatility":"vol100mean vol250mean"},
                            {"ATR's":"atr_perc atr natr"},
                            {"True Range":"trange"},

                            {"Aberration":"aberration"},
                            {"Acceleration Bands":"accbands"},
                            {"Keltner Channel":"kc"},

                            {"Mass Index":"massi"},
                            {"Price Distance":"pdist"},
                            {"Relative Volatility I":"rvi"},
                            {"Elder's Thermometer":"thermo"},
                            {"Ulcer Index":"ui"},

                            {"---TREND---":""},
                            {"Decreasing":"decreasing100 decreasing250 decreasing500 decreasing1000"},
                            {"Increasing":"increasing100 increasing250 increasing500 increasing1000"},

                            {"---VOLUME---":""},
                            {"Volume other":"vpci vpci_ma aobv"},
                            {"Elder's Force Index":"efi"},
                            {"Ease of Movement":"eom"},
                            {"Klinger Volume Osc":"kvo"},
                            {"Negative Volume Index":"nvi"},

                            {"Positive Volume Index":"pvi"},
                            {"Price-Volume":"pvol"},
                            {"Price Volume Rank":"pvr"},
                            {"Volume Profile":"vp"},

                            # {"SUPtttttttttttt":"ttttttttttttttttt"},
                            # {"SUPtttttttttttt":"ttttttttttttttttt"},
                            # {"SUPtttttttttttt":"ttttttttttttttttt"},

               ]

MODULE_LIST = [
                            # "x_other.BUY_SIGNALS.LOW","x_other.BUY_TRENDS.BUYER_LOW","LOW","x_other.BUY_SIGNALS.MID","x_other.BUY_TRENDS.BUYER_MID", "MID", "x_other.BUY_SIGNALS.HIGH","x_other.BUY_TRENDS.BUYER_HIGH","HIGH",
                            # "x_other.BUY_SIGNALS.LONG_UPTREND","x_other.BUY_TRENDS.BUYER_LONG_UPTREND","LONG_UPTREND","x_other.BUY_SIGNALS.LONG_DOWNTREND","x_other.BUY_TRENDS.BUYER_LONG_DOWNTREND","LONG_DOWNTREND",
                            # "x_other.BUY_SIGNALS.SLOW_DOWNTREND","x_other.BUY_TRENDS.BUYER_SLOW_DOWNTREND","SLOW_DOWNTREND",
                            # "x_other.BUY_SIGNALS.DANGER_ZONE","x_other.BUY_TRENDS.BUYER_DANGER_ZONE","DANGER_ZONE","x_other.BUY_TRENDS.BUYER_NOSTALGIA","x_other.BUY_SIGNALS.UPPER_DANGER_ZONE","x_other.BUY_TRENDS.BUYER_UPPER_DANGER_ZONE","UPPER_DANGER_ZONE",
                            # "x_other.BUY_xCOMMON.COMMON_BUYERS","x_other.BUY_xCOMMON.COMMON_BUYERS_LOW", "x_other.BUY_xCOMMON.COMMON_BUYERS_MID", "BUY_xCOMMON.COMMON_BUYERS_HIGH",

                            # "OLD_SELL_SIGNALS.SELLER_LOW","OLD_SELL_SIGNALS.SELLER_MID","OLD_SELL_SIGNALS.SELLER_HIGH","OLD_SELL_SIGNALS.SELLER_LONG_DOWNTREND","OLD_SELL_SIGNALS.SELLER_SLOW_DOWNTREND",
                            # "OLD_SELL_SIGNALS.SELLER_LONG_UPTREND", "OLD_SELL_SIGNALS.SELLER_DANGER_ZONE","OLD_SELL_SIGNALS.SELLER_UPPER_DANGER_ZONE",
                            # "COMMON_SELL.COMMON_SELLERS", "COMMON_SELL.COMMON_SELLERS_LOW","COMMON_SELL.COMMON_SELLERS_MID","COMMON_SELL.COMMON_SELLERS_HIGH",
                            # "SELL_TRENDS.SELLER_NOSTALGIA","SELLER_NOSTALGIA",


                            #BUY RULE MODULES
                             "RULES.LOW.x_BUY_LOW1", "x_BUY_LOW1","RULES.LOW.x_BUY_LOW2", "x_BUY_LOW2","RULES.LOW.x_BUY_LOW3", "x_BUY_LOW3",
                             "RULES.LOW.x_BUY_LOW4", "x_BUY_LOW4","RULES.LOW.x_BUY_LOW5", "x_BUY_LOW5","RULES.LOW.x_BUY_LOW6", "x_BUY_LOW6",
                             "RULES.LOW.x_BUY_LOW7", "x_BUY_LOW7","RULES.LOW.x_BUY_LOW8", "x_BUY_LOW8","RULES.LOW.x_BUY_LOW9", "x_BUY_LOW9",
                             "RULES.LOW.x_BUY_LOW10", "x_BUY_LOW10","RULES.LOW.x_BUY_LOW11", "x_BUY_LOW11","RULES.LOW.x_BUY_LOW12", "x_BUY_LOW12",
                             "RULES.LOW.x_BUY_LOW13", "x_BUY_LOW13","RULES.LOW.x_BUY_LOW14", "x_BUY_LOW14","RULES.LOW.x_BUY_LOW15", "x_BUY_LOW15",
                             "RULES.LOW.x_BUY_LOW16", "x_BUY_LOW16","RULES.LOW.x_BUY_LOW17", "x_BUY_LOW17","RULES.LOW.x_BUY_LOW18", "x_BUY_LOW18",
                             "RULES.LOW.x_BUY_LOW19", "x_BUY_LOW19","RULES.LOW.x_BUY_LOW20", "x_BUY_LOW20",


                             "RULES.MID.x_BUY_MID1", "x_BUY_MID1","RULES.MID.x_BUY_MID2", "x_BUY_MID2","RULES.MID.x_BUY_MID3", "x_BUY_MID3",
                             "RULES.MID.x_BUY_MID4", "x_BUY_MID4","RULES.MID.x_BUY_MID5", "x_BUY_MID5","RULES.MID.x_BUY_MID6", "x_BUY_MID6",
                             "RULES.MID.x_BUY_MID7", "x_BUY_MID7","RULES.MID.x_BUY_MID8", "x_BUY_MID8","RULES.MID.x_BUY_MID9", "x_BUY_MID9",
                             "RULES.MID.x_BUY_MID10", "x_BUY_MID10","RULES.MID.x_BUY_MID11", "x_BUY_MID11","RULES.MID.x_BUY_MID12", "x_BUY_MID12",
                             "RULES.MID.x_BUY_MID13", "x_BUY_MID13","RULES.MID.x_BUY_MID14", "x_BUY_MID14","RULES.MID.x_BUY_MID15", "x_BUY_MID15",
                             "RULES.MID.x_BUY_MID16", "x_BUY_MID16","RULES.MID.x_BUY_MID17", "x_BUY_MID17","RULES.MID.x_BUY_MID18", "x_BUY_MID18",
                             "RULES.MID.x_BUY_MID19", "x_BUY_MID19","RULES.MID.x_BUY_MID20", "x_BUY_MID20",


                             "RULES.HIGH.x_BUY_HIGH1", "x_BUY_HIGH1","RULES.HIGH.x_BUY_HIGH2", "x_BUY_HIGH2","RULES.HIGH.x_BUY_HIGH3", "x_BUY_HIGH3",
                             "RULES.HIGH.x_BUY_HIGH4", "x_BUY_HIGH4","RULES.HIGH.x_BUY_HIGH5", "x_BUY_HIGH5","RULES.HIGH.x_BUY_HIGH6", "x_BUY_HIGH6",
                             "RULES.HIGH.x_BUY_HIGH7", "x_BUY_HIGH7","RULES.HIGH.x_BUY_HIGH8", "x_BUY_HIGH8","RULES.HIGH.x_BUY_HIGH9", "x_BUY_HIGH9",
                             "RULES.HIGH.x_BUY_HIGH10", "x_BUY_HIGH10","RULES.HIGH.x_BUY_HIGH11", "x_BUY_HIGH11","RULES.HIGH.x_BUY_HIGH12", "x_BUY_HIGH12",
                             "RULES.HIGH.x_BUY_HIGH13", "x_BUY_HIGH13","RULES.HIGH.x_BUY_HIGH14", "x_BUY_HIGH14","RULES.HIGH.x_BUY_HIGH15", "x_BUY_HIGH15",
                             "RULES.HIGH.x_BUY_HIGH16", "x_BUY_HIGH16","RULES.HIGH.x_BUY_HIGH17", "x_BUY_HIGH17","RULES.HIGH.x_BUY_HIGH18", "x_BUY_HIGH18",
                             "RULES.HIGH.x_BUY_HIGH19", "x_BUY_HIGH19","RULES.HIGH.x_BUY_HIGH20", "x_BUY_HIGH20",



                             "RULES.LONG_UPTREND.x_BUY_LONG_UPTREND1", "x_BUY_LONG_UPTREND1","RULES.LONG_UPTREND.x_BUY_LONG_UPTREND2", "x_BUY_LONG_UPTREND2","RULES.LONG_UPTREND.x_BUY_LONG_UPTREND3", "x_BUY_LONG_UPTREND3",
                             "RULES.LONG_UPTREND.x_BUY_LONG_UPTREND4", "x_BUY_LONG_UPTREND4","RULES.LONG_UPTREND.x_BUY_LONG_UPTREND5", "x_BUY_LONG_UPTREND5","RULES.LONG_UPTREND.x_BUY_LONG_UPTREND6", "x_BUY_LONG_UPTREND6",
                             "RULES.LONG_UPTREND.x_BUY_LONG_UPTREND7", "x_BUY_LONG_UPTREND7","RULES.LONG_UPTREND.x_BUY_LONG_UPTREND8", "x_BUY_LONG_UPTREND8","RULES.LONG_UPTREND.x_BUY_LONG_UPTREND9", "x_BUY_LONG_UPTREND9",
                             "RULES.LONG_UPTREND.x_BUY_LONG_UPTREND10", "x_BUY_LONG_UPTREND10","RULES.LONG_UPTREND.x_BUY_LONG_UPTREND11", "x_BUY_LONG_UPTREND11","RULES.LONG_UPTREND.x_BUY_LONG_UPTREND12", "x_BUY_LONG_UPTREND12",
                             "RULES.LONG_UPTREND.x_BUY_LONG_UPTREND13", "x_BUY_LONG_UPTREND13","RULES.LONG_UPTREND.x_BUY_LONG_UPTREND14", "x_BUY_LONG_UPTREND14","RULES.LONG_UPTREND.x_BUY_LONG_UPTREND15", "x_BUY_LONG_UPTREND15",
                             "RULES.LONG_UPTREND.x_BUY_LONG_UPTREND16", "x_BUY_LONG_UPTREND16","RULES.LONG_UPTREND.x_BUY_LONG_UPTREND17", "x_BUY_LONG_UPTREND17","RULES.LONG_UPTREND.x_BUY_LONG_UPTREND18", "x_BUY_LONG_UPTREND18",
                             "RULES.LONG_UPTREND.x_BUY_LONG_UPTREND19", "x_BUY_LONG_UPTREND19","RULES.LONG_UPTREND.x_BUY_LONG_UPTREND20", "x_BUY_LONG_UPTREND20",


                             "RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND1" ,"x_BUY_LONG_DOWNTREND1","RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND2" ,"x_BUY_LONG_DOWNTREND2","RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND3" ,"x_BUY_LONG_DOWNTREND3",
                             "RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND4", "x_BUY_LONG_DOWNTREND4","RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND5" ,"x_BUY_LONG_DOWNTREND5","RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND6" ,"x_BUY_LONG_DOWNTREND6",
                             "RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND7", "x_BUY_LONG_DOWNTREND7","RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND8" ,"x_BUY_LONG_DOWNTREND8","RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND9" ,"x_BUY_LONG_DOWNTREND9",
                             "RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND10", "x_BUY_LONG_DOWNTREND10","RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND11" ,"x_BUY_LONG_DOWNTREND11","RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND12" ,"x_BUY_LONG_DOWNTREND12",
                             "RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND13", "x_BUY_LONG_DOWNTREND13","RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND14" ,"x_BUY_LONG_DOWNTREND14","RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND15" ,"x_BUY_LONG_DOWNTREND15",
                             "RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND16", "x_BUY_LONG_DOWNTREND16","RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND17" ,"x_BUY_LONG_DOWNTREND17","RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND18" ,"x_BUY_LONG_DOWNTREND18",
                             "RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND19", "x_BUY_LONG_DOWNTREND19","RULES.LONG_DOWNTREND.x_BUY_LONG_DOWNTREND20" ,"x_BUY_LONG_DOWNTREND20",

                             "RULES.DANGER_ZONE.x_BUY_DANGER_ZONE1" ,"x_BUY_DANGER_ZONE1","RULES.DANGER_ZONE.x_BUY_DANGER_ZONE2" ,"x_BUY_DANGER_ZONE2","RULES.DANGER_ZONE.x_BUY_DANGER_ZONE3" ,"x_BUY_DANGER_ZONE3",
                             "RULES.DANGER_ZONE.x_BUY_DANGER_ZONE4", "x_BUY_DANGER_ZONE4","RULES.DANGER_ZONE.x_BUY_DANGER_ZONE5" ,"x_BUY_DANGER_ZONE5"


                             "RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND1", "x_BUY_SLOW_DOWNTREND1","RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND2", "x_BUY_SLOW_DOWNTREND2","RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND3", "x_BUY_SLOW_DOWNTREND3",
                             "RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND4", "x_BUY_SLOW_DOWNTREND4","RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND5", "x_BUY_SLOW_DOWNTREND5","RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND6", "x_BUY_SLOW_DOWNTREND6",
                             "RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND7", "x_BUY_SLOW_DOWNTREND7","RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND8", "x_BUY_SLOW_DOWNTREND8","RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND9", "x_BUY_SLOW_DOWNTREND9",
                             "RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND10", "x_BUY_SLOW_DOWNTREND10","RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND11", "x_BUY_SLOW_DOWNTREND11","RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND12", "x_BUY_SLOW_DOWNTREND12",
                             "RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND13", "x_BUY_SLOW_DOWNTREND13","RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND14", "x_BUY_SLOW_DOWNTREND14","RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND15", "x_BUY_SLOW_DOWNTREND15",
                             "RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND16", "x_BUY_SLOW_DOWNTREND16","RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND17", "x_BUY_SLOW_DOWNTREND17","RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND18", "x_BUY_SLOW_DOWNTREND18",
                             "RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND19", "x_BUY_SLOW_DOWNTREND19","RULES.SLOW_DOWNTREND.x_BUY_SLOW_DOWNTREND20", "x_BUY_SLOW_DOWNTREND20",


                             "RULES.ANY.x_BUY_ANY1", "x_BUY_ANY1","RULES.ANY.x_BUY_ANY2", "x_BUY_ANY2","RULES.ANY.x_BUY_ANY3", "x_BUY_ANY3",
                             "RULES.ANY.x_BUY_ANY4", "x_BUY_ANY4","RULES.ANY.x_BUY_ANY5", "x_BUY_ANY5","RULES.ANY.x_BUY_ANY6", "x_BUY_ANY6",
                             "RULES.ANY.x_BUY_ANY7", "x_BUY_ANY7","RULES.ANY.x_BUY_ANY8", "x_BUY_ANY8","RULES.ANY.x_BUY_ANY9", "x_BUY_ANY9",
                             "RULES.ANY.x_BUY_ANY10", "x_BUY_ANY10","RULES.ANY.x_BUY_ANY11", "x_BUY_ANY11","RULES.ANY.x_BUY_ANY12", "x_BUY_ANY12",
                             "RULES.ANY.x_BUY_ANY13", "x_BUY_ANY13","RULES.ANY.x_BUY_ANY14", "x_BUY_ANY14","RULES.ANY.x_BUY_ANY15", "x_BUY_ANY15",
                             "RULES.ANY.x_BUY_ANY16", "x_BUY_ANY16","RULES.ANY.x_BUY_ANY17", "x_BUY_ANY17","RULES.ANY.x_BUY_ANY18", "x_BUY_ANY18",
                             "RULES.ANY.x_BUY_ANY19", "x_BUY_ANY19","RULES.ANY.x_BUY_ANY20", "x_BUY_ANY20",

                             "RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE1", "x_BUY_UPPER_DANGER_ZONE1","RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE2", "x_BUY_UPPER_DANGER_ZONE2","RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE3", "x_BUY_UPPER_DANGER_ZONE3",
                             "RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE4", "x_BUY_UPPER_DANGER_ZONE4","RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE5", "x_BUY_UPPER_DANGER_ZONE5","RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE6", "x_BUY_UPPER_DANGER_ZONE6",
                             "RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE7", "x_BUY_UPPER_DANGER_ZONE7","RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE8", "x_BUY_UPPER_DANGER_ZONE8","RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE9", "x_BUY_UPPER_DANGER_ZONE9",
                             "RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE10", "x_BUY_UPPER_DANGER_ZONE10","RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE11", "x_BUY_UPPER_DANGER_ZONE11","RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE12", "x_BUY_UPPER_DANGER_ZONE12",
                             "RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE13", "x_BUY_UPPER_DANGER_ZONE13","RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE14", "x_BUY_UPPER_DANGER_ZONE14","RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE15", "x_BUY_UPPER_DANGER_ZONE15",
                             "RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE16", "x_BUY_UPPER_DANGER_ZONE16","RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE17", "x_BUY_UPPER_DANGER_ZONE17","RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE18", "x_BUY_UPPER_DANGER_ZONE18",
                             "RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE19", "x_BUY_UPPER_DANGER_ZONE19","RULES.UPPER_DANGER_ZONE.x_BUY_UPPER_DANGER_ZONE20", "x_BUY_UPPER_DANGER_ZONE20",

                             "RULES.NOTREND.x_BUY_NOTREND1", "x_BUY_NOTREND1","RULES.NOTREND.x_BUY_NOTREND2", "x_BUY_NOTREND2","RULES.NOTREND.x_BUY_NOTREND3", "x_BUY_NOTREND3",
                             "RULES.NOTREND.x_BUY_NOTREND4", "x_BUY_NOTREND4","RULES.NOTREND.x_BUY_NOTREND5", "x_BUY_NOTREND5","RULES.NOTREND.x_BUY_NOTREND6", "x_BUY_NOTREND6",
                             "RULES.NOTREND.x_BUY_NOTREND7", "x_BUY_NOTREND7","RULES.NOTREND.x_BUY_NOTREND8", "x_BUY_NOTREND8","RULES.NOTREND.x_BUY_NOTREND9", "x_BUY_NOTREND9",
                             "RULES.NOTREND.x_BUY_NOTREND10", "x_BUY_NOTREND10","RULES.NOTREND.x_BUY_NOTREND11", "x_BUY_NOTREND11","RULES.NOTREND.x_BUY_NOTREND12", "x_BUY_NOTREND12",
                             "RULES.NOTREND.x_BUY_NOTREND13", "x_BUY_NOTREND13","RULES.NOTREND.x_BUY_NOTREND14", "x_BUY_NOTREND14","RULES.NOTREND.x_BUY_NOTREND15", "x_BUY_NOTREND15",
                             "RULES.NOTREND.x_BUY_NOTREND16", "x_BUY_NOTREND16","RULES.NOTREND.x_BUY_NOTREND17", "x_BUY_NOTREND17","RULES.NOTREND.x_BUY_NOTREND18", "x_BUY_NOTREND18",
                             "RULES.NOTREND.x_BUY_NOTREND19", "x_BUY_NOTREND19","RULES.NOTREND.x_BUY_NOTREND20", "x_BUY_NOTREND20",

                            #NOSTALGIA ONES

                            "RULES.CUSTOM.OG_NOSTALGIA.NOSTALGIA_OLD", "NOSTALGIA_OLD","RULES.CUSTOM.OG_NOSTALGIA.NOSTALGIA_LONG_UPTREND", "NOSTALGIA_LONG_UPTREND",
                             "RULES.CUSTOM.OG_NOSTALGIA.NOSTALGIA_LONG_DOWNTREND", "NOSTALGIA_LONG_DOWNTREND","RULES.CUSTOM.OG_NOSTALGIA.NOSTALGIA_SLOW_DOWNTREND", "NOSTALGIA_SLOW_DOWNTREND",
                             "RULES.CUSTOM.OG_NOSTALGIA.NOSTALGIA_HIGH", "NOSTALGIA_HIGH","RULES.CUSTOM.OG_NOSTALGIA.NOSTALGIA_LOW", "NOSTALGIA_LOW",
                             "RULES.CUSTOM.OG_NOSTALGIA.NOSTALGIA_MID", "NOSTALGIA_MID","RULES.CUSTOM.OG_NOSTALGIA.NOSTALGIA_DANGER_ZONE", "NOSTALGIA_DANGER_ZONE",
                            "RULES.CUSTOM.OG_NOSTALGIA.NOSTALGIA_ANY", "NOSTALGIA_ANY","RULES.CUSTOM.OG_NOSTALGIA.NOSTALGIA_NOTREND", "NOSTALGIA_NOTREND",
                            "RULES.CUSTOM.OG_NOSTALGIA.NOSTALGIA_UPPER_DANGER_ZONE", "NOSTALGIA_UPPER_DANGER_ZONE",

                             "RULES.CUSTOM.BEAR_4_INFINITY.BEAR_4_INFINITY_LONG_UPTREND", "BEAR_4_INFINITY_LONG_UPTREND","RULES.CUSTOM.BEAR_4_INFINITY.BEAR_4_INFINITY_ANY", "BEAR_4_INFINITY_ANY",
                             "RULES.CUSTOM.BEAR_4_INFINITY.BEAR_4_INFINITY_LONG_DOWNTREND", "BEAR_4_INFINITY_LONG_DOWNTREND","RULES.CUSTOM.BEAR_4_INFINITY.BEAR_4_INFINITY_SLOW_DOWNTREND", "BEAR_4_INFINITY_SLOW_DOWNTREND",
                             "RULES.CUSTOM.BEAR_4_INFINITY.BEAR_4_INFINITY_HIGH", "BEAR_4_INFINITY_HIGH","RULES.CUSTOM.BEAR_4_INFINITY.BEAR_4_INFINITY_LOW", "BEAR_4_INFINITY_LOW",
                             "RULES.CUSTOM.BEAR_4_INFINITY.BEAR_4_INFINITY_MID", "BEAR_4_INFINITY_MID","RULES.CUSTOM.BEAR_4_INFINITY.BEAR_4_INFINITY_DANGER_ZONE", "BEAR_4_INFINITY_DANGER_ZONE",

                             "RULES.CUSTOM.BULL_4_INFINITY.BULL_4_INFINITY_LONG_UPTREND", "BULL_4_INFINITY_LONG_UPTREND","RULES.CUSTOM.BULL_4_INFINITY.BULL_4_INFINITY_ANY", "BULL_4_INFINITY_ANY",
                             "RULES.CUSTOM.BULL_4_INFINITY.BULL_4_INFINITY_LONG_DOWNTREND", "BULL_4_INFINITY_LONG_DOWNTREND","RULES.CUSTOM.BULL_4_INFINITY.BULL_4_INFINITY_SLOW_DOWNTREND", "BULL_4_INFINITY_SLOW_DOWNTREND",
                             "RULES.CUSTOM.BULL_4_INFINITY.BULL_4_INFINITY_HIGH", "BULL_4_INFINITY_HIGH","RULES.CUSTOM.BULL_4_INFINITY.BULL_4_INFINITY_LOW", "BULL_4_INFINITY_LOW",
                             "RULES.CUSTOM.BULL_4_INFINITY.BULL_4_INFINITY_MID", "BULL_4_INFINITY_MID","RULES.CUSTOM.BULL_4_INFINITY.BULL_4_INFINITY_DANGER_ZONE", "BULL_4_INFINITY_DANGER_ZONE",

                             "RULES.CUSTOM.DOWNTREND_4_INFINITY.DOWNTREND_4_INFINITY_LONG_UPTREND", "DOWNTREND_4_INFINITY_LONG_UPTREND","RULES.CUSTOM.DOWNTREND_4_INFINITY.DOWNTREND_4_INFINITY_ANY", "DOWNTREND_4_INFINITY_ANY",
                             "RULES.CUSTOM.DOWNTREND_4_INFINITY.DOWNTREND_4_INFINITY_LONG_DOWNTREND", "DOWNTREND_4_INFINITY_LONG_DOWNTREND","RULES.CUSTOM.DOWNTREND_4_INFINITY.DOWNTREND_4_INFINITY_SLOW_DOWNTREND", "DOWNTREND_4_INFINITY_SLOW_DOWNTREND",
                             "RULES.CUSTOM.DOWNTREND_4_INFINITY.DOWNTREND_4_INFINITY_HIGH", "DOWNTREND_4_INFINITY_HIGH","RULES.CUSTOM.DOWNTREND_4_INFINITY.DOWNTREND_4_INFINITY_LOW", "DOWNTREND_4_INFINITY_LOW",
                             "RULES.CUSTOM.DOWNTREND_4_INFINITY.DOWNTREND_4_INFINITY_MID", "DOWNTREND_4_INFINITY_MID","RULES.CUSTOM.DOWNTREND_4_INFINITY.DOWNTREND_4_INFINITY_DANGER_ZONE", "DOWNTREND_4_INFINITY_DANGER_ZONE",

                             "RULES.CUSTOM.UPTREND_4_INFINITY.UPTREND_4_INFINITY_LONG_UPTREND", "UPTREND_4_INFINITY_LONG_UPTREND","RULES.CUSTOM.UPTREND_4_INFINITY.UPTREND_4_INFINITY_ANY", "UPTREND_4_INFINITY_ANY",
                             "RULES.CUSTOM.UPTREND_4_INFINITY.UPTREND_4_INFINITY_LONG_DOWNTREND", "UPTREND_4_INFINITY_LONG_DOWNTREND","RULES.CUSTOM.UPTREND_4_INFINITY.UPTREND_4_INFINITY_SLOW_DOWNTREND", "UPTREND_4_INFINITY_SLOW_DOWNTREND",
                             "RULES.CUSTOM.UPTREND_4_INFINITY.UPTREND_4_INFINITY_HIGH", "UPTREND_4_INFINITY_HIGH","RULES.CUSTOM.UPTREND_4_INFINITY.UPTREND_4_INFINITY_LOW", "UPTREND_4_INFINITY_LOW",
                             "RULES.CUSTOM.UPTREND_4_INFINITY.UPTREND_4_INFINITY_MID", "UPTREND_4_INFINITY_MID","RULES.CUSTOM.UPTREND_4_INFINITY.UPTREND_4_INFINITY_DANGER_ZONE", "UPTREND_4_INFINITY_DANGER_ZONE",

                            #SELLER NOSTALGIA ONES

                            "SELL_RULES.CUSTOM.OG_NOSTALGIA.SELLER_NOSTALGIA_OLD", "SELLER_NOSTALGIA_OLD","SELL_RULES.CUSTOM.OG_NOSTALGIA.SELLER_NOSTALGIA_LONG_UPTREND", "SELLER_NOSTALGIA_LONG_UPTREND",
                             "SELL_RULES.CUSTOM.OG_NOSTALGIA.SELLER_NOSTALGIA_LONG_DOWNTREND", "SELLER_NOSTALGIA_LONG_DOWNTREND","SELL_RULES.CUSTOM.OG_NOSTALGIA.SELLER_NOSTALGIA_SLOW_DOWNTREND", "SELLER_NOSTALGIA_SLOW_DOWNTREND",
                             "SELL_RULES.CUSTOM.OG_NOSTALGIA.SELLER_NOSTALGIA_HIGH", "SELLER_NOSTALGIA_HIGH","SELL_RULES.CUSTOM.OG_NOSTALGIA.SELLER_NOSTALGIA_LOW", "SELLER_NOSTALGIA_LOW",
                             "SELL_RULES.CUSTOM.OG_NOSTALGIA.SELLER_NOSTALGIA_MID", "SELLER_NOSTALGIA_MID","SELL_RULES.CUSTOM.OG_NOSTALGIA.SELLER_NOSTALGIA_UPPER_DANGER_ZONE", "SELLER_NOSTALGIA_UPPER_DANGER_ZONE",
                            "SELL_RULES.CUSTOM.OG_NOSTALGIA.SELLER_NOSTALGIA_ANY", "SELLER_NOSTALGIA_ANY","SELL_RULES.CUSTOM.OG_NOSTALGIA.SELLER_NOSTALGIA_DANGER_ZONE", "SELLER_NOSTALGIA_DANGER_ZONE",
                            "SELL_RULES.CUSTOM.OG_NOSTALGIA.SELLER_NOSTALGIA_NOTREND", "SELLER_NOSTALGIA_NOTREND",

                             "SELL_RULES.CUSTOM.BEAR_4_INFINITY.SELLER_BEAR_4_INFINITY_LONG_UPTREND", "SELLER_BEAR_4_INFINITY_LONG_UPTREND","SELL_RULES.CUSTOM.BEAR_4_INFINITY.SELLER_BEAR_4_INFINITY_ANY", "SELLER_BEAR_4_INFINITY_ANY",
                             "SELL_RULES.CUSTOM.BEAR_4_INFINITY.SELLER_BEAR_4_INFINITY_LONG_DOWNTREND", "SELLER_BEAR_4_INFINITY_LONG_DOWNTREND","SELL_RULES.CUSTOM.BEAR_4_INFINITY.SELLER_BEAR_4_INFINITY_SLOW_DOWNTREND", "SELLER_BEAR_4_INFINITY_SLOW_DOWNTREND",
                             "SELL_RULES.CUSTOM.BEAR_4_INFINITY.SELLER_BEAR_4_INFINITY_HIGH", "SELLER_BEAR_4_INFINITY_HIGH","SELL_RULES.CUSTOM.BEAR_4_INFINITY.SELLER_BEAR_4_INFINITY_LOW", "SELLER_BEAR_4_INFINITY_LOW",
                             "SELL_RULES.CUSTOM.BEAR_4_INFINITY.SELLER_BEAR_4_INFINITY_MID", "SELLER_BEAR_4_INFINITY_MID","SELL_RULES.CUSTOM.BEAR_4_INFINITY.SELLER_BEAR_4_INFINITY_UPPER_DANGER_ZONE", "SELLER_BEAR_4_INFINITY_UPPER_DANGER_ZONE",

                             "SELL_RULES.CUSTOM.BULL_4_INFINITY.SELLER_BULL_4_INFINITY_LONG_UPTREND", "SELLER_BULL_4_INFINITY_LONG_UPTREND","SELL_RULES.CUSTOM.BULL_4_INFINITY.SELLER_BULL_4_INFINITY_ANY", "SELLER_BULL_4_INFINITY_ANY",
                             "SELL_RULES.CUSTOM.BULL_4_INFINITY.SELLER_BULL_4_INFINITY_LONG_DOWNTREND", "SELLER_BULL_4_INFINITY_LONG_DOWNTREND","SELL_RULES.CUSTOM.BULL_4_INFINITY.SELLER_BULL_4_INFINITY_SLOW_DOWNTREND", "SELLER_BULL_4_INFINITY_SLOW_DOWNTREND",
                             "SELL_RULES.CUSTOM.BULL_4_INFINITY.SELLER_BULL_4_INFINITY_HIGH", "SELLER_BULL_4_INFINITY_HIGH","SELL_RULES.CUSTOM.BULL_4_INFINITY.SELLER_BULL_4_INFINITY_LOW", "SELLER_BULL_4_INFINITY_LOW",
                             "SELL_RULES.CUSTOM.BULL_4_INFINITY.SELLER_BULL_4_INFINITY_MID", "SELLER_BULL_4_INFINITY_MID","SELL_RULES.CUSTOM.BULL_4_INFINITY.SELLER_BULL_4_INFINITY_UPPER_DANGER_ZONE", "SELLER_BULL_4_INFINITY_UPPER_DANGER_ZONE",

                             "SELL_RULES.CUSTOM.DOWNTREND_4_INFINITY.SELLER_DOWNTREND_4_INFINITY_LONG_UPTREND", "SELLER_DOWNTREND_4_INFINITY_LONG_UPTREND","SELL_RULES.CUSTOM.DOWNTREND_4_INFINITY.SELLER_DOWNTREND_4_INFINITY_ANY", "SELLER_DOWNTREND_4_INFINITY_ANY",
                             "SELL_RULES.CUSTOM.DOWNTREND_4_INFINITY.SELLER_DOWNTREND_4_INFINITY_LONG_DOWNTREND", "SELLER_DOWNTREND_4_INFINITY_LONG_DOWNTREND","SELL_RULES.CUSTOM.DOWNTREND_4_INFINITY.SELLER_DOWNTREND_4_INFINITY_SLOW_DOWNTREND", "SELLER_DOWNTREND_4_INFINITY_SLOW_DOWNTREND",
                             "SELL_RULES.CUSTOM.DOWNTREND_4_INFINITY.SELLER_DOWNTREND_4_INFINITY_HIGH", "SELLER_DOWNTREND_4_INFINITY_HIGH","SELL_RULES.CUSTOM.DOWNTREND_4_INFINITY.SELLER_DOWNTREND_4_INFINITY_LOW", "SELLER_DOWNTREND_4_INFINITY_LOW",
                             "SELL_RULES.CUSTOM.DOWNTREND_4_INFINITY.SELLER_DOWNTREND_4_INFINITY_MID", "SELLER_DOWNTREND_4_INFINITY_MID","SELL_RULES.CUSTOM.DOWNTREND_4_INFINITY.SELLER_DOWNTREND_4_INFINITY_UPPER_DANGER_ZONE", "SELLER_DOWNTREND_4_INFINITY_UPPER_DANGER_ZONE",

                             "SELL_RULES.CUSTOM.UPTREND_4_INFINITY.SELLER_UPTREND_4_INFINITY_LONG_UPTREND", "SELLER_UPTREND_4_INFINITY_LONG_UPTREND","SELL_RULES.CUSTOM.UPTREND_4_INFINITY.SELLER_UPTREND_4_INFINITY_ANY", "SELLER_UPTREND_4_INFINITY_ANY",
                             "SELL_RULES.CUSTOM.UPTREND_4_INFINITY.SELLER_UPTREND_4_INFINITY_LONG_DOWNTREND", "SELLER_UPTREND_4_INFINITY_LONG_DOWNTREND","SELL_RULES.CUSTOM.UPTREND_4_INFINITY.SELLER_UPTREND_4_INFINITY_SLOW_DOWNTREND", "SELLER_UPTREND_4_INFINITY_SLOW_DOWNTREND",
                             "SELL_RULES.CUSTOM.UPTREND_4_INFINITY.SELLER_UPTREND_4_INFINITY_HIGH", "SELLER_UPTREND_4_INFINITY_HIGH","SELL_RULES.CUSTOM.UPTREND_4_INFINITY.SELLER_UPTREND_4_INFINITY_LOW", "SELLER_UPTREND_4_INFINITY_LOW",
                             "SELL_RULES.CUSTOM.UPTREND_4_INFINITY.SELLER_UPTREND_4_INFINITY_MID", "SELLER_UPTREND_4_INFINITY_MID","SELL_RULES.CUSTOM.UPTREND_4_INFINITY.SELLER_UPTREND_4_INFINITY_UPPER_DANGER_ZONE", "SELLER_UPTREND_4_INFINITY_UPPER_DANGER_ZONE",


                            #SELL RULE MODULES
                            "SELL_RULES.LOW.x_SELL_LOW1", "x_SELL_LOW1","SELL_RULES.LOW.x_SELL_LOW2", "x_SELL_LOW2","SELL_RULES.LOW.x_SELL_LOW3", "x_SELL_LOW3",
                             "SELL_RULES.LOW.x_SELL_LOW4", "x_SELL_LOW4","SELL_RULES.LOW.x_SELL_LOW5", "x_SELL_LOW5","SELL_RULES.LOW.x_SELL_LOW6", "x_SELL_LOW6",
                             "SELL_RULES.LOW.x_SELL_LOW7", "x_SELL_LOW7","SELL_RULES.LOW.x_SELL_LOW8", "x_SELL_LOW8","SELL_RULES.LOW.x_SELL_LOW9", "x_SELL_LOW9",
                             "SELL_RULES.LOW.x_SELL_LOW10", "x_SELL_LOW10","SELL_RULES.LOW.x_SELL_LOW11", "x_SELL_LOW11","SELL_RULES.LOW.x_SELL_LOW12", "x_SELL_LOW12",
                             "SELL_RULES.LOW.x_SELL_LOW13", "x_SELL_LOW13","SELL_RULES.LOW.x_SELL_LOW14", "x_SELL_LOW14","SELL_RULES.LOW.x_SELL_LOW15", "x_SELL_LOW15",
                             "SELL_RULES.LOW.x_SELL_LOW16", "x_SELL_LOW16","SELL_RULES.LOW.x_SELL_LOW17", "x_SELL_LOW17","SELL_RULES.LOW.x_SELL_LOW18", "x_SELL_LOW18",
                             "SELL_RULES.LOW.x_SELL_LOW19", "x_SELL_LOW19","SELL_RULES.LOW.x_SELL_LOW20", "x_SELL_LOW20",


                             "SELL_RULES.MID.x_SELL_MID1", "x_SELL_MID1","SELL_RULES.MID.x_SELL_MID2", "x_SELL_MID2","SELL_RULES.MID.x_SELL_MID3", "x_SELL_MID3",
                             "SELL_RULES.MID.x_SELL_MID4", "x_SELL_MID4","SELL_RULES.MID.x_SELL_MID5", "x_SELL_MID5","SELL_RULES.MID.x_SELL_MID6", "x_SELL_MID6",
                             "SELL_RULES.MID.x_SELL_MID7", "x_SELL_MID7","SELL_RULES.MID.x_SELL_MID8", "x_SELL_MID8","SELL_RULES.MID.x_SELL_MID9", "x_SELL_MID9",
                             "SELL_RULES.MID.x_SELL_MID10", "x_SELL_MID10","SELL_RULES.MID.x_SELL_MID11", "x_SELL_MID11","SELL_RULES.MID.x_SELL_MID12", "x_SELL_MID12",
                             "SELL_RULES.MID.x_SELL_MID13", "x_SELL_MID13","SELL_RULES.MID.x_SELL_MID14", "x_SELL_MID14","SELL_RULES.MID.x_SELL_MID15", "x_SELL_MID15",
                             "SELL_RULES.MID.x_SELL_MID16", "x_SELL_MID16","SELL_RULES.MID.x_SELL_MID17", "x_SELL_MID17","SELL_RULES.MID.x_SELL_MID18", "x_SELL_MID18",
                             "SELL_RULES.MID.x_SELL_MID19", "x_SELL_MID19","SELL_RULES.MID.x_SELL_MID20", "x_SELL_MID20",


                             "SELL_RULES.HIGH.x_SELL_HIGH1", "x_SELL_HIGH1","SELL_RULES.HIGH.x_SELL_HIGH2", "x_SELL_HIGH2","SELL_RULES.HIGH.x_SELL_HIGH3", "x_SELL_HIGH3",
                             "SELL_RULES.HIGH.x_SELL_HIGH4", "x_SELL_HIGH4","SELL_RULES.HIGH.x_SELL_HIGH5", "x_SELL_HIGH5","SELL_RULES.HIGH.x_SELL_HIGH6", "x_SELL_HIGH6",
                             "SELL_RULES.HIGH.x_SELL_HIGH7", "x_SELL_HIGH7","SELL_RULES.HIGH.x_SELL_HIGH8", "x_SELL_HIGH8","SELL_RULES.HIGH.x_SELL_HIGH9", "x_SELL_HIGH9",
                             "SELL_RULES.HIGH.x_SELL_HIGH10", "x_SELL_HIGH10","SELL_RULES.HIGH.x_SELL_HIGH11", "x_SELL_HIGH11","SELL_RULES.HIGH.x_SELL_HIGH12", "x_SELL_HIGH12",
                             "SELL_RULES.HIGH.x_SELL_HIGH13", "x_SELL_HIGH13","SELL_RULES.HIGH.x_SELL_HIGH14", "x_SELL_HIGH14","SELL_RULES.HIGH.x_SELL_HIGH15", "x_SELL_HIGH15",
                             "SELL_RULES.HIGH.x_SELL_HIGH16", "x_SELL_HIGH16","SELL_RULES.HIGH.x_SELL_HIGH17", "x_SELL_HIGH17","SELL_RULES.HIGH.x_SELL_HIGH18", "x_SELL_HIGH18",
                             "SELL_RULES.HIGH.x_SELL_HIGH19", "x_SELL_HIGH19","SELL_RULES.HIGH.x_SELL_HIGH20", "x_SELL_HIGH20",



                             "SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND1", "x_SELL_LONG_UPTREND1","SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND2", "x_SELL_LONG_UPTREND2","SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND3", "x_SELL_LONG_UPTREND3",
                             "SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND4", "x_SELL_LONG_UPTREND4","SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND5", "x_SELL_LONG_UPTREND5","SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND6", "x_SELL_LONG_UPTREND6",
                             "SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND7", "x_SELL_LONG_UPTREND7","SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND8", "x_SELL_LONG_UPTREND8","SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND9", "x_SELL_LONG_UPTREND9",
                             "SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND10", "x_SELL_LONG_UPTREND10","SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND11", "x_SELL_LONG_UPTREND11","SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND12", "x_SELL_LONG_UPTREND12",
                             "SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND13", "x_SELL_LONG_UPTREND13","SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND14", "x_SELL_LONG_UPTREND14","SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND15", "x_SELL_LONG_UPTREND15",
                             "SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND16", "x_SELL_LONG_UPTREND16","SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND17", "x_SELL_LONG_UPTREND17","SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND18", "x_SELL_LONG_UPTREND18",
                             "SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND19", "x_SELL_LONG_UPTREND19","SELL_RULES.LONG_UPTREND.x_SELL_LONG_UPTREND20", "x_SELL_LONG_UPTREND20",


                             "SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND1" ,"x_SELL_LONG_DOWNTREND1","SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND2" ,"x_SELL_LONG_DOWNTREND2","SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND3" ,"x_SELL_LONG_DOWNTREND3",
                             "SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND4", "x_SELL_LONG_DOWNTREND4","SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND5" ,"x_SELL_LONG_DOWNTREND5","SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND6" ,"x_SELL_LONG_DOWNTREND6",
                             "SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND7", "x_SELL_LONG_DOWNTREND7","SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND8" ,"x_SELL_LONG_DOWNTREND8","SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND9" ,"x_SELL_LONG_DOWNTREND9",
                             "SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND10", "x_SELL_LONG_DOWNTREND10","SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND11" ,"x_SELL_LONG_DOWNTREND11","SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND12" ,"x_SELL_LONG_DOWNTREND12",
                             "SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND13", "x_SELL_LONG_DOWNTREND13","SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND14" ,"x_SELL_LONG_DOWNTREND14","SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND15" ,"x_SELL_LONG_DOWNTREND15",
                             "SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND16", "x_SELL_LONG_DOWNTREND16","SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND17" ,"x_SELL_LONG_DOWNTREND17","SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND18" ,"x_SELL_LONG_DOWNTREND18",
                             "SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND19", "x_SELL_LONG_DOWNTREND19","SELL_RULES.LONG_DOWNTREND.x_SELL_LONG_DOWNTREND20" ,"x_SELL_LONG_DOWNTREND20",


                             "SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND1", "x_SELL_SLOW_DOWNTREND1","SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND2", "x_SELL_SLOW_DOWNTREND2","SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND3", "x_SELL_SLOW_DOWNTREND3",
                             "SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND4", "x_SELL_SLOW_DOWNTREND4","SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND5", "x_SELL_SLOW_DOWNTREND5","SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND6", "x_SELL_SLOW_DOWNTREND6",
                             "SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND7", "x_SELL_SLOW_DOWNTREND7","SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND8", "x_SELL_SLOW_DOWNTREND8","SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND9", "x_SELL_SLOW_DOWNTREND9",
                             "SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND10", "x_SELL_SLOW_DOWNTREND10","SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND11", "x_SELL_SLOW_DOWNTREND11","SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND12", "x_SELL_SLOW_DOWNTREND12",
                             "SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND13", "x_SELL_SLOW_DOWNTREND13","SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND14", "x_SELL_SLOW_DOWNTREND14","SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND15", "x_SELL_SLOW_DOWNTREND15",
                             "SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND16", "x_SELL_SLOW_DOWNTREND16","SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND17", "x_SELL_SLOW_DOWNTREND17","SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND18", "x_SELL_SLOW_DOWNTREND18",
                             "SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND19", "x_SELL_SLOW_DOWNTREND19","SELL_RULES.SLOW_DOWNTREND.x_SELL_SLOW_DOWNTREND20", "x_SELL_SLOW_DOWNTREND20",


                             "SELL_RULES.ANY.x_SELL_ANY1", "x_SELL_ANY1","SELL_RULES.ANY.x_SELL_ANY2", "x_SELL_ANY2","SELL_RULES.ANY.x_SELL_ANY3", "x_SELL_ANY3",
                             "SELL_RULES.ANY.x_SELL_ANY4", "x_SELL_ANY4","SELL_RULES.ANY.x_SELL_ANY5", "x_SELL_ANY5","SELL_RULES.ANY.x_SELL_ANY6", "x_SELL_ANY6",
                             "SELL_RULES.ANY.x_SELL_ANY7", "x_SELL_ANY7","SELL_RULES.ANY.x_SELL_ANY8", "x_SELL_ANY8","SELL_RULES.ANY.x_SELL_ANY9", "x_SELL_ANY9",
                             "SELL_RULES.ANY.x_SELL_ANY10", "x_SELL_ANY10","SELL_RULES.ANY.x_SELL_ANY11", "x_SELL_ANY11","SELL_RULES.ANY.x_SELL_ANY12", "x_SELL_ANY12",
                             "SELL_RULES.ANY.x_SELL_ANY13", "x_SELL_ANY13","SELL_RULES.ANY.x_SELL_ANY14", "x_SELL_ANY14","SELL_RULES.ANY.x_SELL_ANY15", "x_SELL_ANY15",
                             "SELL_RULES.ANY.x_SELL_ANY16", "x_SELL_ANY16","SELL_RULES.ANY.x_SELL_ANY17", "x_SELL_ANY17","SELL_RULES.ANY.x_SELL_ANY18", "x_SELL_ANY18",
                             "SELL_RULES.ANY.x_SELL_ANY19", "x_SELL_ANY19","SELL_RULES.ANY.x_SELL_ANY20", "x_SELL_ANY20",

                             "SELL_RULES.NOTREND.x_SELL_NOTREND1", "x_SELL_NOTREND1","SELL_RULES.NOTREND.x_SELL_NOTREND2", "x_SELL_NOTREND2","SELL_RULES.NOTREND.x_SELL_NOTREND3", "x_SELL_NOTREND3",
                             "SELL_RULES.NOTREND.x_SELL_NOTREND4", "x_SELL_NOTREND4","SELL_RULES.NOTREND.x_SELL_NOTREND5", "x_SELL_NOTREND5","SELL_RULES.NOTREND.x_SELL_NOTREND6", "x_SELL_NOTREND6",
                             "SELL_RULES.NOTREND.x_SELL_NOTREND7", "x_SELL_NOTREND7","SELL_RULES.NOTREND.x_SELL_NOTREND8", "x_SELL_NOTREND8","SELL_RULES.NOTREND.x_SELL_NOTREND9", "x_SELL_NOTREND9",
                             "SELL_RULES.NOTREND.x_SELL_NOTREND10", "x_SELL_NOTREND10","SELL_RULES.NOTREND.x_SELL_NOTREND11", "x_SELL_NOTREND11","SELL_RULES.NOTREND.x_SELL_NOTREND12", "x_SELL_NOTREND12",
                             "SELL_RULES.NOTREND.x_SELL_NOTREND13", "x_SELL_NOTREND13","SELL_RULES.NOTREND.x_SELL_NOTREND14", "x_SELL_NOTREND14","SELL_RULES.NOTREND.x_SELL_NOTREND15", "x_SELL_NOTREND15",
                             "SELL_RULES.NOTREND.x_SELL_NOTREND16", "x_SELL_NOTREND16","SELL_RULES.NOTREND.x_SELL_NOTREND17", "x_SELL_NOTREND17","SELL_RULES.NOTREND.x_SELL_NOTREND18", "x_SELL_NOTREND18",
                             "SELL_RULES.NOTREND.x_SELL_NOTREND19", "x_SELL_NOTREND19","SELL_RULES.NOTREND.x_SELL_NOTREND20", "x_SELL_NOTREND20",

                             "SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE1", "x_SELL_UPPER_DANGER_ZONE1","SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE2", "x_SELL_UPPER_DANGER_ZONE2","SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE3", "x_SELL_UPPER_DANGER_ZONE3",
                             "SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE4", "x_SELL_UPPER_DANGER_ZONE4","SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE5", "x_SELL_UPPER_DANGER_ZONE5","SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE6", "x_SELL_UPPER_DANGER_ZONE6",
                             "SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE7", "x_SELL_UPPER_DANGER_ZONE7","SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE8", "x_SELL_UPPER_DANGER_ZONE8","SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE9", "x_SELL_UPPER_DANGER_ZONE9",
                             "SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE10", "x_SELL_UPPER_DANGER_ZONE10","SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE11", "x_SELL_UPPER_DANGER_ZONE11","SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE12", "x_SELL_UPPER_DANGER_ZONE12",
                             "SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE13", "x_SELL_UPPER_DANGER_ZONE13","SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE14", "x_SELL_UPPER_DANGER_ZONE14","SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE15", "x_SELL_UPPER_DANGER_ZONE15",
                             "SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE16", "x_SELL_UPPER_DANGER_ZONE16","SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE17", "x_SELL_UPPER_DANGER_ZONE17","SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE18", "x_SELL_UPPER_DANGER_ZONE18",
                             "SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE19", "x_SELL_UPPER_DANGER_ZONE19","SELL_RULES.UPPER_DANGER_ZONE.x_SELL_UPPER_DANGER_ZONE20", "x_SELL_UPPER_DANGER_ZONE20",

                            "SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE1", "x_SELL_DANGER_ZONE1","SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE2", "x_SELL_DANGER_ZONE2","SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE3", "x_SELL_DANGER_ZONE3",
                             "SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE4", "x_SELL_DANGER_ZONE4","SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE5", "x_SELL_DANGER_ZONE5","SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE6", "x_SELL_DANGER_ZONE6",
                             "SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE7", "x_SELL_DANGER_ZONE7","SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE8", "x_SELL_DANGER_ZONE8","SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE9", "x_SELL_DANGER_ZONE9",
                             "SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE10", "x_SELL_DANGER_ZONE10","SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE11", "x_SELL_DANGER_ZONE11","SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE12", "x_SELL_DANGER_ZONE12",
                             "SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE13", "x_SELL_DANGER_ZONE13","SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE14", "x_SELL_DANGER_ZONE14","SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE15", "x_SELL_DANGER_ZONE15",
                             "SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE16", "x_SELL_DANGER_ZONE16","SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE17", "x_SELL_DANGER_ZONE17","SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE18", "x_SELL_DANGER_ZONE18",
                             "SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE19", "x_SELL_DANGER_ZONE19","SELL_RULES.DANGER_ZONE.x_SELL_DANGER_ZONE20", "x_SELL_DANGER_ZONE20",


                            "COMMON.COMMON_FUNCTIONS", "COMMON.CONSTANTS","COMMON.TA_FUNCTIONS",
                            "COMMON_FUNCTIONS", "CONSTANTS","TA_FUNCTIONS","POPULATE_INDICATORS", "COMMON.BUYS","COMMON.SELLS",

                            "COMMON.POPULATE_INDICATORS","POPULATE_INDICATORS","COMMON.INDICATORS1","INDICATORS1","COMMON.INDICATORS1_RARE","INDICATORS1_RARE",
                            "COMMON.INDICATORS2","INDICATORS2","COMMON.INDICATORS2_RARE","INDICATORS2_RARE","COMMON.INDICATORS3","INDICATORS3",
                            "COMMON.INDICATORS3_RARE","INDICATORS3_RARE","COMMON.INDICATORS1H","INDICATORS1H","COMMON.INDICATORS1D","INDICATORS1D",
                            "COMMON.INDICATORS_OTHER","INDICATORS_OTHER",

                            "AltcoinTrader15",
                            # "x_Buy1","x_Buy2","x_Buy3","x_Buy4","x_Buy5","x_Sell1","x_Sell2","x_Sell3","x_Sell4","x_Sell5",
                            # "x_Buys_ANY","x_Buys_NOTREND","x_Buys_LOW","x_Buys_MID","x_Buys_HIGH","x_Buys_LONG_UPTREND","x_Buys_LONG_DOWNTREND","x_Buys_SLOW_DOWNTREND","x_Buys_DANGER_ZONE",
                            # "x_Sells_ANY","x_Sells_NOTREND","x_Sells_LOW","x_Sells_MID","x_Sells_HIGH","x_Sells_LONG_UPTREND","x_Sells_LONG_DOWNTREND","x_Sells_SLOW_DOWNTREND","x_Sells_DANGER_ZONE","x_Sells_UPPER_DANGER_ZONE",
                            "z____placeholders______",

                            "BuyerDevDangerZone","buyer_dev_DANGER_ZONE","BuyerDevDowntrendUpswing","BuyerDevHigh","buyer_dev_HIGH",
                            "BuyerDevLongDowntrend","buyer_dev_LONG_DOWNTREND","BuyerDevLongUptrend","buyer_dev_LONG_UPTREND","BuyerDevLow","buyer_dev_LOW",
                            "BuyerDevMid","buyer_dev_MID","BuyerDevSlowDowntrend","buyer_dev_SLOW_DOWNTREND","BuyerDevUpperDangerZone","buyer_dev_UPPER_DANGER_ZONE",
                            "BuyerDevAny","buyer_dev_ANY","BuyerDevNotrend","buyer_dev_NOTREND",

                            "SellerDevDangerZone","seller_dev_DANGER_ZONE","SellerDevDowntrendUpswing","SellerDevHigh","seller_dev_HIGH",
                            "SellerDevLongDowntrend","seller_dev_LONG_DOWNTREND","SellerDevLongUptrend","seller_dev_LONG_UPTREND","SellerDevLow","seller_dev_LOW",
                            "SellerDevMid","seller_dev_MID","SellerDevSlowDowntrend","seller_dev_SLOW_DOWNTREND","SellerDevUpperDangerZone","seller_dev_UPPER_DANGER_ZONE",
                            "SellerDevAny", "seller_dev_ANY", "SellerDevNotrend", "seller_dev_NOTREND",

                            "Common","CommonBuyerLOW","CommonBuyerMID","CommonBuyerHIGH","Constants","BUYS","SELLS","ALL_RULES_BUYS","ALL_RULES_SELLS"
                            ]

timeframes_needed_list=["15m","1h","1d"]

data_loading_time_ms = 1815000000   #21 days


indicators1_default = ['sma50', 'sma200', 'sma400', 'sma10k']

config_file = "run-configuration.json"

fiat_currency = "USDT"

enable_sound = True

# date_until_gap = 5259492000 # 2 months
date_until_gap = 7889238000  # 3 months
# date_until_gap = 9289238000  # 3.5 months


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Freqtrade Strategy Tester'
        self.left = 15
        self.top = 40
        self.width = 1050
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

        # Set indicators 1 dropdown
        self.indicator1_list = []
        self.indicator1_list_labels = []
        for pair in indicators1_list :
            for key, value in pair.items():
                self.indicator1_list_labels.append(key)
                self.indicator1_list.append(value)

        # Set indicators 2 dropdown
        self.indicator2_list = []
        self.indicator2_list_labels = []
        for pair in indicators2_list :
            for key, value in pair.items():
                self.indicator2_list_labels.append(key)
                self.indicator2_list.append(value)

        # Set indicators 3 dropdown
        self.indicator3_list = []
        self.indicator3_list_labels = []
        for pair in indicators3_list :
            for key, value in pair.items():
                self.indicator3_list_labels.append(key)
                self.indicator3_list.append(value)

        # Set indicators_rare 1 dropdown
        self.indicator1_rare_list = []
        self.indicator1_rare_list_labels = []
        for pair in indicators1_rare_list :
            for key, value in pair.items():
                self.indicator1_rare_list_labels.append(key)
                self.indicator1_rare_list.append(value)

        # Set indicators_rare 2 dropdown
        self.indicator2_rare_list = []
        self.indicator2_rare_list_labels = []
        for pair in indicators2_rare_list :
            for key, value in pair.items():
                self.indicator2_rare_list_labels.append(key)
                self.indicator2_rare_list.append(value)

        # Set indicators_rare 3 dropdown
        self.indicator3_rare_list = []
        self.indicator3_rare_list_labels = []
        for pair in indicators3_rare_list :
            for key, value in pair.items():
                self.indicator3_rare_list_labels.append(key)
                self.indicator3_rare_list.append(value)

        # Set configs
        self.configs = configs_json

        f = open(config_file)
        self.data = json.load(f)
        f.close()

        # app.aboutToQuit.connect(self.on_click_save_json)

        self.backtesting_clicked = False
        self.show_plot_clicked = False
        self.hyperopt_clicked = False
        self.download_clicked = False

        self.backtest_data_enabled = False #IF TRUE SHOWS DETAILED BACKTESTING DATA CLASHES
        self.backtest_data_issues_display = ""

        self.command_list = []

        self.ctrl_or_shift_pressed = False
        self.x_pressed = False #Adds indicators to Indicators2
        self.c_pressed = False #Adds indicators to Indicators3

                # Collect events until released
        self.listener = Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.listener.start()

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
        self.combobox_strategy.setMaxVisibleItems(50)
        self.combobox_strategy.addItems(self.strategies_label)
        self.combobox_strategy.setCurrentIndex(self.data["strategy"])
        self.combobox_strategy.currentIndexChanged.connect(self.on_select_strategy)

        # Label Indicators 1
        self.indicator1_text_label = QLabel(self)
        self.indicator1_text_label.setText('Indicators 1:')
        self.indicator1_text_label.move(20, 80)
        # Textbox Indicator 1
        self.indicator1_textbox = QLineEdit(self)
        self.indicator1_textbox.move(90, 78)
        self.indicator1_textbox.resize(260, 20)
        self.indicator1_textbox.setText(self.data["indicators1"]["text"])
        self.indicator1_textbox.editingFinished.connect(self.on_textchange_indicators1)
        if (self.data["indicators1"]["enabled"] == True):
            self.indicator1_textbox.setEnabled(True)
        else:
            self.indicator1_textbox.setEnabled(False)

        # Dropdown Indicators 1
        self.combobox_indicator1 = QComboBox(self)
        self.combobox_indicator1.setGeometry(370, 78, 120, 20)
        self.combobox_indicator1.setMaxVisibleItems(50)
        self.combobox_indicator1.addItems(self.indicator1_list_labels)
        self.combobox_indicator1.setCurrentIndex(self.data["indicator1_dropdown"])
        self.combobox_indicator1.setToolTip('Hold SHIFT or CTRL to add to the indicators, instead of replacing.')
        self.combobox_indicator1.currentIndexChanged.connect(self.on_select_indicator1_list)
        # Dropdown Indicators 1 RARE
        self.combobox_indicator1_rare = QComboBox(self)
        self.combobox_indicator1_rare.setGeometry(490, 78, 120, 20)
        self.combobox_indicator1_rare.setMaxVisibleItems(50)
        self.combobox_indicator1_rare.addItems(self.indicator1_rare_list_labels)
        self.combobox_indicator1_rare.setCurrentIndex(self.data["indicator1_rare_dropdown"])
        self.combobox_indicator1_rare.setToolTip('Hold SHIFT or CTRL to add to the indicators, instead of replacing.')
        self.combobox_indicator1_rare.currentIndexChanged.connect(self.on_select_indicator1_rare_list)

        # Checkbox Indicators 1 Enable
        self.indicator1_checkbox = QCheckBox(self)
        self.indicator1_checkbox.move(353, 82)
        self.indicator1_checkbox.setChecked(self.data["indicators1"]["enabled"])
        self.indicator1_checkbox.stateChanged.connect(self.checkbox_indicators1)

        # Label Indicators 2
        self.indicator2_label = QLabel(self)
        self.indicator2_label.setText('Indicators 2:')
        self.indicator2_label.move(20, 134)
        # Textbox Indicator 2
        self.indicator2_textbox = QLineEdit(self)
        self.indicator2_textbox.move(90, 132)
        self.indicator2_textbox.resize(260, 20)
        self.indicator2_textbox.setText(self.data["indicators2"]["text"])
        self.indicator2_textbox.editingFinished.connect(self.on_textchange_indicators2)
        if (self.data["indicators2"]["enabled"] == True):
            self.indicator2_textbox.setEnabled(True)
        else:
            self.indicator2_textbox.setEnabled(False)

        # Dropdown Indicators 2
        self.combobox_indicator2 = QComboBox(self)
        self.combobox_indicator2.setGeometry(370, 132, 120, 20)
        self.combobox_indicator2.setMaxVisibleItems(50)
        self.combobox_indicator2.addItems(self.indicator2_list_labels)
        self.combobox_indicator2.setCurrentIndex(self.data["indicator2_dropdown"])
        self.combobox_indicator2.setToolTip('Hold SHIFT or CTRL to add to the indicators, instead of replacing. Hold X to add to Indicators 3.')
        self.combobox_indicator2.currentIndexChanged.connect(self.on_select_indicator2_list)
        # Dropdown Indicators 2 RARE
        self.combobox_indicator2_rare = QComboBox(self)
        self.combobox_indicator2_rare.setGeometry(490, 132, 120, 20)
        self.combobox_indicator2_rare.setMaxVisibleItems(50)
        self.combobox_indicator2_rare.addItems(self.indicator2_rare_list_labels)
        self.combobox_indicator2_rare.setCurrentIndex(self.data["indicator2_rare_dropdown"])
        self.combobox_indicator2_rare.setToolTip('Hold SHIFT or CTRL to add to the indicators, instead of replacing.')
        self.combobox_indicator2_rare.currentIndexChanged.connect(self.on_select_indicator2_rare_list)

        # Checkbox Indicators 2 Enable
        self.indicator2_checkbox = QCheckBox(self)
        self.indicator2_checkbox.move(353, 136)
        self.indicator2_checkbox.setChecked(self.data["indicators2"]["enabled"])
        self.indicator2_checkbox.stateChanged.connect(self.checkbox_indicators2)

        # Label Indicators 3
        self.indicator3_label = QLabel(self)
        self.indicator3_label.setText('Indicators 3:')
        self.indicator3_label.move(20, 164)
        # Textbox Indicator 3
        self.indicator3_textbox = QLineEdit(self)
        self.indicator3_textbox.move(90, 162)
        self.indicator3_textbox.resize(260, 20)
        self.indicator3_textbox.setText(self.data["indicators3"]["text"])
        self.indicator3_textbox.editingFinished.connect(self.on_textchange_indicators3)
        if (self.data["indicators3"]["enabled"] == True):
            self.indicator3_textbox.setEnabled(True)
        else:
            self.indicator3_textbox.setEnabled(False)

        # Dropdown Indicators 3
        self.combobox_indicator3 = QComboBox(self)
        self.combobox_indicator3.setGeometry(370, 162, 120, 20)
        self.combobox_indicator3.setMaxVisibleItems(50)
        self.combobox_indicator3.addItems(self.indicator3_list_labels)
        self.combobox_indicator3.setCurrentIndex(self.data["indicator3_dropdown"])
        self.combobox_indicator3.setToolTip('Hold SHIFT or CTRL to add to the indicators, instead of replacing. Hold Z to add to Indicators 2.')
        self.combobox_indicator3.currentIndexChanged.connect(self.on_select_indicator3_list)
        # Dropdown Indicators 3 RARE
        self.combobox_indicator3_rare = QComboBox(self)
        self.combobox_indicator3_rare.setGeometry(490, 162, 120, 20)
        self.combobox_indicator3_rare.setMaxVisibleItems(50)
        self.combobox_indicator3_rare.addItems(self.indicator3_rare_list_labels)
        self.combobox_indicator3_rare.setCurrentIndex(self.data["indicator3_rare_dropdown"])
        self.combobox_indicator3_rare.setToolTip('Hold SHIFT or CTRL to add to the indicators, instead of replacing.')
        self.combobox_indicator3_rare.currentIndexChanged.connect(self.on_select_indicator3_rare_list)

        # Checkbox Indicators 3 Enable
        self.indicator3_checkbox = QCheckBox(self)
        self.indicator3_checkbox.move(353, 166)
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
        self.indicator_extra_dropdown_solo.setMaxVisibleItems(10)
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
        self.time_from_label.move(510, 12)
        # Time From Dropdown
        self.time_from_dropdown = QComboBox(self)
        self.time_from_dropdown.setGeometry(510, 30, 150, 30)
        self.time_from_dropdown.setMaxVisibleItems(20)
        self.time_from_dropdown.addItems(self.timeframes_label)
        self.time_from_dropdown.setCurrentIndex(self.data["time"]["time_from_index"])
        self.time_from_dropdown.currentIndexChanged.connect(self.on_select_time_from)
        # Time From Calendar
        self.time_from_calendar = QDateEdit(self, calendarPopup=True)
        self.time_from_calendar.setGeometry(510, 30, 150, 30)
        self.time_from_calendar.setDateTime(QDateTime.fromMSecsSinceEpoch(self.data["time"]["time_from"]))
        self.time_from_calendar.dateChanged.connect(self.on_select_from_date)
        self.time_from_calendar.hide()
        if (self.data["time"]["time_from_date"] == True):
            self.time_from_calendar.show()
            self.time_from_dropdown.hide()
        # Time From label checkbox
        self.time_from_date_label = QLabel(self)
        self.time_from_date_label.setText('Date')
        self.time_from_date_label.move(620, 12)
        # Time From Checkbox Date
        self.time_from_checkbox_date = QCheckBox(self)
        self.time_from_checkbox_date.move(646, 13)
        self.time_from_checkbox_date.setChecked(self.data["time"]["time_from_date"])
        self.time_from_checkbox_date.stateChanged.connect(self.checkbox_time_from_date)
        # Time From label
        self.time_from_final_date_label = QLabel(self)
        self.time_from_final_date_label.setText(unix_to_datetime(self.data["time"]["time_from"], True, True))
        self.time_from_final_date_label.move(604, 72)

        ## ^ ^ WHEN THIS ONE IS UPDATED, UPDATE THE TIME UNTIL TO THE NEXT NUMBER AUTOMATICALLY

        # Time From to Util arrows label
        self.time_arrow_label = QLabel(self)
        self.time_arrow_label.setText('----->')
        self.time_arrow_label.move(670, 36)
        self.time_arrow_lower_label = QLabel(self)
        self.time_arrow_lower_label.setText('---->')
        self.time_arrow_lower_label.move(670, 72)

        # Time Until label
        self.time_until_label = QLabel(self)
        self.time_until_label.setText('Time Until:')
        self.time_until_label.move(710, 12)
        # Time Until label checkbox
        self.time_until_label_checkbox = QLabel(self)
        self.time_until_label_checkbox.setText('Date')
        self.time_until_label_checkbox.move(820, 12)
        # Time Until Checkbox Date
        self.time_until_checkbox_date = QCheckBox(self)
        self.time_until_checkbox_date.move(846, 13)
        self.time_until_checkbox_date.setChecked(self.data["time"]["time_until_date"])
        self.time_until_checkbox_date.stateChanged.connect(self.checkbox_time_until_date)
        # Time Until Dropdown
        self.time_until_dropdown = QComboBox(self)
        self.time_until_dropdown.setGeometry(710, 30, 150, 30)
        self.time_until_dropdown.setMaxVisibleItems(20)
        self.time_until_dropdown.addItems(self.timeframes_label)
        self.time_until_dropdown.setCurrentIndex(self.data["time"]["time_until_index"])
        self.time_until_dropdown.currentIndexChanged.connect(self.on_select_time_until)
        # Time Until Calendar
        self.time_until_calendar = QDateEdit(self, calendarPopup=True)
        self.time_until_calendar.setGeometry(710, 30, 150, 30)
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
        self.time_until_checkbox.move(867, 37)
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
        self.time_until_final_date_label.move(704, 72)
        # Time difference label
        self.time_difference_label = QLabel(self)
        self.time_difference_label.setText(
            "Days: " + str(days_between_timestamps(self.data["time"]["time_from"], self.data["time"]["time_until"])))
        self.time_difference_label.move(810, 72)


        # Download Data
        self.download_data_button = QPushButton('Download Data', self)
        self.download_data_button.setToolTip('Download 15m and 1h data for the selected pairs')
        self.download_data_button.move(910, 12)
        self.download_data_button.clicked.connect(self.on_click_download_data)
        # # Download Data 1h
        # self.download_1h_button=QPushButton('1h',self)
        # self.download_1h_button.setToolTip('Download 1h data for the selected pairs')
        # self.download_1h_button.move(760, 32)
        # self.download_1h_button.clicked.connect(self.on_click_1h)
        # Download Data days textbox
        self.textbox_download_days = QLineEdit(self)
        self.textbox_download_days.move(992, 15)
        self.textbox_download_days.resize(45, 18)
        self.textbox_download_days.setText(str(self.data["download"]["days_to_download"]))
        self.textbox_download_days.textChanged.connect(self.on_textchange_download_days)

        # Download Data latest from pairlist label
        self.label_download_data_latest = QLabel(self)
        self.label_download_data_latest.setText(
            'Latest Data:           ' + unix_to_datetime(self.data["download"]["latest_update"], True, True))
        self.label_download_data_latest.move(883, 100)
        self.label_download_data_latest.setToolTip("What is the date of most recent download-data update for trading pairs. (From Pairs1)")

        # Download Data days from pairlist label
        self.label_download_days_latest = QLabel(self)
        self.label_download_days_latest.setText("("+str(self.data["download"]["latest_days"]) + " days)")
        self.label_download_days_latest.move(979, 82)
        self.label_download_days_latest.setToolTip("How many days of data downloaded back from latest date. (From Pairs1)")

        # Download Data absolute latest label
        self.label_download_data_abs_latest = QLabel(self)
        self.label_download_data_abs_latest.setText(
            'Abs Latest Data:    ' + unix_to_datetime(self.data["download"]["absolute_latest_update"], True, True))
        self.label_download_data_abs_latest.move(883, 125)
        self.label_download_data_abs_latest.setToolTip("What is the absolute latest (recent) time backtesting data was downloaded for any pairs. (From Pairs1)")

        # Download Data days since update
        self.label_download_days_since_update = QLabel(self)
        self.label_download_days_since_update.setText(f"Time Since Update: {days_between_timestamps( self.data['download']['absolute_latest_update'], int(datetime_to_unix(datetime.datetime.now(), False)))} days")
        self.label_download_days_since_update.move(883, 150)
        self.label_download_days_since_update.setToolTip("How many days have passed since the latest download-data update. (From Pairs1)")
        # Download Data clashes label
        self.label_download_data_clashes = QLabel(self)
        self.label_download_data_clashes.setText("Latest Date Clash!")
        self.label_download_data_clashes.move(900, 46)
        self.label_download_data_clashes.hide()

        # Download Data check button
        self.check_downloaded_data_button = QPushButton('Check', self)
        self.check_downloaded_data_button.setToolTip('Check downloaded data for the selected pairs')
        self.check_downloaded_data_button.move(990, 40)
        self.check_downloaded_data_button.resize(48, 25)
        self.check_downloaded_data_button.clicked.connect(self.on_click_check_download_data)

        # Download Data textfields view
        self.download_data_details_textbox = QPlainTextEdit(self)
        self.download_data_details_textbox.move(1050, 10)
        self.download_data_details_textbox.resize(290, 360)
        self.download_data_details_textbox.setEnabled(False)
        # self.download_data_details_textbox.setPlainText(self.data["pairs1"])
        # self.download_data_details_textbox.textChanged.connect(self.on_textchange_pairs1)

        # Label Pairs 1
        self.pairs1_label = QLabel(self)
        self.pairs1_label.setText('Pairs:')
        self.pairs1_label.move(520, 100)
        # Textbox Pairs 1
        self.pairs1_textbox = QPlainTextEdit(self)
        self.pairs1_textbox.move(555, 100)
        self.pairs1_textbox.resize(60, 246)
        self.pairs1_textbox.setPlainText(self.data["pairs1"])
        self.pairs1_textbox.textChanged.connect(self.on_textchange_pairs1)

        # Label Cache Pairs 2
        self.pairs2_label = QLabel(self)
        self.pairs2_label.setText('Cache:')
        self.pairs2_label.move(670, 100)
        # Textbox Cache Pairs 2
        self.pairs2_textbox = QPlainTextEdit(self)
        self.pairs2_textbox.move(710, 100)
        self.pairs2_textbox.resize(60, 246)
        self.pairs2_textbox.setPlainText(self.data["pairs2"])
        self.pairs2_textbox.textChanged.connect(self.on_textchange_pairs2)

        # Label All Pairs 3
        self.pairs3_label = QLabel(self)
        self.pairs3_label.setText('All:')
        self.pairs3_label.move(780, 100)
        # Textbox All Pairs 3
        self.pairs3_textbox = QPlainTextEdit(self)
        self.pairs3_textbox.move(800, 100)
        self.pairs3_textbox.resize(60, 246)
        self.pairs3_textbox.setPlainText(self.data["pairs3"])
        self.pairs3_textbox.textChanged.connect(self.on_textchange_pairs3)
        # Button ALL Pairs 3
        self.all_pairs_3_button = QPushButton('ALL', self)
        self.all_pairs_3_button.setToolTip('Set the current Pairlist to all the pairs')
        self.all_pairs_3_button.move(630, 280)
        self.all_pairs_3_button.resize(60, 30)
        self.all_pairs_3_button.clicked.connect(self.on_click_all_pairs)

        # Label PairSet 1
        self.pair_set_1_label = QLabel(self)
        self.pair_set_1_label.setText('Pair Set 1')
        self.pair_set_1_label.move(373, 185)
        # Textbox PairSet 1
        self.pair_set_1_textbox = QPlainTextEdit(self)
        self.pair_set_1_textbox.move(370, 200)
        self.pair_set_1_textbox.resize(60, 146)
        self.pair_set_1_textbox.setPlainText(self.data["pair_set1"])
        self.pair_set_1_textbox.textChanged.connect(self.on_textchange_pair_set_1)
        # Button PairSet 1
        self.pair_set_1_button = QPushButton('1', self)
        self.pair_set_1_button.setToolTip('Set the current Pairlist to the 1st Set')
        self.pair_set_1_button.move(630, 220)
        self.pair_set_1_button.resize(60, 30)
        self.pair_set_1_button.clicked.connect(self.on_click_pair_set_1)

        # Label PairSet 2
        self.pair_set_2_label = QLabel(self)
        self.pair_set_2_label.setText('Pair Set 2')
        self.pair_set_2_label.move(455, 185)
        # Textbox PairSet 2
        self.pair_set_2_textbox = QPlainTextEdit(self)
        self.pair_set_2_textbox.move(450, 200)
        self.pair_set_2_textbox.resize(60, 146)
        self.pair_set_2_textbox.setPlainText(self.data["pair_set2"])
        self.pair_set_2_textbox.textChanged.connect(self.on_textchange_pair_set_2)
        # Button PairSet 2
        self.pair_set_2_button = QPushButton('2', self)
        self.pair_set_2_button.setToolTip('Set the current Pairlist to the 2nd Set')
        self.pair_set_2_button.move(630, 250)
        self.pair_set_2_button.resize(60, 30)
        self.pair_set_2_button.clicked.connect(self.on_click_pair_set_2)

        self.addHyperopt()

        # Button backtest
        self.backtest_button = QPushButton('Backtest', self)
        self.backtest_button.setToolTip('Backtest Data')
        self.backtest_button.move(870, 324)
        self.backtest_button.clicked.connect(self.on_click_backtest)

        # Button Show Plot
        self.plot_button = QPushButton('Show Plot', self)
        self.plot_button.setToolTip('Create A plot for the selected pair')
        self.plot_button.move(965, 324)
        self.plot_button.clicked.connect(self.on_click_plot)

        # # Config  label
        # self.label_config = QLabel(self)
        # self.label_config.setText('Config:')
        # self.label_config.move(935, 72)
        # Config Default label
        self.label_config_default = QLabel(self)
        self.label_config_default.setText('Default Config:')
        self.label_config_default.move(275, 38)
        # Config Default checkbox
        self.checkbox_config_default = QCheckBox(self)
        self.checkbox_config_default.move(353, 38)
        self.checkbox_config_default.setChecked(self.data["config_default"])
        self.checkbox_config_default.stateChanged.connect(self.checkbox_config)
        # Config dropdown
        self.dropdown_config = QComboBox(self)
        self.dropdown_config.setGeometry(292, 54, 75, 20)
        self.dropdown_config.addItems(self.configs)
        self.dropdown_config.setCurrentIndex(self.data["config_selection"])
        self.dropdown_config.currentIndexChanged.connect(self.on_select_config)
        if (self.data["config_default"]):
            self.dropdown_config.hide()

        # Button load config pairs
        self.backtest_button = QPushButton('Config Pairs', self)
        self.backtest_button.move(400, 32)
        self.backtest_button.clicked.connect(self.load_config_pairs)
        self.backtest_button.setToolTip("Loads trading pairs from config (pair-whitelist) to the active pair window on the left. Checks if there are download data clashes (missing data)")

        # # Plot Pair label
        # self.label_plot_pair = QLabel(self)
        # self.label_plot_pair.setText('Plot Pair:')
        # self.label_plot_pair.move(705, 300)
        # Plot Pair dropdown
        self.dropdown_plot_pair = QComboBox(self)
        self.dropdown_plot_pair.setGeometry(966, 297, 73, 20)
        self.dropdown_plot_pair.setMaxVisibleItems(50)
        self.dropdown_plot_pair.addItems(self.data["pairs1"].split())
        self.dropdown_plot_pair.setCurrentIndex(self.data["plot_pair"])
        self.dropdown_plot_pair.currentIndexChanged.connect(self.on_select_plot_pair)

        # Pairs no label
        self.label_pairs_no = QLabel(self)
        self.label_pairs_no.setText(self.get_pairlist_length())
        self.label_pairs_no.move(635, 195)
        self.label_pairs_no.adjustSize()

        # Pairs Max label
        self.label_max_pairs = QLabel(self)
        self.label_max_pairs.move(625, 325)
        self.set_max_pairs_label(self.data["max_open_trades"])


        # Funds  label
        self.label_funds = QLabel(self)
        self.label_funds.move(979, 192)
        self.update_funds()

        # Balance Per Pair  label
        self.label_balance_per_pair = QLabel(self)
        self.label_balance_per_pair.move(958, 212)
        self.label_balance_per_pair.setText(f"Pair Balance: {balance_per_pair}")

        # Stake  label
        self.label_stake = QLabel(self)
        self.label_stake.move(979, 232)
        self.label_stake.setText(f"Stake: {stake_amount}")

        # Fee  label
        self.label_fee = QLabel(self)
        self.label_fee.move(979, 252)
        if(fee_enable):
            self.label_fee.setText(f"Fee: {fee_amount}")
        else:
            self.label_fee.setText(f"Fee: None")

        # Processing time  label
        self.label_processing_time = QLabel(self)
        self.label_processing_time.move(868, 305)
        self.label_processing_time.resize(90, 20)
        self.set_label_processing_time(self.data['previous_processing_time'])


        # Profit plot label
        self.display_profit_label = QLabel(self)
        self.display_profit_label.setText('Profit')
        self.display_profit_label.move(989, 275)
        # Profit plot Checkbox
        self.display_profit_checkbox = QCheckBox(self)
        self.display_profit_checkbox.move(1020, 275)
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
        # self.get_backtest_processing_power()
        # self.get_plot_processing_power()
        # self.get_hyperopt_processing_power()
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
                json.dump(self.data, file,indent=2)
        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_click_backtest(self):
        if (self.backtesting_clicked):
            processing_time = main(self.command_list)
            if enable_sound:
                winsound.PlaySound('Welcome.wav', winsound.SND_FILENAME)

            self.set_label_processing_time(processing_time)
            self.set_max_pairs_label(None)
            self.backtesting_clicked = False
            self.show_plot_clicked = False
            self.hyperopt_clicked = False
            self.download_clicked = False
        else:
            self.update_config_pairs()
            self.on_click_save_json()
            time_until = ""
            if (self.data["time"]["time_until_enabled"]):
                time_until = self.data["time"]["time_until"]

            if( fee_enable):
                command_list = ["backtesting", "--config", "user_data/" + self.data["config"],"--fee", str(fee_amount), "--timeframe", "15m","--cache","none",
                            "--strategy", self.strategies[self.data["strategy"]], "--export", "trades",
                            "--timerange=" + str(self.data["time"]["time_from"]-data_loading_time_ms) + "-" + str(time_until)]
            else:
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
            self.download_clicked = False
            self.reload_imports()

    @pyqtSlot()
    def on_click_plot(self):
        if (self.show_plot_clicked):
            processing_time = main(self.command_list)
            self.set_label_processing_time(processing_time)
            self.set_max_pairs_label(None)
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
            self.download_clicked = False
        else:
            self.update_config_pairs()
            self.on_click_save_json()
            # self.get_plot_processing_power()
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
                        "solo=" + str(self.solo_trends[self.data["indicators_extra"]["solo_trend"]]))
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

            if futures:
                command_list = [command, "--config", "user_data/" + self.data["config"], "--strategy",
                            self.strategies[self.data["strategy"]], "-p", pair + "/" + fiat_currency + ":" + fiat_currency,
                            "--timerange=" + str(self.data["time"]["time_from"]-data_loading_time_ms) + "-" + str(time_until)]
            else:
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
            self.download_clicked = False
            self.reload_imports()

    @pyqtSlot()
    def on_click_hyperopt(self):
        if (self.data["hyperopt"]["hyperopt"]):
            if (self.hyperopt_clicked):
                processing_time = main(self.command_list)

                self.set_label_processing_time(processing_time)
                self.set_max_pairs_label(None)
                if enable_sound:
                    winsound.PlaySound('Welcome.wav', winsound.SND_FILENAME)
                self.backtesting_clicked = False
                self.show_plot_clicked = False
                self.hyperopt_clicked = False
                self.download_clicked = False
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

                if( fee_enable):
                    command_list = ["hyperopt", "--config", "user_data/" + self.data["config"], "--timeframe", "15m",
                                "--strategy", self.strategies[self.data["strategy"]], "-e",
                                self.data["hyperopt"]["epochs"],"--fee", str(fee_amount),
                                "--timerange=" + str(self.data["time"]["time_from"]-data_loading_time_ms) + "-" + str(time_until),
                                "--hyperopt-loss", hyperopt_loss_functions[self.data["hyperopt"]["loss_function"]],
                                "--print-all"]
                else:
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
                self.download_clicked = False
                self.reload_imports()
        else:
            print("Hyperopt is disabled")

    @pyqtSlot()
    def on_click_download_data(self):
        if (self.download_clicked):
            self.update_config_pairs()
            self.on_click_save_json()

            pairs = self.data["pairs1"].split()
            datetime_now = datetime.datetime.now() - datetime.timedelta(hours=2)
            timestamp = int(datetime_to_unix(datetime_now, False))
            if (timestamp > self.data["download"]["absolute_latest_update"]):
                self.data["download"]["absolute_latest_update"] = timestamp
            days = self.data["download"]["days_to_download"]
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
            for timeframe in timeframes_needed_list:
                print(f"Downloading data for {timeframe}")
                processing_time = main(["download-data", "-t", timeframe, "--days", str(days)])
                print(f"Processing time for {timeframe} was {processing_time:0.1f}s")

            if enable_sound:
                winsound.PlaySound('Welcome.wav', winsound.SND_FILENAME)
            print("FINISHED DOWNLOADING DATA")

            self.backtesting_clicked = False
            self.show_plot_clicked = False
            self.hyperopt_clicked = False
            self.download_clicked = False
        else:
            self.backtesting_clicked = False
            self.show_plot_clicked = False
            self.hyperopt_clicked = False
            self.download_clicked = True
            days = int(self.data["download"]["days_to_download"])
            self.run_command_args_label.setText(f"Downloading {days} days for timeframes: {timeframes_needed_list}")
            self.reload_imports()

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
            self.combobox_indicator1.setEnabled(False)
        else:
            self.data["indicators1"]["enabled"] = True
            self.indicator1_textbox.setEnabled(True)
            self.combobox_indicator1.setEnabled(True)

    @pyqtSlot()
    def checkbox_indicators2(self):
        if (self.data["indicators2"]["enabled"] == True):
            self.data["indicators2"]["enabled"] = False
            self.indicator2_textbox.setEnabled(False)
            self.combobox_indicator2.setEnabled(False)
        else:
            self.data["indicators2"]["enabled"] = True
            self.indicator2_textbox.setEnabled(True)
            self.combobox_indicator2.setEnabled(True)

    @pyqtSlot()
    def checkbox_indicators3(self):
        if (self.data["indicators3"]["enabled"] == True):
            self.data["indicators3"]["enabled"] = False
            self.indicator3_textbox.setEnabled(False)
            self.combobox_indicator3.setEnabled(False)
        else:
            self.data["indicators3"]["enabled"] = True
            self.indicator3_textbox.setEnabled(True)
            self.combobox_indicator3.setEnabled(True)

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
        if (production_max_trades_enable):
            if (len(self.data["pairs1"].split()) < production_max_trades):
                self.data["max_open_trades"] = len(self.data["pairs1"].split())
            else:
                self.data["max_open_trades"] = production_max_trades
        else:
            self.data["max_open_trades"] = len(self.data["pairs1"].split())
        self.set_max_pairs_label(self.data["max_open_trades"])
        self.label_pairs_no.adjustSize()
        self.set_label_processing_time(0)
        self.update_download_data_labels()
        self.update_onclick_triggers()
        self.update_funds()

    @pyqtSlot()
    def on_textchange_pairs2(self):
        self.data["pairs2"] = self.pairs2_textbox.toPlainText().upper()

    @pyqtSlot()
    def on_textchange_pairs3(self):
        self.data["pairs3"] = self.pairs3_textbox.toPlainText().upper()

    @pyqtSlot()
    def on_textchange_pair_set_1(self):
        self.data["pair_set1"] = self.pair_set_1_textbox.toPlainText().upper()


    @pyqtSlot()
    def on_textchange_pair_set_2(self):
        self.data["pair_set2"] = self.pair_set_2_textbox.toPlainText().upper()


    @pyqtSlot()
    def on_click_all_pairs(self):
        if self.backtest_data_enabled == True:
            self.hide_download_data_details()
        self.data["pairs1"] = self.data["pairs3"]
        self.pairs1_textbox.setPlainText(self.data["pairs1"])
        self.dropdown_plot_pair.clear()
        self.dropdown_plot_pair.addItems(self.data["pairs1"].split())
        self.label_pairs_no.setText("Pairs: " + str(len(self.data["pairs1"].split())))
        if (production_max_trades_enable):
            if (len(self.data["pairs1"].split()) < production_max_trades):
                self.data["max_open_trades"] = len(self.data["pairs1"].split())
            else:
                self.data["max_open_trades"] = production_max_trades
        else:
            self.data["max_open_trades"] = len(self.data["pairs1"].split())
        self.set_max_pairs_label(self.data["max_open_trades"])
        self.label_pairs_no.adjustSize()
        self.set_label_processing_time(0)
        self.update_download_data_labels()
        self.update_onclick_triggers()
        self.update_funds()

    @pyqtSlot()
    def on_click_pair_set_1(self):
        if self.backtest_data_enabled == True:
            self.hide_download_data_details()
        self.data["pairs1"] = self.data["pair_set1"]
        self.pairs1_textbox.setPlainText(self.data["pairs1"])
        self.dropdown_plot_pair.clear()
        self.dropdown_plot_pair.addItems(self.data["pairs1"].split())
        self.label_pairs_no.setText("Pairs: " + str(len(self.data["pairs1"].split())))
        if (production_max_trades_enable):
            if (len(self.data["pairs1"].split()) < production_max_trades):
                self.data["max_open_trades"] = len(self.data["pairs1"].split())
            else:
                self.data["max_open_trades"] = production_max_trades
        else:
            self.data["max_open_trades"] = len(self.data["pairs1"].split())
        self.set_max_pairs_label(self.data["max_open_trades"])
        self.label_pairs_no.adjustSize()
        self.update_download_data_labels()
        self.update_onclick_triggers()
        self.update_funds()

    @pyqtSlot()
    def on_click_pair_set_2(self):
        if self.backtest_data_enabled == True:
            self.hide_download_data_details()
        self.data["pairs1"] = self.data["pair_set2"]
        self.pairs1_textbox.setPlainText(self.data["pairs1"])
        self.dropdown_plot_pair.clear()
        self.dropdown_plot_pair.addItems(self.data["pairs1"].split())
        self.label_pairs_no.setText("Pairs: " + str(len(self.data["pairs1"].split())))
        if (production_max_trades_enable):
            if (len(self.data["pairs1"].split()) < production_max_trades):
                self.data["max_open_trades"] = len(self.data["pairs1"].split())
            else:
                self.data["max_open_trades"] = production_max_trades
        else:
            self.data["max_open_trades"] = len(self.data["pairs1"].split())
        self.set_max_pairs_label(self.data["max_open_trades"])
        self.label_pairs_no.adjustSize()
        self.update_download_data_labels()
        self.update_onclick_triggers()
        self.update_funds()

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
            self.on_select_config(0)
        else:
            self.data["config"] = "config.json"
            self.data["config_default"] = True
            self.dropdown_config.hide()

    def on_select_strategy(self, i):
        self.data["strategy"] = i

    def on_select_indicator1_list(self, i):
        if self.ctrl_or_shift_pressed:
            self.data["indicator1_dropdown"] = i
            self.data["indicators1"]["text"] = self.data["indicators1"]["text"]+ " "+self.indicator1_list[i]
            self.indicator1_textbox.setText(self.data["indicators1"]["text"])
        else:
            self.data["indicator1_dropdown"] = i
            self.data["indicators1"]["text"] = self.indicator1_list[i]
            self.indicator1_textbox.setText(self.indicator1_list[i])

    def on_select_indicator2_list(self, i):
        if self.ctrl_or_shift_pressed:
            if(self.c_pressed):
                self.data["indicator2_dropdown"] = i
                self.data["indicators3"]["text"] = self.data["indicators3"]["text"]+" "+self.indicator2_list[i]
                self.indicator3_textbox.setText(self.data["indicators3"]["text"])
            else:
                self.data["indicator2_dropdown"] = i
                self.data["indicators2"]["text"] = self.data["indicators2"]["text"]+" "+self.indicator2_list[i]
                self.indicator2_textbox.setText(self.data["indicators2"]["text"])
        else:
            if(self.c_pressed):
                self.data["indicator2_dropdown"] = i
                self.data["indicators3"]["text"] = self.indicator2_list[i]
                self.indicator3_textbox.setText(self.indicator2_list[i])
            else:
                self.data["indicator2_dropdown"] = i
                self.data["indicators2"]["text"] = self.indicator2_list[i]
                self.indicator2_textbox.setText(self.indicator2_list[i])

    def on_select_indicator3_list(self, i):
        if self.ctrl_or_shift_pressed:
            if(self.x_pressed):
                self.data["indicator3_dropdown"] = i
                self.data["indicators2"]["text"] = self.data["indicators2"]["text"]+" "+self.indicator3_list[i]
                self.indicator2_textbox.setText(self.data["indicators2"]["text"])
            else:
                self.data["indicator3_dropdown"] = i
                self.data["indicators3"]["text"] = self.data["indicators3"]["text"]+" "+self.indicator3_list[i]
                self.indicator3_textbox.setText(self.data["indicators3"]["text"])
        else:
            if(self.x_pressed):
                self.data["indicator3_dropdown"] = i
                self.data["indicators2"]["text"] = self.indicator3_list[i]
                self.indicator2_textbox.setText(self.indicator3_list[i])
            else:
                self.data["indicator3_dropdown"] = i
                self.data["indicators3"]["text"] = self.indicator3_list[i]
                self.indicator3_textbox.setText(self.indicator3_list[i])


    def on_select_indicator1_rare_list(self, i):
        self.data["indicator1_rare_dropdown"] = i
        self.data["indicators1"]["text"] = self.data["indicators1"]["text"]+ " "+self.indicator1_rare_list[i]
        self.indicator1_textbox.setText(self.data["indicators1"]["text"])

    def on_select_indicator2_rare_list(self, i):
        if(self.c_pressed):
            self.data["indicator2_rare_dropdown"] = i
            self.data["indicators3"]["text"] = self.data["indicators3"]["text"]+" "+self.indicator2_rare_list[i]
            self.indicator3_textbox.setText(self.data["indicators3"]["text"])
        else:
            self.data["indicator2_rare_dropdown"] = i
            self.data["indicators2"]["text"] = self.data["indicators2"]["text"]+" "+self.indicator2_rare_list[i]
            self.indicator2_textbox.setText(self.data["indicators2"]["text"])


    def on_select_indicator3_rare_list(self, i):
        if(self.x_pressed):
            self.data["indicator3_rare_dropdown"] = i
            self.data["indicators2"]["text"] = self.data["indicators2"]["text"]+" "+self.indicator3_rare_list[i]
            self.indicator2_textbox.setText(self.data["indicators2"]["text"])
        else:
            self.data["indicator3_rare_dropdown"] = i
            self.data["indicators3"]["text"] = self.data["indicators3"]["text"]+" "+self.indicator3_rare_list[i]
            self.indicator3_textbox.setText(self.data["indicators3"]["text"])

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
        self.data["config"] = str(config) + ".json"

    def on_select_plot_pair(self, i):
        self.data["plot_pair"] = i

    def on_click_check_download_data(self):
        if self.backtest_data_enabled == False:
            self.check_downloaded_data_button.setText("Hide")
            self.backtest_data_enabled = True
            self.width = 1350
            self.setFixedWidth(1350)
            self.generate_download_data_table()
            self.show()
        else:
            self.hide_download_data_details()

    def hide_download_data_details(self):
        self.check_downloaded_data_button.setText("Check")
        self.backtest_data_enabled = False
        self.width = 1050
        self.setFixedWidth(1050)
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
            self.label_download_data_clashes.setText("Data Days Clash!")
        else:
            self.label_download_data_clashes.setText("Latest Date Clash!")

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
        self.label_download_days_latest.setText("("+str(self.data["download"]["latest_days"]) + " days)")

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
        self.label_download_data_latest.setText('Latest Data:           ' + unix_to_datetime(lowest, True, True))

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
            if futures:
                processed_pairs.append(pair + "/" + fiat_currency + ":" + fiat_currency)
            else:
                processed_pairs.append(pair + "/" + fiat_currency)
        config_json["exchange"]["pair_whitelist"] = processed_pairs

        if (production_max_trades_enable):
            if (len(self.data["pairs1"].split()) < production_max_trades):
                config_json["max_open_trades"] = len(self.data["pairs1"].split())
                self.data["max_open_trades"] = len(self.data["pairs1"].split())
            else:
                config_json["max_open_trades"] = production_max_trades
                self.data["max_open_trades"] = production_max_trades
        else:
            config_json["max_open_trades"] = len(self.data["pairs1"].split())
        self.set_max_pairs_label(self.data["max_open_trades"])
        config_json = self.update_config_funds(config_json)
        try:
            with open(config_url, 'w') as file:
                json.dump(config_json, file,indent=2)
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
            if futures:
                processed_pair = pair.replace("/" + fiat_currency + ":" + fiat_currency,"")
            else:
                processed_pair = pair.replace("/" + fiat_currency,"")
            processed_pair_text += (processed_pair + "\n")
        self.data["pairs1"] = processed_pair_text
        self.pairs1_textbox.setPlainText(self.data["pairs1"])
        self.label_pairs_no.setText("Pairs: " + str(len(config_json["exchange"]["pair_whitelist"])))
        self.label_pairs_no.adjustSize()
        self.set_label_processing_time(0)
        if self.backtest_data_enabled == True:
            self.hide_download_data_details()
        self.update_download_data_labels()
        self.update_onclick_triggers()
        self.update_funds()

    def get_pairlist_length(self):
        pairs = self.data["pairs1"].split()
        if (pairs):
            return "Pairs: " + str(len(pairs))
        else:
            return "0"

    def set_label_processing_time(self,time):
        self.data["previous_processing_time"]=time
        if(time >= 60):
            self.label_processing_time.setText(f"Process: {time/ 60:0.1f} min")
        else:
            self.label_processing_time.setText(f"Process: {time:0.1f} sec")

    def set_max_pairs_label(self,max_pairs):
        if max_pairs:
            if(production_max_trades_enable):
                if max_pairs <= production_max_trades:
                    self.label_max_pairs.setText(f"Max Trades: {max_pairs}")
                else:
                    self.label_max_pairs.setText(f"Max Trades: {production_max_trades}")
        else:
            pair_length = len(self.data["pairs1"].split())
            if(production_max_trades_enable):
                if pair_length <= production_max_trades:
                    self.label_max_pairs.setText(f"Max Trades: {len(self.data['pairs1'].split())}")
                else:
                    self.label_max_pairs.setText(f"Max Trades: {production_max_trades}")
            else:
                self.label_max_pairs.setText(f"Max Trades: {len(self.data['pairs1'].split())}")



    def update_funds(self):
        self.label_funds.setText(f"Funds: {self.data['max_open_trades'] * balance_per_pair}")

    # RESETS ALL IMPORTS BEFORE RUNNING ANY COMMANDS
    def reload_imports(self):
        modules_copy =    sys.modules.copy()
        for item  in modules_copy:
            if(item in MODULE_LIST):
                reload(sys.modules[item])
        return True


    def closeEvent(self, event):
        self.listener.stop()
        self.on_click_save_json()
        sys.exit(0)


    # Updates the balance and order size for the config


    def update_config_funds(self,config_json):
        config_json["dry_run_wallet"] = self.data["max_open_trades"] * balance_per_pair
        config_json["stake_amount"] = stake_amount
        return config_json

    def on_press(self, key):
        # print("button pressed")
        # print('{0} pressed'.format(key))
        if key == Key.ctrl_l or key == Key.ctrl_r:
            # print("ctrl-l pressed")
            self.ctrl_or_shift_pressed = True
        elif key == Key.shift:
            # print("shift pressed")
            self.ctrl_or_shift_pressed = True
        # elif hasattr(key, "char") and ( key.char == "z" or key.char == "Z"):
        #     # print("z pressed")
        #     self.z_pressed = True
        elif hasattr(key, "char") and ( key.char == "x" or key.char == "X"):
            # print("x pressed")
            self.x_pressed = True
        elif hasattr(key, "char") and ( key.char == "c" or key.char == "C"):
            # print("c pressed")
            self.c_pressed = True

    def on_release(self, key):
        # print("button released")
        # print('{0} released'.format(key))
        if key == Key.ctrl_l or key == Key.ctrl_r:
            # print("ctrl-l released")
            self.ctrl_or_shift_pressed = False
        elif key == Key.shift:
            # print("shift released")
            self.ctrl_or_shift_pressed = False
        # elif hasattr(key, "char") and ( key.char == "z" or key.char == "Z"):
        #     # print("z released")
        #     self.z_pressed = False
        elif hasattr(key, "char") and (key.char == "x" or key.char == "X"):
            # print("x released")
            self.x_pressed = False
        elif hasattr(key, "char") and (key.char == "c" or key.char == "C"):
            # print("c released")
            self.c_pressed = False

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
