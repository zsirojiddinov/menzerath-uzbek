# -*- coding: utf-8 -*-
"""MENZERATH-1 — reproduce the main fit table from the released data only (no text, no analyser, no database).

Usage (from the package root):
    python code/reproduce_from_data.py            # exit 0 = every compared value equals results/natija.json

Reads `data/clauses.csv` and `data/tokens.csv`, rebuilds the observations of the nine main rows exactly as
`tahlil.py` does (same order -> same paired bootstrap indices), runs `tahlil.qator` (the frozen fit, bootstrap and
§4.4 verdict) and compares a, b, the 95 % intervals, the cells and the verdict with `results/natija.json`.
Also recomputes Q4(a) / Q4(b) paired differences and the token exclusion counts.
Requires numpy, scipy (same versions as in README for bit-identical intervals).
"""
import csv
import importlib.util
import json
import sys
from collections import Counter, OrderedDict
from pathlib import Path

KOD = Path(__file__).resolve().parent
PAKET = KOD.parent
_spec = importlib.util.spec_from_file_location('tahlil', KOD / 'tahlil.py')
T = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(T)

TOL = 1e-9
Q1_QATORLAR = (('Q1 treebank tor', 'treebank', 'narrow'), ('Q1 treebank keng', 'treebank', 'broad'),
               ('Q4b A: treebank V0', 'treebank', 'automatic'), ('Q1 K1 VDU', 'K1', 'automatic'),
               ('Q1 K2 VDU', 'K2', 'automatic'))
SINF = {'valid': 'yaroqli', 'punctuation': 'tinish', 'digit': 'raqam', 'non_alphabet': 'alifbo'}


def oqi(nom):
    with open(PAKET / 'data' / nom, encoding='utf-8', newline='') as fh:
        return list(csv.DictReader(fh))


def manba(sid):
    s = sid.split('-')[0]
    return 'treebank' if s in ('UT', 'UzUDT') else s


def q1_kuzatuvlar(C, korpus, tarif):
    """Gap tartibida (fayldagi birinchi ko'rinish): x = so'zli klauzalar soni, y = ularning o'rtacha uzunligi."""
    G = OrderedDict()
    for r in C:
        if r['definition'] == tarif and manba(r['sentence_id']) == korpus:
            G.setdefault(r['sentence_id'], []).append(int(r['n_words']))
    x, y = [], []
    for u in G.values():
        u = [v for v in u if v > 0]
        if u:
            x.append(len(u))
            y.append(sum(u) / len(u))
    return x, y


def yaqin(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(yaqin(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(yaqin(u, v) for u, v in zip(a, b))
    if isinstance(a, float) or isinstance(b, float):
        return a is not None and b is not None and abs(a - b) <= TOL * max(1.0, abs(b))
    return a == b


def main():
    nat = json.loads((PAKET / 'results' / 'natija.json').read_text(encoding='utf-8'))
    C, Tk = oqi('clauses.csv'), oqi('tokens.csv')
    Q, xato = {}, []
    for nom, korpus, tarif in Q1_QATORLAR:
        x, y = q1_kuzatuvlar(C, korpus, tarif)
        Q[nom] = T.qator(x, y, nom)
    q2x, q2y, q3x, q3y = [], [], [], []
    sanoq = {k: Counter() for k in ('K1', 'K2', 'treebank')}
    for r in Tk:
        s = sanoq[manba(r['sentence_id'])]
        s['kirish'] += 1
        if r['token_class'] == 'apostrophe_only':
            s['q3_faqat_tutuq'] += 1
            continue
        if r['token_class'] != 'valid':
            s[SINF[r['token_class']]] += 1
            continue
        s['yaroqli'] += 1
        ng, nv = int(r['n_graphemes']), int(r['n_syllables'])
        st = r['analyzer_status']
        s[{'analysed': 'q2_namuna', 'unknown': 'q2_noma_lum', 'mismatch': 'q2_yuza_teng_emas'}[st]] += 1
        if st == 'analysed':
            m = int(r['n_morphemes'])
            q2x.append(m)
            q2y.append(ng / m)
        if ng == 1:
            s['q3_bir_grafema'] += 1
        elif nv == 0:
            s['q3_unlisiz'] += 1
        else:
            s['q3_namuna'] += 1
            q3x.append(nv)
            q3y.append(ng / nv)
    Q['Q2 jami (max score)'] = T.qator(q2x, q2y, 'Q2 jami (max score)')
    Q['Q3 jami'] = T.qator(q3x, q3y, 'Q3 jami')

    print('| row | N | a | b | b 95 % | verdict | equal to natija.json |')
    print('|---|---|---|---|---|---|---|')
    for nom, q in Q.items():
        n = nat['qatorlar'][nom]
        teng = {'N': q['N'] == n['N'], 'jadval': yaqin(q['jadval'], n['jadval']),
                'fit': yaqin(q['fit'], n['fit']), 'oraliq': yaqin(q['oraliq'], n['oraliq']),
                'hukm': yaqin(q['hukm'], n['hukm'])}
        s = q['fit']['sodda']
        ok = all(teng.values())
        if not ok:
            xato.append(f"{nom}: {[k for k, v in teng.items() if not v]}")
        print(f"| {nom} | {q['N']} | {s['p'][0]:.6f} | {s['p'][1]:.6f} | [{q['oraliq']['sodda']['b'][0]:.6f}; "
              f"{q['oraliq']['sodda']['b'][1]:.6f}] | {q['hukm']['hukm']} | {'yes' if ok else 'NO'} |")
    for kalit, q1, q2 in (('Q4a_keng_minus_tor', 'Q1 treebank keng', 'Q1 treebank tor'),
                          ('Q4b_A_minus_B', 'Q4b A: treebank V0', 'Q1 treebank tor')):
        d = {'b': T.delta(Q[q1], Q[q2]), 'a': T.delta(Q[q1], Q[q2], i=0)}
        ok = yaqin(d['b'], nat[kalit]['b']) and yaqin(d['a'], nat[kalit]['a'])
        if not ok:
            xato.append(kalit)
        print(f"{kalit}: delta b = {d['b']['nuqta']:.6f} [{d['b']['oraliq'][0]:.6f}; {d['b']['oraliq'][1]:.6f}] "
              f"— {'equal' if ok else 'DIFFERENT'}")
    for k, c in sanoq.items():
        ok = dict(c) == {kk: v for kk, v in nat['tokenlar'][k].items() if v}
        if not ok:
            xato.append(f'token counts {k}')
        print(f"token counts {k}: {'equal' if ok else 'DIFFERENT'}")
    if xato:
        print('MISMATCH:', '; '.join(xato))
        return 1
    print('OK — all compared values equal results/natija.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
