# Project map

This is a small collection of FPVS statistics lessons. Each numbered Python script reads the same synthetic dataset and prints results. There is no application server, shared analysis pipeline, or required execution order.

## Lessons

| File | Statistical question |
| --- | --- |
| `01_one_sample_ttest.py` | Is the adult Positive Valence mean BCA above zero? |
| `02_paired_ttest.py` | Do adult Positive Valence and Negative Valence responses differ within participants? |
| `03_independent_ttests_and_holm.py` | Do adults and adolescents differ overall or within conditions? Four Welch tests use Holm correction. |
| `04_mann_whitney_u.py` | How does a rank-based adult/adolescent comparison work for Neutral Angry? |
| `05_repeated_measures_anova.py` | Do adult responses differ across the three conditions? Uses Greenhouse-Geisser correction. |
| `06_mixed_anova.py` | Do group, condition, and their interaction explain differences? Reports Greenhouse-Geisser adjustments for the repeated effects. |

The ANOVA lecture notes discuss adding LOT and ROT. The executable examples still use a single occipital ROI.

## Data and dependencies

`synthetic_occipital_roi.csv` is the long-format analysis input: one BCA value per participant and condition, with participant, group, condition, ROI, and amplitude columns. There are 50 participants, 25 per group, each measured in three conditions. The 150 rows are repeated observations, not 150 independent participants.

`synthetic_occipital_roi_wide.csv` is a viewing copy. Editing it does not affect the lessons. `extras/make_synthetic_data.py` is an optional generator that overwrites both CSV files. EEG preprocessing and harmonic aggregation happen upstream and are not implemented here.

`requirements.txt` lists the Python dependencies and pins Pingouin. Use a local virtual environment; it is excluded from Git.

## Documentation and verification

- `README.txt`: student setup and lesson overview.
- `SOURCES.md`: FPVS references, DOI links, and method descriptions.
- `EXAMPLE_OUTPUT.txt`: saved console output; rerun a lesson for its current results.
- `AGENTS.md`: editing and verification conventions.

Run a lesson with `python 01_one_sample_ttest.py`, substituting the other filenames as needed. Each lesson only reads the supplied CSV and prints its results. Verify affected calculations by running the corresponding scripts; verify all six before publishing a full project update.
