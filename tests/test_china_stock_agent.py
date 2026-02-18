from china_stock_agent import (
    ChinaStockSelectionAgent,
    StockSnapshot,
    choose_best_stock,
    default_candidate_universe,
)


def test_default_universe_returns_deterministic_top_pick() -> None:
    top = choose_best_stock(default_candidate_universe())
    assert top.stock.ticker == "600519"


def test_ranking_prefers_higher_quality_growth_with_reasonable_valuation() -> None:
    agent = ChinaStockSelectionAgent()
    low_quality = StockSnapshot("000001", "Low Quality", 10.0, 4.0, 0.0, 5.0, -35.0, 100.0)
    high_quality = StockSnapshot("000002", "High Quality", 18.0, 24.0, 25.0, 10.0, -15.0, 150.0)

    ranked = agent.rank([low_quality, high_quality])
    assert ranked[0].stock.ticker == "000002"
