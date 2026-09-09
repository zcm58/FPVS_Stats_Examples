# Working on these teaching examples

Read [ARCHITECTURE.md](ARCHITECTURE.md) for the project map and [README.txt](README.txt) for student setup instructions. The numbered scripts contain the lecture explanations; [SOURCES.md](SOURCES.md) maps methods to FPVS papers.

- Keep changes small and specific to the request. Preserve the author's manual edits and casual teaching voice.
- Keep the six lessons independently runnable. Avoid shared abstractions or extra error handling for scenarios that cannot occur in the supplied synthetic data.
- Group_A represents adults; Group_B represents adolescents. The conditions are Positive Valence, Negative Valence, and Neutral Angry.
- Preserve participant pairing within conditions and independence between groups. The supplied data contain one occipital ROI; LOT/ROT discussions in the ANOVA lessons describe an extension.
- Keep documented statistical methods distinct from methods actually executed. Verify paper methods before adding citations.
- Do not regenerate the CSV files unless requested. The optional generator overwrites both supplied datasets.
- Keep virtual environments, editor settings, caches, and credentials out of Git.

For changes to calculations, run the affected scripts with the installed dependencies and inspect their results. For explanation-only edits, check syntax and confirm that executable code is unchanged. Before publishing a full project update, run all six scripts. On Windows, an existing project environment can be used with `.venv\Scripts\python.exe`.
