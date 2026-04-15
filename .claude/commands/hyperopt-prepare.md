# Hyperopt Prepare

Convert the selected strategy from hardcoded values to hyperoptable Parameter declarations.

## Arguments
$STRATEGY_NAME - The strategy class name to prepare (e.g., x_BUY_LOW1)
$INSTRUCTIONS - Optional instructions (e.g., "only rule 11 thresholds", "only guards 1-5")

## Steps

1. **Read the guide**: Read `.claude/HYPEROPT_GUIDE.md` for conversion patterns.

2. **Discover files**:
```bash
python -m user_data.llm_optimizer.hyperopt_helper -s $STRATEGY_NAME --action discover
```

3. **Read the strategy file** and any related CUSTOM NFI files found above.

4. **Identify hardcoded values** to convert based on $INSTRUCTIONS:
   - Guard thresholds: `df["rsi"] > 16.0`, `df["ppo5"] < -0.25`
   - Trigger function args: `shift_before=3`, `depth=-1.2`
   - Enable/disable flags for conditions

5. **Add Parameter import** to the strategy file:
```python
from freqtrade.strategy import IntParameter, DecimalParameter, CategoricalParameter
```

6. **Add Parameter declarations** as class attributes with sensible ranges.

7. **Replace hardcoded values** with `self.<param>.value`.

8. **Verify** the file compiles:
```bash
python -c "import py_compile; py_compile.compile('path/to/strategy.py', doraise=True)"
```

9. **Report** what was changed and what parameters were added.

The user can now run Hyperopt via the GUI button.
