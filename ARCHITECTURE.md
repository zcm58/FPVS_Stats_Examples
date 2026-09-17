# Project map

This is a small collection of FPVS statistics lessons. Each numbered Python script reads a supplied synthetic dataset and prints results. There is no application server, shared analysis pipeline, or required execution order.

## Lessons

| File | Statistical question |
| --- | --- |
| `01_one_sample_ttest.py` | Is the adult Positive Valence mean BCA above zero? |
| `02_paired_ttest.py` | Do adult Positive Valence and Negative Valence responses differ within participants? |
| `03_independent_ttests_and_holm.py` | Do adults and adolescents differ overall or within conditions? Four Welch tests use Holm correction. |
| `04_mann_whitney_u.py` | How does a rank-based adult/adolescent comparison work for Neutral Angry? |
| `05_repeated_measures_anova.py` | Tests Condition, ROI, and Condition x ROI in adults. Both factors are repeated; uses Greenhouse-Geisser correction. |
| `06_mixed_anova.py` | Tests all seven effects of Group x Condition x ROI, with Greenhouse-Geisser adjustments for effects involving condition. |

Examples 05-06 execute analyses of LOT and ROT. Example 06 uses ROI averages and ROT-minus-LOT differences to decompose the balanced two-ROI design, plus a group-adjusted intercept test for the ROI main effect. It is an ANOVA, not a linear mixed-effects model.

## Data and dependencies

`synthetic_occipital_roi.csv` is the long-format input for Examples 01-04: one BCA value per participant and condition, with participant, group, condition, ROI, and amplitude columns. There are 50 participants, 25 per group, each measured in three conditions. The 150 rows are repeated observations, not 150 independent participants.

`synthetic_occipital_roi_wide.csv` is a viewing copy. Editing it does not affect the lessons. `extras/make_synthetic_data.py` is an optional generator that overwrites both CSV files. EEG preprocessing and harmonic aggregation happen upstream and are not implemented here.

`synthetic_multi_roi.csv` is the separate long-format input for Examples 05-06. It uses the same columns and teaching labels, with six cells per participant: three conditions at LOT and ROT. Its 300 rows represent 50 participants. The amplitudes are a separate simulation, not derived from the occipital file. `extras/make_multi_roi_data.py` recreates only this file with seed 20260917.

`requirements.txt` lists the Python dependencies and pins Pingouin. Use a local virtual environment; it is excluded from Git.

## Documentation and verification

- `README.txt`: student setup and lesson overview.
- `SOURCES.md`: FPVS references, DOI links, and method descriptions.
- `EXAMPLE_OUTPUT.txt`: saved console output; rerun a lesson for its current results.
- `AGENTS.md`: editing and verification conventions.
- `tests/test_multi_roi_anova.py`: checks data structure, compares Example 05 with Statsmodels, and checks all seven Example 06 effects using independent orthonormal contrasts from the six raw cells per person. It checks F, degrees of freedom, GG epsilon, p-values, effect sizes, and invariance to row order and ROI label reversal.

Run a lesson with `python 01_one_sample_ttest.py`, substituting the other filenames as needed. Each lesson only reads its supplied CSV and prints results. Run the numerical checks with `python -m unittest discover -s tests -v`. Verify affected calculations by running the corresponding scripts; verify all six before publishing a full project update.
