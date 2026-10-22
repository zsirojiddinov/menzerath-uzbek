# -*- coding: utf-8 -*-
"""MENZERATH-1 — recompute the results from the released data only (no text, no analyser, no database).

Usage (from the package root):
    python code/reproduce_from_data.py            # exit 0 = every compared section equals results/ and data/cells_*.csv

Rebuilds every observation from `data/tokens.csv` and `data/clauses.csv` in the order of the analysis and runs the
UNCHANGED functions of `tahlil.py` (fit, bootstrap, §4.4 verdict, B&Č model) and `posthoc.py`.
* natija.json: the body of `tahlil.main` (rows, Q4, Q5, sensitivity) is repeated step by step on the rebuilt observations.
* posthoc.json: the `posthoc.py` section functions are called as they are. Where they read a word, the released counts
  are supplied instead: the token key is `type_id` (word type), and the helpers that turn a word into graphemes /
  morphemes (`tozala_tok`, `morf_grafemalari`, `tahlil.norm`, `tozala`, `tok_toifa`, `morf_chegaralari`, `grafemalar`)
  return the released lengths; `e5_birliklar` returns the clause units of `clauses.csv`; E3 gets the UT sentence numbers.
  The recomputed natija.json (not the published one) is what `posthoc.py` reads.
Each section is reported as exact (bit-identical) or with its largest relative difference (accepted <= 1e-9).
Not recomputable from the release (need sentence text, UD files or repository history): posthoc E8h, E10f, E11h,
E8k `iii_eski`; natija.json `langar` and the held-out / positive-control entries of `materiallar`.
Requires numpy, scipy (README versions for bit-identical results).
"""
import contextlib
import csv
import importlib.util
import json
import math
import sys
import tempfile
from collections import Counter, OrderedDict
from pathlib import Path

import numpy as np

KOD = Path(__file__).resolve().parent
PAKET = KOD.parent
_spec = importlib.util.spec_from_file_location('tahlil', KOD / 'tahlil.py')
T = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(T)
sys.modules['tahlil'] = T
_spec = importlib.util.spec_from_file_location('posthoc', KOD / 'posthoc.py')
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)
P.T = T

TOL = 1e-9
SINF = {'valid': 'yaroqli', 'punctuation': 'tinish', 'digit': 'raqam', 'non_alphabet': 'alifbo', 'apostrophe_only': 'faqat_tutuq'}
TARIF = {'narrow': 'tor', 'broad': 'keng', 'automatic': 'v0'}


def oqi(nom):
    with open(PAKET / 'data' / nom, encoding='utf-8', newline='') as fh:
        return list(csv.DictReader(fh))


def korpus(sid):
    s = sid.split('-')[0]
    return 'treebank' if s in ('UT', 'UzUDT') else s


def sonlar(v):
    return [int(z) for z in v.split(',')] if v else []


class Morf(list):
    """Morfema ro'yxati o'rnida: uzunligi = morfema soni, `mg` — har morfemaning grafema soni (tokens.csv dan)."""

    def __init__(self, mg):
        super().__init__(['m'] * len(mg))
        self.mg = list(mg)


# ---------------------------------------------------------------- materiallar
def klauzalar(C):
    """-> tb (soxta gap yozuvlari: q1_xy uchun so'z/birlik ro'yxatlari), B, root_bosh (posthoc.e5_birliklar shakli), V0 (K1/K2)."""
    G = OrderedDict()
    for r in C:
        G.setdefault(r['sentence_id'], {}).setdefault(TARIF[r['definition']], []).append(
            (int(r['clause_id']), r['clause_type'], r['relation'], int(r['n_words'])))
    tb, B, rb, V0 = [], {'tor': [], 'keng': []}, Counter(), {'K1': OrderedDict(), 'K2': OrderedDict()}
    for sid, D in G.items():
        k = korpus(sid)
        if k != 'treebank':
            V0[k][sid] = D['v0']
            continue
        W = {sum(n for *_, n in u) for u in D.values()}
        if len(W) != 1:
            raise SystemExit(f'{sid}: definitions disagree on the number of words')
        W = W.pop()
        Z = max(sum(n == 0 for *_, n in u) for u in D.values())
        g = {'tb': sid.split('-')[0], 'sent_id': sid.split('-')[1].lstrip('0') if sid.startswith('UT-') else sid,
             'words': ['a'] * W + ['.'] * Z}
        for kalit, u in D.items():
            bir = [c for c, _, _, n in u for _ in range(n)]
            nol = [c for c, _, _, n in u if n == 0]
            g[kalit] = bir + nol + [u[0][0]] * (Z - len(nol))
            if kalit in B:
                kl = [x for x in u if x[3] > 0]
                root = [x for x in u if x[1] == 'main']
                if len(root) != 1:
                    raise SystemExit(f'{sid}: not exactly one main clause')
                r = root[0]
                B[kalit].append({'k': len(kl), 'y': sum(x[3] for x in kl) / len(kl) if kl else None,
                                 'M': r[3] if r[3] > 0 else None, 'ergash': [(x[2], x[3]) for x in kl if x is not r]})
                rb[kalit, r[3] > 0] += 1
        tb.append(g)
    return tb, B, rb, V0


def k_gaplar(Tk, V0):
    """K1/K2 gaplari tahlil.k_birliklar shaklida: so'z o'rnida belgi (so'z — 'a'/'o', faqat tutuq — "'", boshqa — '-'),
    `v0` — unit_id. clauses.csv `automatic` birliklari bilan moslik tekshiriladi."""
    K = {'K1': OrderedDict(), 'K2': OrderedDict()}
    for r in Tk:
        k = korpus(r['sentence_id'])
        if k == 'treebank':
            continue
        g = K[k].setdefault(r['sentence_id'], {'words': [], 'v0': []})
        if r['token_class'] == 'apostrophe_only':
            w = "'"
        elif r['is_word'] == '1':
            w = 'o' if r['ends_o_g_before_apostrophe'] == '1' else 'a'
        else:
            w = '-'
        g['words'].append(w)
        g['v0'].append(int(r['unit_id']))
    for k in K:
        if list(K[k]) != list(V0[k]):
            raise SystemExit(f'{k}: sentences of tokens.csv and clauses.csv differ')
        for sid, g in K[k].items():
            c = Counter(b for w, b in zip(g['words'], g['v0']) if T.sozmi(w))
            if [c[cid] for cid, *_ in V0[k][sid]] != [n for *_, n in V0[k][sid]]:
                raise SystemExit(f'{sid}: unit lengths of tokens.csv and clauses.csv differ')
        K[k] = list(K[k].values())
    return K


def kalit(r):
    if r['token_class'] == 'apostrophe_only':
        return "'"
    return 'T' + r['type_id'] if r['token_class'] == 'valid' else 'X' + r['token_class']


def tokenlar(Tk, tb_sid):
    """-> Tg [(korpus, gap indeksi, kalit)], A, kodlar, gr (kalit -> (segmentli, segmentsiz) soxta grafema ro'yxati)."""
    Tg, A, kodlar, gr, gi, gs = [], {}, {}, {}, {}, Counter()
    for r in Tk:
        k = korpus(r['sentence_id'])
        if k == 'treebank':
            i = tb_sid[r['sentence_id']]
        else:
            if (k, r['sentence_id']) not in gi:
                gi[k, r['sentence_id']] = gs[k]
                gs[k] += 1
            i = gi[k, r['sentence_id']]
        key = kalit(r)
        Tg.append((k, i, key))
        if r['token_class'] != 'valid':
            continue
        st = r['analyzer_status']
        ng, nu, v = int(r['n_graphemes']), int(r['n_graphemes_unsegmented']), int(r['n_syllables'])
        oxiri = ['a'] if r['final_vowel'] == '1' else ['b']
        seg = ['a'] * (v - (oxiri == ['a'])) + ['b'] * (ng - v - (oxiri == ['b'])) + oxiri
        uns = ['a'] * (v - (oxiri == ['a'])) + ['b'] * (nu - v - (oxiri == ['b'])) + oxiri
        if st != 'analysed' and ng != nu:
            raise SystemExit('non-analysed token with boundary-dependent grapheme count')
        rec = {'unk': st == 'unknown', 'teng': st == 'analysed'}
        if st == 'analysed':
            for nom, (n, rl, sl) in (('score', ('n_morphemes', 'root_len', 'suffix_lens')),
                                     ('kam', ('n_morphemes_fewest', 'root_len_fewest', 'suffix_lens_fewest')),
                                     ('kop', ('n_morphemes_most', 'root_len_most', 'suffix_lens_most'))):
                mg = [int(r[rl])] + sonlar(r[sl])
                if len(mg) != int(r[n]) or sum(mg) != ng and nom == 'score':
                    raise SystemExit('morpheme columns inconsistent')
                rec[nom] = Morf(mg)
            kd = [r['pos_code']] + (r['suffix_type_codes'].split(',') if r['suffix_type_codes'] else [])
        else:
            rec['score'], kd = Morf([]), None
        if key in A:
            o = A[key]
            if (o['unk'], o['teng'], o['score'].mg) != (rec['unk'], rec['teng'], rec['score'].mg) or gr[key] != (seg, uns):
                raise SystemExit('one type_id with two different analyses')
            continue
        A[key], gr[key] = rec, (seg, uns)
        if kd is not None:
            kodlar[key] = kd
    return Tg, A, kodlar, gr


# ---------------------------------------------------------------- tahlil.main (Q1–Q5, sezgirlik)
def q2_q3(Tk):
    """tahlil.q2_q3 ning chiqishi tokens.csv ustunlaridan."""
    sanoq = {k: Counter() for k in ('K1', 'K2', 'treebank')}
    q2 = {'x': [], 'y': [], 'korpus': [], 'kam_x': [], 'kam_y': [], 'kop_x': [], 'kop_y': []}
    q2i, q3, q3ng = {'x': [], 'y': []}, {'x': [], 'y': [], 'korpus': []}, {'x': [], 'y': []}
    ozgardi = Counter()
    for r in Tk:
        kor = korpus(r['sentence_id'])
        s = sanoq[kor]
        s['kirish'] += 1
        if r['token_class'] == 'apostrophe_only':
            s['q3_faqat_tutuq'] += 1
            continue
        if r['token_class'] != 'valid':
            s[SINF[r['token_class']]] += 1
            continue
        s['yaroqli'] += 1
        ng, nu, v = int(r['n_graphemes']), int(r['n_graphemes_unsegmented']), int(r['n_syllables'])
        st = r['analyzer_status']
        if st == 'unknown':
            s['q2_noma_lum'] += 1
            q2i['x'].append(1)
            q2i['y'].append(nu)
        elif st == 'mismatch':
            s['q2_yuza_teng_emas'] += 1
        else:
            s['q2_namuna'] += 1
            m = int(r['n_morphemes'])
            q2['x'].append(m)
            q2['y'].append(ng / m)
            q2['korpus'].append(kor)
            q2i['x'].append(m)
            q2i['y'].append(ng / m)
            std = (r['n_morphemes'], r['root_len'], r['suffix_lens'])
            for rejim, suf in (('kam', '_fewest'), ('kop', '_most')):
                mm = int(r['n_morphemes' + suf])
                q2[rejim + '_x'].append(mm)
                q2[rejim + '_y'].append((int(r['root_len' + suf]) + sum(sonlar(r['suffix_lens' + suf]))) / mm)
                ozgardi[rejim] += (r['n_morphemes' + suf], r['root_len' + suf], r['suffix_lens' + suf]) != std
        if ng == 1:
            s['q3_bir_grafema'] += 1
            continue
        if v == 0:
            s['q3_unlisiz'] += 1
            continue
        s['q3_namuna'] += 1
        q3['x'].append(v)
        q3['y'].append(ng / v)
        q3['korpus'].append(kor)
        q3ng['x'].append(v)
        q3ng['y'].append(nu / v)
    return sanoq, q2, q2i, q3, q3ng, ozgardi


def tahlil_qismi(tb, K, Tk):
    """tahlil.main dagi hisob qismi, so'zma-so'z tartibda (materiallar, analizator va yozish o'rniga — ma'lumot)."""
    out = {'materiallar': {'treebank': {'gap': len(tb)}, 'K1': {'gap': len(K['K1'])}, 'K2': {'gap': len(K['K2'])}}}
    Q, xy = {}, {}
    for nom, gaplar, kal in (('Q1 treebank tor', tb, 'tor'), ('Q1 treebank keng', tb, 'keng'),
                             ('Q4b A: treebank V0', tb, 'v0'), ('Q1 K1 VDU', K['K1'], 'v0'),
                             ('Q1 K2 VDU', K['K2'], 'v0')):
        x, y, L, bosh = T.q1_xy(gaplar, kal)
        xy[nom] = (x, y, L)
        Q[nom] = T.qator(x, y, nom)
        Q[nom]['bosh_birlik'] = bosh
        Q[nom]['gap_x_ga_kirmadi'] = len(gaplar) - len(x)
    out['Q4a_keng_minus_tor'] = {'b': T.delta(Q['Q1 treebank keng'], Q['Q1 treebank tor']),
                                 'a': T.delta(Q['Q1 treebank keng'], Q['Q1 treebank tor'], i=0)}
    d = T.delta(Q['Q4b A: treebank V0'], Q['Q1 treebank tor'])
    out['Q4b_A_minus_B'] = {'b': d, 'a': T.delta(Q['Q4b A: treebank V0'], Q['Q1 treebank tor'], i=0),
                            'bashorat_tasdiqlandi': bool(d and d['nuqta'] < 0 and d['oraliq'][1] < 0)}
    sanoq, q2, q2i, q3, q3ng, ozgardi = q2_q3(Tk)
    out['tokenlar'] = {k: dict(v) for k, v in sanoq.items()}
    out['Q4c_ozgargan_token'] = dict(ozgardi)
    Q['Q2 jami (max score)'] = T.qator(q2['x'], q2['y'], 'Q2 jami (max score)')
    Q['Q4c eng kam morfema'] = T.qator(q2['kam_x'], q2['kam_y'], 'Q4c eng kam morfema')
    Q['Q4c eng ko\'p morfema'] = T.qator(q2['kop_x'], q2['kop_y'], 'Q4c eng ko\'p morfema')
    Q['Q3 jami'] = T.qator(q3['x'], q3['y'], 'Q3 jami')
    out['Q4c'] = {}
    for r in ('Q4c eng kam morfema', 'Q4c eng ko\'p morfema'):
        out['Q4c'][r + ' − max score'] = {'b': T.delta(Q[r], Q['Q2 jami (max score)']),
                                           'a': T.delta(Q[r], Q['Q2 jami (max score)'], i=0)}
    bl = [Q[r]['fit'].get('sodda') for r in ('Q2 jami (max score)', 'Q4c eng kam morfema', 'Q4c eng ko\'p morfema')]
    out['Q4c']['ishora_bir_xil'] = (all(isinstance(s, dict) for s in bl)
                                    and len({np.sign(s['p'][1]) for s in bl}) == 1)
    x, y, L = xy['Q1 treebank tor']
    rng5 = np.random.default_rng(T.SEED)
    tas = []
    for _ in range(T.BC_TAKROR):
        kx, ky = T.bc_model(L, rng5)
        r = T.qator(kx, ky, 'B&Č', toliq_boot=False)
        s = r['fit'].get('sodda')
        tas.append({'b': s['p'][1] if isinstance(s, dict) else None, 'hukm': r['hukm']['hukm'],
                    'oraliq_b': r['oraliq']['sodda']['b'] if r['oraliq'].get('sodda') else None})
    bh = Q['Q1 treebank tor']['fit']['sodda']['p'][1]
    bt = [t['b'] for t in tas if t['b'] is not None]
    out['Q5'] = {'b_haqiqiy': bh, 'takror': T.BC_TAKROR, 'muvaffaqiyatli': len(bt),
                 'b_tasodifiy_mediana': float(np.median(bt)), 'b_tasodifiy_2_5_97_5': [float(np.percentile(bt, 2.5)), float(np.percentile(bt, 97.5))],
                 'b_tasodifiy_min_max': [float(min(bt)), float(max(bt))],
                 'ulush_b_tasodifiy_le_b_haqiqiy': sum(b <= bh for b in bt) / len(bt),
                 'ulush_b_tasodifiy_manfiy': sum(b < 0 for b in bt) / len(bt),
                 'mezon_bajarilgan_takror': sum(t['hukm'] == 'bajarildi' for t in tas), 'takrorlar': tas}
    S = {}
    for nom in ('Q1 treebank tor', 'Q1 treebank keng', 'Q1 K1 VDU', 'Q1 K2 VDU', 'Q2 jami (max score)', 'Q3 jami'):
        q = Q[nom]
        if len(q['fit_kataklar']) < 1:
            continue
        oxirgi = q['fit_kataklar'][-1]
        if nom.startswith('Q1'):
            x, y, _ = xy[nom]
        elif nom.startswith('Q2'):
            x, y = q2['x'], q2['y']
        else:
            x, y = q3['x'], q3['y']
        mm = [i for i, v in enumerate(x) if v != oxirgi]
        S[nom + ' · oxirgi katak (x = %d) chiqarilgan' % oxirgi] = T.qator([x[i] for i in mm], [y[i] for i in mm],
                                                                         nom + ' · oxirgi katak chiqarilgan')
    for tbn in ('UT', 'UzUDT'):
        x, y, _, _ = T.q1_xy([g for g in tb if g['tb'] == tbn], 'tor')
        S[f'Q1 {tbn} tor'] = T.qator(x, y, f'Q1 {tbn} tor')
    S['Q2 (i) noma\'lum so\'zlar x = 1'] = T.qator(q2i['x'], q2i['y'], 'Q2 (i) noma\'lum so\'zlar x = 1')
    for k in ('K1', 'K2', 'treebank'):
        m = [i for i, v in enumerate(q2['korpus']) if v == k]
        S[f'Q2 (ii) {k}'] = T.qator([q2['x'][i] for i in m], [q2['y'][i] for i in m], f'Q2 (ii) {k}')
    S['Q3 ng har doim 1'] = T.qator(q3ng['x'], q3ng['y'], 'Q3 ng har doim 1')
    tozalash = lambda q: {k: v for k, v in q.items() if k != '_boot'}          # noqa: E731
    out['qatorlar'] = {k: tozalash(v) for k, v in Q.items()}
    out['sezgirlik'] = {k: tozalash(v) for k, v in S.items()}
    return out, q2, q3


# ---------------------------------------------------------------- posthoc.py bo'limlari
@contextlib.contextmanager
def almashtir(B, rb, A, gr, natija, tb):
    """posthoc.py / tahlil.py dagi so'zni o'qiydigan yordamchilar o'rniga ma'lumotdagi uzunliklar (faqat shu blok ichida)."""
    eski_P = {k: getattr(P, k) for k in ('tozala_tok', 'morf_grafemalari', 'e5_birliklar', 'NATIJA')}
    eski_T = {k: getattr(T, k) for k in ('norm', 'tozala', 'tok_toifa', 'morf_chegaralari', 'grafemalar', 'SUPP')}
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / 'natija.json').write_text(json.dumps(natija, ensure_ascii=False), encoding='utf-8')
        (td / 'data').mkdir()
        (td / 'data' / 'ud_system_output.json').write_text(
            json.dumps({'sentences': [{'sent_id': g['sent_id']} for g in tb]}), encoding='utf-8')

        def tozala_tok(raw):
            if raw == "'":
                return 'faqat_tutuq', None
            return ('yaroqli', raw) if raw[0] == 'T' else (SINF[raw[1:]], None)

        def grafemalar(w, chegaralar=()):
            seg, uns = gr[w]
            return list(seg if isinstance(chegaralar, Morf) or chegaralar else uns)
        P.tozala_tok, P.morf_grafemalari, P.NATIJA = tozala_tok, (lambda w, m: list(m.mg)), td
        P.e5_birliklar = lambda tb_: (B, rb)
        T.norm, T.tozala, T.morf_chegaralari, T.grafemalar, T.SUPP = (lambda s: s), (lambda s: s), (lambda m: m), grafemalar, td
        T.tok_toifa = lambda t: None if t[:1] == 'T' else 'x'
        try:
            yield
        finally:
            for k, v in eski_P.items():
                setattr(P, k, v)
            for k, v in eski_T.items():
                setattr(T, k, v)


def posthoc_qismi(tb, K, B, rb, Tg, A, kodlar, gr, nat, q2, q3):
    Tk = [(k, key) for k, _, key in Tg]
    Q = nat['qatorlar']
    out = {}
    out['E4'] = P.e4(K['K1'])
    with almashtir(B, rb, A, gr, nat, tb):
        out['E1'], _ = P.e1(Tk, A)
        out['E2'] = P.e2(Tk, A)
        obs = out['E2'].pop('_obs')
        out['E3'] = P.e3(tb)
        out['E5'], _ = P.e5(tb)
        out['E6'] = P.e6(obs)
        out['E7'], _ = P.e7(tb, Tk, A, out)
        r = {}
        r['a'] = P.e8a(Tg, A, q2, q3, Q)
        r['b'] = P.e8b(P.qism_massivlari(B, Tk, A), out)
        r['c'] = P.e8c(B, tb, {**Q, 'Q5': nat['Q5']})
        r['d'] = P.e8d(tb, Q, out['E3'])
        r['e'] = P.e8e(tb, q2, q3, Q)
        r['f'] = P.e8f(Q)
        r['g'] = P.e8g(B, Tk, A, kodlar, out)
        r['i'] = P.e8i(Q)
        r['k'] = P.e8k(B, r)
        out['E8'] = r
        out['E10'] = {'a': P.e10a(), 'b': P.e10b(Tg, A, q2, q3, Q, r['a']), 'c': P.e10c(tb, B, out['E3']),
                      'd': P.e10d(Tk, A, kodlar), 'e': P.e10e(Tk, A), 'g': P.e10g(B, tb, r['c'])}
        M = P.qism_massivlari(B, Tk, A)
        X2, _, mg, kor = P._q2_massiv(Tk, A, q2)
        tip = P._tip_massivlari(Tk, A)
        out['E11'] = {'a': P.e11a(M, tip, Q, r['b']), 'b': P.e11b(B, tb, out), 'c': P.e11c(X2, mg, Q),
                      'd': P.e11d(tb, X2, mg, q3), 'e': P.e11e(q2, q3, X2, mg, kor), 'f': P.e11f(),
                      'g': P.e11g(tip, out, Q)}
    return out


# ---------------------------------------------------------------- taqqoslash
def jsonla(v):
    return json.loads(json.dumps(v, ensure_ascii=False, default=lambda o: o.item() if hasattr(o, 'item') else str(o)))


def farq(a, b):
    """-> (aynan, eng katta nisbiy farq, tuzilma mos). NaN = NaN."""
    if isinstance(a, dict) and isinstance(b, dict):
        if a.keys() != b.keys():
            return False, math.inf, False
        r = [farq(a[k], b[k]) for k in a]
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return False, math.inf, False
        r = [farq(u, v) for u, v in zip(a, b)]
    elif isinstance(a, float) or isinstance(b, float):
        if isinstance(a, bool) or isinstance(b, bool) or a is None or b is None:
            return a == b, (0.0 if a == b else math.inf), a == b
        if math.isnan(a) and math.isnan(b):
            return True, 0.0, True
        if a == b:
            return True, 0.0, True
        return False, abs(a - b) / max(1.0, abs(b)), True
    else:
        return a == b, (0.0 if a == b else math.inf), a == b
    return all(x[0] for x in r) if r else True, max([x[1] for x in r] or [0.0]), all(x[2] for x in r) if r else True


def son(v):
    return '' if v is None else repr(float(v)) if isinstance(v, float) else str(v)


def kataklar(nat, ph):
    yn = lambda v: 'yes' if v else 'no'                                         # noqa: E731
    Qd = nat['qatorlar']
    F = {'cells_table1.csv': [['row', 'x', 'n', 'mean_y', 'sd', 'in_fit']] + [
        [qn, c['x'], c['n'], son(c['y']), son(c['sd']), yn(c['fitga'])]
        for nom, qn in (('Q1 treebank tor', 'clause_narrow'), ('Q2 jami (max score)', 'morpheme_standard'), ('Q3 jami', 'syllable'))
        for c in Qd[nom]['jadval']]}
    F['cells_A1.csv'] = [['row', 'x', 'n', 'mean_y', 'sd', 'model_m_x', 'in_fit']] + [
        [qn, c['x'], c['n'], son(c['y']), son(c['sd']), son(c['m']), yn(c['fitga'])]
        for nom, qn in (('Q1 treebank keng', 'treebank_broad'), ('Q1 K1 VDU', 'K1_automatic'), ('Q1 K2 VDU', 'K2_automatic'))
        for c in ph['E8']['i'][nom]['jadval']]
    g = ph['E11']['g']
    F['cells_A2.csv'] = [['x', 'n_types', 'mean_y', 'root_R', 'suffix_S', 'in_fit']] + [
        [c['x'], c['n'], son(c['y']), son(c['R']), son(c['S']), yn(c['fitga'])] for c in g['A2']]
    F['cells_A3.csv'] = [['level', 'x', 'n', 'first_part', 'other_parts', 'mean_y', 'y_pure_mixture', 'observed_minus_pure',
                          'in_fit']] + [
        [lv, c['x'], c['n'], son(c[p]), son(c['S']), son(c['y']), son(c['y_sof']), son(c['farq']), yn(c['fitga'])]
        for lv, key, p in (('clause_narrow', 'A3 klauza tor', 'M'), ('morpheme_standard', 'A3 morfema standart', 'R'))
        for c in g[key]]
    return {k: [[str(z) for z in r] for r in v] for k, v in F.items()}


def main():
    C, Tk = oqi('clauses.csv'), oqi('tokens.csv')
    nat0 = json.loads((PAKET / 'results' / 'natija.json').read_text(encoding='utf-8'))
    ph0 = json.loads((PAKET / 'results' / 'posthoc.json').read_text(encoding='utf-8'))
    tb, B, rb, V0 = klauzalar(C)
    K = k_gaplar(Tk, V0)
    tb_sid = {('UT-%04d' % int(g['sent_id'])) if g['tb'] == 'UT' else g['sent_id']: i for i, g in enumerate(tb)}
    Tg, A, kodlar, gr = tokenlar(Tk, tb_sid)
    nat, q2, q3 = tahlil_qismi(tb, K, Tk)
    nat = jsonla(nat)
    ph = jsonla(posthoc_qismi(tb, K, B, rb, Tg, A, kodlar, gr, nat, q2, q3))

    qatorlar, xato = [], []

    def tekshir(nom, a, b):
        ay, d, tz = farq(a, b)
        ok = ay or (tz and d <= TOL)
        qatorlar.append((nom, 'exact' if ay else (f'max rel. diff {d:.1e}' if tz else 'DIFFERENT')))
        if not ok:
            xato.append(nom)
    for k in ('qatorlar', 'Q4a_keng_minus_tor', 'Q4b_A_minus_B', 'Q4c', 'Q4c_ozgargan_token', 'Q5', 'sezgirlik', 'tokenlar'):
        tekshir(f'natija.json · {k}', nat[k], nat0[k])
    tekshir('natija.json · materiallar (sentence counts)', nat['materiallar'],
            {k: {'gap': v['gap']} for k, v in nat0['materiallar'].items()})
    for k in ('E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7'):
        tekshir(f'posthoc.json · {k}', ph[k], {kk: vv for kk, vv in ph0[k].items() if kk != '_obs'})
    for k in sorted(ph['E8']):
        b = ph0['E8'][k]
        if k == 'k':
            b = {kk: vv for kk, vv in b.items() if kk != 'iii_eski'}
        tekshir(f'posthoc.json · E8{k}', ph['E8'][k], b)
    for e in ('E10', 'E11'):
        for k in sorted(ph[e]):
            tekshir(f'posthoc.json · {e}{k}', ph[e][k], ph0[e][k])
    F = kataklar(nat, ph)
    for nom, rows in F.items():
        with open(PAKET / 'data' / nom, encoding='utf-8', newline='') as fh:
            fayl = list(csv.reader(fh))
        qatorlar.append((f'data/{nom}', 'exact' if fayl == rows else 'DIFFERENT'))
        if fayl != rows:
            xato.append(nom)
    w = max(len(n) for n, _ in qatorlar)
    for n, s in qatorlar:
        print(f'{n:<{w}}  {s}')
    if xato:
        print('MISMATCH:', '; '.join(xato))
        return 1
    print(f'OK — {len(qatorlar)} sections equal results/ and data/cells_*.csv')
    return 0


if __name__ == '__main__':
    sys.exit(main())
