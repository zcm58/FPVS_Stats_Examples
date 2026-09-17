"""Recreate the LOT/ROT teaching data for Examples 05 and 06.

These are invented BCA values, not real EEG data. Running this file overwrites
synthetic_multi_roi.csv. It leaves the original occipital CSV files alone.
"""
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(20260917)
conditions = ["Positive Valence", "Negative Valence", "Neutral Angry"]
rois = ["LOT", "ROT"]

# Each row holds the LOT and ROT population means for one condition, in uV.
# We made the adult ROT-minus-LOT gap change more across conditions so we can
# teach the Group x Condition x ROI interaction. These aren't empirical estimates.
population_means = {
    "Group_A": [[0.12, 0.15], [0.22, 0.32], [0.36, 0.50]],
    "Group_B": [[0.12, 0.15], [0.18, 0.20], [0.22, 0.25]],
}

rows = []
for group, means in population_means.items():
    for person in range(1, 26):
        participant = f"{group[-1]}{person:02d}"
        # Measurements from one person belong together. A person-wide offset
        # affects all six values, and an ROI offset affects that person's three
        # values at that ROI. Neither creates an extra independent participant.
        person_offset = rng.normal(0.0, 0.08)
        roi_offsets = rng.normal(0.0, 0.025, size=2)
        for condition, roi_means in zip(conditions, means):
            condition_offset = rng.normal(0.0, 0.04)
            for roi, mean, roi_offset in zip(rois, roi_means, roi_offsets):
                value = mean + person_offset + roi_offset + condition_offset + rng.normal(0.0, 0.06)
                rows.append([participant, group, condition, roi, value])

# This complete, balanced simulation uses the same error model in both groups.
# Its population covariance satisfies sphericity for the repeated effects.
# Sample estimates still vary. We keep negative values rather than clipping them.
data = pd.DataFrame(rows, columns=["participant", "group", "condition", "roi", "bca_uv"])
data.to_csv(Path(__file__).resolve().parents[1] / "synthetic_multi_roi.csv", index=False, float_format="%.6f")
print("Created synthetic_multi_roi.csv: 300 rows, 50 people, 3 conditions, 2 ROIs.")
