FPVS: SIMPLE PYTHON STATISTICS EXAMPLES
======================================
So I set up some synthetic fake data for the sake of example to
illustrate the different statistical methods use for data analaysis in FPVS.

Assume all this data comes from the occipital lobe ROI and has been
processed/cleaned through the FPVS Toolbox. All values represent baseline-corrected amplitude (BCA).


START HERE
----------
Extract the zip file in the location of your choice. Use PyCharm (or your preferred IDE)
to open the project and set up a virtual environment.

Install the required packages in your virtual environment:
    python -m pip install -r requirements.txt

Then run the first file. Each file outputs hypothetical results.

    python 01_one_sample_ttest.py

Run the other examples by substituting their filenames. There is no required
execution order: each numbered script reads the same CSV independently. The
scripts print their results; they do not change the supplied data. Opening a
script in PyCharm or VS Code also lets you read/edit its explanatory comments.
Use Python 3.10 or later. On Windows, use "py" instead of "python" when that is
the command configured for your Python installation.

For examples 1-4 only, a smaller installation is sufficient:
    python -m pip install pandas scipy statsmodels

Execution note: Examples 1-4 were run successfully during preparation. Examples
5-6 passed syntax checks and API review, but were NOT executed with Pingouin:
that dependency could not be installed in the preparation environment because
network/DNS access was unavailable. Do not interpret their inclusion as a
claim of a successful end-to-end Pingouin run. See VALIDATION.txt.

THE EXPERIMENT REPRESENTED BY THE DATA
------------------------------------
There are two independent groups: Group_A and Group_B, with 25 participants
in each group. For these examples, EVERY participant completes all three
conditions: Positive Valence, Negative Valence, and Neutral Angry. Thus the conditions are
repeated measurements of the same people, while group membership is between
people. A01 and B01 are different people; their numbers do not imply pairing.

Each participant-condition cell contains ONE final occipital ROI BCA value in
microvolts. It has already been baseline corrected and averaged over the ROI
electrodes. Any upstream harmonic aggregation is already complete and defined
consistently. No FFT, spectral baseline subtraction, harmonic summing, electrode
averaging, or trial averaging is performed in these analysis examples.

There are 150 rows, but only 50 participants. For a comparison between the
groups within any one condition, the sample sizes are 25 versus 25, not 75
versus 75. A single-group condition comparison uses 25 paired participants.

The simulation uses chosen population means plus a person-specific offset and
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

Only the LONG file is read by the six examples. Editing the wide viewing copy
will not change their inputs. Neither file contains raw electrode-level data.
The optional extras/make_synthetic_data.py recreates BOTH CSVs using the fixed
seed 20260909. It overwrites those example CSVs when run.

THE SIX LESSONS
---------------
01_one_sample_ttest.py
    One group and one condition versus zero. Explains the null hypothesis,
    t-value, p-value, mean, SD, and a 95% confidence interval. The example is
    two-sided; comments explain a prespecified positive-only alternative.

02_paired_ttest.py
    Negative Valence versus Positive Valence in Group_A. Matches measurements by person
    ID, then tests the within-person differences. Explains why the observations
    are paired and why the difference-score distribution matters.

03_independent_ttests_and_holm.py
    Compares Group_A and Group_B overall and within each of the three conditions.
    The overall comparison FIRST averages the three conditions within each
    participant. Welch's independent t-test is used; changing equal_var=False
    to equal_var=True selects Student's independent t-test. Holm correction is
    applied to all four planned comparisons together. Comments also give the
    Bonferroni and BH-FDR method names and explain their different goals.

04_mann_whitney_u.py
    Demonstrates a rank-based between-group comparison in Neutral Angry. Explains
    what U measures, how it differs from a t-test, and why this is not simply
    a test of medians without additional assumptions. This is an alternative
    lesson, not a second chance to claim the same contrast is significant.

05_repeated_measures_anova.py
    An overall comparison of all three conditions within Group_A. Explains
    the F statistic, within-person design, partial eta-squared, sphericity,
    and Greenhouse-Geisser correction. Requires Pingouin.

06_mixed_anova.py
    Uses both groups and all three conditions. Separates the group effect,
    condition effect, and Group x Condition interaction. Explicitly calculates
    Greenhouse-Geisser-adjusted p-values for both repeated-measures effects
    using epsilon estimated from within-group errors. Requires Pingouin.

HOW TO USE THE OUTPUT
--------------------
The comments in the Python files are the main tutorial. They explain the
statistical question before the test call and the output immediately afterward.
EXAMPLE_OUTPUT.txt contains the actual console output from executed examples
1-4. It does not fabricate output for the two unexecuted Pingouin scripts.
SOURCES.md lists the official statistical/software references used.

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

The input checks intentionally expect the supplied balanced teaching design.
Replacing the CSV with real data requires revisiting those checks, missing
measurements, unusual observations, model assumptions, and the analysis plan.
A final ROI value alone is not sufficient to reconstruct a spectral Z-score;
these examples therefore do not attempt spectral response detection.
