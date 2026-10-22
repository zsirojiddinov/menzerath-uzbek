# What the Menzerath–Altmann exponent measures: clauses, morphemes and syllables in Uzbek — supplementary package

Version 1.0.0 · 2026 · Z. Sirojiddinov (ORCID 0000-0002-6249-032X), M. Khakimov (ORCID 0000-0001-6937-800X)

This package accompanies the article *What the Menzerath–Altmann exponent measures: clauses, morphemes and syllables
in Uzbek*. It contains the preregistration, the frozen analysis script and its single run, the post hoc analyses,
all figures, and the token- and clause-level data needed to recompute the main fit table **without any text**.

## Contents

| path | what |
|---|---|
| `prereg/prereg.md` | preregistration (questions Q1–Q5, definitions, fit, bootstrap, verdict criterion §4.4), committed before any y–x computation |
| `prereg/tuzatish_1.md` | amendment 1 (Q3 exclusions), committed before the analysis script was frozen |
| `prereg/inventar.md`, `inventar.json` | pre-analysis inventory of materials (counts only) |
| `code/tahlil.py` | frozen confirmatory analysis (Q1–Q5); produced `results/natija.*` in one run |
| `code/posthoc.py` | post hoc analyses E1–E11 (not confirmatory); produced `results/posthoc.*` |
| `code/rasm_en.py`, `code/rasm_uz.py` | figures (English / Uzbek labels) from the two JSON result files; no computation |
| `code/reproduce_from_data.py` | recomputes the main fit table from `data/` and checks it against `results/natija.json` |
| `code/zenodo_eksport.py` | the script that built this package |
| `results/natija.md`, `natija.json` | confirmatory results (Uzbek-language report; JSON has every number) |
| `results/posthoc.md`, `posthoc.json` | post hoc results |
| `results/figures/en/` | fig1–fig6 (300 dpi, English) |
| `results/figures/uz/` | the same figures with Uzbek labels |
| `results/figures/run/` | diagnostic figures written by `tahlil.py` / `posthoc.py` themselves (Uzbek labels) |
| `data/` | `tokens.csv`, `clauses.csv`, `cells_*.csv`, `DATA_DICTIONARY.md` |
| `MANIFEST.json` | sha256 and source commit of every file |

The working language of the scripts and reports is Uzbek; identifiers such as `qator` (row), `jadval` (table), `hukm`
(verdict), `tor` / `keng` (narrow / broad clause), `bajarildi` / `bajarilmadi` (criterion met / not met) recur.

## Which table and figure comes from where

| item | script | file / key |
|---|---|---|
| Table 1 (treebank cells, three unit definitions) | `tahlil.py` | `natija.json` → `qatorlar` → `Q1 treebank tor`, `Q1 treebank keng`, `Q4b A: treebank V0` → `jadval`; `data/cells_table1.csv` |
| Table 2 (fits: a, b, 95 % interval, verdict) | `tahlil.py` | `natija.json` → `qatorlar` → `fit`, `oraliq`, `hukm`; recomputed by `reproduce_from_data.py` |
| Q4(a), Q4(b), Q4(c) differences | `tahlil.py` | `natija.json` → `Q4a_keng_minus_tor`, `Q4b_A_minus_B`, `Q4c` |
| Q5 random model | `tahlil.py` | `natija.json` → `Q5` |
| Sensitivity rows | `tahlil.py` | `natija.json` → `sezgirlik` |
| Table A1 | `posthoc.py` (E8i) | `posthoc.json` → `E8` → `i`; `data/cells_A1.csv` |
| Tables A2, A3 | `posthoc.py` (E11g) | `posthoc.json` → `E11` → `g`; `data/cells_A2.csv`, `cells_A3.csv` |
| Fig. 1 (Q1) | `rasm_en.py` | `natija.json` |
| Fig. 2 (Q5 / random models, 1 000 replications) | `rasm_en.py` | `posthoc.json` → `E10` → `g` |
| Fig. 3 (Q2), Fig. 4 (Q3), Fig. 5 (Q4b) | `rasm_en.py` | `natija.json` |
| Fig. 6 (part-type decomposition) | `rasm_en.py` | `posthoc.json` → `E7`, `E8` → `b` |

## Reproducing

Environment used for the published run: Python 3.9.6, `numpy==2.0.2`, `scipy==1.13.1`, `matplotlib==3.9.4`.

```
python3 -m venv venv && . venv/bin/activate
pip install numpy==2.0.2 scipy==1.13.1 matplotlib==3.9.4
```

**1. Main fit table from the released data** (standalone):

```
python code/reproduce_from_data.py
```

It rebuilds the observations of seven of the nine main rows (Q1 treebank narrow / broad, Q1 K1 and K2 automatic
units, Q4(b) treebank automatic units, Q2, Q3), the Q4(a)/Q4(b) paired differences and the token exclusion counts from
`data/clauses.csv` and `data/tokens.csv`, runs the frozen `tahlil.qator` (weighted NLS, 1 000-draw bootstrap, seed
20261021, §4.4 verdict) and compares a, b, c, the 95 % intervals, the cells and the verdict with `results/natija.json`;
exit code 0 = all equal. With the versions above the values are bit-identical. The two Q4(c) rows (fewest / most
morphemes) need the alternative analyses of the analyser and are not recomputable from the release; nor are Q5 and the
post hoc results that use word types or sentence text.

**2. Figures from the result files** (standalone): the figure scripts read `natija/` next to themselves.

```
mkdir -p code/natija && cp results/natija.json results/posthoc.json code/natija/
python code/rasm_en.py     # -> code/natija/fig1.png ... fig6.png
python code/rasm_uz.py     # -> code/natija/rasm_uz/*.png
```

**3. Full pipeline** (not runnable from this package alone). The order is

```
python3 analysis/menzerath-1/tahlil.py --db COPY.db     # once
python3 analysis/menzerath-1/posthoc.py --db COPY.db
python3 analysis/menzerath-1/rasm_en.py
python3 analysis/menzerath-1/rasm_uz.py
```

run from the root of the authors' research repository: the scripts need the morphological analyser and its lexicon
database (`--db` is a copy of it, checked by md5), the sentence texts of K1/K2 and of the treebanks, and helper modules of
an earlier study. Those are not distributed here; this package releases their numeric output (`data/`) instead.

### The run-once rule

`tahlil.py` was frozen before it was run: it refuses to start unless its own sha256 and those of `prereg.md` and
`tuzatish_1.md` are recorded in the study manifest, and it stops if its output folder `natija/` already exists — so the
confirmatory analysis can be run exactly once per output folder. Fingerprints of the published run
(`results/natija.json` → `langar`):

| file | sha256 |
|---|---|
| `tahlil.py` | `618d333f287cd3b5e9a4b87fc5f842b853f46cd0e4676b64302d29a2a53f4b4f` |
| `prereg.md` | `6b5e3cc3665737d940163a18708e89e006ef6627b939b1a8b57ab1fa5d3ca56f` |
| `tuzatish_1.md` | `066652538d5e82ca4e583349384e31ca315a4c30d5f5ba6cf8d19d0f5669a08b` |

Order of events (repository commits, 2026-10-21, UTC+5): inventory 13:16 → preregistration 15:10 → amendment 1 15:24 →
script frozen 15:33 → single run 15:44. Everything in `posthoc.*` was planned after the results and is descriptive, not
confirmatory. The analyser lexicon database was the same file before and after the run (md5 `732a97a56205a00c1c28a100275782ce`).

## Note on internal references

`prereg/prereg.md`, `prereg/inventar.md`, `prereg/inventar.json` and `code/tahlil.py` refer to «Heaps paketi» (the Heaps
package), to paths such as `analysis/ijcl-paket/...` and to «maqoladagi (4.2, 4.7)» (equations 4.2 and 4.7 of the
article). These are paths in the authors' private research repository and references to a companion manuscript. The
files are frozen — their sha256 values are recorded above and in the study manifest — and have therefore not been
edited. The companion manuscript will be deposited separately with its own DOI.

## Held-out data

The analysed sentences were checked against the evaluation sets that are held out from the development of the
authors' machine-translation system (sentence hashes and 8-word window hashes; strict and input lists). Matches: K1 0,
K2 0, treebank 0 — nothing was excluded. The package itself contains no sentence text; its files were scanned with the
same filter before release (0 matches).

## Sources and licences

- UD_Uzbek-UT and UD_Uzbek-UzUDT, release 2.18 (Universal Dependencies). Only counts derived from them are released;
  the treebanks are available from UD under their own licences.
- K1 (Uzbek news and scientific-technical sentences) and K2 (Uzbek translation of Tagore): only counts are released.
- Documentation and data: CC BY 4.0 (`LICENSE`). Code in `code/`: MIT (`LICENSE-CODE`).

## Citation

See `CITATION.cff`.
