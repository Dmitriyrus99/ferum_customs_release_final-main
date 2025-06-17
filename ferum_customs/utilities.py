"""General utility functions for Ferum Customs."""

from __future__ import annotations

from typing import Iterable


def sum_values(values: Iterable[float | int]) -> float:
    """Return the sum of numeric values."""
    return float(sum(values))
