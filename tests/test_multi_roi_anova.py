"""Check the teaching ANOVAs against independent calculations from the raw cells.

Run: python -m unittest discover -s tests -v
"""
import contextlib
import io
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
from scipy import stats
from scipy.linalg import helmert
from statsmodels.stats.anova import AnovaRM

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = ["Positive Valence", "Negative Valence", "Neutral Angry"]
ROIS = ["LOT", "ROT"]


def run_lesson(filename, data):
    with patch("pandas.read_csv", return_value=data.copy()), contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(str(ROOT / filename))["result"]


def contrast_reference(data):
    """Balanced factorial ANOVA via orthonormal contrasts, without Pingouin.

    Project each person's six cells onto the grand-mean, condition, ROI, and
    interaction spaces. Each space has its own participant-within-group error.
    This verifies the full design directly, not the lesson's two mixed-ANOVA calls.
    """
    cells = data.pivot(index=["participant", "group"], columns=["condition", "roi"], values="bca_uv")
    cells = cells.reindex(columns=pd.MultiIndex.from_product([CONDITIONS, ROIS]))
    y = cells.to_numpy()
    labels = cells.index.get_level_values("group").to_numpy()
    groups = np.unique(labels)
    n, g = len(y), len(groups)
    condition = helmert(3).T
    roi = np.array([[-1.0], [1.0]]) / np.sqrt(2)
    spaces = {
        "Grand": np.ones((6, 1)) / np.sqrt(6),
        "Condition": np.kron(condition, np.ones((2, 1)) / np.sqrt(2)),
        "ROI": np.kron(np.ones((3, 1)) / np.sqrt(3), roi),
        "Condition x ROI": np.kron(condition, roi),
    }
    records = []
    for name, basis in spaces.items():
        scores = y @ basis
        q = basis.shape[1]
        grand = scores.mean(axis=0)
        errors = scores.copy()
        between_ss = 0.0
        for group in groups:
            mask = labels == group
            mean = scores[mask].mean(axis=0)
            errors[mask] -= mean
            between_ss += mask.sum() * np.sum((mean - grand) ** 2)
        error_ss = np.sum(errors ** 2)
        covariance = errors.T @ errors / (n - g)
        epsilon = min(1.0, np.trace(covariance) ** 2 / (q * np.trace(covariance @ covariance)))
        effects = []
        if name != "Grand":
            effects.append((name, n * np.sum(grand ** 2), q))
        if g > 1:
            effects.append(("Group" if name == "Grand" else "Group x " + name, between_ss, (g - 1) * q))
        for effect, ss, df1 in effects:
            df2 = (n - g) * q
            f_value = (ss / df1) / (error_ss / df2)
            records.append({
                "Source": effect, "F": f_value, "epsilon": epsilon,
                "df1_for_report": df1 * epsilon, "df2_for_report": df2 * epsilon,
                "p_for_report": stats.f.sf(f_value, df1 * epsilon, df2 * epsilon),
                "np2": ss / (ss + error_ss),
            })
    return pd.DataFrame(records).set_index("Source")


class MultiROIAnovaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pd.read_csv(ROOT / "synthetic_multi_roi.csv")

    def test_complete_balanced_participant_condition_roi_cells(self):
        data = self.data
        self.assertEqual(len(data), 300)
        self.assertEqual(data["participant"].nunique(), 50)
        self.assertEqual(set(data["condition"]), set(CONDITIONS))
        self.assertEqual(set(data["roi"]), set(ROIS))
        self.assertFalse(data.duplicated(["participant", "condition", "roi"]).any())
        self.assertTrue(data.groupby("participant").size().eq(6).all())
        self.assertTrue(data.groupby("participant")["group"].nunique().eq(1).all())
        self.assertTrue(data.groupby("group")["participant"].nunique().eq(25).all())
        self.assertTrue(np.isfinite(data["bca_uv"]).all())

    def test_example_05_matches_statsmodels_and_contrast_covariance(self):
        data = self.data[self.data["group"] == "Group_A"]
        actual = run_lesson("05_repeated_measures_anova.py", self.data).set_index("Source")
        reference = AnovaRM(data, "bca_uv", "participant", within=["condition", "roi"]).fit().anova_table
        contrasts = contrast_reference(data)
        for name, other, effect in [("condition", "condition", "Condition"), ("roi", "roi", "ROI"), ("condition * roi", "condition:roi", "Condition x ROI")]:
            np.testing.assert_allclose(actual.loc[name, ["F", "ddof1", "ddof2"]].to_numpy(dtype=float),
                                       reference.loc[other, ["F Value", "Num DF", "Den DF"]].to_numpy(dtype=float), rtol=1e-10)
            np.testing.assert_allclose(actual.loc[name, ["eps", "p_GG_corr", "np2"]].to_numpy(dtype=float),
                                       contrasts.loc[effect, ["epsilon", "p_for_report", "np2"]].to_numpy(dtype=float), rtol=1e-9)

    def test_example_06_all_seven_effects_match_independent_projection(self):
        actual = run_lesson("06_mixed_anova.py", self.data).set_index("Source")
        reference = contrast_reference(self.data).loc[actual.index, actual.columns]
        self.assertEqual(len(actual), 7)
        np.testing.assert_allclose(actual.to_numpy(dtype=float), reference.to_numpy(dtype=float), rtol=1e-9, atol=1e-13)

    def test_row_order_and_roi_direction_do_not_change_omnibus_tests(self):
        actual = run_lesson("06_mixed_anova.py", self.data).set_index("Source")
        changed = self.data.sample(frac=1, random_state=42).copy()
        changed["roi"] = changed["roi"].map({"LOT": "ROT", "ROT": "LOT"})
        reordered = run_lesson("06_mixed_anova.py", changed).set_index("Source")
        np.testing.assert_allclose(actual.to_numpy(dtype=float), reordered.to_numpy(dtype=float), rtol=1e-9, atol=1e-13)


if __name__ == "__main__":
    unittest.main()
