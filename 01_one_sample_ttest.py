"""EXAMPLE 1: Is the average final ROI response above zero?

Data: SYNTHETIC data from Elizabeth's experiment. We'll use a hypothetical FPVS condition,
Positive Valence, from the occipital ROI. Assume all data has already been processed through FPVS Toolbox.
(I can explain FPVS Toolbox data processing if you'd like)

The first question we might want to ask when analyzing our FPVS data is this: is the 'oddball response'
significantly greater than random noise in the EEG signal?

To test this, we'll use a one-sided, one sample t-test against zero.

But why?

This involves how baseline corrected amplitude (BCA) is calculated. Let me know if you aren't sure about this.
Understanding what BCA is and how we calculate this is super important to conceptualizing FPVS Stats.
Basically, if the BCA value is zero, then the measured oddball response is null. Aka no response.

If BCA = 0, then there is no response to the oddball images.

If BCA is greater than zero, then the oddball response is stronger than the noise. This is good (but does
not necessarily mean the response is significant). We need to run a statistical test to confirm
whether the response is significantly greater than zero (aka, whether your p-value is less than 0.05).

Run python 01_one_sample_ttest.py to test whether this oddball response is significantly greater than zero.

"""
from pathlib import Path
import pandas as pd
from scipy import stats

# Path(__file__) finds this script's location. The CSV file with our hypothetical data
# is next to this script after you extracted these files, so we don't need to hardcode anything if
# we do it this way. You can hard code things if you like, but I prefer a generic approach.
# It's easier to adapt the code later.

data = pd.read_csv(Path(__file__).with_name("synthetic_occipital_roi.csv"))

"""
Later on, we might compare your dataset with another dataset collected from adolescents,
because we have a lot of kids aged 13-15 that completed some of the same conditions as your experiment.
Because of that, I'm considering your dataset as 'Group_A' in this example and the adolescent
dataset will later be 'Group_B'.
"""

# We need to select your group and the specific condition that we want to test. In this example,
# we'll be testing whether the group average response in the occipital ROI to the hypothetical positive
# valence condition was significantly above zero, so I am defining those variables here.

selected = data[(data["group"] == "Group_A") & (data["condition"] == "Positive Valence")]
values = selected["bca_uv"]

# The t-statistic tells us how far our average is from zero compared with the
# uncertainty in that average. Here, it's the mean divided by its standard error.
# That standard error depends on how much people vary across recordings and how many people we have.
# We only care about BCA responses above zero, so we're using alternative="greater".
# This tests whether the population average is above zero, with zero or below
# as the null hypothesis. We're choosing that direction based on our question.
# The t-statistic is calculated the same way, but the p-value now looks only
# in the positive direction.

result = stats.ttest_1samp(values, popmean=0.0, alternative="greater")
interval = result.confidence_interval(confidence_level=0.95)

print("SYNTHETIC DATA | Group_A | Positive Valence | Occipital ROI")
print(f"n = {len(values)} participants")
print(f"Mean BCA = {values.mean():.4f} uV; SD = {values.std(ddof=1):.4f} uV")
print(f"t({result.df:.0f}) = {result.statistic:.4f}; one-sided p = {result.pvalue:.6g}")
print(f"95% one-sided lower confidence bound for the population mean = {interval.low:.4f} uV")

# Basically, the p-value asks how unusual a t-statistic this large or larger would be
# if the population average really were zero, assuming the test's assumptions hold.

# It doesn't tell us the probability that our hypothesis is true or that this was chance.
# Because we're testing for responses above zero, we report a lower confidence bound.
# The one-sided interval goes from that bound up to infinity; it doesn't set an upper limit.
# If we repeated this process with new samples, about 95% of these lower bounds
# would be below the population mean. That's what the "95%" refers to.
# A lower bound above zero supports a population average above zero at the 5% level.

# With real data, we'd also look at the spread of the values and see if there were any outliers in the data.
# Also, a positive group average doesn't mean every person had a positive response, but we can talk about
# how to interpret your results later.

""" Run this file to simulate a one sample t-test against zero. """


