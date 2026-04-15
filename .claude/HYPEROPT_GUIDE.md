# Hyperopt Preparation Guide

Reference for converting freqtrade strategies between hardcoded and hyperoptable forms.

## Strategy Architecture

Strategies are in `freqtrade/user_data/strategies/`. Each rule (e.g., `x_BUY_LOW1`) is a standalone `IStrategy` class with:
- **Triggers**: `buy_trigger1_function(self, df)` — main entry condition
- **Guards**: `buy_guard1_function(self, df)` through `buy_guard9_function` — additional filters
- **Prevents**: `buy_prevent1_function(self, df)` through `buy_prevent29_function` — conditions that block entry
- **Trend guard**: `buy_trend_guard(self, df)` — market regime filter

Enable/disable flags in `COMMON/COMMON_FUNCTIONS.py::default_buy_rule_settings()` control which guards/prevents are active.

## NFI Strategies (rules 10, 11, 21+)

NFI rules call `BUYER_NFI(self, df, "TREND", "TYPE")` which routes to functions in `RULES/CUSTOM/{TYPE}_NFI/{TYPE}_NFI_{TREND}.py`. These functions contain numbered sub-rules (1-26+) with hardcoded thresholds. NFI functions do NOT receive `self`, so Parameters must be handled differently.

## Converting Hardcoded to Hyperoptable

### Step 1: Add Import
```python
from freqtrade.strategy import IntParameter, DecimalParameter, CategoricalParameter
```

### Step 2: Declare Parameters at Class Level
```python
class x_BUY_LOW1(IStrategy):
    # Hyperopt parameters
    buy_guard2_rsi = IntParameter(0, 50, default=16, space='buy', optimize=True, load=True)
    buy_guard3_ppo5 = DecimalParameter(-3.0, 0.0, default=-0.25, decimals=2, space='buy', optimize=True, load=True)
```

### Step 3: Replace Hardcoded Values
```python
# BEFORE:
def buy_guard2_function(self, df):
    return df["rsi"] > 16.0

# AFTER:
def buy_guard2_function(self, df):
    return df["rsi"] > self.buy_guard2_rsi.value
```

### Common Ranges
| Indicator | Type | Range | Default behavior |
|-----------|------|-------|-----------------|
| RSI | IntParameter | 0-70 | Oversold < 30 |
| PPO | DecimalParameter(decimals=1) | -10.0 to 10.0 | Negative = bearish |
| Fisher RSI | IntParameter | -100 to 0 | Lower = more oversold |
| Candle size | DecimalParameter(decimals=2) | 0.0-3.0 | Smaller = less volatile |
| Convergence | DecimalParameter(decimals=2) | 0.0-3.0 | Higher = more stable |
| up_turna depth | DecimalParameter(decimals=1) | -5.0 to 0.0 | Threshold for turn |
| up_turna shifts | IntParameter | 1-15 | Lookback periods |
| EMA offset | DecimalParameter(decimals=3) | 0.001-0.1 | % difference |

## Converting Back After Hyperopt

### Step 1: Read Results
Hyperopt saves to `<StrategyName>.json` next to the .py file. Use:
```bash
python -m user_data.llm_optimizer.hyperopt_helper -s STRATEGY_NAME --action results
```

### Step 2: Replace .value with Literals
```python
# BEFORE (parameterized):
def buy_guard2_function(self, df):
    return df["rsi"] > self.buy_guard2_rsi.value

# AFTER (hardcoded with optimized value):
def buy_guard2_function(self, df):
    return df["rsi"] > 22.0
```

### Step 3: Clean Up
- Remove all Parameter class declarations
- Remove the Parameter import line (keep IStrategy import)
- Delete the `.json` results file if you don't want freqtrade to load it

## NFI Sub-Rules (Special Case)

For NFI strategies, the thresholds are in separate function files that don't have `self`. Two approaches:

**Approach A (recommended for few rules):** Copy the NFI conditions into the strategy's `populate_entry_trend` method so they can use `self.<param>.value`.

**Approach B (for many rules):** Add function parameters and pass values from the strategy:
```python
# In NFI file:
def UPTREND_NFI_LONG_DOWNTREND(df, buys, indexes, type, trend, params=None):
    if 1 in indexes:
        rsi_threshold = params.get("rule1_rsi", 37) if params else 37
        rule_signal = nfi_c(df, type, trend) & (df["rsi"] < rsi_threshold)
```
