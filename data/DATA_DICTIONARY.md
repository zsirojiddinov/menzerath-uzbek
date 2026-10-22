# Data dictionary

All files are UTF-8 CSV with a header row, comma separator and `\n` line ends. Empty cell = not applicable.
**No surface form, lemma or root text is released**: every column is a count, a length, an identifier, a keyed hash or a
closed-vocabulary code. Floats are written with full precision (Python `repr`).

Sentence identifiers are `<source>-<n>` with `n` counted from 1 inside each source, in the order used by `code/tahlil.py`
(K1/K2: corpus order; UT/UzUDT: order of the 1 182 treebank sentences in the analysis, UzUDT s130/s132 duplicates
removed). `UT-<n>` is UD_Uzbek-UT `sent_id` n (sentences 1–250 news, 251–500 fiction — used by post hoc E3); UzUDT
numbers are package-internal. The same `sentence_id` is used in `tokens.csv` and `clauses.csv`; row order in both files
is the order of observations in the analysis (which fixes the bootstrap draws).

## tokens.csv — one row per token (K1, K2: corpus tokens = words of the sentence; UT, UzUDT: UD tokens without PUNCT)

| column | type | definition |
|---|---|---|
| source | K1 / K2 / UT / UzUDT | corpus (K1 news / scientific-technical Uzbek; K2 Uzbek translation of Tagore; UT and UzUDT — UD treebanks r2.18) |
| sentence_id | string | see above |
| token_id | int | position of the token in its sentence, from 1 |
| token_class | valid / apostrophe_only / punctuation / digit / non_alphabet | prereg §2 and tuzatish_1: `apostrophe_only` = token consisting only of apostrophe marks (checked before cleaning; excluded from Q2 and Q3); after cleaning (lower case, apostrophes unified to `'`, edge punctuation stripped) `punctuation` = nothing left, `digit` = contains a digit, `non_alphabet` = contains a character outside the Uzbek Latin alphabet; `valid` = everything else. Measurement columns are filled only for `valid` tokens |
| n_graphemes | int | graphemes of the normalised word (hyphens removed; `sh`, `ch`, `o'`, `g'` one grapheme; `ng` one grapheme unless a morpheme boundary of the max(score) analysis falls between `n` and `g`; non-analysed tokens: no boundaries) |
| n_syllables | int | vowel graphemes (a, e, i, o, u, o') = syllables (Q3 x) |
| n_morphemes | int | morphemes in the max(score) analysis (Q2 x); `analysed` only |
| root_len | int | graphemes in the root (first morpheme); `analysed` only |
| suffix_lens | comma list of int | graphemes of each suffix, left to right; empty for a bare root |
| suffix_type_codes | comma list of codes | analyser element code of each suffix, aligned with `suffix_lens` (e.g. `X3` case, `X` plural, `X2` possessive, `U5` person — see `code/posthoc.py`, `QOSHIMCHA_TURI`); a composite suffix carries its component codes joined by `+` (e.g. `X3+A2`) |
| analyzer_status | analysed / unknown / mismatch | `analysed` — the analysis concatenates to the surface word (Q2 sample); `unknown` — root not identified; `mismatch` — analysis does not reproduce the surface form (excluded from Q2) |
| pos_code | code | analyser code of the root element (e.g. `C` noun, `G` verb); `analysed` only |
| n_morphemes_fewest, root_len_fewest, suffix_lens_fewest | int, int, comma list | Q4(c) «fewest morphemes» selection rule: the same three quantities for the candidate analysis with the fewest morphemes that reproduces the surface form (= max(score) analysis when there is no other candidate); `analysed` only |
| n_morphemes_most, root_len_most, suffix_lens_most | int, int, comma list | the same for the «most morphemes» rule |
| type_id | decimal int | word-type identifier: tokens with the same cleaned surface form share it. First 64 bits of HMAC-SHA256 keyed with an undisclosed salt held only by the authors (not distributed); **the text cannot be recovered from it** and no unsalted hash is used. For grouping types only (Table A2, post hoc E10e, E11) |
| n_graphemes_unsegmented | int | graphemes when `ng` is always one grapheme (no morpheme boundaries) — sensitivity row «Q3 ng har doim 1» |
| final_vowel | 0 / 1 | 1 if the last grapheme (as counted in `n_graphemes`) is a vowel (post hoc E6: open / closed one-syllable words) |
| is_word | 0 / 1 | token contains at least one letter or digit (the Q1 word criterion) |
| unit_id | int | K1/K2 only: the automatic unit (V0) of the token = `clause_id` of the `automatic` row in `clauses.csv` |
| ends_o_g_before_apostrophe | 0 / 1 | K1/K2 only, filled for a word immediately followed by an `apostrophe_only` token: 1 if the word ends in `o` or `g` (post hoc E4) |

Derived quantities: Q2 y = n_graphemes / n_morphemes (analysed tokens); n_graphemes = root_len + Σ suffix_lens (and the
same identity for the fewest / most columns). Q3 sample = valid tokens with n_graphemes > 1 and n_syllables > 0;
Q3 y = n_graphemes / n_syllables.

## clauses.csv — one row per unit (clause or automatic unit), including units with 0 words

| column | type | definition |
|---|---|---|
| sentence_id | string | see above |
| clause_id | int | unit index in the sentence, from 1 |
| clause_type | main / subordinate / NA | `main` = the unit headed by the UD `root`; `NA` for automatic units |
| relation | UD deprel / NA | base deprel (subtype removed) of the unit head: root, advcl, ccomp, conj, parataxis, csubj, xcomp, acl ...; `NA` for automatic units |
| n_words | int | words of the unit that contain at least one letter or digit; units with 0 words are not part of x (Q1) |
| definition | narrow / broad / automatic | `narrow` — gold clause, clause heads `root, ccomp, advcl, csubj, parataxis` and predicate-linking `conj` (`xcomp`, `acl` not clauses); `broad` — the same plus `xcomp`, `acl`; `automatic` — verb-delimited unit V0 (cut after every maximal verb chain); treebank and K1/K2 |

Q1 x = number of units with n_words > 0 in a sentence; y = their mean n_words. Treebank words are whitespace tokens of
the sentence text with edge punctuation removed (system words of the analysis, not UD tokens).

## cells_*.csv — published table cells (recomputed from the files above by `code/reproduce_from_data.py`)

- `cells_table1.csv` — Table 1: cells of the three main series — `clause_narrow` (Q1, treebank, gold narrow clauses),
  `morpheme_standard` (Q2, max(score) analysis), `syllable` (Q3): x, n, mean y, SD, used in fit (n ≥ 30).
- `cells_A1.csv` — Table A1: broad treebank clauses, K1 and K2 automatic units; `model_m_x` = a·x^b of the simple model.
- `cells_A2.csv` — Table A2: Q2 by word types (`n_types` distinct analysed word types, grouped by `type_id`), mean y,
  mean root length R(x) and mean suffix length S(x).
- `cells_A3.csv` — Table A3: part-type decomposition (post hoc E7). `clause_narrow`: `first_part` = main clause M(k),
  `other_parts` = subordinate clause S(k), `mean_y` = y(k); `morpheme_standard`: `first_part` = root R(x), `other_parts` =
  suffix S(x), `mean_y` = y(x); `y_pure_mixture` = [first(1) + (x − 1)·other(2)]/x; `observed_minus_pure` = mean_y − y_pure_mixture.
