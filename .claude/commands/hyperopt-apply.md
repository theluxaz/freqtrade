# Hyperopt Apply

Convert a parameterized strategy back to hardcoded values using optimized hyperopt results.

## Arguments
$STRATEGY_NAME - The strategy class name to apply results to (e.g., x_BUY_LOW1)

## Steps

1. **Read the guide**: Read `.claude/HYPEROPT_GUIDE.md` for conversion patterns.

2. **Check for hyperopt results**:
```bash
python -m user_data.llm_optimizer.hyperopt_helper -s $STRATEGY_NAME --action results
```

3. **Read the current strategy file** (should have Parameter declarations from prepare step).

4. **For each Parameter** in the code:
   - Find the optimized value from the results JSON
   - If no result exists, use the Parameter's `default` value
   - Replace `self.<param>.value` with the literal optimized value
   - Remove the Parameter class declaration line

5. **Clean up**:
   - Remove Parameter imports if no Parameters remain (keep IStrategy import!)
   - Remove `buy_params = {...}` dict if it was part of the parameterization

6. **Verify** the file compiles:
```bash
python -c "import py_compile; py_compile.compile('path/to/strategy.py', doraise=True)"
```

7. **Run a backtest** to verify the strategy works with new values:
```bash
python -m freqtrade backtesting --config user_data/config.json --fee 0.0025 --timeframe 15m --cache none --strategy $STRATEGY_NAME --export trades
```

8. **Report** what values were applied and the backtest results.
