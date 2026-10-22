# Data dictionary

All files are UTF-8 CSV with a header row, comma separator and `\n` line ends. Empty cell = not applicable.
**No surface form, lemma or root text is released**: every column is a count, a length, an identifier or a closed-vocabulary
code. Floats are written with full precision (Python `repr`).

Sentence identifiers are `<source>-<n>` with `n` counted from 1 inside each source, in the order used by `code/tahlil.py`
(K1/K2: corpus order; UT/UzUDT: order of the 1 182 treebank sentences in the analysis, UzUDT s130/s132 duplicates
removed). They are package-internal and are **not** UD `sent_id`s. The same `sentence_id` is used in `tokens.csv` and
`clauses.csv`; row order in both files is the order of observations in the analysis (which fixes the bootstrap draws).

## tokens.csv — one row per token (K1, K2: corpus tokens; UT, UzUDT: UD tokens without PUNCT)

| column | type | definition |
|---|---|---|
| source | K1 / K2 / UT / UzUDT | corpus (K1 news / scientific-technical Uzbek; K2 Uzbek translation of Tagore; UT and UzUDT — UD treebanks r2.18) |
| sentence_id | string | see above |
| token_id | int | position of the token in its sentence, from 1 |
| token_class | valid / apostrophe_only / punctuation / digit / non_alphabet | prereg §2 and tuzatish_1: `apostrophe_only` = token consisting only of apostrophe marks (checked before cleaning; excluded from Q2 and Q3); after cleaning (lower case, apostrophes unified to `'`, edge punctuation stripped) `punctuation` = nothing left, `digit` = contains a digit, `non_alphabet` = contains a character outside the Uzbek Latin alphabet; `valid` = everything else. Columns below are filled only for `valid` tokens |
| n_graphemes | int | number of graphemes of the normalised word (hyphens removed; `sh`, `ch`, `o'`, `g'` one grapheme; `ng` one grapheme unless a morpheme boundary of the chosen analysis falls between `n` and `g` — for non-analysed tokens no boundaries) |
| n_syllables | int | number of vowel graphemes (a, e, i, o, u, o') = syllables (Q3 x) |
| n_morphemes | int | number of morphemes in the max(score) analysis (Q2 x); `analysed` tokens only |
| root_len | int | graphemes in the root (first morpheme); `analysed` only |
| suffix_lens | comma list of int | graphemes of each suffix, left to right; empty for a bare root |
| suffix_type_codes | comma list of codes | analyser element code of each suffix, aligned with `suffix_lens` (e.g. `X3` case, `X` plural, `X2` possessive, `U5` person — see `code/posthoc.py`, `QOSHIMCHA_TURI`); a composite suffix carries its component codes joined by `+` (e.g. `X3+A2`) |
| analyzer_status | analysed / unknown / mismatch | `analysed` — the analysis concatenates to the surface word (Q2 sample); `unknown` — root not identified; `mismatch` — analysis does not reproduce the surface form (excluded from Q2) |
| pos_code | code | analyser code of the root element (e.g. `C` noun, `G` verb); `analysed` only |

Derived quantities: Q2 y = n_graphemes / n_morphemes (analysed tokens); n_graphemes = root_len + Σ suffix_lens.
Q3 sample = valid tokens with n_graphemes > 1 and n_syllables > 0; Q3 y = n_graphemes / n_syllables.

## clauses.csv — one row per unit (clause or automatic unit), including units with 0 words

| column | type | definition |
|---|---|---|
| sentence_id | string | see above |
| clause_id | int | unit index in the sentence, from 1 |
| clause_type | main / subordinate / NA | `main` = the unit headed by the UD `root`; `NA` for automatic units |
| relation | UD deprel / NA | base deprel (subtype removed) of the unit head: root, advcl, ccomp, conj, parataxis, csubj, xcomp, acl ...; `NA` for automatic units |
| n_words | int | words of the unit that contain at least one letter or digit (punctuation-only words not counted); units with 0 words are not part of x (Q1) |
| definition | narrow / broad / automatic | `narrow` — gold clause, clause heads `root, ccomp, advcl, csubj, parataxis` and predicate-linking `conj` (`xcomp`, `acl` not clauses); `broad` — the same plus `xcomp`, `acl`; `automatic` — verb-delimited unit V0 (cut after every maximal verb chain); treebank and K1/K2 |

Q1 x = number of units with n_words > 0 in a sentence; y = their mean n_words. Words are whitespace tokens of the
sentence text with edge punctuation removed (treebank: system words of the analysis, not UD tokens).

## cells_*.csv — published table cells (copied from results/natija.json and results/posthoc.json)

- `cells_table1.csv` — Table 1: treebank Q1 cells for the three unit definitions (x, n, mean y, SD, used in fit = n ≥ 30).
- `cells_A1.csv` — Table A1: broad treebank, K1 and K2 automatic units; `model_m_x` = a·x^b of the simple model.
- `cells_A2.csv` — Table A2: Q2 by word types (`n_types` distinct analysed word forms), mean y, mean root length R(x) and
  mean suffix length S(x). Not recomputable from `tokens.csv` (types are not identified in the release).
- `cells_A3.csv` — Table A3: part-type decomposition (E7). `first_part` = main clause M(k) or root R(x); `other_parts` =
  subordinate clause S(k) or suffix S(x); `y_pure_mixture` = [first(1) + (x − 1)·other(2)]/x; `observed_minus_pure` = mean_y − y_pure_mixture.
