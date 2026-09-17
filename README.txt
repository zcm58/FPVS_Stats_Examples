FPVS: SIMPLE PYTHON STATISTICS EXAMPLES
======================================
So I set up some synthetic fake data for the sake of example to
illustrate the different statistical methods use for data analaysis in FPVS.

Assume all this data has been processed/cleaned through the FPVS Toolbox.
Examples 01-04 use one occipital ROI. Examples 05-06 use synthetic LOT and ROT
responses. All values represent baseline-corrected amplitude (BCA).


START HERE
----------
Extract the zip file in the location of your choice. Use PyCharm (or your preferred IDE)
to open the project and set up a virtual environment.

Install the required packages in your virtual environment:
    python -m pip install -r requirements.txt

Then run the first file. Each file outputs hypothetical results.

    python 01_one_sample_ttest.py

Run the other examples by substituting their filenames. There is no required
execution order: each numbered script reads its supplied CSV independently. The
scripts print their results; they do not change the supplied data. Opening a
script in PyCharm or VS Code also lets you read/edit its explanatory comments.
Use Python 3.10 or later. On Windows, use "py" instead of "python" when that is
the command configured for your Python installation.

For examples 1-4 only, a smaller installation is sufficient:
    python -m pip install pandas scipy statsmodels

All six examples have been run successfully with the supplied data. The ANOVA
calculations are also checked against independent calculations. Run those checks with:
    python -m unittest discover -s tests -v

THE EXPERIMENT REPRESENTED BY THE DATA
------------------------------------
There are two independent groups: Group_A and Group_B, with 25 participants
in each group. For these examples, EVERY participant completes all three
conditions: Positive Valence, Negative Valence, and Neutral Angry. Thus the conditions are
repeated measurements of the same people, while group membership is between
people. A01 and B01 are different people; their numbers do not imply pairing.

For Examples 01-04, each participant-condition cell contains ONE final occipital ROI BCA value in
microvolts. It has already been baseline corrected and averaged over the ROI
electrodes. Any upstream harmonic aggregation is already complete and defined
consistently. No FFT, spectral baseline subtraction, harmonic summing, electrode
averaging, or trial averaging is performed in these analysis examples.

In the original occipital data, there are 150 rows, but only 50 participants. For a comparison between the
groups within any one condition, the sample sizes are 25 versus 25, not 75
versus 75. A single-group condition comparison uses 25 paired participants.

The original occipital simulation uses chosen population means plus a person-specific offset and
condition-specific random noise. The shared offset makes one person's three
values correlated. The population error model is normal, with equal covariance
across groups and sphericity. Sample statistics vary around the generating
parameters. The amplitudes are invented for teaching, not empirical estimates
of a typical FPVS response. Negative values have NOT been clipped or deleted.

DATA FILES
----------
synthetic_occipital_roi.csv is the analysis input, in LONG format:
    participant: unique person ID (A01-A25 or B01-B25)
    group: Group_A or Group_B
    condition: Positive Valence, Negative Valence, or Neutral Angry
    roi: Occipital for every observation
    bca_uv: final baseline-corrected ROI response, in microvolts

synthetic_occipital_roi_wide.csv is an equivalent viewing copy, in WIDE format:
    one participant per row, with one BCA column for each condition.

Only the LONG occipital file is read by Examples 01-04. Editing the wide viewing copy
will not change their inputs. Neither file contains raw electrode-level data.
The optional extras/make_synthetic_data.py recreates BOTH CSVs using the fixed
seed 20260909. It overwrites those example CSVs when run.

synthetic_multi_roi.csv is a separate simulation for Examples 05-06:
    participant: unique person ID (A01-A25 or B01-B25)
    group: Group_A (adults) or Group_B (adolescents)
    condition: Positive Valence, Negative Valence, or Neutral Angry
    roi: LOT (left occipito-temporal) or ROT (right occipito-temporal)
    bca_uv: final baseline-corrected ROI response, in microvolts

Each person has all six condition-ROI combinations. That gives us 300 rows,
but still only 50 participants. Example 05 selects the 25 adults (150 rows).
Example 06 uses both groups (300 rows). The optional extras/make_multi_roi_data.py
recreates just this file with seed 20260917; it leaves the occipital files alone.
These amplitudes are separately simulated, not derived from the occipital data.
The simulation includes shared person, ROI, and condition offsets plus cell noise.
We chose the adult LOT/ROT gap to vary more by condition to illustrate an interaction.

THE SIX LESSONS
---------------
01_one_sample_ttest.py
    One group and one condition versus zero. Explains the null hypothesis,
    t-value, p-value, mean, SD, and a one-sided 95% lower confidence bound.
    The example tests the prespecified positive-only alternative.

02_paired_ttest.py
    Negative Valence versus Positive Valence in Group_A. Matches measurements by person
    ID, then tests the within-person differences. Explains why the observations
    are paired and why the difference-score distribution matters.

03_independent_ttests_and_holm.py
    Compares Group_A and Group_B overall and within each of the three conditions.
    The overall comparison FIRST averages the three conditions within each
    participant. Welch's independent t-test is used; changing equal_var=False
    to equal_var=True selects Student's independent t-test. Holm correction is
    applied to all four planned comparisons together.

04_mann_whitney_u.py
    Demonstrates a rank-based between-group comparison in Neutral Angry. Explains
    what U measures, how it differs from a t-test, and why this is not simply
    a test of medians without additional assumptions. This is an alternative
    lesson, not a second chance to claim the same contrast is significant.

05_repeated_measures_anova.py
    A 3-condition x 2-ROI repeated-measures ANOVA within Group_A. Tests Condition,
    ROI, and Condition x ROI. Explains F, participant pairing, partial eta-squared,
    and Greenhouse-Geisser correction. Prints LOT/ROT means. Requires Pingouin.

06_mixed_anova.py
    A 2-group x 3-condition x 2-ROI mixed ANOVA. Tests all three main effects,
    all three two-way interactions, and Group x Condition x ROI. Uses ROI averages
    and ROT-minus-LOT differences to calculate the balanced two-ROI design in Python.
    Effects involving condition use GG epsilon estimated from within-group errors,
    separately for each view. Requires Pingouin and Statsmodels.

HOW TO USE THE OUTPUT
--------------------
The comments in the Python files are the main tutorial. They explain the
statistical question before the test call and the output immediately afterward.
EXAMPLE_OUTPUT.txt contains the actual console output from all six examples.
SOURCES.md lists FPVS papers and explains which methods match these lessons.

The mean or mean difference in microvolts describes the size and direction of
an amplitude effect. The t/F/U statistic and its p-value answer a model-based
testing question, not whether that effect is practically important. The 95%
intervals in examples 1-3 are ordinary unadjusted intervals, not simultaneous
intervals for a family of tests. Example 3's adjusted p-values need not make
the same reject/do-not-reject decision as those unadjusted intervals.

These lessons are separate demonstrations, NOT a recommendation to run all
of them as independent confirmatory tests on one real dataset. Prespecify the
outcome, hypotheses, alternative test, contrast direction, and multiplicity
families. A significant result in one group but not another is not itself a
group difference; similarly, different condition-specific p-values do not
establish an interaction. Avoid selecting a test because its p-value is lower.

Example 3 deliberately puts the overall comparison and three specific
comparisons in ONE Holm family. Examples 1, 2, and 4 each illustrate one planned
contrast. The ANOVA scripts show sphericity correction, not adjustment across
all omnibus hypotheses. A real study may need a broader correction plan than
any one standalone lesson. Greenhouse-Geisser and Holm address different issues.

The lessons assume the supplied complete, balanced teaching design.
Replacing the CSV with real data requires reviewing its structure, missing
measurements, unusual observations, model assumptions, and the analysis plan.
Example 06's calculation is specific to two ROIs and equal-sized groups; adding
more ROIs requires a model that supports the expanded repeated-measures design.
A final ROI value alone is not sufficient to reconstruct a spectral Z-score;
these examples therefore do not attempt spectral response detection.
