# -*- coding: utf-8 -*-
"""MENZERATH-1 — E13: Zenodo / GitHub qo'shimcha paketi eksporti (HISOB YO'Q — faqat sanoq, nusxa va tekshiruv).

Ishlatish (repo ildizidan):
    python3 analysis/menzerath-1/zenodo_eksport.py --db NUSXA.db [--chiqish ~/menzerath-uzbek]

Chiqish papkasi mavjud bo'lsa TO'XTA. Yoziladi: prereg/, code/, results/ (+ figures/en, figures/uz, figures/run), data/
(tokens.csv, clauses.csv, cells_*.csv, DATA_DICTIONARY.md), README.md, CITATION.cff, .zenodo.json, LICENSE, LICENSE-CODE,
.gitignore, MANIFEST.json. Materiallar va analizator `tahlil.py` / `posthoc.py` funksiyalari orqali (o'sha tartib,
o'sha normallashtirish); kuzatuvlar natija.json bilan AYNAN bo'lishi tekshiriladi. YUZA SATR, LEMMA, O'ZAK MATNI yozilmaydi.
Oxirida tekshiruvlar: (a) data/ da harfli satr yo'q, (b) held-out (gap xeshi + 8-oyna, «qattiq» ∪ «kirish», ID) 0,
(c) maxfiylik (kalit/parol/.env/DB/services/xom matn), (d) hajm. `--db` — `instance/new_phd.db` NUSXASI (md5 teng).
"""
import argparse
import csv
import hashlib
import hmac
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

SIKL = Path(__file__).resolve().parent
REPO = SIKL.parents[1]
NATIJA = SIKL / 'natija'
_spec = importlib.util.spec_from_file_location('posthoc', SIKL / 'posthoc.py')
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)
T = P.T

SARLAVHA = ('What the Menzerath–Altmann exponent measures: clauses, morphemes and syllables in Uzbek — '
            'supplementary package')
VERSIYA = '1.0.0'
GH = 'https://github.com/zsirojiddinov/menzerath-uzbek'
MUALLIFLAR = (('Sirojiddinov', 'Ziyoviddin', '0000-0002-6249-032X'), ('Khakimov', 'Muftakh', '0000-0001-6937-800X'))
TUZ = Path.home() / '.config' / 'menzerath-uzbek' / 'type_id.salt'     # maxfiy tuz — faqat lokal, hech qaysi repoda emas
AFFIL = 'National University of Uzbekistan'
SINF = {'yaroqli': 'valid', 'faqat_tutuq': 'apostrophe_only', 'tinish': 'punctuation', 'raqam': 'digit',
        'alifbo': 'non_alphabet'}
TARIF = {'tor': 'narrow', 'keng': 'broad'}
NUSXA = {'prereg': ('prereg.md', 'tuzatish_1.md', 'inventar.md', 'inventar.json'),
         'code': ('tahlil.py', 'posthoc.py', 'rasm_uz.py', 'rasm_en.py', 'zenodo_eksport.py', 'reproduce_from_data.py'),
         'results': ('natija/natija.md', 'natija/natija.json', 'natija/posthoc.md', 'natija/posthoc.json')}
LUGAT = {'tokens.csv': {'source': {'K1', 'K2', 'UT', 'UzUDT'}, 'token_class': set(SINF.values()),
                        'analyzer_status': {'analysed', 'unknown', 'mismatch', ''}, 'final_vowel': {'0', '1', ''},
                        'is_word': {'0', '1'}, 'ends_o_g_before_apostrophe': {'0', '1', ''}},
         'clauses.csv': {'clause_type': {'main', 'subordinate', 'NA'}, 'definition': {'narrow', 'broad', 'automatic'}},
         'cells_table1.csv': {'row': {'clause_narrow', 'morpheme_standard', 'syllable'}, 'in_fit': {'yes', 'no'}},
         'cells_A1.csv': {'row': {'treebank_broad', 'K1_automatic', 'K2_automatic'}, 'in_fit': {'yes', 'no'}},
         'cells_A2.csv': {'in_fit': {'yes', 'no'}},
         'cells_A3.csv': {'level': {'clause_narrow', 'morpheme_standard'}, 'in_fit': {'yes', 'no'}}}
UD_DEPREL = re.compile(r'[a-z]+')                 # clauses.csv `relation` — UD deprel asosi (boshqaruvchi lug'at)
KOD_RE = re.compile(r'[A-Z][A-Z0-9]*(\+[A-Z][A-Z0-9]*)*')   # analizator element kodlari (C, G, X3, U5, X3+A2 ...)


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*a):
    return subprocess.run(['git', *a], cwd=REPO, capture_output=True, text=True, check=True).stdout.strip()


def son(v):
    return '' if v is None else repr(float(v)) if isinstance(v, float) else str(v)


def yoz_csv(yol, ustunlar, qatorlar):
    with open(yol, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(ustunlar)
        w.writerows(qatorlar)


# ---------------------------------------------------------------- gap ID
def gap_idlari(tb, K):
    """(korpus, indeks) -> 'K1-0001' / 'UT-0001' ...; treebank manbasi UT / UzUDT, har manbada 1 dan."""
    out, c = {}, Counter()
    for k in ('K1', 'K2'):
        for i in range(len(K[k])):
            out[k, i] = f'{k}-{i + 1:04d}'
    for i, g in enumerate(tb):
        c[g['tb']] += 1
        out['treebank', i] = f"{g['tb']}-{c[g['tb']]:04d}"
    return out


# ---------------------------------------------------------------- tokens.csv
TOKEN_USTUN = ['source', 'sentence_id', 'token_id', 'token_class', 'n_graphemes', 'n_syllables', 'n_morphemes', 'root_len',
               'suffix_lens', 'suffix_type_codes', 'analyzer_status', 'pos_code',
               'n_morphemes_fewest', 'root_len_fewest', 'suffix_lens_fewest', 'n_morphemes_most', 'root_len_most',
               'suffix_lens_most', 'type_id', 'n_graphemes_unsegmented', 'final_vowel', 'is_word', 'unit_id',
               'ends_o_g_before_apostrophe']


def type_id(tuz, t):
    """HMAC-SHA256(kalit = maxfiy tuz, xabar = tozalangan yuza shakl) ning birinchi 64 biti, o'nlik son. Tuzsiz xesh YO'Q."""
    if len(tuz) < 32:
        raise SystemExit("TO'XTA — tuz juda qisqa")
    return str(int.from_bytes(hmac.new(tuz, t.encode('utf-8'), hashlib.sha256).digest()[:8], 'big'))


def _qism_ustun(w, m):
    mg = P.morf_grafemalari(w, m)
    return [len(m), mg[0], ','.join(map(str, mg[1:]))]


def tokenlar_qatorlari(Tg, A, kodlar, gid, K, tuz):
    """Tg tartibida. K1/K2: unit_id — V0 birligining gapdagi tartib raqami (clauses.csv `automatic` clause_id bilan bir xil)."""
    rows, pos = [], Counter()
    for korpus, i, raw in Tg:
        pos[korpus, i] += 1
        j = pos[korpus, i] - 1
        sid = gid[korpus, i]
        guruh, t = P.tozala_tok(raw)
        r = [sid.split('-')[0], sid, pos[korpus, i], SINF[guruh]]
        qosh = [int(T.sozmi(raw)), '', '']
        if korpus in ('K1', 'K2'):
            g = K[korpus][i]
            if g['words'][j] != raw:
                raise SystemExit("TO'XTA — K token tartibi so'zlar bilan mos emas")
            qosh[1] = sorted(set(g['v0'])).index(g['v0'][j]) + 1
            if T.sozmi(raw) and j + 1 < len(g['words']) and P.tutuqmi(g['words'][j + 1]):
                qosh[2] = int(T.norm(raw)[-1:] in ('o', 'g'))
        if guruh != 'yaroqli':
            rows.append(r + [''] * 17 + qosh)
            continue
        w, a = T.norm(t), A[t]
        if a['unk']:
            holat, B = 'unknown', []
        elif not a['teng']:
            holat, B = 'mismatch', []
        elif not all(a['score']):
            raise SystemExit("TO'XTA — bo'sh morfemali tahlil (natija.json da 0)")
        else:
            holat, B = 'analysed', T.morf_chegaralari(a['score'])
        gr = T.grafemalar(w, B)
        if holat == 'analysed':
            m = a['score']
            mg = P.morf_grafemalari(w, m)
            kd = kodlar[t]
            if sum(mg) != len(gr) or len(kd) != len(m) or not all(KOD_RE.fullmatch(k) for k in kd):
                raise SystemExit("TO'XTA — morfema grafemalari / kodlari mos emas")
            r += [len(gr), T.unli_soni(gr), len(m), mg[0], ','.join(map(str, mg[1:])), ','.join(kd[1:]), holat, kd[0]]
            r += _qism_ustun(w, a['kam']) + _qism_ustun(w, a['kop'])
        else:
            r += [len(gr), T.unli_soni(gr), '', '', '', '', holat, ''] + [''] * 6
        r += [type_id(tuz, t), len(T.grafemalar(w)), int(gr[-1] in T.UNLI)]
        rows.append(r + qosh)
    return rows


# ---------------------------------------------------------------- clauses.csv
def klauza_qatorlari(tb, K, gid):
    """Treebank: tor/keng (UD daraxtidan, relation = boshqaruvchi deprel asosi) va V0; K1/K2: V0. Har birlik
    (0 so'zli ham) bitta qator; birlik tartibi — birlik indeksi. Proyeksiya tahlil.py dagi bilan AYNAN tekshiriladi."""
    import ud_tools as U
    import iq
    import naqsh_kesh as NK
    Y = json.loads((T.SUPP / 'data' / 'ud_system_output.json').read_text(encoding='utf-8'))['sentences']
    G = {(g['tb'], g['sent_id']): g for t in U.TREEBANK for g in U.load_treebank(t)}
    if len(Y) != len(tb):
        raise SystemExit("TO'XTA — treebank gaplari soni teng emas")
    rows = {'narrow': [], 'broad': [], 'automatic': []}

    def birliklar(sid, words, birlik, tarif, dep=None):
        c = Counter(b for w, b in zip(words, birlik) if T.sozmi(w))
        for n, k in enumerate(sorted(set(birlik)), 1):
            if dep is None:
                tur, rel = 'NA', 'NA'
            else:
                rel = dep[k]
                tur = 'main' if rel == 'root' else 'subordinate'
                if not UD_DEPREL.fullmatch(rel):
                    raise SystemExit("TO'XTA — kutilmagan deprel")
            rows[tarif].append([sid, n, tur, rel, c[k], tarif])

    for i, (rec, y) in enumerate(zip(tb, Y)):
        g = G[(y['tb'], y['sent_id'])]
        sozlar = iq.soz_spanlari(g['text'])
        of = NK.ofsetlar(g['text'], g['tokenlar'])
        x = {t['id']: t for t in g['tokenlar']}
        for variant, kalit in ((T.TOR, 'tor'), (T.KENG, 'keng')):
            Pb = NK.daraxt_bolinishi(g, variant)
            proj, _, _ = iq.proyeksiya(sozlar, g['tokenlar'], of, {t: k for k, (_, ids) in enumerate(Pb) for t in ids})
            if proj != rec[kalit]:
                raise SystemExit(f"TO'XTA — {kalit} proyeksiya tahlil.py dagidan farq qiladi")
            dep = {k: x[h]['deprel'].split(':')[0] for k, (h, _) in enumerate(Pb)}
            if sum(v == 'root' for v in dep.values()) != 1:
                raise SystemExit("TO'XTA — gapda root klauza bitta emas")
            birliklar(gid['treebank', i], rec['words'], proj, TARIF[kalit], dep)
        birliklar(gid['treebank', i], rec['words'], rec['v0'], 'automatic')
    for k in ('K1', 'K2'):
        for i, rec in enumerate(K[k]):
            birliklar(gid[k, i], rec['words'], rec['v0'], 'automatic')
    return rows['narrow'] + rows['broad'] + rows['automatic']


def klauza_nazorat(rows, tb, K, gid):
    """clauses.csv dan qayta qurilgan Q1 kuzatuvlari tahlil.q1_xy bilan AYNAN."""
    for korpus, gaplar, kalit, tarif in (('treebank', tb, 'tor', 'narrow'), ('treebank', tb, 'keng', 'broad'),
                                         ('treebank', tb, 'v0', 'automatic'), ('K1', K['K1'], 'v0', 'automatic'),
                                         ('K2', K['K2'], 'v0', 'automatic')):
        x, y, _, _ = T.q1_xy(gaplar, kalit)
        ids = {gid[korpus, i] for i in range(len(gaplar))}
        G = {}
        for r in rows:
            if r[5] == tarif and r[0] in ids:
                G.setdefault(r[0], []).append(r[4])
        u = [[v for v in G[s] if v > 0] for s in G]
        u = [v for v in u if v]
        if [len(v) for v in u] != x or [sum(v) / len(v) for v in u] != y:
            raise SystemExit(f"TO'XTA — clauses.csv ({korpus}, {tarif}) Q1 kuzatuvlari tahlil.py dan farq qiladi")


# ---------------------------------------------------------------- cells_*.csv
def kataklar(chiq, nat, ph):
    Qd, yn = nat['qatorlar'], (lambda v: 'yes' if v else 'no')                   # noqa: E731
    r1 = [[qn, c['x'], c['n'], son(c['y']), son(c['sd']), yn(c['fitga'])]
          for nom, qn in (('Q1 treebank tor', 'clause_narrow'), ('Q2 jami (max score)', 'morpheme_standard'), ('Q3 jami', 'syllable'))
          for c in Qd[nom]['jadval']]
    yoz_csv(chiq / 'cells_table1.csv', ['row', 'x', 'n', 'mean_y', 'sd', 'in_fit'], r1)
    A1 = ph['E8']['i']
    r = [[qn, c['x'], c['n'], son(c['y']), son(c['sd']), son(c['m']), yn(c['fitga'])]
         for nom, qn in (('Q1 treebank keng', 'treebank_broad'), ('Q1 K1 VDU', 'K1_automatic'), ('Q1 K2 VDU', 'K2_automatic'))
         for c in A1[nom]['jadval']]
    for nom in ('Q1 treebank keng', 'Q1 K1 VDU', 'Q1 K2 VDU'):
        if [{k: v for k, v in c.items() if k != 'm'} for c in A1[nom]['jadval']] != Qd[nom]['jadval']:
            raise SystemExit("TO'XTA — A1 kataklari natija.json dan farq qiladi")
    yoz_csv(chiq / 'cells_A1.csv', ['row', 'x', 'n', 'mean_y', 'sd', 'model_m_x', 'in_fit'], r)
    g = ph['E11']['g']
    yoz_csv(chiq / 'cells_A2.csv', ['x', 'n_types', 'mean_y', 'root_R', 'suffix_S', 'in_fit'],
            [[c['x'], c['n'], son(c['y']), son(c['R']), son(c['S']), yn(c['fitga'])] for c in g['A2']])
    r = [['clause_narrow', c['x'], c['n'], son(c['M']), son(c['S']), son(c['y']), son(c['y_sof']), son(c['farq']),
          yn(c['fitga'])] for c in g['A3 klauza tor']]
    r += [['morpheme_standard', c['x'], c['n'], son(c['R']), son(c['S']), son(c['y']), son(c['y_sof']), son(c['farq']),
           yn(c['fitga'])] for c in g['A3 morfema standart']]
    yoz_csv(chiq / 'cells_A3.csv', ['level', 'x', 'n', 'first_part', 'other_parts', 'mean_y', 'y_pure_mixture',
                                    'observed_minus_pure', 'in_fit'], r)


# ---------------------------------------------------------------- matnlar
DATA_DICTIONARY = """# Data dictionary

All files are UTF-8 CSV with a header row, comma separator and `\\n` line ends. Empty cell = not applicable.
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
"""

README = """# {title}

Version {ver} · 2026 · {authors}

This package accompanies the article *What the Menzerath–Altmann exponent measures: clauses, morphemes and syllables
in Uzbek*. It contains the preregistration, the frozen analysis script and its single run, the post hoc analyses,
all figures, and token- and clause-level data (no text) from which every reported table, row and replication can be
recomputed.

## Contents

| path | what |
|---|---|
| `prereg/prereg.md` | preregistration (questions Q1–Q5, definitions, fit, bootstrap, verdict criterion §4.4), committed before any y–x computation |
| `prereg/tuzatish_1.md` | amendment 1 (Q3 exclusions), committed before the analysis script was frozen |
| `prereg/inventar.md`, `inventar.json` | pre-analysis inventory of materials (counts only) |
| `code/tahlil.py` | frozen confirmatory analysis (Q1–Q5); produced `results/natija.*` in one run |
| `code/posthoc.py` | post hoc analyses E1–E11 (not confirmatory); produced `results/posthoc.*` |
| `code/rasm_en.py`, `code/rasm_uz.py` | figures (English / Uzbek labels) from the two JSON result files; no computation |
| `code/reproduce_from_data.py` | recomputes the results from `data/` with the functions of `tahlil.py` / `posthoc.py` and compares them with `results/` |
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
| Table 1 (cells: Q1 narrow clauses, Q2 morphemes, Q3 syllables) | `tahlil.py` | `natija.json` → `qatorlar` → `Q1 treebank tor`, `Q2 jami (max score)`, `Q3 jami` → `jadval`; `data/cells_table1.csv` |
| Table 2 (fits: a, b, 95 % interval, verdict) | `tahlil.py` | `natija.json` → `qatorlar` → `fit`, `oraliq`, `hukm` |
| Table 3 (Q4 differences: unit definition, segmentation rule) | `tahlil.py` | `natija.json` → `Q4a_keng_minus_tor`, `Q4b_A_minus_B`, `Q4c` |
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
python code/reproduce_from_data.py                 # ~8 min; exit 0 = everything listed below equals results/
mkdir -p code/natija && cp results/natija.json results/posthoc.json code/natija/
python code/rasm_en.py && python code/rasm_uz.py   # -> code/natija/fig*.png, code/natija/rasm_uz/*.png
```

`reproduce_from_data.py` rebuilds every observation from `data/tokens.csv` and `data/clauses.csv` and runs the
**unchanged** functions of `tahlil.py` (fit, bootstrap, §4.4 verdict, random model) and `posthoc.py`; where a
`posthoc.py` function reads a word, the script supplies the released counts in its place (`type_id` for the word type,
the length columns for graphemes and morphemes). Every recomputed section is compared with `results/natija.json` /
`results/posthoc.json` and `data/cells_*.csv` and reported as *exact* (bit-identical) or with its largest relative
difference (accepted up to 1e−9). With the versions above all sections are bit-identical. Seeds: bootstrap and Q5
20261021; cluster bootstrap 20261022; type-preserving model 20261023; pooled-clause reassembly (1 000) 20261024.

## Reproducibility

**Recomputed from this package** (`code/reproduce_from_data.py`):

- `natija.json` → `qatorlar`: all nine rows — Q1 treebank narrow, Q1 treebank broad, Q1 K1 and K2 automatic units,
  Q4(b) treebank automatic units, Q2 (max score), Q4(c) fewest and most morphemes, Q3 — with cells, a, b, c, ΔAIC,
  bootstrap intervals, verdicts, empty-unit counts;
- `Q4a_keng_minus_tor`, `Q4b_A_minus_B`, `Q4c` (both paired differences, the sign criterion), `Q4c_ozgargan_token`;
- `Q5`: 100 pooled-clause reassemblies (seed 20261021), each b, interval and verdict, and the summary;
- `sezgirlik`: all sensitivity rows (last cell removed, UT and UzUDT separately, unknown words as x = 1, Q2 by corpus,
  Q3 with `ng` always one grapheme);
- `tokenlar` (token exclusion counts) and the sentence counts in `materiallar`;
- `posthoc.json`: E1, E2, E3, E4, E5, E6, E7, E8a–g, E8i, E8k, E10a–e, E10g, E11a–g — including the 1 000
  type-preserving and 1 000 pooled-clause replications behind Fig. 2;
- `data/cells_table1.csv`, `cells_A1.csv`, `cells_A2.csv`, `cells_A3.csv`.

**Recomputable only in the authors' original repository** (they need sentence text, UD files or repository history,
which are not distributed):

- `posthoc.json` → `E8h` — alignment of UD tokens with system words (multiword tokens, words split into several UD
  tokens) and a check of the preregistration commit history;
- `posthoc.json` → `E10f` — punctuation inside the source lines of the longest K1/K2 sentences;
- `posthoc.json` → `E11h` — gold UPOS of the token before each clause boundary (and the long-K2-sentence table in the
  same section);
- in `natija.json` → `materiallar`, the held-out exclusion counts (0) and the positive control (re-built narrow units equal
  to the gold units, 1182/1182), and the run fingerprints in `langar`.

**Full pipeline** (original repository). From its root:

```
python3 {sikl}/tahlil.py --db COPY.db     # once
python3 {sikl}/posthoc.py --db COPY.db
python3 {sikl}/rasm_en.py
python3 {sikl}/rasm_uz.py
```

The scripts need the morphological analyser and its lexicon database (`--db` is a copy of it, checked by md5), the
sentence texts of K1/K2 and of the treebanks, and helper modules of an earlier study; this package releases their numeric
output (`data/`) instead.

### The run-once rule

`tahlil.py` was frozen before it was run: it refuses to start unless its own sha256 and those of `prereg.md` and
`tuzatish_1.md` are recorded in the study manifest, and it stops if its output folder `natija/` already exists — so the
confirmatory analysis can be run exactly once per output folder. Fingerprints of the published run
(`results/natija.json` → `langar`):

| file | sha256 |
|---|---|
| `tahlil.py` | `{tahlil}` |
| `prereg.md` | `{prereg}` |
| `tuzatish_1.md` | `{tuz}` |

Order of events (repository commits, 2026-10-21, UTC+5): inventory 13:16 → preregistration 15:10 → amendment 1 15:24 →
script frozen 15:33 → single run 15:44. Everything in `posthoc.*` was planned after the results and is descriptive, not
confirmatory. The analyser lexicon database was the same file before and after the run (md5 `{db}`).

## Note on internal references

`prereg/prereg.md`, `prereg/inventar.md`, `prereg/inventar.json` and `code/tahlil.py` refer to «Heaps paketi» (the Heaps
package), to paths such as `{ichki}` and to «maqoladagi (4.2, 4.7)» (equations 4.2 and 4.7 of the
article). These are paths in the authors' private research repository and references to a companion manuscript. The
files are frozen — their sha256 values are recorded above and in the study manifest — and have therefore not been
edited. The companion manuscript will be deposited separately with its own DOI.

## Held-out data

The analysed sentences were checked against the evaluation sets that are held out from the development of the
authors' machine-translation system (sentence hashes and 8-word window hashes; strict and input lists). Matches: K1 0,
K2 0, treebank 0 — nothing was excluded. The package itself contains no sentence text; its files were scanned with the
same filter before release (0 matches).

## Word-type identifiers

`type_id` in `data/tokens.csv` is only for grouping tokens into word types (Table A2, post hoc E10e, E11): it is a keyed
hash (HMAC-SHA256, first 64 bits) of the cleaned surface form with an undisclosed salt that is not distributed, so the text
cannot be recovered from it; no unsalted hash of any word is used anywhere in the package.

## Sources and licences

- UD_Uzbek-UT and UD_Uzbek-UzUDT, release 2.18 (Universal Dependencies). Only counts derived from them are released;
  the treebanks are available from UD under their own licences.
- K1 (Uzbek news and scientific-technical sentences) and K2 (Uzbek translation of Tagore): only counts are released.
- Documentation and data: CC BY 4.0 (`LICENSE`). Code in `code/`: MIT (`LICENSE-CODE`).

## Citation

See `CITATION.cff`.
"""

MIT = """MIT License

Copyright (c) 2026 Ziyoviddin Sirojiddinov, Muftakh Khakimov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

CC_BY = """Creative Commons Attribution 4.0 International (CC BY 4.0)

Copyright (c) 2026 Ziyoviddin Sirojiddinov, Muftakh Khakimov

All files in this package except those in `code/` (preregistration, documentation, results, figures and data) are
licensed under the Creative Commons Attribution 4.0 International License. The files in `code/` are licensed under
the MIT License (see LICENSE-CODE).

You are free to share (copy and redistribute the material in any medium or format) and adapt (remix, transform, and
build upon the material) for any purpose, even commercially, under the following term: Attribution — you must give
appropriate credit, provide a link to the license, and indicate if changes were made.

Full legal code: https://creativecommons.org/licenses/by/4.0/legalcode
"""

TAVSIF = ('Supplementary package for a preregistered study of the Menzerath–Altmann law in Uzbek at three levels: '
          'sentence–clause–word, word–morpheme–grapheme and word–syllable–grapheme. It contains the preregistration and '
          'its amendment, the frozen analysis script and the results of its single run, post hoc analyses, figures, '
          'and token- and clause-level count data (no text) from two Uzbek corpora and the UD Uzbek treebanks. '
          'The main fit table can be recomputed from the released data with the included script.')
KALITLAR = ['Menzerath–Altmann law', 'Uzbek', 'agglutination', 'preregistration', 'quantitative linguistics']


def citation():
    s = ['cff-version: 1.2.0', 'message: "If you use this package, please cite it as below."', 'type: dataset',
         f'title: "{SARLAVHA}"', f'version: {VERSIYA}', 'authors:']
    for fam, ism, orc in MUALLIFLAR:
        s += [f'  - family-names: {fam}', f'    given-names: {ism}', f'    orcid: "https://orcid.org/{orc}"',
              f'    affiliation: "{AFFIL}"']
    s += ['license:', '  - CC-BY-4.0', '  - MIT', f'repository-code: "{GH}"', 'keywords:'] + [f'  - "{k}"' for k in KALITLAR]
    return '\n'.join(s) + '\n'


def zenodo():
    return {'title': SARLAVHA, 'upload_type': 'dataset', 'description': TAVSIF, 'version': VERSIYA,
            'creators': [{'name': f'{fam}, {ism}', 'orcid': orc, 'affiliation': AFFIL} for fam, ism, orc in MUALLIFLAR],
            'keywords': KALITLAR, 'license': 'cc-by-4.0', 'access_right': 'open'}


# ---------------------------------------------------------------- tekshiruvlar
SIR = re.compile(r'(?i)(api[_-]?key|sec' r'ret|passw(or)?d|token\s*[:=]\s*[\'"]?[0-9A-Za-z_-]{20,}|AIza[0-9A-Za-z_-]{20,}|'
                 r'gh[pousr]_[0-9A-Za-z]{20,}|sk-[0-9A-Za-z]{20,}|BEGIN [A-Z ]*PRIVATE KEY|GEM' r'INI|DATABASE_URL\s*=)')


def type_id_tekshir(tuz, A, tr):
    """type_id: (1) har tip — bitta id, to'qnashuv yo'q; (2) tuzsiz xesh (sha256 / md5 / sha1, tozalangan va
    normallangan shakl, 64-bit o'nlik va hex) birorta id ga teng emas; (3) tokens.csv dagi id lar faqat tuzli xeshdan."""
    turlar = sorted(A)
    ids = {t: type_id(tuz, t) for t in turlar}
    toq = len(set(ids.values())) != len(ids)
    toplam = set(ids.values())
    tuzsiz = 0
    for t in turlar:
        for s in {t, T.norm(t)}:
            for h in (hashlib.sha256, hashlib.md5, hashlib.sha1):
                d = h(s.encode('utf-8')).digest()
                tuzsiz += str(int.from_bytes(d[:8], 'big')) in toplam or d.hex() in toplam or d[:8].hex() in toplam
    i = TOKEN_USTUN.index('type_id')
    faylda = {r[i] for r in tr if r[i] != ''}
    return {'ok': not toq and tuzsiz == 0 and faylda <= toplam, 'tip': len(ids), 'toqnashuv': toq,
            'tuzsiz_xesh_mosligi': tuzsiz, 'fayldagi_id': len(faylda)}


def tuz_paketda(chiq, tuz):
    """Tuz (hex yoki bayt) paketning hech bir faylida yo'q."""
    for p in chiq.rglob('*'):
        if p.is_file() and '.git' not in p.relative_to(chiq).parts:
            b = p.read_bytes()
            if tuz in b or tuz.hex().encode() in b or tuz.hex().upper().encode() in b:
                return True
    return False


def sonmi(v):
    if v == '':
        return True
    try:
        float(v)
        return True
    except ValueError:
        return False


def tekshiruvlar(chiq, gaplar):
    out = {}
    fayllar = sorted(p for p in chiq.rglob('*') if p.is_file() and '.git' not in p.relative_to(chiq).parts)
    matnli = [p for p in fayllar if p.suffix in ('.md', '.json', '.csv', '.py', '.cff', '') or p.name.startswith('.')]
    # (a) data/: boshqaruvchi lug'atdan tashqari harfli satr yo'q
    topildi = Counter()
    for p in sorted((chiq / 'data').glob('*.csv')):
        lug = LUGAT.get(p.name, {})
        with open(p, encoding='utf-8', newline='') as fh:
            for r in csv.DictReader(fh):
                for k, v in r.items():
                    if k in lug:
                        if v not in lug[k]:
                            topildi[p.name, k, 'lug\'atdan tashqari'] += 1
                    elif k == 'relation':
                        if not (v == 'NA' or UD_DEPREL.fullmatch(v)):
                            topildi[p.name, k] += 1
                    elif k in ('suffix_type_codes', 'pos_code'):
                        if v and not all(KOD_RE.fullmatch(c) for c in v.split(',')):
                            topildi[p.name, k] += 1
                    elif k == 'sentence_id':
                        if not re.fullmatch(r'(K1|K2|UT|UzUDT)-\d{4}', v):
                            topildi[p.name, k] += 1
                    elif not all(sonmi(c) for c in v.split(',')):    # erkin ustun: faqat son(lar) yoki bo'sh
                        topildi[p.name, k] += 1
    toks = (chiq / 'data' / 'tokens.csv').read_text(encoding='utf-8').splitlines()
    sarl = toks[0].split(',')
    erkin = [i for i, k in enumerate(sarl) if k not in LUGAT['tokens.csv'] and k != 'sentence_id']
    grep3 = sum(1 for s in toks[1:] for i, v in enumerate(next(csv.reader([s]))) if i in erkin and re.search(r'[a-z]{3,}', v))
    out['a'] = {'ok': not topildi and grep3 == 0, 'buzilish': {'/'.join(k): v for k, v in topildi.items()},
                'tokens_grep_a_z3_erkin_ustunlar': grep3,
                'tokens_lugat_qiymatlari': {k: sorted(v - {''}) for k, v in LUGAT['tokens.csv'].items()}}
    # (b) held-out: har matnli faylning har qatori — gap xeshi (qator/katak/qo'shtirnoq) + 8-oyna + ID, «qattiq» ∪ «kirish»
    import held_out as H
    r, xato = H.royxat_yukla()
    if xato:
        raise SystemExit(f"TO'XTA — held-out ro'yxati: {xato}")
    gap = r['qattiq'][0] | r['kirish'][0]
    oyna = r['qattiq'][1] | r['kirish'][1]
    hb = {}
    for p in matnli:
        qat = p.read_text(encoding='utf-8', errors='replace').splitlines()
        t = H.hunk_tekshir(list(enumerate(qat, 1)), gap, oyna, r['kirish_id'])
        if t:
            hb[str(p.relative_to(chiq))] = len(t)
    out['b'] = {'ok': not hb, 'fayl': len(matnli), 'moslik': hb}
    # (c) maxfiylik
    db_md5 = T.md5(T.DB)
    katta = {}
    for p in fayllar:
        rel = str(p.relative_to(chiq))
        if p.name == '.env' or p.suffix in ('.db', '.sqlite3', '.db-wal', '.db-shm') or rel.startswith('services/') \
                or hashlib.md5(p.read_bytes()).hexdigest() == db_md5:
            katta[rel] = 'taqiqlangan fayl'
    for p in matnli:
        m = SIR.findall(p.read_text(encoding='utf-8', errors='replace'))
        if m:
            katta[str(p.relative_to(chiq))] = f'kalit/parol naqshi {len(m)}'
        s = p.read_text(encoding='utf-8', errors='replace')
        for naqsh in ('/Us' 'ers/', 'kapital' 'sugurta', '@gm' 'ail'):          # bo'lingan — o'zini ushlamasin
            if naqsh in s:
                katta.setdefault(str(p.relative_to(chiq)), f"'{naqsh}'")
    out['c'] = {'ok': not katta, 'topildi': katta}
    # (c2) xom K1/K2 / treebank gap matni: har gapning normallashtirilgan xeshi paket fayllarida yo'q
    gx = {H.gap_xesh(g) for g in gaplar}
    ox = set()
    for g in gaplar:
        ox |= set(H.oyna_xeshlar(H.norm_tok(g)))
    xm = {}
    for p in matnli:
        t = H.hunk_tekshir(list(enumerate(p.read_text(encoding='utf-8', errors='replace').splitlines(), 1)), gx, ox)
        if t:
            xm[str(p.relative_to(chiq))] = len(t)
    out['c']['xom_matn_moslik'] = xm
    out['c']['xom_matn_gaplar'] = len(gx)
    out['c']['ok'] = out['c']['ok'] and not xm
    # (d) hajm
    hajm = {str(p.relative_to(chiq)): p.stat().st_size for p in fayllar}
    out['d'] = {'ok': sum(hajm.values()) < 100 * 2 ** 20 and max(hajm.values()) < 50 * 2 ** 20,
                'jami_bayt': sum(hajm.values()), 'eng_katta': max(hajm.items(), key=lambda kv: kv[1])}
    return out


# ---------------------------------------------------------------- main
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--db', required=True)
    p.add_argument('--chiqish', default=str(Path.home() / 'menzerath-uzbek'))
    p.add_argument('--tuz', default=str(TUZ), help='maxfiy tuz fayli (hex); repo ichida bo\'lsa TO\'XTA')
    a = p.parse_args()
    chiq = Path(a.chiqish).expanduser().resolve()
    if chiq.exists():
        raise SystemExit(f"TO'XTA — {chiq} mavjud")
    if REPO in chiq.parents or chiq == REPO:
        raise SystemExit("TO'XTA — chiqish asosiy repo ish daraxti ichida")
    tuz_yol = Path(a.tuz).expanduser().resolve()
    if not tuz_yol.is_file() or REPO in tuz_yol.parents or chiq in tuz_yol.parents:
        raise SystemExit("TO'XTA — tuz fayli yo'q yoki repo / chiqish ichida")
    tuz = bytes.fromhex(tuz_yol.read_text(encoding='utf-8').strip())
    db0 = T.md5(T.DB)
    if T.md5(a.db) != db0:
        raise SystemExit("TO'XTA — --db nusxasi md5 ishchi DB ga teng emas")
    head = git('rev-parse', 'HEAD')
    manbalar = [SIKL / f for v in NUSXA.values() for f in v] + sorted(NATIJA.rglob('*.png'))
    iflos = git('status', '--porcelain', '--', *[str(m.relative_to(REPO)) for m in manbalar])
    nat = json.loads((NATIJA / 'natija.json').read_text(encoding='utf-8'))
    ph = json.loads((NATIJA / 'posthoc.json').read_text(encoding='utf-8'))

    # --- materiallar va analizator (tahlil.py / posthoc.py bilan bir xil)
    tb, tb_s = T.treebank_birliklar()
    K, k_s = {}, {}
    for k in ('K1', 'K2'):
        K[k], k_s[k] = T.k_birliklar(k)
    Tk = T.tokenlar(tb, K)
    Tg = P.tokenlar_gap(tb, K, Tk)
    turlar = {T.tozala(w) for _, w in Tk}
    turlar = {t for t in turlar if T.tok_toifa(t) is None}
    an = T.Analizator(a.db)
    try:
        A = an.tahlil(turlar)
        kodlar = P.qoshimcha_kodlari(an, A)
    finally:
        an.yop()
    _, q2, _, q3, _, _ = T.q2_q3(Tk, A)
    if T.jadval(q2['x'], q2['y']) != nat['qatorlar']['Q2 jami (max score)']['jadval'] or \
            T.jadval(q3['x'], q3['y']) != nat['qatorlar']['Q3 jami']['jadval']:
        raise SystemExit("TO'XTA — moslik nazorati: Q2/Q3 jadvallari natija.json dan farq qiladi")
    gid = gap_idlari(tb, K)

    # --- yozish
    chiq.mkdir(parents=True)
    for papka, fl in NUSXA.items():
        (chiq / papka).mkdir()
        for f_ in fl:
            shutil.copy2(SIKL / f_, chiq / papka / Path(f_).name)
    rasm = {'en': sorted(NATIJA.glob('fig*.png')), 'uz': sorted((NATIJA / 'rasm_uz').glob('*.png')),
            'run': sorted(NATIJA.glob('rasm_*.png'))}
    for k, fl in rasm.items():
        (chiq / 'results' / 'figures' / k).mkdir(parents=True)
        for f_ in fl:
            shutil.copy2(f_, chiq / 'results' / 'figures' / k / f_.name)
    d = chiq / 'data'
    d.mkdir()
    tr = tokenlar_qatorlari(Tg, A, kodlar, gid, K, tuz)
    yoz_csv(d / 'tokens.csv', TOKEN_USTUN, tr)
    tid = type_id_tekshir(tuz, A, tr)
    kr = klauza_qatorlari(tb, K, gid)
    klauza_nazorat(kr, tb, K, gid)
    yoz_csv(d / 'clauses.csv', ['sentence_id', 'clause_id', 'clause_type', 'relation', 'n_words', 'definition'], kr)
    kataklar(d, nat, ph)
    (d / 'DATA_DICTIONARY.md').write_text(DATA_DICTIONARY, encoding='utf-8')
    L = nat['langar']
    (chiq / 'README.md').write_text(README.format(
        title=SARLAVHA, ver=VERSIYA, authors=', '.join(f'{ism} {fam} (ORCID {orc})' for fam, ism, orc in MUALLIFLAR),
        sikl=SIKL.relative_to(REPO).as_posix(), ichki='/'.join(('analysis', 'ijcl-paket', '...')), tahlil=L['tahlil_sha256'], prereg=L['prereg_sha256'], tuz=L['tuzatish_1_sha256'], db=L['db_md5']), encoding='utf-8')
    (chiq / 'CITATION.cff').write_text(citation(), encoding='utf-8')
    (chiq / '.zenodo.json').write_text(json.dumps(zenodo(), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (chiq / 'LICENSE').write_text(CC_BY, encoding='utf-8')
    (chiq / 'LICENSE-CODE').write_text(MIT, encoding='utf-8')
    (chiq / '.gitignore').write_text('__pycache__/\n*.pyc\n.DS_Store\n', encoding='utf-8')

    # --- MANIFEST
    manba_yol = {}
    for papka, fl in NUSXA.items():
        for f_ in fl:
            manba_yol[f'{papka}/{Path(f_).name}'] = SIKL / f_
    for k, fl in rasm.items():
        for f_ in fl:
            manba_yol[f'results/figures/{k}/{f_.name}'] = f_
    yozuv = []
    for p_ in sorted(x for x in chiq.rglob('*') if x.is_file()):
        rel = str(p_.relative_to(chiq))
        m = manba_yol.get(rel)
        if m is not None:
            src = str(m.relative_to(REPO))
            yozuv.append({'path': rel, 'sha256': sha256(p_), 'bytes': p_.stat().st_size, 'source': src,
                          'source_commit': git('log', '-1', '--format=%h', '--', src)})
        else:
            yozuv.append({'path': rel, 'sha256': sha256(p_), 'bytes': p_.stat().st_size,
                          'source': 'generated by code/zenodo_eksport.py', 'source_commit': head[:7]})
    tek = tekshiruvlar(chiq, [g['text'] for g in tb + K['K1'] + K['K2']])
    tek['e'] = {**tid, 'ok': tid['ok'] and not tuz_paketda(chiq, tuz)}
    man = {'package': SARLAVHA, 'version': VERSIYA, 'export_commit': head[:7],
           'export_tree_clean_for_sources': not iflos, 'analyser_db_md5': db0,
           'materials': {'treebank': tb_s, **k_s},
           'rows': {'tokens.csv': len(tr), 'clauses.csv': len(kr)},
           'checks': {'no_text_in_data': tek['a']['ok'], 'type_id_salted_only': tek['e']['ok'], 'held_out_matches': sum(tek['b']['moslik'].values()),
                      'raw_sentence_matches': sum(tek['c']['xom_matn_moslik'].values()),
                      'total_bytes_excl_manifest': tek['d']['jami_bayt']},
           'files': yozuv}
    (chiq / 'MANIFEST.json').write_text(json.dumps(man, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    if T.md5(T.DB) != db0:
        raise SystemExit("TO'XTA — ishchi DB md5 o'zgardi")
    print(json.dumps({'chiqish': str(chiq), 'export_commit': head[:7], 'manba_iflos': iflos or None,
                      'tokens': len(tr), 'clauses': len(kr), 'manifest_sha256': sha256(chiq / 'MANIFEST.json'),
                      'tekshiruv': tek}, ensure_ascii=False, indent=1, default=str))
    return 0 if all(tek[k]['ok'] for k in 'abcde') and not iflos else 1


if __name__ == '__main__':
    sys.exit(main())
