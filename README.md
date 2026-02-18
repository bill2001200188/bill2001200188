# China Stock Selection Agent

A lightweight Python agent that ranks candidate Chinese A-share stocks using a transparent multi-factor scoring model.

## What it does

- Scores each stock on valuation, quality, growth, momentum, risk, and liquidity.
- Produces a ranked list and highlights the top pick.
- Keeps the logic explicit and easy to tune.

> Educational use only — not financial advice.

## Run

```bash
python china_stock_agent.py
```

## Test

```bash
python -m pytest -q
```

## Customize

Edit `default_candidate_universe()` in `china_stock_agent.py` with your latest market data from your preferred data provider.
