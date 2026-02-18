"""Simple stock-picking agent for the Chinese A-share market.

This script ranks candidate stocks with a transparent, rule-based scoring model.
It is for educational purposes only (not financial advice).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class StockSnapshot:
    ticker: str
    name: str
    pe_ttm: float
    roe_pct: float
    revenue_growth_pct: float
    momentum_6m_pct: float
    max_drawdown_1y_pct: float
    avg_turnover_mn_cny: float


@dataclass(frozen=True)
class ScoredStock:
    stock: StockSnapshot
    score: float
    rationale: str


class ChinaStockSelectionAgent:
    """Ranks Chinese stocks by a weighted multi-factor score."""

    def __init__(
        self,
        pe_floor: float = 5.0,
        pe_ceiling: float = 40.0,
    ) -> None:
        self.pe_floor = pe_floor
        self.pe_ceiling = pe_ceiling

    def _score_valuation(self, pe_ttm: float) -> float:
        if pe_ttm <= 0:
            return 0.0
        clipped = min(max(pe_ttm, self.pe_floor), self.pe_ceiling)
        # Lower PE gets higher score.
        return (self.pe_ceiling - clipped) / (self.pe_ceiling - self.pe_floor) * 100

    @staticmethod
    def _clamp_pct(value: float, low: float, high: float) -> float:
        return max(low, min(value, high))

    def score(self, stock: StockSnapshot) -> ScoredStock:
        valuation = self._score_valuation(stock.pe_ttm)
        quality = self._clamp_pct(stock.roe_pct, 0, 30) / 30 * 100
        growth = self._clamp_pct(stock.revenue_growth_pct, -10, 40)
        growth = (growth + 10) / 50 * 100
        momentum = self._clamp_pct(stock.momentum_6m_pct, -20, 50)
        momentum = (momentum + 20) / 70 * 100
        risk = self._clamp_pct(stock.max_drawdown_1y_pct, -70, -5)
        # Smaller drawdown (closer to -5) is better.
        risk = (risk + 70) / 65 * 100
        liquidity = self._clamp_pct(stock.avg_turnover_mn_cny, 50, 500)
        liquidity = (liquidity - 50) / 450 * 100

        # Weighted blend tuned for balance of quality + growth + safety.
        total_score = (
            0.20 * valuation
            + 0.25 * quality
            + 0.25 * growth
            + 0.10 * momentum
            + 0.15 * risk
            + 0.05 * liquidity
        )

        rationale = (
            f"valuation={valuation:.1f}, quality={quality:.1f}, growth={growth:.1f}, "
            f"momentum={momentum:.1f}, risk={risk:.1f}, liquidity={liquidity:.1f}"
        )
        return ScoredStock(stock=stock, score=total_score, rationale=rationale)

    def rank(self, stocks: Iterable[StockSnapshot]) -> List[ScoredStock]:
        scored = [self.score(stock) for stock in stocks]
        return sorted(scored, key=lambda x: x.score, reverse=True)


def default_candidate_universe() -> Sequence[StockSnapshot]:
    """Example candidate universe.

    Replace these with current data from your provider before investing.
    """

    return [
        StockSnapshot("600519", "Kweichow Moutai", 29.8, 31.0, 17.0, 8.0, -18.0, 420.0),
        StockSnapshot("300750", "CATL", 24.2, 19.0, 22.0, 15.0, -24.0, 480.0),
        StockSnapshot("601318", "Ping An Insurance", 8.7, 12.0, 6.0, 10.0, -20.0, 260.0),
        StockSnapshot("600036", "China Merchants Bank", 6.1, 15.0, 8.0, 6.0, -17.0, 300.0),
        StockSnapshot("002594", "BYD", 27.5, 18.0, 28.0, 24.0, -26.0, 510.0),
    ]


def choose_best_stock(stocks: Iterable[StockSnapshot]) -> ScoredStock:
    agent = ChinaStockSelectionAgent()
    ranked = agent.rank(stocks)
    if not ranked:
        raise ValueError("No stocks provided.")
    return ranked[0]


def main() -> None:
    ranked = ChinaStockSelectionAgent().rank(default_candidate_universe())
    best = ranked[0]

    print("Top pick in current candidate set:")
    print(f"{best.stock.ticker} {best.stock.name} | score={best.score:.2f}")
    print(f"Rationale: {best.rationale}")
    print("\nFull ranking:")
    for idx, item in enumerate(ranked, start=1):
        print(f"{idx}. {item.stock.ticker} {item.stock.name} | {item.score:.2f}")


if __name__ == "__main__":
    main()
