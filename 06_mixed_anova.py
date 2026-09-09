"""EXAMPLE 6: Compare both groups across all three conditions.

Now let's put all the previous examples together. We have your adult group and the adolescent group,
and everyone completed Positive Valence, Negative Valence, and Neutral Angry.
We might want to know whether the groups differ overall, whether the conditions differ overall,
and whether the pattern across conditions is different between the groups.

Those are three related questions, but they aren't the same question.

For example, imagine the adult group responds more strongly than the adolescent group in
all three conditions. That's one possible pattern. Now imagine they're similar in Positive
Valence, but much farther apart in Neutral Angry. That gives us a different story about how
the group difference changes with the condition. We call that a group-by-condition interaction.

To look at these questions together, we'll use a mixed ANOVA. 'Mixed' means we're combining
a between-person factor (group) with a within-person factor (condition).
Each person belongs to only one group, but contributes a response in all three conditions.
We have two groups and three conditions, so you'll also hear this called a 2 x 3 mixed design.

Why use ANOVA here? We want to compare the patterns across conditions between the groups.
Separate tests could tell us whether adults and adolescents differ in each condition,
but simply comparing which p-values are significant wouldn't tell us whether the group
difference changes across conditions. The interaction tests that question directly.
Also, adults and adolescents are different people, so comparing those groups calls for
an independent-group comparison. Paired tests apply to measurements from the same person.

We're still using synthetic data, with 25 people per group. The goal is to understand the
three questions and how to read the output before applying this to your actual dataset.
The code uses one occipital ROI. The lecture notes at the end explain how we'd add LOT and ROT.

Run: python 06_mixed_anova.py
You'll need Pingouin installed. It's listed in requirements.txt.
"""
from pathlib import Path

import pandas as pd
import pingouin as pg
from scipy import stats

# This time, we keep the whole spreadsheet: both groups and all three conditions.
# Participant IDs need to identify different people across the whole dataset.
# A01 and B01 are different people. Within A01, the three condition rows belong together.

data = pd.read_csv(Path(__file__).with_name("synthetic_occipital_roi.csv"))

# Now we're putting the two ideas together: different groups of people,
# with each person completing all three conditions. That's the "mixed" design.
# Group is the between-person factor, and condition is the within-person factor.
# We still have 50 people, even though the spreadsheet has 150 rows.
#
# There are three questions in the output:
# group: Do the groups differ when we average across the three conditions?
# condition: Do the conditions differ when we average across the two groups?
# Interaction: Does the size or direction of the group difference change by condition?
#
# For example, Group_A might be higher in positive valence but lower in negative
# valence. An overall group average could hide that pattern.
# Finding significance in one condition but not another doesn't establish an
# interaction by itself. We need the interaction test to answer that question.
# The first two questions are called main effects. They average over the other factor.
# For the group effect, each condition contributes equally to the comparison.
# For the condition effect, we're looking across the two equally sized groups.
# An interaction asks about differences IN those differences.
# For example, an adult-adolescent gap of 0.02 uV in Positive Valence and 0.20 uV
# in Neutral Angry suggests a different pattern from a constant 0.10 uV gap everywhere.
# Those numbers are just an illustration. The test uses participant-level variation
# to evaluate the pattern, rather than deciding based on two sample gaps alone.
#
# dv is our BCA outcome. between identifies group, within identifies condition,
# and subject identifies each person. We use correction=False here because we're
# going to calculate the GG-adjusted results explicitly in the next section.
# effsize="np2" asks Python to include partial eta-squared in the results.

result = pg.mixed_anova(
    data=data,
    dv="bca_uv",
    between="group",
    within="condition",
    subject="participant",
    correction=False,
    effsize="np2",
)

# This next part is a little more involved. We're applying the GG correction
# from Example 5 to both the condition effect and the interaction.
# The ANOVA call above gives us uncorrected tests, so we calculate those two
# corrected p-values below. The group effect doesn't need a sphericity correction
# because it compares different people rather than repeated measurements.
#
# First, we subtract each group-condition average from the values in that group
# and condition. The leftover values are called residuals, or errors.
# We use these to estimate epsilon, so differences in the groups' condition
# patterns don't get mixed into our estimate of the error relationships.
# The ANOVA itself still uses the original BCA values.
# This approach assumes the groups have the same pattern of error variances
# and relationships between conditions (their covariance matrices).
# For example, if A01 has 0.30 uV and their group-condition average is 0.20 uV,
# their residual is 0.10 uV. "Error" here means deviation from the fitted average;
# it doesn't mean the recording was a mistake or that we should remove it.
# data.copy() gives us a separate table for this calculation.
# groupby finds each group-condition combination, and transform("mean") puts its
# average beside every corresponding row so the subtraction lines up correctly.

errors = data.copy()
errors["bca_uv"] = data["bca_uv"] - data.groupby(["group", "condition"])["bca_uv"].transform("mean")
epsilon = pg.epsilon(errors, dv="bca_uv", within="condition", subject="participant", correction="gg")

# Now we multiply both degrees of freedom by epsilon, keeping F the same.
# stats.f.sf gives us the chance of an F value at least this large under the null,
# using those degrees of freedom. That's our p-value.
# p_for_report uses GG for condition and the interaction, and the ordinary
# p-value for group. We haven't applied a Holm correction here.
result["df1_for_report"] = result["DF1"].astype(float)
result["df2_for_report"] = result["DF2"].astype(float)
repeated_effect = result["Source"].isin(["condition", "Interaction"])
result.loc[repeated_effect, ["df1_for_report", "df2_for_report"]] *= epsilon
result["p_for_report"] = stats.f.sf(result["F"], result["df1_for_report"], result["df2_for_report"])

# repeated_effect marks the condition and Interaction rows. The .loc line above
# changes the reporting degrees of freedom for those rows only.
# Decimal degrees of freedom are expected after multiplying by epsilon.
# The group row keeps its original degrees of freedom.
# columns below selects the parts of the result table we'll show in the console.

print("SYNTHETIC DATA | 2 groups x 3 conditions | 25 people per group")
print(f"GG epsilon estimated from within-group errors = {epsilon:.6f}")
columns = ["Source", "F", "df1_for_report", "df2_for_report", "p_for_report", "np2"]
print(result[columns].to_string(index=False, float_format=lambda value: f"{value:.6g}"))

# When we read the table, start by matching each row to its research question.
# A small group p_for_report supports an overall group difference.
# A small condition p_for_report supports a difference somewhere across conditions.
# A small Interaction p_for_report supports a group difference that changes by condition.
# Each interpretation assumes the model is appropriate, and the significance threshold
# needs to match whatever multiple-testing plan we chose (more on that below).
#
# An interaction doesn't require the groups to switch which one is higher.
# A gap that grows from one condition to another can also be an interaction.
# If we find one, we'd look at group-condition averages and planned follow-up comparisons
# to explain the pattern. The interaction test alone doesn't identify the specific pairs.
# Example 3 shows the between-group comparisons within each condition.
#
# If the interaction isn't significant, that doesn't prove the patterns are identical.
# And if it is significant, the main effects are still averages, so they may leave out
# a lot of the story. We'd describe the condition-specific pattern alongside them.
# A simple plot of each group's condition averages would help explain that in a lecture.
#
# np2 is partial eta-squared. It describes each effect relative to that effect's
# variation plus its error variation. It isn't the percentage of all EEG variation explained.
# Also, a mixed ANOVA and a linear mixed-effects model are different analyses.
# We're using the ANOVA here.
#
# With real data, we'd look at the residuals and unusual values, and check that
# people are independent and the groups have a similar covariance structure.
# GG addresses sphericity. It doesn't fix outliers, different covariance matrices
# between groups, or bias from missing data.
#
# We'd also decide ahead of time which of the three effects answer our main questions.
# If we're treating all three as one family of tests, we'd adjust their p_for_report
# values together, for example with multipletests(..., method="holm").
# This example hasn't done that extra adjustment. Example 3 shows how Holm works.
# Before using these lessons together on real data, we'd plan which questions
# we're answering, which tests we need, and which comparisons belong together.
#
# Now let's think about the fuller study with LOT and ROT.
# LOT is left occipito-temporal and ROT is right occipito-temporal.
# Assume we measure both ROIs in every condition for each adult and adolescent.
# We'd compare the conditions that both age groups actually completed.
#
# We'd have three factors:
# Group: adults or adolescents. Each person belongs to only one group.
# Condition: Positive Valence, Negative Valence, and Neutral Angry in this example.
# ROI: LOT or ROT. Both measurements come from the same person.
# Group is between people; condition and ROI are within people.
# That would be a 2 groups x 3 conditions x 2 ROIs mixed-design ANOVA.
# With eight shared conditions, the design would become 2 x 8 x 2.
#
# We'd keep one row per participant, condition, and ROI, with their BCA value.
# The same participant ID would connect all six measurements in the three-condition
# example. With 50 people, we'd have 300 rows, but still only 50 participants.
# We wouldn't treat LOT and ROT as independent participants or combine them into
# one ROI average if our question is whether the responses differ between them.
#
# This fuller ANOVA would let us ask seven questions. The first three are main effects:
# Group: Do adults and adolescents differ, averaging across conditions and ROIs?
# Condition: Do conditions differ, averaging across groups and ROIs?
# ROI: Do LOT and ROT differ, averaging across groups and conditions?
#
# The next three are interactions between two factors:
# Group x Condition: Does the adult-adolescent gap change by condition, averaging ROIs?
# Group x ROI: Does the adult-adolescent gap change between LOT and ROT, averaging conditions?
# Condition x ROI: Do condition differences change between LOT and ROT, averaging groups?
#
# Finally, Group x Condition x ROI asks whether the condition-by-ROI pattern
# differs between adults and adolescents. That's a three-way interaction.
# Basically, does the way condition differences change between LOT and ROT depend on age group?
#
# Here's a made-up example using just Negative Valence minus Positive Valence:
#                              LOT          ROT
# Adults' average difference:  0.02 uV      0.20 uV
# Adolescents' difference:     0.02 uV      0.02 uV
# For adults, the condition difference is larger at ROT. For adolescents, it stays
# the same across the two ROIs. The change across ROIs is 0.18 uV in adults and
# 0.00 uV in adolescents. That's the kind of pattern a three-way interaction tests.
# These numbers alone don't establish significance. We'd need the individual data
# to judge the uncertainty, and the full ANOVA would include all three conditions.
#
# This is why adding ROI to the model can matter. Averaging LOT and ROT together
# could hide a regional difference. Running an ANOVA separately at each ROI and
# finding significance at only one wouldn't establish that the ROIs differ.
# Including ROI lets us test those differences directly, while accounting for the
# fact that both measurements came from the same participant.
#
# Then we'd use focused follow-up comparisons to explain the pattern. For example,
# we could compare Negative Valence with Positive Valence within ROT for each group.
# Those are paired comparisons because each person completed both conditions.
# To ask whether that contrast differs between age groups, we'd compare each person's
# Negative-minus-Positive difference between adults and adolescents. That's an
# independent-group comparison of difference scores, not a comparison of two p-values.
# We'd choose the relevant comparisons and their multiple-testing correction in advance.
#
# One ANOVA model still gives us several tests, so it doesn't automatically solve
# multiple testing. We'd focus on the effects that answer our research questions
# and plan the corrections for those effects and any follow-up comparisons.
# Planned contrasts can also be tested without requiring a significant overall ANOVA first.
#
# These are notes for extending the real study. The current dataset and ANOVA call
# still have one ROI, so the printed output contains only Group, Condition, and
# their interaction. Adding LOT and ROT requires ROI-level data and a model that
# includes both repeated factors; it isn't just a change to the labels.
# Documentation: SOURCES.md [7], [9], [10].
