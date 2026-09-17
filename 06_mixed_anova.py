# FPVS paper using mixed-design ANOVA:
# - Differences in own-face but not own-name discrimination between autistic and
#   neurotypical adults: A fast periodic visual stimulation-EEG study.
#   DOI: https://doi.org/10.1016/j.cortex.2023.10.023

"""EXAMPLE 6: Compare groups, conditions, and LOT/ROT responses together.

Now let's put all the previous examples together. We have your adult group and the adolescent group,
and everyone completed Positive Valence, Negative Valence, and Neutral Angry at LOT and ROT.
We might want to know whether the groups differ overall, whether the conditions differ overall,
and whether the pattern across conditions is different between the groups.

Those are three related questions, but they aren't the same question.

For example, imagine the adult group responds more strongly than the adolescent group in
all three conditions. That's one possible pattern. Now imagine they're similar in Positive
Valence, but much farther apart in Neutral Angry. That gives us a different story about how
the group difference changes with the condition. We call that a group-by-condition interaction.

To look at these questions together, we'll use a mixed ANOVA. 'Mixed' means we're combining
a between-person factor (group) with two within-person factors (condition and ROI).
Each person belongs to only one group, but contributes six responses: three conditions at two ROIs.
We have two groups, three conditions, and two ROIs: a 2 x 3 x 2 mixed design.

Why use ANOVA here? We want to compare the patterns across conditions between the groups.
Separate tests could tell us whether adults and adolescents differ in each condition,
but simply comparing which p-values are significant wouldn't tell us whether the group
difference changes across conditions. The interaction tests that question directly.
Also, adults and adolescents are different people, so comparing those groups calls for
an independent-group comparison. Paired tests apply to measurements from the same person.

We're still using synthetic data, with 25 people per group. The goal is to understand the
group and condition questions above, plus the ROI questions explained below. We now test
all seven effects, including whether the Group x Condition pattern changes between LOT and ROT.

Run: python 06_mixed_anova.py
You'll need Pingouin installed. It's listed in requirements.txt.
"""
from pathlib import Path

import pandas as pd
import pingouin as pg
from scipy import stats
from statsmodels.formula.api import ols

# This time, we keep both groups, all three conditions, and both ROIs.
# A01 and B01 are different people. A01's six rows all belong to the same adult.
# We have 300 rows, but still only 50 independent participants.
data = pd.read_csv(Path(__file__).with_name("synthetic_multi_roi.csv"))

# First, line up LOT and ROT for the SAME person in the SAME condition.
# This is the same idea as matching participants for the paired test in Example 2.
wide = data.pivot(index=["participant", "group", "condition"], columns="roi", values="bca_uv").reset_index()
wide["roi_average"] = (wide["LOT"] + wide["ROT"]) / 2
wide["roi_difference"] = wide["ROT"] - wide["LOT"]

# Why make an average AND a difference? Together they retain both ROI values.
# The average tells us about responses across the two ROIs. The difference tells
# us how much stronger ROT is than LOT. A negative difference means LOT is higher.
# We keep both views, so we aren't averaging away the ROI question.
#
# Pingouin's mixed_anova accepts only one within-person factor. With exactly TWO
# ROIs and this complete, balanced design, these two views let us calculate the
# same F tests as the full Group x Condition x ROI ANOVA using smaller ANOVAs.
# This is a decomposition of the full design, not two separate tests at LOT and ROT.
# It is specific to two ROIs; adding a third ROI would require a different calculation.
#
# On the averages, Group, Condition, and their interaction have their usual meaning.
# On the differences, each question gains an ROI component:
# Group asks whether the ROT-minus-LOT gap differs between age groups (Group x ROI).
# Condition asks whether that gap changes by condition (Condition x ROI).
# Their interaction asks whether that change differs by group (Group x Condition x ROI).
views = [
    ("roi_average", {"group": "Group", "condition": "Condition", "Interaction": "Group x Condition"}),
    ("roi_difference", {"group": "Group x ROI", "condition": "Condition x ROI", "Interaction": "Group x Condition x ROI"}),
]
tables = []
for outcome, effect_names in views:
    result = pg.mixed_anova(
        data=wide,
        dv=outcome,
        between="group",
        within="condition",
        subject="participant",
        correction=False,
        effsize="np2",
    )

    # Apply the GG correction to the effects involving condition in this view.
    # We subtract each group-condition mean to estimate the error covariance.
    # This keeps the groups' different mean patterns out of the epsilon estimate.
    # The average view and the difference view each get their OWN epsilon.
    errors = wide.copy()
    errors[outcome] = wide[outcome] - wide.groupby(["group", "condition"])[outcome].transform("mean")
    epsilon = pg.epsilon(errors, dv=outcome, within="condition", subject="participant", correction="gg")
    repeated_effect = result["Source"].isin(["condition", "Interaction"])
    result["epsilon"] = 1.0
    result.loc[repeated_effect, "epsilon"] = epsilon
    result["df1_for_report"] = result["DF1"] * result["epsilon"]
    result["df2_for_report"] = result["DF2"] * result["epsilon"]
    result["p_for_report"] = stats.f.sf(result["F"], result["df1_for_report"], result["df2_for_report"])
    result["Source"] = result["Source"].map(effect_names)
    tables.append(result)

# That gives us six effects. We still need the overall ROI effect: is the mean
# ROT-minus-LOT gap zero after averaging conditions and giving both groups equal weight?
# First, give each person ONE average ROI difference. The model below keeps group
# in the analysis, so its error comes from differences between people WITHIN groups.
# An ordinary one-sample test that ignored group would use the wrong error term here.
participant_differences = wide.groupby(["participant", "group"], as_index=False)["roi_difference"].mean()
roi_model = ols("roi_difference ~ C(group, Sum)", data=participant_differences).fit()

# This formula is a small regression used to calculate one ANOVA effect.
# C(group, Sum) codes the groups around their shared average. The Intercept is
# the equally weighted average ROI difference, rather than one group's difference.
# Testing that Intercept against zero gives the ROI main effect. With one effect
# degree of freedom, F = t squared. The error df is 50 people minus 2 group means = 48.
roi_f = float(roi_model.tvalues["Intercept"] ** 2)
roi_df = float(roi_model.df_resid)
tables.append(pd.DataFrame([{
    "Source": "ROI", "F": roi_f, "df1_for_report": 1.0, "df2_for_report": roi_df,
    "epsilon": 1.0, "p_for_report": stats.f.sf(roi_f, 1, roi_df), "np2": roi_f / (roi_f + roi_df),
}]))

# Put the seven effects into one table. For effects involving condition, the
# reporting df and p-values already include GG. ROI has two levels, so ROI and
# Group x ROI don't require a sphericity correction. Group doesn't require one either.
# Decimal degrees of freedom are expected after GG. F stays the same.
effect_order = ["Group", "Condition", "ROI", "Group x Condition", "Group x ROI", "Condition x ROI", "Group x Condition x ROI"]
result = pd.concat(tables, ignore_index=True).set_index("Source").loc[effect_order].reset_index()
columns = ["Source", "F", "df1_for_report", "df2_for_report", "epsilon", "p_for_report", "np2"]
result = result[columns]

print("SYNTHETIC DATA | 2 groups x 3 conditions x 2 ROIs | 50 people, 300 rows")
print("Group_A = adults; Group_B = adolescents. Mean BCA in uV:")
print(data.groupby(["group", "condition", "roi"], sort=False)["bca_uv"].mean().unstack().to_string(float_format=lambda value: f"{value:.4f}"))
print(result.to_string(index=False, float_format=lambda value: f"{value:.6g}"))

# Now let's read the full study design with LOT and ROT.
# LOT is left occipito-temporal and ROT is right occipito-temporal.
# Each participant completed the same three conditions at both ROIs.
# We'd compare only conditions that both age groups completed in a real study.
#
# We have three factors:
# Group: adults or adolescents. Each person belongs to only one group.
# Condition: Positive Valence, Negative Valence, and Neutral Angry.
# ROI: LOT or ROT. Both measurements come from the same person.
# Group is between people; condition and ROI are within people.
#
# There are seven questions in the output. The first three are main effects:
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
# Here's a made-up illustration using just Negative Valence minus Positive Valence:
#                              LOT          ROT
# Adults' average difference:  0.02 uV      0.20 uV
# Adolescents' difference:     0.02 uV      0.02 uV
# For adults, the condition difference is larger at ROT. For adolescents, it stays
# the same across the two ROIs. The change across ROIs is 0.18 uV in adults and
# 0.00 uV in adolescents. That's the kind of pattern a three-way interaction tests.
# These illustration numbers aren't the generated sample means printed above.
# They alone don't establish significance. We need individual data to judge the
# uncertainty, and the full ANOVA includes all three conditions.
#
# This is why adding ROI to the model can matter. Averaging LOT and ROT together
# could hide a regional difference. Running an ANOVA separately at each ROI and
# finding significance at only one wouldn't establish that the ROIs differ.
# Including ROI lets us test those differences directly, while accounting for the
# fact that both measurements came from the same participant.
#
# For each row, a small p_for_report supports that effect if the assumptions hold
# and it meets our chosen multiple-testing threshold. A nonsignificant result
# doesn't prove that the means or patterns are identical.
# np2 is partial eta-squared: each effect relative to itself plus its error variation.
# It isn't the percentage of all EEG variation explained. Look at the BCA means too.
#
# An interaction doesn't require the groups to switch which one is higher.
# A gap that grows from one condition or ROI to another can also be an interaction.
# Main effects are averages, so they may leave out a lot of the story if an
# interaction is present. We'd describe the condition- and ROI-specific patterns.
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
# multiple testing. GG addresses sphericity, not the fact that we tested seven effects.
# If all seven effects form one confirmatory family, we could apply Holm to their
# seven p_for_report values together. This file hasn't applied that extra correction.
# Planned contrasts can also be tested without requiring a significant overall ANOVA first.
#
# This calculation is for the complete, balanced two-group, two-ROI teaching design.
# It assumes independent people and comparable error covariance in the two groups.
# GG doesn't fix outliers, missing data, or different covariance matrices between groups.
# A mixed ANOVA and a linear mixed-effects model are different analyses; we're using ANOVA.
# Documentation: SOURCES.md [7], [9], [10].
