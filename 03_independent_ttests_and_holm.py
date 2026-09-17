# FPVS paper using Welch's t-test for behavioral outcomes:
# - Fast periodic visual stimulation EEG reveals reduced neural sensitivity to
#   fearful faces in children with autism.
#   DOI: https://doi.org/10.1007/s10803-019-04172-0
# FPVS paper using Holm correction:
# - Identity-specific neural responses to three categories of face familiarity
#   (own, friend, stranger) using fast periodic visual stimulation.
#   DOI: https://doi.org/10.1016/j.neuropsychologia.2020.107415

"""EXAMPLE 3: Do the two groups respond differently?

What if we wanted to make a general comparison between your group and the adolescent group? There are
four tests in this 'family' of tests that we can run.

1. We could pool all of your conditions together as a 'grand average', do the same thing for the adolescent
   group data, then just make a coarse comparison. Your group vs adolescent group.

2. Negative Valence Adult vs Negative Valence Adolescent.
3. Positive Valence Adult vs Positive Valence Adolescent.
4. Neutral Angry Adult vs Neutral Angry Adolescent.

That gives us four total statistical tests, which means we are now making
multiple comparisons. Each time we run a statistical test with a p-value of 0.05, we are accepting that
there's a 5% chance we're wrong. If we do that four time, the effect stacks: 5x4 = 20% chance of a false
positive. No bueno.

But there is hope! We can correct for multiple comparisons using a method called Holm correction.

I've made up some more fake data to illustrate this point.
"""
from pathlib import Path
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

data = pd.read_csv(Path(__file__).with_name("synthetic_occipital_roi.csv"))

# First, what if we wanted to compare the groups across all three conditions?
# We'd average the three responses for EACH PERSON, giving every condition equal weight.
# The ROI electrodes were already averaged during processing. This is a separate step.
# Now we have one value per person, so 50 values altogether.
# We don't want to treat the 75 rows in each group as 75 different people.
# We also don't want just one average per group, because the test needs to know
# how much responses vary from person to person.

participant_means = data.groupby(["participant", "group"], as_index=False)["bca_uv"].mean()
comparisons = [("Overall: mean of 3 conditions", participant_means)]
for condition in ["Positive Valence", "Negative Valence", "Neutral Angry"]:
    comparisons.append((condition, data[data["condition"] == condition]))

# We also want to compare the groups within each condition.
# Group_A and Group_B have different people in them, so we use independent t-tests, not paired tests like
# the previous examples.

rows = []
for label, selected in comparisons:
    first = selected.loc[selected["group"] == "Group_A", "bca_uv"]
    second = selected.loc[selected["group"] == "Group_B", "bca_uv"]

    # equal_var=False tells Python to use Welch's t-test. This lets the amount
    # of variation differ between the two groups. That's also why the degrees
    # of freedom (df) in the output might have decimal places.
    # equal_var=True would use Student's t-test, which assumes equal population variances.
    # We'd choose which test makes sense before looking at the results.

    result = stats.ttest_ind(first, second, equal_var=False, alternative="two-sided")
    interval = result.confidence_interval(confidence_level=0.95)
    rows.append({
        "comparison": label,
        "mean_A_uv": first.mean(),
        "mean_B_uv": second.mean(),
        "A_minus_B_uv": first.mean() - second.mean(),
        "t": result.statistic,
        "df": result.df,
        "p_raw": result.pvalue,
        "CI95_low_unadjusted": interval.low,
        "CI95_high_unadjusted": interval.high,
    })
results = pd.DataFrame(rows)

# We're doing four tests: one overall comparison and one for each condition.
# More tests give us more chances for our tests to return a false positive.

# Holm correction adjusts the p-values across this set, or "family," of tests.
# Assuming the tests are valid, this keeps the chance of one or more false positives
# across the family at no more than 5% when we use alpha=0.05.
# The [1] below selects the adjusted p-values from what multipletests returns.
# We compare p_holm directly with 0.05. We don't divide 0.05 by four again.
results["p_holm"] = multipletests(results["p_raw"], alpha=0.05, method="holm")[1]
print("SYNTHETIC DATA | 25 participants per group | one family of four tests")
print(results.to_string(index=False, float_format=lambda value: f"{value:.6g}"))