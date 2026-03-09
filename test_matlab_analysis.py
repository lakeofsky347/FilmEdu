# test_matlab_analysis.py
"""Unit tests for matlab_analysis.py"""

import math
import unittest

import numpy as np

from matlab_analysis import (
    corrcoef,
    dot,
    fft,
    fft_frequencies,
    fft_magnitude,
    histogram,
    linspace,
    mean,
    median,
    norm,
    ones,
    polyfit,
    polyval,
    std,
    var,
    zeros,
)


class TestArrayCreation(unittest.TestCase):
    def test_linspace_default_num(self):
        arr = linspace(0, 1)
        self.assertEqual(arr.shape, (100,))
        self.assertAlmostEqual(arr[0], 0.0)
        self.assertAlmostEqual(arr[-1], 1.0)

    def test_linspace_custom_num(self):
        arr = linspace(0, 10, 11)
        self.assertEqual(len(arr), 11)
        np.testing.assert_allclose(arr, np.arange(11, dtype=float))

    def test_linspace_single_point(self):
        arr = linspace(5, 5, 1)
        self.assertEqual(arr[0], 5.0)

    def test_linspace_raises_on_zero_num(self):
        with self.assertRaises(ValueError):
            linspace(0, 1, 0)

    def test_zeros_shape(self):
        m = zeros(3, 4)
        self.assertEqual(m.shape, (3, 4))
        self.assertTrue(np.all(m == 0))

    def test_zeros_default_cols(self):
        m = zeros(5)
        self.assertEqual(m.shape, (5, 1))

    def test_ones_shape(self):
        m = ones(2, 3)
        self.assertEqual(m.shape, (2, 3))
        self.assertTrue(np.all(m == 1))


class TestDescriptiveStatistics(unittest.TestCase):
    _scores = [70.0, 80.0, 90.0, 85.0, 75.0]

    def test_mean(self):
        self.assertAlmostEqual(mean(self._scores), 80.0)

    def test_mean_numpy_array(self):
        self.assertAlmostEqual(mean(np.array(self._scores)), 80.0)

    def test_std_sample(self):
        result = std(self._scores, ddof=1)
        expected = float(np.std(self._scores, ddof=1))
        self.assertAlmostEqual(result, expected)

    def test_std_population(self):
        result = std(self._scores, ddof=0)
        expected = float(np.std(self._scores, ddof=0))
        self.assertAlmostEqual(result, expected)

    def test_var(self):
        result = var(self._scores)
        expected = float(np.var(self._scores, ddof=1))
        self.assertAlmostEqual(result, expected)

    def test_median_odd(self):
        self.assertAlmostEqual(median([1, 3, 2]), 2.0)

    def test_median_even(self):
        self.assertAlmostEqual(median([1, 2, 3, 4]), 2.5)

    def test_corrcoef_perfect_positive(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        r_matrix = corrcoef(x, y)
        self.assertAlmostEqual(r_matrix[0, 1], 1.0, places=10)

    def test_corrcoef_perfect_negative(self):
        x = [1, 2, 3]
        y = [3, 2, 1]
        r_matrix = corrcoef(x, y)
        self.assertAlmostEqual(r_matrix[0, 1], -1.0, places=10)

    def test_corrcoef_shape(self):
        self.assertEqual(corrcoef([1, 2], [3, 4]).shape, (2, 2))


class TestPolynomialFitting(unittest.TestCase):
    def test_polyfit_linear(self):
        x = [0, 1, 2, 3]
        y = [1, 3, 5, 7]  # y = 2x + 1
        coeffs = polyfit(x, y, 1)
        self.assertAlmostEqual(coeffs[0], 2.0, places=5)
        self.assertAlmostEqual(coeffs[1], 1.0, places=5)

    def test_polyval_scalar(self):
        coeffs = [2.0, 1.0]  # 2x + 1
        self.assertAlmostEqual(float(polyval(coeffs, 3)), 7.0)

    def test_polyval_array(self):
        coeffs = [1.0, 0.0, 0.0]  # x^2
        x = [0, 1, 2, 3]
        result = polyval(coeffs, x)
        np.testing.assert_allclose(result, [0, 1, 4, 9])

    def test_polyfit_polyval_roundtrip(self):
        x = linspace(0, 2 * math.pi, 50)
        y = np.sin(x)
        coeffs = polyfit(x, y, 7)
        y_hat = polyval(coeffs, x)
        # High-degree polynomial should fit sin closely over training points
        self.assertLess(float(np.max(np.abs(y - y_hat))), 0.01)


class TestSignalProcessing(unittest.TestCase):
    def test_fft_dc_component(self):
        # Constant signal → all energy at DC (index 0)
        signal = [1.0] * 8
        spectrum = fft(signal)
        self.assertAlmostEqual(abs(spectrum[0]), 8.0)
        for k in range(1, 8):
            self.assertAlmostEqual(abs(spectrum[k]), 0.0, places=10)

    def test_fft_magnitude_real_signal(self):
        signal = [1.0, -1.0] * 4  # Nyquist frequency square wave
        mag = fft_magnitude(signal)
        self.assertTrue(np.all(mag >= 0))

    def test_fft_frequencies_length(self):
        freqs = fft_frequencies(8, sample_rate=8.0)
        self.assertEqual(len(freqs), 8)

    def test_fft_frequencies_raises_on_nonpositive(self):
        with self.assertRaises(ValueError):
            fft_frequencies(0)

    def test_fft_length_preserved(self):
        signal = linspace(0, 1, 32)
        self.assertEqual(len(fft(signal)), 32)


class TestLinearAlgebra(unittest.TestCase):
    def test_norm_vector(self):
        self.assertAlmostEqual(norm([3.0, 4.0]), 5.0)

    def test_norm_order_1(self):
        self.assertAlmostEqual(norm([1.0, -2.0, 3.0], order=1), 6.0)

    def test_dot_product(self):
        self.assertAlmostEqual(float(dot([1, 2, 3], [4, 5, 6])), 32.0)

    def test_dot_orthogonal(self):
        self.assertAlmostEqual(float(dot([1, 0], [0, 1])), 0.0)


class TestHistogram(unittest.TestCase):
    def test_histogram_counts_sum(self):
        data = list(range(20))
        counts, edges = histogram(data, bins=4)
        self.assertEqual(int(counts.sum()), 20)

    def test_histogram_bin_edges_length(self):
        _, edges = histogram([1, 2, 3, 4], bins=4)
        self.assertEqual(len(edges), 5)

    def test_histogram_all_same_bin(self):
        counts, _ = histogram([5, 5, 5, 5], bins=1)
        self.assertEqual(int(counts[0]), 4)


if __name__ == "__main__":
    unittest.main()
