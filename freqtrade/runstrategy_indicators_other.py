


# #change spot to futures in config and change to use orderbook= true
# #add GUI
futures = False

computer_processing_power = 1.3  # 0.00001 to.. 2.0
config_file = "run-configuration.json"
other_configs_json = ["config-production"]
fiat_currency = "USDT"

#GET OTHER INDICATORS FROM PREVIOUS LAPTOP
#GET OTHER INDICATORS FROM PREVIOUS LAPTOP
#GET OTHER INDICATORS FROM PREVIOUS LAPTOP
#GET OTHER INDICATORS FROM PREVIOUS LAPTOP
#GET OTHER INDICATORS FROM PREVIOUS LAPTOP

timeframes_needed_list=["15m","1h","1d"]

indicators1_default = ['sma50', 'sma200', 'sma400', 'sma10k']

indicators1_solo_trends = [{"5": "Upper Danger"},
                           # {"4":"Huge Fall Turnaround"},
                           {"3": "Long Uptrend"},
                           # {"2": "Downtrend Upswing"},
                           # {"1":"Small Upswing"},
                           {"0": "Normal"},
                           {"-1": "Slow Downtrend"},
                           {"-2": "Long Downtrend"},
                           {"-3": "Bottom Danger"},
                           ]

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
indicators2_list  = [   {"---FAVORITES---":""},
                        {"PPO mix":"ppo5 ppo10 ppo25 ppo50 ppo100 ppo200 ppo500"},#ppos
                        {"ROC candlesize mix":"candlesize roc roc2 "},
                        {"RSI":"rsi rsi5"},
                        {"MUL":"mul mul_conv"},

                        {"---RATE OF CHANGE---":""},
                        {"Short ROC":"roc roc2 roc10"},
                        {"Mid ROC":"roc25 roc50 roc50avg roc50smaavg"},

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
                        {"ROC candlesize mix":"candlesize roc roc2 "},
                        {"Volatility":"vol50 vol100 vol175 vol250"},
                        {"Convergence":"convsmall convmedium"},
                        {"ROC sma":"roc200sma roc400sma roc10ksma roc30ksma"},
                        {"MUL":"mul mul_conv"},
                        # {"BULL/BEAR":"BULL"},
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