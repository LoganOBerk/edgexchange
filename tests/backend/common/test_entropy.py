import pytest

from common import entropy
from argparse import ArgumentTypeError


def test_set_volatile_percent_inrange(monkeypatch):
    monkeypatch.setattr(entropy, "_volatile_percent", 0)

    entropy.set_volatile_percent(20)
    assert entropy._volatile_percent == 20


def test_set_volatile_percent_lower_edge_valid(monkeypatch):
    monkeypatch.setattr(entropy, "_volatile_percent", 0)

    entropy.set_volatile_percent(1)
    assert entropy._volatile_percent == 1


def test_set_volatile_percent_upper_edge_valid(monkeypatch):
    monkeypatch.setattr(entropy, "_volatile_percent", 0)

    entropy.set_volatile_percent(100)
    assert entropy._volatile_percent == 100


def test_set_volatile_percent_zero_rejected(monkeypatch):
    monkeypatch.setattr(entropy, "_volatile_percent", 0)

    with pytest.raises(ArgumentTypeError):
        entropy.set_volatile_percent(0)


def test_set_volatile_percent_101_rejected(monkeypatch):
    monkeypatch.setattr(entropy, "_volatile_percent", 0)

    with pytest.raises(ArgumentTypeError):
        entropy.set_volatile_percent(101)


def test_set_volatile_percent_negative_rejected(monkeypatch):
    monkeypatch.setattr(entropy, "_volatile_percent", 0)

    with pytest.raises(ArgumentTypeError):
        entropy.set_volatile_percent(-1)


def test_set_volatile_percent_non_numeric_rejected(monkeypatch):
    monkeypatch.setattr(entropy, "_volatile_percent", 0)

    with pytest.raises(ArgumentTypeError):
        entropy.set_volatile_percent("abc")

    assert entropy._volatile_percent == 0


def test_set_volatile_percent_does_not_mutate_on_failure(monkeypatch):
    monkeypatch.setattr(entropy, "_volatile_percent", 50)

    with pytest.raises(ArgumentTypeError):
        entropy.set_volatile_percent(101)

    assert entropy._volatile_percent == 50


def test_inject_volatility_bounds(monkeypatch):
    monkeypatch.setattr(entropy, "_volatile_percent", 20)
    price = 1000
    expected_range = 200

    for _ in range(10000):
        assert -expected_range <= entropy.inject_volatility(price) <= expected_range


def test_inject_volatility_zero_percent_is_zero(monkeypatch):
    monkeypatch.setattr(entropy, "_volatile_percent", 0)
    price = 1000

    for _ in range(100):
        assert entropy.inject_volatility(price) == 0