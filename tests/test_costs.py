import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.costs import CostModel, after_tax_expectancy, net_r
from src.markets import get_profile


def test_roundtrip_fraction_bps_and_tds():
    cm = CostModel(entry_fee_bps=10, exit_fee_bps=10, slippage_bps=20, tds_pct=0.01)
    # (10+10+40)/10000 = 0.006 + 0.01 tds = 0.016
    assert cm.roundtrip_fraction() == pytest.approx(0.016)


def test_net_r_reduces_gross():
    cm = CostModel(slippage_bps=50)  # 0.01 round trip
    # entry 100, stop 95 -> risk 5; cost_in_price = 0.01*100 = 1.0 -> 0.2 R drag
    nr = net_r(2.0, 100.0, 95.0, cm)
    assert nr == pytest.approx(1.8)


def test_net_r_zero_cost_is_identity():
    cm = CostModel(slippage_bps=0)
    assert net_r(1.5, 100, 95, cm) == pytest.approx(1.5)


def test_after_tax_no_tax_is_mean():
    cm = CostModel(tax_pct=0.0)
    assert after_tax_expectancy([1.0, -1.0, 2.0], cm) == pytest.approx(2.0 / 3)


def test_after_tax_no_loss_offset_taxes_only_wins():
    cm = CostModel(tax_pct=0.30, no_loss_offset=True)
    # wins taxed 30%, losses untouched: [2*0.7, -1, 1*0.7] = [1.4,-1,0.7] -> mean 0.3667
    assert after_tax_expectancy([2.0, -1.0, 1.0], cm) == pytest.approx((1.4 - 1.0 + 0.7) / 3)


def test_crypto_high_tds_can_flip_sign():
    cm = CostModel.from_dict(get_profile("crypto").costs.__dict__)
    # a small +0.3R gross edge on a tight 0.5% stop gets eaten by 1.6% round trip
    nr = net_r(0.3, 100.0, 99.5, cm)  # risk 0.5, cost 1.6 -> huge drag
    assert nr < 0


def test_market_profiles_load():
    for m in ("us", "india", "crypto", "forex"):
        p = get_profile(m)
        assert len(p.watchlist) >= 1
        assert p.costs.roundtrip_fraction() >= 0
        assert callable(p.yf_symbol)


def test_yf_symbol_mapping():
    assert get_profile("india").yf_symbol("RELIANCE") == "RELIANCE.NS"
    assert get_profile("crypto").yf_symbol("BTC") == "BTC-USD"
    assert get_profile("forex").yf_symbol("USDINR") == "USDINR=X"
    assert get_profile("us").yf_symbol("AAPL") == "AAPL"


def test_unknown_market_raises():
    with pytest.raises(ValueError):
        get_profile("commodities")
