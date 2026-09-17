# FPVS paper using repeated-measures ANOVA:
# - Identity-specific neural responses to three categories of face familiarity
#   (own, friend, stranger) using fast periodic visual stimulation.
#   DOI: https://doi.org/10.1016/j.neuropsychologia.2020.107415

"""EXAMPLE 5: Do responses differ across conditions and between LOT and ROT?

Example 2 compared Positive Valence with Negative Valence within your group.
But you have a third condition too: Neutral Angry. In your actual data, there are 7 or 8 conditions I think!
What if we wanted to ask whether there's a difference anywhere across your conditions?

We could run three paired t-tests, one for each pair. That would answer three specific
questions, and we'd need to account for those multiple comparisons like we did in Example 3.
Here, we're starting with one broader question: are all three population averages equal?

This becomes more useful as we add conditions. With eight conditions, comparing every pair
would mean 28 paired tests at just one ROI in one group. Doing that separately at LOT and ROT
would give us 56 comparisons. That's a lot of individual questions to keep track of, and we'd
need to decide which comparisons belong together when correcting for multiple testing.

To ask about an overall condition effect, we'll use a repeated-measures ANOVA.

ANOVA stands for analysis of variance. Even though we're asking about averages, the test uses
variation in the data to evaluate whether the differences between those averages are larger than
we'd expect.

The 'repeated-measures' part matters because the same people completed every condition.
Each participant has responses to 3 conditions at LOT and ROT in this fake data.
That gives us 150 total responses, but we only have 25 adults measured six times.

This is the same reason we needed a paired test in Example 2, just expanded to three conditions.

If the corrected p-value is below 0.05, we have evidence that the population condition means
aren't all equal, assuming the test's assumptions hold. Translation: we would have evidence that, at the
group level, at least one condition mean differs from another. That doesn't mean every condition
is significantly different from every other condition. We'd need follow-up tests for that to get more specific
evidence (which we will discuss later).

This example now includes LOT (left occipito-temporal) and ROT (right occipito-temporal).
We measure both in every condition for every participant, just like in the fuller study design.
Now condition AND ROI are repeated measurements. LOT and ROT aren't separate groups of people.
With three conditions and two ROIs, each person contributes six values, but they're still one person.

We'll use a two-factor repeated-measures ANOVA for that design. A factor is just something
we're comparing: here, which condition we're showing and which ROI we're measuring.
We can ask whether conditions differ on average across the two ROIs, whether LOT and ROT
differ on average across conditions, and whether the condition differences depend on the ROI.
That last question is called a condition-by-ROI interaction.

For example, maybe Positive Valence and Negative Valence have similar responses at LOT,
but Negative Valence has a much larger response at ROT. We'd want to test whether that
condition difference actually changes between ROIs. Finding a significant paired test at ROT
and a nonsignificant one at LOT wouldn't, by itself, establish that interaction.

This is another reason to use ANOVA: it can test how these factors work together.
If our only question was Positive Valence versus Negative Valence at a planned ROI, a paired
test could answer that directly. We don't have to get a significant ANOVA first to run a
comparison we planned ahead of time. We still need a plan for any multiple comparisons.

The code below tests all three effects in adults: Condition, ROI, and Condition x ROI.
Example 6 adds adolescents and asks whether these patterns also depend on age group.

"""
from pathlib import Path

import pandas as pd
import pingouin as pg

# First, we'll load the data and keep Group_A. We keep ALL THREE conditions this time and we're
# only looking at our fake adult dataset in this example.

# Our spreadsheet is in long format: each person has a row for each condition AND ROI.
# Pingouin is a different python library that can use that format directly, so we don't need to
# pivot the table here.

# The participant column tells it which six rows belong to the same person.

data = pd.read_csv(Path(__file__).with_name("synthetic_multi_roi.csv"))
selected = data[data["group"] == "Group_A"]

# The starting assumption is that all three population means are equal. We assume that each condition
# produced exactly the same response, then we use rm-ANOVA to test whether that assumption is false.

# A significant result suggests a difference somewhere, but doesn't tell us which
# specific conditions differ. We'd need follow-up paired comparisons to look at that,
# (go back to example 02) to examine more closely.

# Think about someone who has a relatively strong baseline response in every condition.
# practically, this can happen if someone comes into the lab and is bald. They will likely
# have a higher overall baseline BCA response just by the nature of how EEG works.

# We don't want that person's overall response level to get confused with a condition effect.
# It doesn't mean that person has a stronger response, it just means their baseline is higher.

# The repeated-measures analysis separates that person-to-person variation from the
# variation used to test condition. We're interested in how responses change within people.
# The null hypothesis is: Positive Valence mean = Negative Valence mean = Neutral Angry mean.
# These are population means. Our sample averages almost certainly won't be exactly equal in real life.
# That condition comparison averages LOT and ROT within each person.
# The ROI null is that LOT and ROT have the same mean after averaging conditions.
# The interaction null is that the ROT-minus-LOT gap is the same across conditions.

# These arguments tell Python how our data are organized when using ANOVA.

# dv is the value we're analyzing, which is BCA in microvolts.
# within lists BOTH factors measured repeatedly in each person: condition and ROI.
# subject tells it which column identifies the same person across the rows.
# correction=True asks for the Greenhouse-Geisser (GG) correction, explained below.
# effsize="np2" adds partial eta-squared, a measure of effect size, to the output.

result = pg.rm_anova(
    data=selected,
    dv="bca_uv",
    within=["condition", "roi"],
    subject="participant",
    correction=True,
    detailed=True,
    effsize="np2",
)
# With two within-person factors, the table has a row for each of the three effects.
# Each effect has its own error term. This table doesn't print separate Error rows.
# to_string prints the whole table so we can read it in the console.
# The formatting changes how many digits we see; it doesn't change the calculation.

print("SYNTHETIC DATA | Group_A (adults) | 3 conditions x 2 ROIs | 25 people, 150 rows")
print("Mean BCA in uV:")
print(selected.groupby(["condition", "roi"], sort=False)["bca_uv"].mean().unstack().to_string(float_format=lambda value: f"{value:.4f}"))
print(result.to_string(index=False, float_format=lambda value: f"{value:.6g}"))

# F compares variation linked to condition with the within-person error variation.
# ddof1 and ddof2 are the uncorrected effect and error degrees of freedom.
# np2 is the partial eta-squared effect size.
# In the version I'm using (Pingouin 0.6.1), p_unc is the uncorrected p-value.
# p_GG_corr is the corrected one. That's the p-value we're using for this example.
# eps is epsilon, the adjustment factor. For Condition and Condition x ROI,
# it's between 0.5 and 1. ROI has only two levels, so its epsilon is 1.
# GG multiplies both degrees of freedom by epsilon, while keeping F the same.

# After you run this file, here's some help on how to interpret the result.

# Start with the condition row. SS means sum of squares, a measure of variation.
# MS is SS divided by its effect degrees of freedom. F is effect MS divided by its error MS.
# A larger F means more condition-related variation relative to the remaining error.
# How unusual that F is depends on the degrees of freedom, which give us the p-value.
# Use p_GG_corr here because we chose the GG correction in advance.
# If it is below 0.05, we'd say there is evidence of a condition effect.
# If it is above 0.05, we'd say this test didn't establish a difference.
# That wouldn't prove the conditions are identical.
#
# np2 describes condition variation relative to condition variation plus its error.
# It adds information about effect size, but we still want the averages in microvolts.
# Read the roi row for the overall LOT/ROT difference and condition * roi for the interaction.
# A significant interaction means the condition differences depend on ROI. It doesn't
# identify which condition pair drives that pattern, so look at the means and follow-ups.

# So why use the GG correction? There's an assumption called "sphericity."
# Basically, if we calculated everyone's differences for each pair of conditions,
# we'd expect a similar amount of variation in those differences across the pairs.
# GG adjusts for departures from that assumption. It handles a different issue
# from Holm or Bonferroni, which account for running multiple tests.
#
# For the condition effect, first average LOT and ROT within each person and condition.
# The three sets of differences we'd use to think about sphericity are:
# Positive Valence minus Negative Valence, Positive Valence minus Neutral Angry,
# and Negative Valence minus Neutral Angry. It's their variances we're comparing.
# We aren't assuming that the three condition averages are equal when checking sphericity.
# Epsilon near 1 means a small GG adjustment. A smaller epsilon means a larger adjustment.
# For Condition x ROI, we look at how each person's ROT-minus-LOT gap changes
# across conditions. This effect gets its own epsilon, which can differ from condition's.
# ROI alone has only one LOT/ROT comparison, so sphericity is automatic for that effect.
# Pingouin doesn't provide Mauchly's interaction test here; we use GG as planned.
#
# If we wanted to locate the differences, we'd use paired tests like Example 2.
# For all three condition pairs averaged across ROIs, we'd apply Holm to those three p-values.
# The GG correction above doesn't replace that multiple-comparisons correction.
# With a condition-by-ROI interaction, we'd follow up on the condition differences
# within the relevant ROIs, using a comparison plan that includes those ROI questions.
# A significant ANOVA doesn't make every follow-up comparison significant or remove
# the need to account for running several tests.
# Those follow-up tests aren't run in this file.
# There are also three omnibus effects in this table. GG is not a correction across
# those three tests; we'd plan any correction for that family based on our hypotheses.
