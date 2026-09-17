# Working on these teaching examples

Read [ARCHITECTURE.md](ARCHITECTURE.md) for the project map and [README.txt](README.txt) for student setup instructions. The numbered scripts contain the lecture explanations; [SOURCES.md](SOURCES.md) maps methods to FPVS papers.

- Keep changes small and specific to the request. Preserve the author's manual edits and casual teaching voice.
- Keep the six lessons independently runnable. Avoid shared abstractions or extra error handling for scenarios that cannot occur in the supplied synthetic data.
- Group_A represents adults; Group_B represents adolescents. The conditions are Positive Valence, Negative Valence, and Neutral Angry.
- Preserve participant pairing across conditions and ROIs, and independence between groups. Examples 01-04 use the original occipital data; Examples 05-06 use the separate LOT/ROT dataset.
- Keep documented statistical methods distinct from methods actually executed. Verify paper methods before adding citations.
- Do not regenerate the CSV files unless requested. `extras/make_synthetic_data.py` overwrites the two original occipital files; `extras/make_multi_roi_data.py` overwrites only the LOT/ROT file.
- Keep virtual environments, editor settings, caches, and credentials out of Git.

For changes to calculations, run the affected scripts with the installed dependencies and inspect their results. For explanation-only edits, check syntax and confirm that executable code is unchanged. Before publishing a full project update, run all six scripts. On Windows, an existing project environment can be used with `.venv\Scripts\python.exe`.

For changes to the ANOVAs or LOT/ROT data, also run `python -m unittest discover -s tests -v`. Example 06's decomposition is specific to the complete, balanced two-group, two-ROI design; do not treat it as a general factorial-ANOVA implementation.
