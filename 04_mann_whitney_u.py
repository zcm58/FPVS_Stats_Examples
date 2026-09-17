# FPVS paper using Mann-Whitney U for behavioral outcomes:
# - Fast periodic visual stimulation EEG reveals reduced neural sensitivity to
#   fearful faces in children with autism.
#   DOI: https://doi.org/10.1007/s10803-019-04172-0

"""EXAMPLE 4: Compare two groups using the ranks of their responses.

Example three compared the average responses between your group and the adolescent group.
But comparing averages isn't the only question we could ask about those groups.
What if we wanted to know whether responses in one group tend to be higher than the other?

For this example, we'll focus on the Neutral Angry condition and use a Mann-Whitney U test.
We still have two separate groups of people, so this is an independent-groups comparison.
We're using the same synthetic ROI responses, but we're looking at their ranks this time.

What does that mean? Basically, we put everyone's responses in order from smallest to largest.
The smallest response gets rank 1, the next gets rank 2, and so on. If Group_A tends to have
larger responses, those people will tend to appear closer to the top of that ordered list.
The test uses those ranks to evaluate the difference between the groups.

You'll hear this called a nonparametric test. It doesn't require normally distributed
responses, but it still has assumptions and asks a different question from a test of means.
We'd choose it based on our research question and data, rather than trying to get a smaller p-value.

Run: python 04_mann_whitney_u.py
"""
from pathlib import Path

import pandas as pd
from scipy import stats

# First, let's load the same spreadsheet we've been using. We select Neutral Angry,
# then separate the responses into Group_A (your group) and Group_B (the adolescents).
# first and second each contain 25 BCA values. There's one value per person here.
# We don't pivot or match people across groups, because they are different people.

data = pd.read_csv(Path(__file__).with_name("synthetic_occipital_roi.csv"))
selected = data[data["condition"] == "Neutral Angry"]
first = selected.loc[selected["group"] == "Group_A", "bca_uv"]
second = selected.loc[selected["group"] == "Group_B", "bca_uv"]

# What if we compared where people's responses rank, from smallest to largest?
# That's what Mann-Whitney uses to compare the two independent groups.
# The starting assumption is that the population distributions are the same.
# This test can pick up a tendency for one group to have higher values, but it
# won't detect every possible way that two distributions could differ.
#
# You'll sometimes see this described as a test of medians. That interpretation
# needs extra assumptions, like distributions with the same shape that only shift
# higher or lower. It isn't just a t-test with the normality rule removed.
# It also differs from the Wilcoxon signed-rank test, which is for paired data.

# Here's a small made-up example just to illustrate the ranking:
# Group_A has responses of 0.4 and 0.6 uV, and Group_B has 0.1 and 0.3 uV.
# Putting all four values in order gives B, B, A, A. Group_A gets ranks 3 and 4.
# If two values are tied, they share the average of the ranks they would have occupied.
# Python does this ranking for us. We pass in the original BCA values below.
#
# alternative="two-sided" lets either group have the higher responses.
# Unlike Example 1, we're comparing two groups here, not asking whether BCA is above zero.

# We have 25 people per group. method="asymptotic" uses an approximation to
# calculate the p-value, and Python accounts for ties (people with the same value).

result = stats.mannwhitneyu(
    first, second, alternative="two-sided", method="asymptotic"
)

# Now let's look at the output. n_A and n_B are the numbers of people in each group.
# The median is the middle response after putting that group's values in order.
# U is the test statistic for the first group we passed in, which is Group_A.
# Its size depends on the group sizes, so we don't compare U directly with 0.05.
# We compare the p-value with our chosen significance level instead.
# A small p-value is evidence against identical population distributions, under
# the test's assumptions. The summaries help us see which way the sample difference goes.

print("SYNTHETIC DATA | Neutral Angry | Group_A versus Group_B")
print(f"n_A = {len(first)}; n_B = {len(second)}")
print(f"Group_A median = {first.median():.4f} uV")
print(f"Group_B median = {second.median():.4f} uV")
print(f"U for Group_A = {result.statistic:.2f}; p = {result.pvalue:.6g}")

# We can also compare every person in Group_A with every person in Group_B.
# This fraction tells us how often A's value was larger in those comparisons.
# A tie counts as half. It's a description of our sample, not the probability
# that a hypothesis about the population is true.

# With 25 people in each group, there are 25 x 25 = 625 cross-group comparisons.
# These aren't 625 independent participants! We're just describing the same 50 people.
# A fraction of 0.80, for example, would mean A wins 80% of these comparisons,
# counting ties as half a win. Around 0.50 means neither group tends to win more often.
# This is a useful way to explain the direction without treating U as a difference in uV.

fraction = result.statistic / (len(first) * len(second))
print(f"Observed A > B pair fraction, with half-credit for ties: {fraction:.3f}")

# The medians help us describe the groups. Treating this as a test of their
# medians would need the extra assumptions we talked about above.
# We're only comparing one condition here. If we compared all three, we'd need
# to plan how to account for those multiple tests.

# With real data, a normality-test p-value alone shouldn't decide which test we use.
# We also shouldn't try both tests and keep whichever gives the smaller p-value. We could run both tests
# and report values from both tests to be scientifically accurate and transparent.

