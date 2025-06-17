from __future__ import annotations

"""General utility functions for Ferum Customs."""

from typing import Iterable


def sum_values(values: Iterable[float | int]) -> float:
    """Return the sum of numeric values."""
    return float(sum(values))
