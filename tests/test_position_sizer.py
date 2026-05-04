from src.position_sizer import kelly_fraction, size_position


def test_kelly_negative_when_win_rate_low_and_ratio_low():
    assert kelly_fraction(0.3, 1.0) < 0


def test_kelly_positive_when_win_rate_high():
    k = kelly_fraction(0.6, 2.0)
    assert k > 0


def test_size_position_invalid_bracket():
    r = size_position(equity=100_000, entry=100.0, stop=100.0, recent_trades=[])
    assert r.qty == 0
    assert r.reason == "invalid_bracket"


def test_size_position_caps_at_max_position_pct():
    # Cold-start defaults: W=0.5, R=1.5 -> Kelly = 0.5 - 0.5/1.5 ≈ 0.166
    # Quarter Kelly ≈ 0.0417 -> ~ $4170 on $100k equity
    r = size_position(equity=100_000, entry=100.0, stop=98.0, recent_trades=[])
    assert r.qty >= 1
    assert r.notional <= 100_000 * 0.10 + 1e-6


def test_size_position_caps_by_risk_budget():
    # Tight stop: $1 risk per share. 1% of $10k = $100 budget -> max 100 shares.
    # Quarter-Kelly notional ~ $416 -> 4 shares is the binding cap.
    r = size_position(equity=10_000, entry=100.0, stop=99.0, recent_trades=[])
    assert r.qty >= 1
    # whichever is smaller of qty_by_risk and qty_by_kelly applies
    assert r.qty <= 100


def test_size_position_zero_when_negative_kelly():
    losers = [{"pnl_r": -1.0} for _ in range(20)] + [{"pnl_r": 0.5} for _ in range(2)]
    r = size_position(equity=100_000, entry=100.0, stop=98.0, recent_trades=losers)
    assert r.qty == 0
    assert r.reason == "non_positive_kelly"
