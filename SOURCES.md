# FPVS papers behind the statistical examples

These references connect our examples to published FPVS research, with DOI links and pointers to the relevant methods. The synthetic examples are not reproductions of these studies. Differences in outcomes, test direction, and corrections are identified below so we can describe the papers accurately in a lecture.

Checked September 9, 2026. Bracketed numbers retain the method topics used by existing source comments in the scripts. **An exact published match was not verified for every setting in our code.**

## [1] Example 01: One-sample t-test against zero

Dzhelyova, M., Jacques, C., & Rossion, B. (2017). At a single glance: Fast periodic visual stimulation uncovers the spatio-temporal dynamics of brief facial expression changes in the human brain. *Cerebral Cortex, 27*(8), 4106–4123.

[DOI: 10.1093/cercor/bhw223](https://doi.org/10.1093/cercor/bhw223) · [Author-hosted full text](https://15138e68bf.clvaw-cdnwnd.com/1caef9d353414e8be4f34c4530c14df0/200001890-6dec270fc0/Dzhelyova2016.pdf)

**Where to look:** Results → EEG Data: Frequency Analysis → “Response over the whole scalp,” page 6 of the linked advance-publication PDF.

**What matches:** A one-sample t-test against zero on participants' baseline-corrected amplitudes, averaged across channels and summed over oddball harmonics.

## [2] Example 02: Two-sided paired t-test

Nijhof, A. D., Catmur, C., Brewer, R., Coll, M.-P., Wiersema, J. R., & Bird, G. (2024). Differences in own-face but not own-name discrimination between autistic and neurotypical adults: A fast periodic visual stimulation-EEG study. *Cortex, 171*, 308–318.

[DOI: 10.1016/j.cortex.2023.10.023](https://doi.org/10.1016/j.cortex.2023.10.023) · [University-hosted full text](https://backoffice.biblio.ugent.be/download/01HMY1H77C4WFVAZR4DX4YYEZB/01HMY1HXD3MCYRAJ24VS092KXM)

**Where to look:** Section 2.7, EEG data pre-processing and analysis, pages 312–313.

**What matches:** Explicitly two-tailed paired-samples t-tests following analyses of baseline-subtracted FPVS amplitudes.

**Difference:** The authors assess Bonferroni correction for multiple comparisons. Our paired example demonstrates one planned comparison without that correction.

## [3] Example 03: Welch's independent-samples t-test

Van der Donck, S., Dzhelyova, M., Vettori, S., Thielen, H., Steyaert, J., Rossion, B., & Boets, B. (2019). Fast periodic visual stimulation EEG reveals reduced neural sensitivity to fearful faces in children with autism. *Journal of Autism and Developmental Disorders, 49*, 4658–4673.

[DOI: 10.1007/s10803-019-04172-0](https://doi.org/10.1007/s10803-019-04172-0) · [Publisher full text](https://link.springer.com/article/10.1007/s10803-019-04172-0)

**Where to look:** Behavioral Data Analysis; Results → Behavioral Measures: Orthogonal Task and Explicit Facial Emotion Processing.

**What matches:** Welch–Satterthwaite degrees of freedom for unequal-variance group comparisons of behavioral outcomes in an FPVS study, with fractional degrees of freedom reported for emotion-matching results.

## [4] Example 04: Mann–Whitney U test

**Reference:** Van der Donck et al. (2019), full citation and DOI in [3].

**Where to look:** The same behavioral methods/results sections, including fixation-cross accuracy and reaction times.

**What matches:** Mann–Whitney U comparisons of behavioral accuracy and reaction times between independent participant groups in an FPVS study.

## [5] Example 03 and follow-up comparisons: Holm correction

Campbell, A., Louw, R., Michniak, E., & Tanaka, J. W. (2020). Identity-specific neural responses to three categories of face familiarity (own, friend, stranger) using fast periodic visual stimulation. *Neuropsychologia, 141*, 107415.

[DOI: 10.1016/j.neuropsychologia.2020.107415](https://doi.org/10.1016/j.neuropsychologia.2020.107415) · [University-hosted full text](https://onlineacademiccommunity.uvic.ca/differentmindslab/wp-content/uploads/sites/3462/2020/03/Campbell_etal_2020_Neuropsychologia.pdf)

**Where to look:** Section 2.5.5, Region-of-interest analysis, pages 5–6.

**What matches:** Bonferroni–Holm correction for paired-sample comparisons of FPVS responses. This is the Holm procedure demonstrated in our code.

**Difference:** Their comparisons are paired and concern face familiarity. Example 03 applies Holm to four independent-group Welch tests: an across-condition participant average plus three condition comparisons.

## [6] Example 05: Repeated-measures ANOVA with Greenhouse–Geisser correction

**Reference:** Campbell et al. (2020), full citation and DOI in [5].

**Where to look:** Section 2.5.5, Region-of-interest analysis.

**What matches:** Repeated-measures ANOVA on baseline-corrected, summed-harmonic ROI responses with three within-person conditions; Greenhouse–Geisser (GG) correction is specified.

**Difference:** Their conditions are own, friend, and stranger. Example 05 adds a second repeated factor, LOT versus ROT, and tests Condition, ROI, and their interaction. They apply GG when Mauchly's test indicates a sphericity violation; our script always requests the GG result. With two ROI levels, the ROI effect's epsilon is 1.

## [7] Example 06: Mixed-design ANOVA

**Reference:** Nijhof et al. (2024), full citation and DOI in [2].

**Where to look:** Section 2.7, pages 312–313.

**What matches:** ANOVA combining between-person Group with within-person Condition on baseline-subtracted FPVS amplitudes, with GG correction and partial eta-squared specified.

**Difference:** Their design also includes stimulus type and, for parieto-occipital analyses, laterality. Example 06 now includes two groups, three conditions, and LOT/ROT as a repeated ROI factor. Their GG correction is conditional on sphericity violation; our script applies it to the four effects involving condition. The two-level ROI effects require no sphericity adjustment.

## [8] Other multiple-comparisons methods

Holm is supported by [5]; Bonferroni is supported by [2]. These are different procedures. No FPVS reference for Benjamini–Hochberg FDR was verified for this list; the current Example 03 executes Holm only.

Both Vandenheever et al. papers below also describe Bonferroni correction, which we mention in Example 05. In both studies, we used it for follow-up contrasts from linear mixed models of FPVS responses. The 2025a and 2025b labels match the saved papers in our FPVS reading folder.

Vandenheever, D., Davidson, H., Kemp, J., Murphy, Z., Kujawa, A., Shi, J., Nadorff, M. R., Bates-Brantley, K., & Sidwell, M. (2025a). Exploring facial expression processing with fast periodic visual stimulation and diverse stimuli. *Brain and Cognition, 189*, 106338.

[DOI: 10.1016/j.bandc.2025.106338](https://doi.org/10.1016/j.bandc.2025.106338)

**Where to look:** Section 2.5, EEG processing and analysis, page 3; Section 3, Results, page 4.

**What matches:** Bonferroni correction for posthoc contrasts. We modeled summed BCA using facial expression, ROI, and their interaction as fixed effects, with participant as a random effect. This lets us ask about expression and ROI differences while accounting for repeated responses from the same person.

Vandenheever, D., Davidson, H., Kemp, J., Murphy, Z., Kujawa, A., Shi, J., Nadorff, M. R., Bates-Brantley, K., & Sidwell, M. (2025b). Preliminary evidence for anxiety-linked neural sensitivity to emotional faces using fast periodic visual stimulation. *International Journal of Psychophysiology, 214*, 113212.

[DOI: 10.1016/j.ijpsycho.2025.113212](https://doi.org/10.1016/j.ijpsycho.2025.113212)

**Where to look:** Section 2.6, Statistical analysis, pages 3–4.

**What matches:** Bonferroni correction for planned posthoc contrasts. We fitted separate linear mixed models for each facial expression, with ROI and anxiety group as fixed factors and a participant random intercept. We also examined anxiety continuously, included depression as a covariate, and analyzed ratios between ROIs.

For the lecture, these papers give us examples of Bonferroni correction and accounting for repeated measurements. Their main analyses use linear mixed models; Examples 05 and 06 use repeated-measures and mixed-design ANOVA. Both papers assess spectral response detection with one-tailed z-score thresholds, which is a separate method from Example 01's one-sample t-test against zero.

## [9]–[10] Example 06: Epsilon and adjusted F-test calculations

For the complete, balanced two-ROI design, Example 06 creates two views of each participant-condition cell: the average of LOT and ROT, and the ROT-minus-LOT difference. The average view gives Group, Condition, and Group × Condition. The difference view gives Group × ROI, Condition × ROI, and Group × Condition × ROI. A group-adjusted intercept test on each participant's across-condition ROI difference gives the ROI main effect.

Within each view, the script subtracts group-condition means and estimates GG epsilon from the residuals. It adjusts both degrees of freedom for the effects involving condition and calculates upper-tail F probabilities. Group, ROI, and Group × ROI retain their original degrees of freedom. This calculation is specific to the balanced two-ROI teaching design.

**An FPVS paper explicitly documenting this exact decomposition and residual-based implementation was not verified.** References [6]–[7] establish use of GG, but don't verify our calculation or numerical equivalence to the authors' software. The repository's numerical tests compare all seven Example 06 effects with an independent orthonormal-contrast calculation, including F, degrees of freedom, epsilon, p-values, and partial eta-squared. Example 05 is also compared with Statsmodels' repeated-measures ANOVA. These checks validate the supplied synthetic design; they do not reproduce the papers' analyses. The four-test family in Example 03 and the one-sided confidence bound in Example 01 are also teaching choices.

For the lecture, describe [3]–[4] as behavioral uses of the methods within an FPVS paper. For the other entries, state the matching statistical method and the listed differences. This avoids presenting every example as an exact published FPVS analysis when that has not been established.
