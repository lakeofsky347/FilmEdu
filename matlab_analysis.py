# matlab_analysis.py
"""
MATLAB-style numerical analysis utilities.

Provides NumPy-backed equivalents of commonly used MATLAB functions,
covering statistics, signal processing, and linear algebra operations.
These helpers are general-purpose but are particularly useful for
analyzing student scores, audio waveforms, and other numerical datasets.
"""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np
import numpy.typing as npt

# ---------------------------------------------------------------------------
# Type alias
# ---------------------------------------------------------------------------
Array = npt.NDArray[np.float64]


# ---------------------------------------------------------------------------
# Array creation (MATLAB-style)
# ---------------------------------------------------------------------------

def linspace(start: float, stop: float, num: int = 100) -> Array:
    """Return *num* evenly spaced values over [*start*, *stop*].

    Equivalent to MATLAB's ``linspace(start, stop, num)``.

    Parameters
    ----------
    start:
        Starting value of the sequence.
    stop:
        End value of the sequence (inclusive).
    num:
        Number of points to generate (must be >= 1).

    Returns
    -------
    Array
        1-D array of *num* equally spaced values.
    """
    if num < 1:
        raise ValueError("num must be at least 1")
    return np.linspace(start, stop, num)


def zeros(rows: int, cols: int = 1) -> Array:
    """Return a zero matrix of shape (*rows*, *cols*).

    Equivalent to MATLAB's ``zeros(rows, cols)``.
    """
    return np.zeros((rows, cols), dtype=np.float64)


def ones(rows: int, cols: int = 1) -> Array:
    """Return a ones matrix of shape (*rows*, *cols*).

    Equivalent to MATLAB's ``ones(rows, cols)``.
    """
    return np.ones((rows, cols), dtype=np.float64)


# ---------------------------------------------------------------------------
# Descriptive statistics
# ---------------------------------------------------------------------------

def mean(data: Sequence[float] | Array) -> float:
    """Return the arithmetic mean of *data*.

    Equivalent to MATLAB's ``mean(A)``.
    """
    arr = np.asarray(data, dtype=np.float64)
    return float(np.mean(arr))


def std(data: Sequence[float] | Array, ddof: int = 1) -> float:
    """Return the standard deviation of *data*.

    Parameters
    ----------
    data:
        Input values.
    ddof:
        Delta degrees of freedom.  Use ``ddof=1`` (default) for the sample
        standard deviation — matching MATLAB's ``std(A)`` — or ``ddof=0``
        for the population standard deviation.
    """
    arr = np.asarray(data, dtype=np.float64)
    return float(np.std(arr, ddof=ddof))


def var(data: Sequence[float] | Array, ddof: int = 1) -> float:
    """Return the variance of *data*.

    Equivalent to MATLAB's ``var(A)`` (sample variance, ``ddof=1``).
    """
    arr = np.asarray(data, dtype=np.float64)
    return float(np.var(arr, ddof=ddof))


def median(data: Sequence[float] | Array) -> float:
    """Return the median of *data*.

    Equivalent to MATLAB's ``median(A)``.
    """
    arr = np.asarray(data, dtype=np.float64)
    return float(np.median(arr))


def corrcoef(x: Sequence[float] | Array,
             y: Sequence[float] | Array) -> Array:
    """Return the 2×2 Pearson correlation-coefficient matrix for *x* and *y*.

    Equivalent to MATLAB's ``corrcoef(x, y)``.

    Returns
    -------
    Array
        ``[[1, r], [r, 1]]`` where *r* is the Pearson correlation.
    """
    xarr = np.asarray(x, dtype=np.float64)
    yarr = np.asarray(y, dtype=np.float64)
    return np.corrcoef(xarr, yarr)


# ---------------------------------------------------------------------------
# Polynomial fitting
# ---------------------------------------------------------------------------

def polyfit(x: Sequence[float] | Array,
            y: Sequence[float] | Array,
            deg: int) -> Array:
    """Fit a polynomial of degree *deg* to (*x*, *y*) data.

    Equivalent to MATLAB's ``polyfit(x, y, n)``.

    Returns
    -------
    Array
        Polynomial coefficients, highest power first.
    """
    xarr = np.asarray(x, dtype=np.float64)
    yarr = np.asarray(y, dtype=np.float64)
    return np.polyfit(xarr, yarr, deg)


def polyval(coeffs: Sequence[float] | Array,
            x: Sequence[float] | float | Array) -> Array:
    """Evaluate polynomial with coefficients *coeffs* at values *x*.

    Equivalent to MATLAB's ``polyval(p, x)``.

    Parameters
    ----------
    coeffs:
        Polynomial coefficients, highest power first (as returned by
        :func:`polyfit`).
    x:
        Value(s) at which to evaluate the polynomial.
    """
    return np.polyval(np.asarray(coeffs, dtype=np.float64), x)


# ---------------------------------------------------------------------------
# Signal processing
# ---------------------------------------------------------------------------

def fft(signal: Sequence[float] | Array) -> Array:
    """Compute the one-dimensional Discrete Fourier Transform.

    Equivalent to MATLAB's ``fft(x)``.

    Returns
    -------
    Array
        Complex-valued spectrum of *signal*.
    """
    return np.fft.fft(np.asarray(signal, dtype=np.float64))


def fft_magnitude(signal: Sequence[float] | Array) -> Array:
    """Return the magnitude (absolute value) of the FFT spectrum.

    Useful for quick frequency-content inspection of an audio track or
    any time-series signal without needing to handle complex numbers.
    """
    return np.abs(fft(signal))


def fft_frequencies(n: int, sample_rate: float = 1.0) -> Array:
    """Return the FFT sample frequencies for a signal of length *n*.

    Equivalent to MATLAB's ``(0:n-1) * (sample_rate / n)`` (single-sided).

    Parameters
    ----------
    n:
        Number of samples.
    sample_rate:
        Sampling rate in Hz (default 1.0 → normalised frequencies).
    """
    if n <= 0:
        raise ValueError("n must be positive")
    return np.fft.fftfreq(n, d=1.0 / sample_rate)


# ---------------------------------------------------------------------------
# Linear algebra helpers
# ---------------------------------------------------------------------------

def norm(data: Sequence[float] | Array, order: int | None = None) -> float:
    """Return the vector (or matrix) norm of *data*.

    Equivalent to MATLAB's ``norm(A)`` / ``norm(A, p)``.
    """
    arr = np.asarray(data, dtype=np.float64)
    return float(np.linalg.norm(arr, ord=order))


def dot(a: Sequence[float] | Array,
        b: Sequence[float] | Array) -> float | Array:
    """Compute the dot product of *a* and *b*.

    Equivalent to MATLAB's ``dot(a, b)`` for 1-D inputs.
    """
    return np.dot(np.asarray(a, dtype=np.float64),
                  np.asarray(b, dtype=np.float64))


# ---------------------------------------------------------------------------
# Histogram utility
# ---------------------------------------------------------------------------

def histogram(data: Sequence[float] | Array,
              bins: int = 10) -> tuple[Array, Array]:
    """Compute the histogram of *data*.

    Equivalent to MATLAB's ``[n, edges] = histcounts(data, bins)``.

    Returns
    -------
    counts : Array
        Bin counts.
    bin_edges : Array
        Bin edge values (length = ``bins + 1``).
    """
    arr = np.asarray(data, dtype=np.float64)
    counts, bin_edges = np.histogram(arr, bins=bins)
    return counts.astype(np.float64), bin_edges
