# FPVS paper using paired t-tests:
# - Differences in own-face but not own-name discrimination between autistic and
#   neurotypical adults: A fast periodic visual stimulation-EEG study.
#   DOI: https://doi.org/10.1016/j.cortex.2023.10.023

"""EXAMPLE 2: Do the SAME participants respond differently in two conditions?

Example one explored how to test whether an ROI has a statistically significant response. That information
is important, but it doesn't tell you much outside of whether an oddball response was present. In your case,
you might want to compare two specific conditions within your group to see if your participants responded
differently to those conditions.

For example, imagine you wanted to know whether the oddball responses to the 'Positive Valence' and the
'Negative Valence' condition were statistically significantly different within the group. To do this,
we could run a PAIRED t-test. We use a paired t-test because the same participants are present in
both conditions. If the p-value is lower than 0.05, we can conclude that the mean response between
those conditions is statistically significantly different.
"""
from pathlib import Path
import pandas as pd
from scipy import stats

# First, let's load the data from the .csv file with our synthetic data.

data = pd.read_csv(Path(__file__).with_name("synthetic_occipital_roi.csv"))
group_data = data[data["group"] == "Group_A"]

# We need to line up each person's positive and negative valence responses.
# Python's pivot function puts each person on one row, using their participant ID to match the values.
# We would never want to compare P21's response to Positive Valence to P15's response to Negative Valence.
# That comparison doesn't really tell you anything. We want to line things up so we can compare each
# participant with themselves (hence the term 'paired tests'). This section of code does that while definining
# some variables

wide = group_data.pivot(index="participant", columns="condition", values="bca_uv")
first = wide["Positive Valence"]
second = wide["Negative Valence"]

"""
Basically, we subtract each person's negative valence values from their
positive valence response. Then we test whether those differences average to zero.

If the difference is zero, then we can conclude that the responses to positive valence and 
negative valence were the same. If the difference is NOT zero, then we know the responses to those 
conditions are different. 

"""

differences = first - second
result = stats.ttest_rel(first, second, alternative="two-sided")
interval = result.confidence_interval(confidence_level=0.95)

print("SYNTHETIC DATA | Group_A | Positive Valence minus Negative Valence")
print(f"n = {len(wide)} paired participants")
print(f"Positive Valence mean occipital oddball response = {first.mean():.4f} uV")
print(f"Negative Valence mean occipital oddball response = {second.mean():.4f} uV")
print(f"Mean within-person difference = {differences.mean():.4f} uV")
print(f"t({result.df:.0f}) = {result.statistic:.4f}; p = {result.pvalue:.6g}")
print(f"95% CI for the mean difference: [{interval.low:.4f}, {interval.high:.4f}] uV")

# A positive difference here means the positive valence response was larger.
# We could get the same result by running a one sample t-test on these differences,
# using zero as the value we're comparing them with.
#
# For the normality assumption, we'd look at the distribution of the DIFFERENCES.
# We don't need each condition on its own to be normally distributed.
# People still need to be independent of each other, and we'd look for unusual
# differences that might have a big effect on the result.
#
# The p-value doesn't tell us how large or useful the difference is. We'd also
# report the average difference, its confidence interval, and how many people we had.
# We're doing one planned comparison here. Comparing every pair across three
# conditions would mean three tests, so we'd need a correction like Holm (Example 3).
# Example 5 shows how to compare all three conditions in one overall test.
# Documentation: SOURCES.md [2].
