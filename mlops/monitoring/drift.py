import numpy as np


class DataDriftDetector:
    @staticmethod
    def psi(
        expected,
        actual,
        bins: int = 10,
    ) -> float:
        expected = np.asarray(expected)
        actual = np.asarray(actual)

        edges = np.histogram_bin_edges(
            expected,
            bins=bins,
        )

        expected_counts, _ = np.histogram(
            expected,
            bins=edges,
        )

        actual_counts, _ = np.histogram(
            actual,
            bins=edges,
        )

        expected_pct = (
            expected_counts + 1e-6
        ) / len(expected)

        actual_pct = (
            actual_counts + 1e-6
        ) / len(actual)

        psi = np.sum(
            (actual_pct - expected_pct)
            * np.log(actual_pct / expected_pct)
        )

        return float(psi)

    @staticmethod
    def status(psi: float) -> str:
        if psi < 0.1:
            return "stable"

        if psi < 0.2:
            return "warning"

        return "drift"
