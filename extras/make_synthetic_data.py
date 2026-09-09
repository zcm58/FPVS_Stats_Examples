"""OPTIONAL: recreate the teaching CSV files. These are NOT real EEG data.

The CSVs are already supplied; you do not need to run this script first.
Running it writes new CSVs over the supplied examples in the parent folder.
"""
from pathlib import Path

import numpy as np
import pandas as pd

# A fixed seed makes the random-number sequence reproducible.
rng = np.random.default_rng(20260909)
folder = Path(__file__).resolve().parents[1]
conditions = ["Positive Valence", "Negative Valence", "Neutral Angry"]

# These are chosen population means, in microvolts, NOT published estimates.
# The two fictional populations differ most in Neutral Angry.
# The realized sample means will not equal these population means exactly.
population_means = {
    "Group_A": [0.12, 0.22, 0.36],
    "Group_B": [0.12, 0.18, 0.22],
}
rows = []
for group, means in population_means.items():
    for person in range(1, 26):
        participant = f"{group[-1]}{person:02d}"
        # A participant-specific offset is shared across their conditions.
        # This makes repeated observations from one person correlated.
        person_offset = rng.normal(loc=0.0, scale=0.10)
        for condition, mean in zip(conditions, means):
            residual = rng.normal(loc=0.0, scale=0.06)
            value = mean + person_offset + residual
            rows.append([participant, group, condition, "Occipital", value])

# Values are already final ROI BCA outcomes: no electrode, harmonic, or
# baseline processing belongs in the analysis examples. Do not clip negatives.
# The normal model has the same covariance in both groups and is spherical
# in the population. A finite sample still has sampling variability.
data = pd.DataFrame(rows, columns=["participant", "group", "condition", "roi", "bca_uv"])
data.to_csv(folder / "synthetic_occipital_roi.csv", index=False, float_format="%.6f")

# Read the rounded file before creating the wide view so both files agree.
data = pd.read_csv(folder / "synthetic_occipital_roi.csv")
wide = data.pivot(index=["participant", "group", "roi"], columns="condition", values="bca_uv")
wide = wide.reset_index()
wide.to_csv(folder / "synthetic_occipital_roi_wide.csv", index=False, float_format="%.6f")
print("Created synthetic_occipital_roi.csv: 150 rows, 50 people, 3 conditions.")
print("Created synthetic_occipital_roi_wide.csv: one row per person.")
