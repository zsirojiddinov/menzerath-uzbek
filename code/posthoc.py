# -*- coding: utf-8 -*-
"""MENZERATH-1 — POST HOC — prereg'da yo'q, natijadan keyin rejalashtirilgan, tasdiqlovchi emas.

Ishlatish (repo ildizidan):
    python3 analysis/menzerath-1/posthoc.py --db NUSXA.db     # -> natija/posthoc.md, posthoc.json, rasm_e1.png, rasm_e2.png

Bu skript `tahlil.py` ni O'ZGARTIRMAYDI va qayta yurgizmaydi: undan faqat funksiyalar import qilinadi (materiallar,
normallashtirish, grafema, analizator, `qator`). Natijalar tavsifiy; prereg hukmlari o'zgarmaydi.

E1  Q2 ajratish: har x uchun o'rtacha o'zak va qo'shimcha uzunligi (grafema); «doimiy R, S» aralashma modeli
    y(x) = S + (R − S)/x, R = ȳ(1), S = 2·ȳ(2) − ȳ(1) (x = 1 va x = 2 dan aniq o'tadi); kuzatilgan − bashorat,
    bootstrap 1 000 (token, seed 20261021). Uchala tanlash qoidasi.
E2  Q3 ajratish: Q2 namunasi (tahlil qilingan, yuzaga teng) vs noma'lum vs yuza teng emas; korpus bo'yicha.
E3  Q1 treebank: UT vs UzUDT Δb (mustaqil bootstrap); janr belgisi (UzUDT da yo'q; UT da sent_id 1–250 yangilik,
    251–500 badiiy — README).
E4  Q1 K1 VDU: faqat tutuq belgisidan iborat tokenlar so'z sifatida sanalganmi; qo'shni tokenlar tavsifi;
    qo'shimcha: tutuq bilan bo'lingan so'zlar birlashtirilgan qayta hisob.
POST HOC 2 (qo'shimcha): E1 ga R(x), S(x) bootstrap oraliqlari; E5 Q1 treebank bosh (root) vs ergash klauza, aralashma
    [M + (k−1)·S]/k, ergash klauza deprel bo'yicha; E6 Q3 faqat Q2 namunasida (fit, mezon) + 1 bo'g'inli yopiq/ochiq.
POST HOC 3: E7 qism turi ichidagi ko'rsatkichlar — M(k), S(k) (klauza) va R(x), S(x) (morfema) ga a·x^b, «sof aralashma»
    y_sof = [M(1) + (k−1)·S(2)]/k, bitta taqqoslov jadvali.
POST HOC 4 (E8): a — Q2/Q3 klasterli (gap) bootstrap; b — sof aralashma tayanch sezgirligi; c — turlarni saqlovchi
    tasodifiy model + B&Č 1 000 takror; d — n-chegara va UzUDT/UT uch katak; e — vaznsiz NLS; f — ΔAIC; g — ikkinchi
    darajali aralashma (deprel, qo'shimcha turi); h — uch aniqlik; i — ilova A1 jadvali; k — E8c/E8b (iii) nomuvofiqligi.
E10: a — AIC formulasi; b — klaster diagnostikasi (ICC, token-klaster nazorati); c — UT/UzUDT ajratish; d — o'zak R(x) ot/fe'l;
    e — Q2 tiplar bo'yicha; f — K1/K2 eng katta x gaplari (faqat sonlar); g — 2-rasm uchun takror b qiymatlari.
POST HOC 5 (E11): a — giperbola y = β + α/x; b — mezon nol modellar ostida; c — morfema nol modeli; d — η² (m, x);
    e — manba bo'yicha; f — xato chiziqlari birligi; g — A2, A3 jadvallari; h — K2 uzun gaplar, chegara to'liqligi yuqori chegarasi.
Matn chop etilmaydi va yozilmaydi — faqat sonlar.
"""
import argparse
import hashlib
import importlib.util
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

SIKL = Path(__file__).resolve().parent
REPO = SIKL.parents[1]
NATIJA = SIKL / 'natija'
_spec = importlib.util.spec_from_file_location('tahlil', SIKL / 'tahlil.py')
T = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(T)

SEED, BOOT, NMIN = T.SEED, T.BOOT, T.NMIN
QOIDALAR = (('score', 'max(score)'), ('kam', 'eng kam morfema'), ('kop', "eng ko'p morfema"))


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def f(v, r=3):
    return T.f(v, r)


def morf_grafemalari(w, morflar):
    """Har morfemaning grafema soni (grafema boshlangan morfemaga yoziladi; ng qoidasi T.grafemalar dagidek)."""
    B = T.morf_chegaralari(morflar)
    boshlar = [0] + B
    out, i = [0] * len(morflar), 0
    for g in T.grafemalar(w, B):
        k = max(j for j, b in enumerate(boshlar) if b <= i)
        out[k] += 1
        i += len(g)
    return out


def tozala_tok(raw):
    """-> (guruh, w) — tahlil.q2_q3 dagi tartib: faqat tutuq / tinish / raqam / alifbo / yaroqli."""
    n = T.norm(raw).strip()
    if n and set(n) <= {"'"}:
        return 'faqat_tutuq', None
    t = T.tozala(raw)
    sabab = T.tok_toifa(t)
    return (sabab, None) if sabab else ('yaroqli', t)


# ---------------------------------------------------------------- E1
def e1(Tk, A):
    out, rasm = {}, {}
    for kod, nom in QOIDALAR:
        X, Y, R, S, Sn = [], [], [], [], []
        for _, raw in Tk:
            g, t = tozala_tok(raw)
            if g != 'yaroqli':
                continue
            a = A[t]
            if a['unk'] or not a['teng'] or not all(a['score']):
                continue
            m = a[kod]
            w = T.norm(t)
            mg = morf_grafemalari(w, m)
            X.append(len(m))
            Y.append(sum(mg) / len(m))
            R.append(mg[0])
            S.append(sum(mg[1:]))
            Sn.append(len(m) - 1)
        X, Y, R, S, Sn = (np.array(v, dtype=float) for v in (X, Y, R, S, Sn))
        X = X.astype(int)
        xs = sorted(set(X.tolist()))
        jad = []
        for x in xs:
            m = X == x
            jad.append({'x': x, 'n': int(m.sum()), 'y': float(Y[m].mean()), 'ozak': float(R[m].mean()),
                        'qoshimcha': float(S[m].sum() / Sn[m].sum()) if Sn[m].sum() else None,
                        'fitga': bool(m.sum() >= NMIN)})
        kat = [r['x'] for r in jad if r['fitga']]

        def hisob(idx):
            L = max(xs) + 1
            nn = np.bincount(X[idx], minlength=L)
            ss = np.bincount(X[idx], weights=Y[idx], minlength=L)
            yb = np.divide(ss, nn, out=np.full(len(nn), np.nan), where=nn > 0)
            Rx = np.divide(np.bincount(X[idx], weights=R[idx], minlength=L), nn, out=np.full(L, np.nan), where=nn > 0)
            sn = np.bincount(X[idx], weights=Sn[idx], minlength=L)
            Sx = np.divide(np.bincount(X[idx], weights=S[idx], minlength=L), sn, out=np.full(L, np.nan), where=sn > 0)
            Rr, Ss = yb[1], 2 * yb[2] - yb[1]
            return yb, Rr, Ss, Rx, Sx
        yb, R0, S0, _, _ = hisob(np.arange(len(X)))
        rng = np.random.default_rng(SEED)
        D = defaultdict(list)
        RS, RX, SX = [], [], []
        for _ in range(BOOT):
            idx = rng.integers(0, len(X), len(X))
            ybb, Rb, Sb, Rx, Sx = hisob(idx)
            RS.append((Rb, Sb))
            RX.append(Rx)
            SX.append(Sx)
            for x in kat:
                D[x].append(ybb[x] - (Sb + (Rb - Sb) / x))
        RX, SX = np.array(RX), np.array(SX)
        for r in jad:
            x = r['x']
            r['aralashma'] = float(S0 + (R0 - S0) / x)
            r['farq'] = r['y'] - r['aralashma']
            if x in D and x > 2:
                d = np.array(D[x])
                r['farq_95'] = [float(np.nanpercentile(d, 2.5)), float(np.nanpercentile(d, 97.5))]
            if r['fitga']:                                       # post hoc 2: R(x), S(x) oraliqlari (o'sha takrorlar)
                r['ozak_95'] = [float(np.nanpercentile(RX[:, x], 2.5)), float(np.nanpercentile(RX[:, x], 97.5))]
                if x > 1:
                    r['qoshimcha_95'] = [float(np.nanpercentile(SX[:, x], 2.5)), float(np.nanpercentile(SX[:, x], 97.5))]
        RS = np.array(RS)
        out[nom] = {'N': int(len(X)), 'R': float(R0), 'S': float(S0),
                    'R_95': [float(np.percentile(RS[:, 0], 2.5)), float(np.percentile(RS[:, 0], 97.5))],
                    'S_95': [float(np.percentile(RS[:, 1], 2.5)), float(np.percentile(RS[:, 1], 97.5))],
                    'jadval': jad}
        rasm[nom] = jad
    return out, rasm


# ---------------------------------------------------------------- E2
def e2(Tk, A):
    """Q3 kuzatuvlari guruh bo'yicha (tahlil.q2_q3 bilan bir xil Q3 qoidasi)."""
    obs = []
    for korpus, raw in Tk:
        g, t = tozala_tok(raw)
        if g != 'yaroqli':
            continue
        a = A[t]
        w = T.norm(t)
        if a['unk']:
            guruh, B = "noma'lum", []
        elif not a['teng'] or not all(a['score']):
            guruh, B = 'yuza teng emas', []
        else:
            guruh, B = 'Q2 namunasi', T.morf_chegaralari(a['score'])
        gr = T.grafemalar(w, B)
        if len(gr) == 1:
            continue
        v = T.unli_soni(gr)
        if v == 0:
            continue
        obs.append((korpus, guruh, v, len(gr) / v, gr[-1] not in T.UNLI))
    out = {}
    for korpus in ('jami', 'K1', 'K2', 'treebank'):
        bo = {}
        for guruh in ('Q2 namunasi', "noma'lum", 'yuza teng emas', 'hammasi'):
            sel = [(x, y) for k, gg, x, y, _ in obs if (korpus == 'jami' or k == korpus) and (guruh == 'hammasi' or gg == guruh)]
            c = defaultdict(list)
            for x, y in sel:
                c[x].append(y)
            bo[guruh] = [{'x': x, 'n': len(v), 'y': float(np.mean(v))} for x, v in sorted(c.items())]
        out[korpus] = bo
    # x >= 7 tarkibi
    yuq = Counter(gg for k, gg, x, y, _ in obs if x >= 7)
    out['x_ge_7_tarkib'] = dict(yuq)
    out['N'] = len(obs)
    out['_obs'] = obs
    return out


# ---------------------------------------------------------------- E3
def e3(tb):
    Y = json.loads((T.SUPP / 'data' / 'ud_system_output.json').read_text(encoding='utf-8'))['sentences']
    if len(Y) != len(tb):
        raise SystemExit("TO'XTA — E3: treebank gaplari ud_system_output bilan teng emas (held-out chiqargan)")
    for g, y in zip(tb, Y):
        g['sent_id'] = y['sent_id']
    Q = {}
    for nom, sel in (('UT', lambda g: g['tb'] == 'UT'), ('UzUDT', lambda g: g['tb'] == 'UzUDT'),
                     ('UT yangilik (1–250)', lambda g: g['tb'] == 'UT' and int(g['sent_id']) <= 250),
                     ('UT badiiy (251–500)', lambda g: g['tb'] == 'UT' and int(g['sent_id']) > 250)):
        x, y, _, _ = T.q1_xy([g for g in tb if sel(g)], 'tor')
        Q[nom] = T.qator(x, y, f'Q1 {nom} tor')

    def mustaqil(q1, q2):
        b1 = [p[1] if p is not None else None for p in q1['_boot']['sodda']]
        b2 = [p[1] if p is not None else None for p in q2['_boot']['sodda']]
        d = [a - b for a, b in zip(b1, b2) if a is not None and b is not None]
        s1, s2 = q1['fit'].get('sodda'), q2['fit'].get('sodda')
        if not (isinstance(s1, dict) and isinstance(s2, dict)) or not d:
            return None
        return {'nuqta': s1['p'][1] - s2['p'][1], 'oraliq': [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))],
                'takror': len(d)}
    return {'qatorlar': {k: {kk: vv for kk, vv in v.items() if kk != '_boot'} for k, v in Q.items()},
            'UT_minus_UzUDT': mustaqil(Q['UT'], Q['UzUDT']),
            'yangilik_minus_badiiy': mustaqil(Q['UT yangilik (1–250)'], Q['UT badiiy (251–500)']),
            'uzudt_janr_belgisi': "yo'q (sent_id s1…s684, izoh qatorlari faqat sent_id va text; README: «fiction academic»)"}


# ---------------------------------------------------------------- E4
def tutuqmi(w):
    n = T.norm(w).strip()
    return bool(n) and set(n) <= {"'"}


def e4(K1):
    jami = gaplar = sozmi = 0
    oldin_og = oldin_soz = keyin_soz = 0
    for g in K1:
        w = g['words']
        bor = False
        for i, t in enumerate(w):
            if not tutuqmi(t):
                continue
            jami += 1
            bor = True
            sozmi += T.sozmi(t)
            if i > 0 and T.sozmi(w[i - 1]):
                oldin_soz += 1
                oldin_og += T.norm(w[i - 1])[-1:] in ('o', 'g')
            if i + 1 < len(w) and T.sozmi(w[i + 1]):
                keyin_soz += 1
        gaplar += bor
    asl = T.q1_xy(K1, 'v0')
    q_asl = T.qator(asl[0], asl[1], 'Q1 K1 VDU (asl)')
    # (a) tutuq tokenlarisiz — so'z sanog'iga kirmagan bo'lsa natija aynan
    K1a = [{**g, 'words': [w for w in g['words'] if not tutuqmi(w)],
            'v0': [b for w, b in zip(g['words'], g['v0']) if not tutuqmi(w)]} for g in K1]
    xa = T.q1_xy(K1a, 'v0')
    q_a = T.qator(xa[0], xa[1], 'Q1 K1 VDU (tutuq tokenlarisiz)')
    # (b) qo'shimcha: so'z + tutuq + so'z -> bitta so'z (oldingi so'zning birligida)
    K1b, birlash = [], 0
    for g in K1:
        w, b = g['words'], g['v0']
        nw, nb, i = [], [], 0
        while i < len(w):
            if (tutuqmi(w[i]) and nw and T.sozmi(nw[-1]) and i + 1 < len(w) and T.sozmi(w[i + 1])):
                nw[-1] = nw[-1] + "'" + w[i + 1]
                birlash += 1
                i += 2
                continue
            nw.append(w[i])
            nb.append(b[i])
            i += 1
        K1b.append({**g, 'words': nw, 'v0': nb})
    xb = T.q1_xy(K1b, 'v0')
    q_b = T.qator(xb[0], xb[1], "Q1 K1 VDU (tutuq bilan bo'lingan so'zlar birlashtirilgan)")
    tozala = lambda q: {k: v for k, v in q.items() if k != '_boot'}  # noqa: E731
    return {'tutuq_token': jami, 'gap': gaplar, 'sozmi_true': sozmi, 'oldin_soz': oldin_soz, 'oldin_o_g': oldin_og,
            'keyin_soz': keyin_soz, 'birlashtirildi': birlash,
            'asl': tozala(q_asl), 'tutuqsiz': tozala(q_a), 'birlashtirilgan': tozala(q_b),
            'tutuqsiz_aynan': q_asl['jadval'] == q_a['jadval']}


# ---------------------------------------------------------------- E5 (post hoc 2)
def e5_birliklar(tb):
    """Har gap, har ta'rif: klauza uzunliklari (PUNCT siz), bosh (root) klauza, ergash klauzalar deprel bilan.
    Proyeksiya tahlil.py dagidek; tb dagi tor/keng bilan aynan bo'lishi tekshiriladi."""
    import ud_tools as U
    import iq
    import naqsh_kesh as NK
    Y = json.loads((T.SUPP / 'data' / 'ud_system_output.json').read_text(encoding='utf-8'))['sentences']
    G = {(g['tb'], g['sent_id']): g for t in U.TREEBANK for g in U.load_treebank(t)}
    if len(Y) != len(tb):
        raise SystemExit("TO'XTA — E5: treebank gaplari soni teng emas")
    out = {'tor': [], 'keng': []}
    root_bosh = Counter()
    for rec, y in zip(tb, Y):
        g = G[(y['tb'], y['sent_id'])]
        x = {t['id']: t for t in g['tokenlar']}
        sozlar = iq.soz_spanlari(g['text'])
        of = NK.ofsetlar(g['text'], g['tokenlar'])
        for variant, kalit in ((T.TOR, 'tor'), (T.KENG, 'keng')):
            P = NK.daraxt_bolinishi(g, variant)
            proj, _, _ = iq.proyeksiya(sozlar, g['tokenlar'], of, {t: k for k, (_, ids) in enumerate(P) for t in ids})
            if proj != rec[kalit]:
                raise SystemExit(f"TO'XTA — E5: {kalit} proyeksiya tahlil.py dagidan farq qiladi")
            c = Counter(b for w, b in zip(rec['words'], proj) if T.sozmi(w))
            dep = {k: x[h]['deprel'].split(':')[0] for k, (h, _) in enumerate(P)}
            root = [k for k, d in dep.items() if d == 'root']
            if len(root) != 1:
                raise SystemExit("TO'XTA — E5: gapda root klauza bitta emas")
            r = root[0]
            kl = sorted(c)
            out[kalit].append({'k': len(kl), 'y': sum(c.values()) / len(kl) if kl else None,
                               'M': c[r] if r in c else None,
                               'ergash': [(dep[k], c[k]) for k in kl if k != r]})
            root_bosh[kalit, r in c] += 1
    return out, root_bosh


def e5(tb):
    B, rb = e5_birliklar(tb)
    out, rasm = {}, {}
    for kalit, R in B.items():
        # Q1 bilan moslik (x, y aynan)
        qx, qy, _, _ = T.q1_xy(tb, kalit)
        if [r['k'] for r in R if r['k']] != qx or [r['y'] for r in R if r['k']] != qy:
            raise SystemExit(f"TO'XTA — E5 {kalit}: k, y Q1 dan farq qiladi")
        R = [r for r in R if r['k'] and r['M'] is not None]
        K = np.array([r['k'] for r in R])
        Yv = np.array([r['y'] for r in R], dtype=float)
        M = np.array([r['M'] for r in R], dtype=float)
        S = np.array([np.mean([l for _, l in r['ergash']]) if r['ergash'] else np.nan for r in R], dtype=float)
        ks = sorted(set(K.tolist()))
        L = max(ks) + 1

        def hisob(idx):
            nn = np.bincount(K[idx], minlength=L)
            yb = np.divide(np.bincount(K[idx], weights=Yv[idx], minlength=L), nn, out=np.full(L, np.nan), where=nn > 0)
            Mb = np.divide(np.bincount(K[idx], weights=M[idx], minlength=L), nn, out=np.full(L, np.nan), where=nn > 0)
            sm = ~np.isnan(S[idx])
            ns = np.bincount(K[idx][sm], minlength=L)
            Sb = np.divide(np.bincount(K[idx][sm], weights=S[idx][sm], minlength=L), ns, out=np.full(L, np.nan), where=ns > 0)
            m0, s0 = yb[1], 2 * yb[2] - yb[1]
            return yb, Mb, Sb, m0, s0
        yb, Mb, Sb, m0, s0 = hisob(np.arange(len(K)))
        rng = np.random.default_rng(SEED)
        BB = {'M': [], 'S': [], 'farq': [], 'm0': [], 's0': []}
        for _ in range(BOOT):
            idx = rng.integers(0, len(K), len(K))
            y2, M2, S2, a2, b2 = hisob(idx)
            BB['M'].append(M2)
            BB['S'].append(S2)
            BB['farq'].append(y2 - (a2 + (np.arange(L) - 1) * b2) / np.maximum(np.arange(L), 1))
            BB['m0'].append(a2)
            BB['s0'].append(b2)
        BB = {k: np.array(v) for k, v in BB.items()}
        ci = lambda a: [float(np.nanpercentile(a, 2.5)), float(np.nanpercentile(a, 97.5))]  # noqa: E731
        jad = []
        for k in ks:
            n = int((K == k).sum())
            r = {'k': k, 'n': n, 'y': float(yb[k]), 'M': float(Mb[k]), 'S': None if np.isnan(Sb[k]) else float(Sb[k]),
                 'aralashma': float((m0 + (k - 1) * s0) / k), 'fitga': n >= NMIN}
            r['farq'] = r['y'] - r['aralashma']
            if r['fitga']:
                r['M_95'] = ci(BB['M'][:, k])
                if k > 1:
                    r['S_95'] = ci(BB['S'][:, k])
                if k >= 3:
                    r['farq_95'] = ci(BB['farq'][:, k])
            jad.append(r)
        erg = defaultdict(list)
        for r in R:
            for d, l in r['ergash']:
                erg[d].append(l)
        jami_erg = sum(len(v) for v in erg.values())
        out[kalit] = {'N': len(R), 'root_bosh_klauza_bosh_qolgan_gap': rb[kalit, False],
                      'M0': float(m0), 'S0': float(s0), 'M0_95': ci(BB['m0']), 'S0_95': ci(BB['s0']), 'jadval': jad,
                      'bosh_klauza_ortacha': float(M.mean()), 'bosh_klauza_sd': float(M.std(ddof=1)),
                      'ergash_tur': [{'deprel': d, 'n': len(v), 'ulush': len(v) / jami_erg, 'ortacha': float(np.mean(v)),
                                      'sd': float(np.std(v, ddof=1)) if len(v) > 1 else None}
                                     for d, v in sorted(erg.items(), key=lambda z: -len(z[1]))]}
        rasm[kalit] = jad
    return out, rasm


# ---------------------------------------------------------------- E6 (post hoc 2)
def e6(obs):
    x = [o[2] for o in obs if o[1] == 'Q2 namunasi']
    y = [o[3] for o in obs if o[1] == 'Q2 namunasi']
    q = T.qator(x, y, 'E6 Q3 · faqat Q2 namunasi (post hoc)')
    q = {k: v for k, v in q.items() if k != '_boot'}
    bir = {}
    for korpus in ('jami', 'K1', 'K2', 'treebank'):
        for guruh in ('Q2 namunasi', "noma'lum", 'yuza teng emas', 'hammasi'):
            sel = [(o[3], o[4]) for o in obs if o[2] == 1 and (korpus == 'jami' or o[0] == korpus)
                   and (guruh == 'hammasi' or o[1] == guruh)]
            if not sel:
                continue
            yop = [yy for yy, z in sel if z]
            och = [yy for yy, z in sel if not z]
            bir[f'{korpus} · {guruh}'] = {'n': len(sel), 'yopiq': len(yop), 'yopiq_ulush': len(yop) / len(sel),
                                         'y_yopiq': float(np.mean(yop)) if yop else None,
                                         'y_ochiq': float(np.mean(och)) if och else None}
    return {'qator': q, 'bir_bogin': bir}


def rasm_e5(R, yol):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(11, 4))
    for ax, (nom, jad) in zip(axs, R.items()):
        J = [r for r in jad if r['fitga']]
        kk = [r['k'] for r in J]
        ax.plot(kk, [r['y'] for r in J], 'o-', color='#1f4e79', label='kuzatilgan ȳ')
        ax.plot(kk, [r['aralashma'] for r in J], 's--', color='#c0392b', label='aralashma [M + (k−1)·S]/k')
        ax.errorbar(kk, [r['M'] for r in J], yerr=[[r['M'] - r['M_95'][0] for r in J], [r['M_95'][1] - r['M'] for r in J]],
                    fmt='^:', color='#27864a', capsize=3, label='bosh klauza M(k)')
        J2 = [r for r in J if 'S_95' in r]
        ax.errorbar([r['k'] for r in J2], [r['S'] for r in J2],
                    yerr=[[r['S'] - r['S_95'][0] for r in J2], [r['S_95'][1] - r['S'] for r in J2]],
                    fmt='v:', color='#8e6c00', capsize=3, label='ergash klauza S(k)')
        for r in J:
            if 'farq_95' in r:
                lo, hi = r['farq_95']
                ax.vlines(r['k'], r['aralashma'] + lo, r['aralashma'] + hi, color='#c0392b', alpha=.35, lw=6)
        ax.set_title(f'Q1 treebank · {nom}', fontsize=10)
        ax.set_xlabel('k = klauza soni')
        ax.set_ylabel("so'z")
        ax.grid(alpha=.3)
        ax.legend(fontsize=7)
    fig.suptitle('E5 (POST HOC) — Q1 ajratish: bosh va ergash klauza; qizil ustun: kuzatilgan − aralashma, 95 % (n ≥ 30, k ≥ 3)',
                 fontsize=10)
    fig.tight_layout()
    fig.savefig(yol, dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------- E7 (post hoc 3)
def _b(x, ybar, n):
    """a·x^b (n-vaznli NLS, tahlil.fit) -> (a, b) yoki None."""
    ok = [i for i in range(len(x)) if n[i] > 0 and np.isfinite(ybar[i])]
    if len(ok) < 3:
        return None
    r = T.fit(np.array(x, float)[ok], np.array(ybar, float)[ok], np.array(n, float)[ok]).get('sodda')
    return tuple(r['p']) if isinstance(r, dict) else None


def _ci(v):
    v = [z for z in v if z is not None and np.isfinite(z)]
    return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] if v else None


def _qism(X, Y, P, Q, Qn, nom_p, nom_q):
    """X — birlik soni (k yoki x); Y — kuzatuv y; P — bosh qism uzunligi (M yoki R); Q, Qn — ergash/qo'shimcha yig'indisi va
    soni. Kataklar n ≥ 30 (asl namuna). Bootstrap SEED bilan kuzatuv darajasida."""
    xs = sorted(set(X.tolist()))
    kat = [x for x in xs if (X == x).sum() >= NMIN]
    L = max(xs) + 1

    def hisob(idx):
        nn = np.bincount(X[idx], minlength=L).astype(float)
        dv = lambda w, d: np.divide(np.bincount(X[idx], weights=w[idx], minlength=L), d, out=np.full(L, np.nan),  # noqa: E731
                                    where=d > 0)
        yb, pb = dv(Y, nn), dv(P, nn)
        qn = np.bincount(X[idx], weights=Qn[idx], minlength=L)
        qb = dv(Q, qn)
        sof = np.array([(pb[1] + (x - 1) * qb[2]) / x if x >= 1 else np.nan for x in range(L)])
        kp = [x for x in kat]
        kq = [x for x in kat if x >= 2]
        r = {'yb': yb, 'pb': pb, 'qb': qb, 'sof': sof, 'nn': nn,
             'b_p': _b(kp, pb[kp], nn[kp]), 'b_q': _b(kq, qb[kq], nn[kq]), 'b_sof': _b(kp, sof[kp], nn[kp])}
        return r
    a0 = hisob(np.arange(len(X)))
    rng = np.random.default_rng(SEED)
    BB = defaultdict(list)
    for _ in range(BOOT):
        r = hisob(rng.integers(0, len(X), len(X)))
        for k in ('b_p', 'b_q', 'b_sof'):
            BB[k].append(r[k][1] if r[k] else None)
        BB['farq'].append(r['yb'] - r['sof'])
    F = np.array(BB['farq'])
    jad = []
    for x in xs:
        rr = {'x': x, 'n': int(a0['nn'][x]), 'y': float(a0['yb'][x]), nom_p: float(a0['pb'][x]),
              nom_q: None if np.isnan(a0['qb'][x]) else float(a0['qb'][x]), 'y_sof': float(a0['sof'][x]), 'fitga': x in kat}
        rr['farq'] = rr['y'] - rr['y_sof']
        if x in kat and x >= 3:
            rr['farq_95'] = _ci(F[:, x])
        jad.append(rr)
    nat = lambda k: ({'a': a0[k][0], 'b': a0[k][1], 'b_95': _ci(BB[k]),  # noqa: E731
                      'yaqinlashmagan': sum(v is None for v in BB[k])} if a0[k] else None)
    return {'kataklar': kat, 'b_' + nom_p: nat('b_p'), 'b_' + nom_q: nat('b_q'), 'b_sof': nat('b_sof'), 'jadval': jad}


def e7(tb, Tk, A, out):
    nat = json.loads((NATIJA / 'natija.json').read_text(encoding='utf-8'))['qatorlar']
    umumiy = lambda k: {'b': nat[k]['fit']['sodda']['p'][1], 'b_95': nat[k]['oraliq']['sodda']['b']}  # noqa: E731
    res, rasm = {'klauza': {}, 'morfema': {}}, {}
    B, _ = e5_birliklar(tb)
    for kalit, qq in (('tor', 'Q1 treebank tor'), ('keng', 'Q1 treebank keng')):
        R = [r for r in B[kalit] if r['k'] and r['M'] is not None]
        X = np.array([r['k'] for r in R])
        Y = np.array([r['y'] for r in R], float)
        P = np.array([r['M'] for r in R], float)
        Q = np.array([np.mean([l for _, l in r['ergash']]) if r['ergash'] else 0.0 for r in R], float)
        Qn = np.array([1.0 if r['ergash'] else 0.0 for r in R])
        q = _qism(X, Y, P, Q, Qn, 'M', 'S')
        q['umumiy'] = umumiy(qq)
        res['klauza'][kalit] = q
        if kalit == 'tor':
            rasm['klauza'] = q
    for (kod, nom), qq in zip(QOIDALAR, ('Q2 jami (max score)', 'Q4c eng kam morfema', "Q4c eng ko'p morfema")):
        X, Y, P, Q, Qn = [], [], [], [], []
        for _, raw in Tk:
            g, t = tozala_tok(raw)
            if g != 'yaroqli':
                continue
            a = A[t]
            if a['unk'] or not a['teng'] or not all(a['score']):
                continue
            m = a[kod]
            mg = morf_grafemalari(T.norm(t), m)
            X.append(len(m))
            Y.append(sum(mg) / len(m))
            P.append(mg[0])
            Q.append(sum(mg[1:]))
            Qn.append(len(m) - 1)
        X = np.array(X)
        q = _qism(X, *(np.array(v, float) for v in (Y, P, Q, Qn)), 'R', 'S')
        if q['kataklar'] != list(range(1, 6)):
            q['qayd'] = f"kataklar {q['kataklar']} (prompt: x = 1…5)"
        q['umumiy'] = umumiy(qq)
        # E1 bilan moslik: R(x), S(x) va ȳ aynan
        e1j = {r['x']: r for r in out['E1'][nom]['jadval']}
        for r in q['jadval']:
            if abs(r['R'] - e1j[r['x']]['ozak']) > 1e-12 or abs(r['y'] - e1j[r['x']]['y']) > 1e-12:
                raise SystemExit("TO'XTA — E7 morfema: E1 jadvali bilan mos emas")
        res['morfema'][nom] = q
        if kod == 'score':
            rasm['morfema'] = q
    # E5 bilan moslik (klauza M(k), ȳ)
    for kalit in ('tor', 'keng'):
        e5j = {r['k']: r for r in out['E5'][kalit]['jadval']}
        for r in res['klauza'][kalit]['jadval']:
            if abs(r['M'] - e5j[r['x']]['M']) > 1e-12 or abs(r['y'] - e5j[r['x']]['y']) > 1e-12:
                raise SystemExit("TO'XTA — E7 klauza: E5 jadvali bilan mos emas")
    return res, rasm


def e7_md(o):
    E = o['E7']

    def bci(d):
        if not d:
            return '—'
        c = d.get('b_95')
        return f"{f(d['b'])} [{f(c[0])}; {f(c[1])}]" if c else f(d['b'])
    s = ['## E7 (post hoc 3) — qism turi ichidagi ko\'rsatkichlar', '',
         'Har qism uchun a·x^b (n-vaznli NLS, n ≥ 30 kataklar; bosh qism x = 1… , ergash/qo\'shimcha x = 2…). '
         '«Sof aralashma»: y_sof(x) = [P(1) + (x − 1)·S(2)]/x, P(1) = M(1) yoki R(1), S(2) — kuzatilgan o\'rtachalar; '
         'b_sof — y_sof ga o\'sha kataklarda fit. 95 % — bootstrap (klauza: gap, morfema: token; 1 000, seed 20261021). '
         'Umumiy b — prereg natijasi (natija.json).', '',
         '### (c) Taqqoslov jadvali', '',
         '| daraja | umumiy b (prereg) [95 %] | b_M / b_R [95 %] | b_S [95 %] | b_sof (sof aralashma) [95 %] |',
         '|---|---|---|---|---|']
    for kalit, q in E['klauza'].items():
        s.append(f"| Q1 klauza · {kalit} | {bci(q['umumiy'])} | {bci(q['b_M'])} | {bci(q['b_S'])} | {bci(q['b_sof'])} |")
    for nom, q in E['morfema'].items():
        s.append(f"| Q2 morfema · {nom} | {bci(q['umumiy'])} | {bci(q['b_R'])} | {bci(q['b_S'])} | {bci(q['b_sof'])} |")
    s.append('')
    yq = [f"{d} {k}: {q[b]['yaqinlashmagan']}" for d, grp in (('klauza', E['klauza']), ('morfema', E['morfema']))
          for k, q in grp.items() for b in (('b_M', 'b_S', 'b_sof') if d == 'klauza' else ('b_R', 'b_S', 'b_sof'))
          if q.get(b) and q[b]['yaqinlashmagan']]
    s += [f"Bootstrap yaqinlashmagan fitlar: {', '.join(yq) if yq else 'yo' + chr(39) + 'q'}.", '']
    s += ['### (a) Klauza (treebank)', '']
    for kalit, q in E['klauza'].items():
        s += [f"**{kalit}** — kataklar {q['kataklar']}", '',
              '| k | n | M(k) | S(k) | kuzatilgan ȳ | y_sof | farq | 95 % (farq) |', '|---|---|---|---|---|---|---|---|']
        for r in q['jadval']:
            c = f"[{f(r['farq_95'][0])}; {f(r['farq_95'][1])}]" if 'farq_95' in r else '—'
            s.append(f"| {r['x']} | {r['n']} | {f(r['M'])} | {f(r['S'])} | {f(r['y'])} | {f(r['y_sof'])} | {f(r['farq'])} | {c} |")
        s.append('')
    s += ['### (b) Morfema (Q2 namunasi)', '']
    for nom, q in E['morfema'].items():
        s += [f"**{nom}** — kataklar {q['kataklar']}" + (f" · {q['qayd']}" if q.get('qayd') else ''), '',
              '| x | n | R(x) | S(x) | kuzatilgan ȳ | y_sof | farq | 95 % (farq) |', '|---|---|---|---|---|---|---|---|']
        for r in q['jadval']:
            c = f"[{f(r['farq_95'][0])}; {f(r['farq_95'][1])}]" if 'farq_95' in r else '—'
            s.append(f"| {r['x']} | {r['n']} | {f(r['R'])} | {f(r['S'])} | {f(r['y'])} | {f(r['y_sof'])} | {f(r['farq'])} | {c} |")
        s.append('')
    return s


def rasm_e7(R, yol):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(11, 4))
    for ax, (nom, q, p, xl, yl) in zip(axs, (('klauza · treebank tor', R['klauza'], 'M', 'k = klauza soni', "so'z"),
                                              ('morfema · max(score)', R['morfema'], 'R', 'x = morfema soni', 'grafema'))):
        J = [r for r in q['jadval'] if r['fitga']]
        xx = [r['x'] for r in J]
        ax.plot(xx, [r['y'] for r in J], 'o-', color='#1f4e79', label='kuzatilgan ȳ')
        ax.plot(xx, [r['y_sof'] for r in J], 's--', color='#c0392b', label='y_sof = [P(1) + (x−1)·S(2)]/x')
        ax.plot(xx, [r[p] for r in J], '^:', color='#27864a', label=f"{p}({'k' if p == 'M' else 'x'})")
        J2 = [r for r in J if r['S'] is not None]
        ax.plot([r['x'] for r in J2], [r['S'] for r in J2], 'v:', color='#8e6c00', label=f"S({'k' if p == 'M' else 'x'})")
        for r in J:
            if 'farq_95' in r:
                lo, hi = r['farq_95']
                ax.vlines(r['x'], r['y_sof'] + lo, r['y_sof'] + hi, color='#c0392b', alpha=.35, lw=6)
        ax.set_title(nom, fontsize=10)
        ax.set_xlabel(xl)
        ax.set_ylabel(yl)
        ax.grid(alpha=.3)
        ax.legend(fontsize=7)
    fig.suptitle('E7 (POST HOC) — qism turi ichida; qizil ustun: kuzatilgan − y_sof, 95 % (n ≥ 30, x ≥ 3)', fontsize=10)
    fig.tight_layout()
    fig.savefig(yol, dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------- E8 (post hoc 4)
SEED_8A, SEED_8C, SEED_8C_BC = 20261022, 20261023, 20261024
TAKROR_8C = 1000


def _son(v):
    """JSON uchun: nan/inf -> None (avvalgi versiya bilan tenglik tekshiruvi nan da buziladi)."""
    v = float(v)
    return v if np.isfinite(v) else None


def tokenlar_gap(tb, K, Tk):
    """T.tokenlar bilan bir xil tartib, har tokenga (manba, gap indeksi held-out filtridan keyin)."""
    out = []
    for k in ('K1', 'K2'):
        out += [(k, i, w) for i, g in enumerate(K[k]) for w in g['words']]
    out += [('treebank', i, w) for i, g in enumerate(tb) for w in g['ud_toks']]
    if [(k, w) for k, _, w in out] != Tk:
        raise SystemExit("TO'XTA — E8: gap indeksli tokenlar T.tokenlar bilan mos emas")
    return out


def q2_q3_gap(Tg, A, q2, q3):
    """T.q2_q3 dagi Q2 (max score) va Q3 kuzatuvlari + gap kaliti; x, y tahlil.py bilan aynan bo'lishi shart."""
    o2, o3 = {'x': [], 'y': [], 'g': []}, {'x': [], 'y': [], 'g': []}
    for korpus, i, raw in Tg:
        n = T.norm(raw).strip()
        if n and set(n) <= {"'"}:
            continue
        t = T.tozala(raw)
        if T.tok_toifa(t):
            continue
        w, a, B = T.norm(t), A[t], []
        if not a['unk'] and a['teng'] and all(a['score']):
            B = T.morf_chegaralari(a['score'])
            o2['x'].append(len(a['score']))
            o2['y'].append(len(T.grafemalar(w, B)) / len(a['score']))
            o2['g'].append((korpus, i))
        gr = T.grafemalar(w, B)
        if len(gr) == 1:
            continue
        v = T.unli_soni(gr)
        if v == 0:
            continue
        o3['x'].append(v)
        o3['y'].append(len(gr) / v)
        o3['g'].append((korpus, i))
    if o2['x'] != q2['x'] or o2['y'] != q2['y'] or o3['x'] != q3['x'] or o3['y'] != q3['y']:
        raise SystemExit("TO'XTA — E8a: gap indeksli Q2/Q3 kuzatuvlari tahlil.py dan farq qiladi")
    return o2, o3


def _klaster_boot(x, y, g, seed):
    """Gap bo'yicha klasterli bootstrap: gaplar (kamida bitta kuzatuvli) qaytarib tanlanadi; kataklar asl namunadan."""
    x, y = np.asarray(x, int), np.asarray(y, float)
    J = [r for r in T.jadval(x, y) if r['fitga']]
    kat = [r['x'] for r in J]
    kod = {v: i for i, v in enumerate(kat)}
    gid = {}
    gi = np.array([gid.setdefault(z, len(gid)) for z in g])
    G = len(gid)
    m = np.isin(x, kat)
    ci_ = np.array([kod[v] for v in x[m]])
    Nm = np.zeros((G, len(kat)))
    Sm = np.zeros((G, len(kat)))
    np.add.at(Nm, (gi[m], ci_), 1)
    np.add.at(Sm, (gi[m], ci_), y[m])
    xs = np.array(kat, float)
    asl = T.fit(xs, [r['y'] for r in J], [r['n'] for r in J])['sodda']        # tahlil.qator dagidek (jadval o'rtachalari)
    rng = np.random.default_rng(seed)
    b, xato = [], 0
    for _ in range(BOOT):
        w = np.bincount(rng.integers(0, G, G), minlength=G).astype(float)
        nn, ss = w @ Nm, w @ Sm
        bor = nn > 0
        r = T._faqat_sodda(xs[bor], ss[bor] / nn[bor], nn[bor])['sodda']
        if isinstance(r, dict):
            b.append(r['p'][1])
        else:
            xato += 1
    hajm = np.bincount(gi)
    return {'N': int(len(x)), 'kataklar': kat, 'b': asl['p'][1], 'b_95': _ci(b), 'yaqinlashmagan': xato,
            'klaster': G, 'klaster_manba': dict(Counter(k for k, _ in gid)),
            'klaster_hajmi_ortacha': float(hajm.mean()), 'klaster_hajmi_max': int(hajm.max())}


def e8a(Tg, A, q2, q3, nat):
    o2, o3 = q2_q3_gap(Tg, A, q2, q3)
    out = {'gap_id': {'K1': "bor (surat gapi indeksi, held-out filtridan keyin)",
                      'K2': "bor (surat gapi indeksi, held-out filtridan keyin)",
                      'treebank': "bor (ud_system_output gapi indeksi, held-out filtridan keyin)"}}
    for nom, o, qq in (('Q2 standart (max score)', o2, 'Q2 jami (max score)'), ('Q3', o3, 'Q3 jami')):
        r = _klaster_boot(o['x'], o['y'], o['g'], SEED_8A)
        q = nat[qq]
        if abs(r['b'] - q['fit']['sodda']['p'][1]) > 1e-12 or r['kataklar'] != q['fit_kataklar']:
            raise SystemExit(f"TO'XTA — E8a {nom}: nuqta b natija.json dan farq qiladi")
        r['b_95_token'] = q['oraliq']['sodda']['b']
        r['kenglik_nisbati'] = (r['b_95'][1] - r['b_95'][0]) / (r['b_95_token'][1] - r['b_95_token'][0])
        out[nom] = r
    return out


def qism_massivlari(B, Tk, A):
    """E7 dagi (X, Y, P, Q, Qn) massivlari: klauza tor/keng (gap), morfema uchala qoida (token)."""
    M = {}
    for kalit in ('tor', 'keng'):
        R = [r for r in B[kalit] if r['k'] and r['M'] is not None]
        M['klauza · ' + kalit] = (np.array([r['k'] for r in R]), np.array([r['y'] for r in R], float),
                                  np.array([r['M'] for r in R], float),
                                  np.array([sum(l for _, l in r['ergash']) for r in R], float),         # E8k tuzatish: yig'indi va
                                  np.array([len(r['ergash']) for r in R], float))                      # soni (klauza-vaznli S̄)
    for kod, nom in zip(('score', 'kam', 'kop'), ('standart', 'eng kam', "eng ko'p")):
        X, Y, P, Q, Qn = [], [], [], [], []
        for _, raw in Tk:
            g, t = tozala_tok(raw)
            if g != 'yaroqli':
                continue
            a = A[t]
            if a['unk'] or not a['teng'] or not all(a['score']):
                continue
            m = a[kod]
            mg = morf_grafemalari(T.norm(t), m)
            X.append(len(m))
            Y.append(sum(mg) / len(m))
            P.append(mg[0])
            Q.append(sum(mg[1:]))
            Qn.append(len(m) - 1)
        M['morfema · ' + nom] = (np.array(X), *(np.array(v, float) for v in (Y, P, Q, Qn)))
    return M


def _tayanch(X, Y, P, Q, Qn):
    """Sof aralashma y_mix(x) = [P₀ + (x − 1)·S₀]/x uch tayanch bilan: (i) P(1), S(2); (ii) P(1), S(3);
    (iii) P̄ (n ≥ 30 kataklardagi barcha kuzatuvlar), S̄ (x ≥ 2 kataklar, qism birligi bo'yicha). Bootstrap SEED (E7 dagidek)."""
    xs = sorted(set(X.tolist()))
    kat = [x for x in xs if (X == x).sum() >= NMIN]
    L, xl = max(xs) + 1, kat[-1]

    def hisob(idx):
        Xi = X[idx]
        nn = np.bincount(Xi, minlength=L).astype(float)
        dv = lambda w, d: np.divide(np.bincount(Xi, weights=w[idx], minlength=L), d, out=np.full(L, np.nan),  # noqa: E731
                                    where=d > 0)
        yb, pb = dv(Y, nn), dv(P, nn)
        qb = dv(Q, np.bincount(Xi, weights=Qn[idx], minlength=L))
        mk = np.isin(Xi, kat)
        m2 = mk & (Xi >= 2)
        V = {'i': (pb[1], qb[2]), 'ii': (pb[1], qb[3] if L > 3 else np.nan),
             'iii': (P[idx][mk].mean(), Q[idx][m2].sum() / Qn[idx][m2].sum())}
        r = {}
        for v, (p0, s0) in V.items():
            mix = np.array([(p0 + (x - 1) * s0) / x if x >= 1 else np.nan for x in range(L)])
            r[v] = {'P0': p0, 'S0': s0, 'mix': mix, 'farq': yb - mix, 'b': _b(kat, mix[kat], nn[kat]),
                    'ulush': (mix[1] - mix[xl]) / (yb[1] - yb[xl])}
        return yb, nn, r
    yb, nn, a0 = hisob(np.arange(len(X)))
    rng = np.random.default_rng(SEED)
    BB = {v: defaultdict(list) for v in a0}
    for _ in range(BOOT):
        _, _, r = hisob(rng.integers(0, len(X), len(X)))
        for v, d in r.items():
            for k in ('P0', 'S0', 'ulush'):
                BB[v][k].append(d[k])
            BB[v]['b'].append(d['b'][1] if d['b'] else None)
            BB[v]['farq'].append(d['farq'])
    out = {'kataklar': kat, 'x_oxirgi': xl}
    for v, d in a0.items():
        F = np.array(BB[v]['farq'])
        out[v] = {'P0': _son(d['P0']), 'P0_95': _ci(BB[v]['P0']), 'S0': _son(d['S0']), 'S0_95': _ci(BB[v]['S0']),
                  'b_mix': d['b'][1] if d['b'] else None, 'b_mix_95': _ci(BB[v]['b']),
                  'yaqinlashmagan': sum(z is None for z in BB[v]['b']),
                  'pasayish_ulushi': _son(d['ulush']), 'pasayish_ulushi_95': _ci(BB[v]['ulush']),
                  'jadval': [{'x': x, 'n': int(nn[x]), 'y': float(yb[x]), 'y_mix': _son(d['mix'][x]),
                              'farq': _son(d['farq'][x]), 'farq_95': _ci(F[:, x])} for x in kat]}
    return out


def e8b(M, out):
    E7 = {'klauza · tor': out['E7']['klauza']['tor'], 'klauza · keng': out['E7']['klauza']['keng'],
          'morfema · standart': out['E7']['morfema']['max(score)'], 'morfema · eng kam': out['E7']['morfema']['eng kam morfema'],
          "morfema · eng ko'p": out['E7']['morfema']["eng ko'p morfema"]}
    res = {}
    for nom, arr in M.items():
        r = _tayanch(*arr)
        s = E7[nom]['b_sof']                                   # ijobiy nazorat: (i) = E7 b_sof (nuqta va oraliq)
        if abs(r['i']['b_mix'] - s['b']) > 1e-12 or any(abs(p - q) > 1e-12 for p, q in zip(r['i']['b_mix_95'], s['b_95'])):
            raise SystemExit(f"TO'XTA — E8b {nom}: (i) tayanch E7 b_sof dan farq qiladi")
        r['umumiy_b'] = E7[nom]['umumiy']['b']
        res[nom] = r
    return res


def _b_fit(kat, nn, ss):
    r = T.fit(np.array(kat, float), ss / nn, nn)['sodda']
    return r['p'][1] if isinstance(r, dict) else None


def _taqsimot(b, b_haq):
    v = [z for z in b if z is not None]
    return {'takror': len(b), 'muvaffaqiyatli': len(v), 'mediana': float(np.median(v)),
            '95': [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))], 'min_max': [float(min(v)), float(max(v))],
            'b_manfiy': sum(z < 0 for z in v), 'b_le_haqiqiy': sum(z <= b_haq for z in v)}


def e8c(B, tb, nat):
    R = [r for r in B['tor'] if r['k'] and r['M'] is not None]
    K = np.array([r['k'] for r in R])
    M = np.array([r['M'] for r in R], float)
    Sp = np.array([l for r in R for _, l in r['ergash']], float)
    if len(Sp) != int((K - 1).sum()):
        raise SystemExit("TO'XTA — E8c: ergash klauzalar soni Σ(k − 1) ga teng emas")
    Y = np.array([r['y'] for r in R], float)
    kat = [r['x'] for r in T.jadval(K, Y) if r['fitga']]
    nn = np.bincount(K)[kat].astype(float)
    b_haq = _b_fit(kat, nn, np.bincount(K, weights=Y)[kat])
    ch = np.cumsum(np.concatenate([[0], K - 1]))

    def yigish(Mv, Sv):
        cs = np.concatenate([[0.0], np.cumsum(Sv)])
        y = (Mv + cs[ch[1:]] - cs[ch[:-1]]) / K
        ss = np.bincount(K, weights=y)[kat]
        yy = ss / nn
        return _b_fit(kat, nn, ss), bool(all(q < p for p, q in zip(yy, yy[1:])))
    out = {'N': len(R), 'gap_bosh_klauzasi_sozsiz_chiqarildi': len([r for r in B['tor'] if r['k']]) - len(R),
           'ergash_klauza': len(Sp), 'kataklar': kat, 'b_haqiqiy_shu_namunada': b_haq,
           'b_haqiqiy_Q1': nat['Q1 treebank tor']['fit']['sodda']['p'][1]}
    for nom, bosh in (('bosh va ergash almashtirilgan', True), ("o'z bosh klauzasi, ergash almashtirilgan", False)):
        rng = np.random.default_rng(SEED_8C)
        b, mon = [], 0
        for _ in range(TAKROR_8C):
            Mv = rng.permutation(M) if bosh else M
            bb, mm = yigish(Mv, rng.permutation(Sp))
            b.append(bb)
            mon += mm
        out[nom] = {**_taqsimot(b, b_haq), 'monoton': mon}
    # B&Č qayta: Q1 tor, tahlil.bc_model
    x, y, L, _ = T.q1_xy(tb, 'tor')
    bh = nat['Q1 treebank tor']['fit']['sodda']['p'][1]

    def bc(rng):
        kx, ky = T.bc_model(L, rng)
        J = T.jadval(kx, ky)
        kk = [r['x'] for r in J if r['fitga']]
        yy = [r['y'] for r in J if r['fitga']]
        s = T.fit(np.array(kk, float), yy, [r['n'] for r in J if r['fitga']])['sodda']
        return (s['p'][1] if isinstance(s, dict) else None), bool(all(q < p for p, q in zip(yy, yy[1:])))
    rng = np.random.default_rng(T.SEED)                        # ijobiy nazorat: natija.json Q5 dagi 100 takror aynan
    nz = [bc(rng)[0] for _ in range(T.BC_TAKROR)]
    if any(abs(p - t['b']) > 1e-12 for p, t in zip(nz, nat['Q5']['takrorlar'])) or len(nz) != len(nat['Q5']['takrorlar']):
        raise SystemExit("TO'XTA — E8c: B&Č qayta qurish natija.json Q5 takrorlari bilan aynan emas")
    rng = np.random.default_rng(SEED_8C_BC)
    b, mon = [], 0
    for _ in range(TAKROR_8C):
        bb, mm = bc(rng)
        b.append(bb)
        mon += mm
    out['B&Č 1 000'] = {**_taqsimot(b, bh), 'monoton': mon, 'b_haqiqiy': bh, 'nazorat_q5_100_aynan': True}
    return out


def _qisqa(q):
    s = q['fit']['sodda']
    return {'N': q['N'], 'kataklar': q['fit_kataklar'], 'b': s['p'][1] if isinstance(s, dict) else None,
            'b_95': q['oraliq']['sodda']['b'] if q['oraliq'].get('sodda') else None, 'monoton': q['hukm']['monoton'],
            'hukm': q['hukm']['hukm']}


def e8d(tb, nat, e3):
    x, y, _, _ = T.q1_xy(tb, 'tor')
    out = {'chegara': {}}
    asl = T.NMIN
    try:                                                       # T.NMIN faqat shu jarayon xotirasida (jadval() o'qiydi)
        for n in (20, 25, 30):
            T.NMIN = n
            q = T.qator(x, y, f'Q1 treebank tor · n ≥ {n}')
            out['chegara'][str(n)] = {**_qisqa(q), 'jadval': [{'x': r['x'], 'n': r['n'], 'y': r['y']} for r in q['jadval']]}
    finally:
        T.NMIN = asl
    q0 = nat['Q1 treebank tor']
    c30 = out['chegara']['30']
    if abs(c30['b'] - q0['fit']['sodda']['p'][1]) > 1e-12 or c30['b_95'] != q0['oraliq']['sodda']['b']:
        raise SystemExit("TO'XTA — E8d: n ≥ 30 natija.json dan farq qiladi")
    kat = e3['qatorlar']['UT']['fit_kataklar']
    xu, yu, _, _ = T.q1_xy([g for g in tb if g['tb'] == 'UzUDT'], 'tor')
    m = [i for i, v in enumerate(xu) if v in kat]
    qu = T.qator([xu[i] for i in m], [yu[i] for i in m], 'Q1 UzUDT tor · UT kataklari')
    if qu['fit_kataklar'] != kat:
        raise SystemExit("TO'XTA — E8d: UzUDT kataklari UT bilan mos emas")
    xt, yt, _, _ = T.q1_xy([g for g in tb if g['tb'] == 'UT'], 'tor')
    qt = T.qator(xt, yt, 'Q1 UT tor')
    if abs(qt['fit']['sodda']['p'][1] - e3['qatorlar']['UT']['fit']['sodda']['p'][1]) > 1e-12:
        raise SystemExit("TO'XTA — E8d: UT qatori E3 dan farq qiladi")
    b1 = [p[1] if p is not None else None for p in qt['_boot']['sodda']]
    b2 = [p[1] if p is not None else None for p in qu['_boot']['sodda']]
    d = [p - q for p, q in zip(b1, b2) if p is not None and q is not None]
    out['UT_UzUDT_uch_katak'] = {
        'kataklar': kat, 'UT': _qisqa(qt), 'UzUDT (UT kataklari)': _qisqa(qu),
        'UzUDT (barcha n ≥ 30 kataklar)': _qisqa(e3['qatorlar']['UzUDT']),
        'UzUDT_chiqarilgan_gap': len(xu) - len(m),
        'UT_minus_UzUDT': {'nuqta': qt['fit']['sodda']['p'][1] - qu['fit']['sodda']['p'][1], 'oraliq': _ci(d), 'takror': len(d)}}
    return out


def _fit_vaznsiz(x, ybar):
    from scipy.optimize import curve_fit, OptimizeWarning
    import warnings
    x, ybar = np.asarray(x, float), np.asarray(ybar, float)
    if len(x) < 3 or not (ybar > 0).all():
        return None
    lx, ly = np.log(x), np.log(ybar)
    b0 = float(np.polyfit(lx, ly, 1)[0])
    a0 = float(np.exp(ly.mean() - b0 * lx.mean()))
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', OptimizeWarning)
            warnings.simplefilter('ignore', RuntimeWarning)
            p, _ = curve_fit(T._model_sodda, x, ybar, p0=(a0, b0), maxfev=20000)
        return [float(v) for v in p] if np.all(np.isfinite(p)) else None
    except (RuntimeError, ValueError, OptimizeWarning, FloatingPointError):
        return None


def _vaznsiz_qator(x, y):
    """Vaznsiz NLS (sigma yo'q) — kataklar va bootstrap indekslari tahlil.qator dagidek (seed SEED, kuzatuv darajasida)."""
    x, y = np.asarray(x, int), np.asarray(y, float)
    J = T.jadval(x, y)
    kat = [r['x'] for r in J if r['fitga']]
    p = _fit_vaznsiz(kat, [r['y'] for r in J if r['fitga']])
    L = x.max() + 1
    rng = np.random.default_rng(SEED)
    b, xato = [], 0
    for _ in range(BOOT):
        idx = rng.integers(0, len(x), len(x))
        nn = np.bincount(x[idx], minlength=L)[kat]
        ss = np.bincount(x[idx], weights=y[idx], minlength=L)[kat]
        bor = nn > 0
        r = _fit_vaznsiz(np.array(kat)[bor], ss[bor] / nn[bor])
        if r is None:
            xato += 1
        else:
            b.append(r[1])
    return {'N': int(len(x)), 'kataklar': kat, 'a': p[0] if p else None, 'b': p[1] if p else None, 'b_95': _ci(b),
            'yaqinlashmagan': xato}


def e8e(tb, q2, q3, nat):
    x, y, _, _ = T.q1_xy(tb, 'tor')
    out = {}
    for nom, (xx, yy), qq in (('Q1 treebank tor', (x, y), 'Q1 treebank tor'),
                              ('Q2 standart (max score)', (q2['x'], q2['y']), 'Q2 jami (max score)'),
                              ('Q3', (q3['x'], q3['y']), 'Q3 jami')):
        r = _vaznsiz_qator(xx, yy)
        r['b_vaznli'] = nat[qq]['fit']['sodda']['p'][1]
        r['b_vaznli_95'] = nat[qq]['oraliq']['sodda']['b']
        out[nom] = r
    return out


E8F_QATORLAR = ('Q1 treebank tor', 'Q1 treebank keng', 'Q1 K1 VDU', 'Q1 K2 VDU', 'Q2 jami (max score)', 'Q3 jami',
                'Q4b A: treebank V0', 'Q4c eng kam morfema', "Q4c eng ko'p morfema")


def e8f(nat):
    out = {}
    for k in E8F_QATORLAR:
        q = nat[k]
        J = [r for r in q['jadval'] if r['fitga']]
        r = T.fit([r['x'] for r in J], [r['y'] for r in J], [r['n'] for r in J])   # natija.json bilan qayta tekshiruv
        s, t = q['fit'].get('sodda'), q['fit'].get('toliq')
        if not (isinstance(s, dict) and isinstance(t, dict)):
            out[k] = {'K': q['fit']['K'], 'aniqlanmadi': f"to'liq model: {t!r}, sodda: {'bor' if isinstance(s, dict) else s!r}"}
            continue
        if abs(r['sodda']['aic'] - s['aic']) > 1e-9 or abs(r['toliq']['aic'] - t['aic']) > 1e-9:
            raise SystemExit(f"TO'XTA — E8f {k}: AIC qayta hisobi natija.json dan farq qiladi")
        out[k] = {'K': q['fit']['K'], 'aic_sodda': s['aic'], 'aic_toliq': t['aic'], 'delta_aic': t['aic'] - s['aic'],
                  'afzal': q['fit']['afzal'], 'c_toliq': t['p'][2]}
    return out


def qoshimcha_kodlari(an, A):
    """Q2 namunasi turlari uchun max(score) tahlilining element kodlari (analizator qayta chaqiriladi, tanlash qoidasi
    yo'q); morfemalar A[t]['score'] bilan aynan bo'lishi shart."""
    MSM = an.MSM
    out = {}
    with an.app.app_context():
        aff = MSM._affikslar_saralangan(MSM.kesh_manbasi()) if MSM._kesh_ishlaydimi() else \
            sorted(MSM.Affix.query.all(), key=MSM._affiks_saralash_kaliti)
        for w in sorted(t for t, a in A.items() if not a['unk'] and a['teng'] and all(a['score'])):
            an.holat.update(rejim=None, i=0, ishlatildi=False, nomzod=None)
            r = an.ms._analyze_word_hisobla(w, aff)
            if [T.norm(e['value']) for e in r['elements']] != A[w]['score']:
                raise SystemExit("TO'XTA — E8g: qayta tahlil morfemalari A[score] dan farq qiladi")
            out[w] = [e['code'] for e in r['elements']]
    return out


KLAUZA_TURLARI = ('advcl', 'ccomp', 'conj', 'parataxis', 'csubj')
QOSHIMCHA_TURI = {'X3': 'kelishik', 'X': "ko'plik", 'X2': 'egalik', 'U5': 'shaxs'}
QOSHIMCHA_TURLARI = ('kelishik', "ko'plik", 'egalik', 'shaxs', 'boshqa')


def _turlar_jadvali(juft, turlar):
    """juft — [(tur, uzunlik)] -> {tur: n, ulush, o'rtacha}."""
    n = len(juft)
    c = defaultdict(list)
    for t, l in juft:
        c[t].append(l)
    return {t: {'n': len(c[t]), 'ulush': len(c[t]) / n if n else None,
                'ortacha': float(np.mean(c[t])) if c[t] else None} for t in turlar}


def e8g(B, Tk, A, kodlar, out):
    res = {'klauza': {}, 'morfema': {}}
    for kalit in ('tor', 'keng'):
        R = [r for r in B[kalit] if r['k'] and r['M'] is not None]
        e7j = {r['x']: r for r in out['E7']['klauza'][kalit]['jadval']}
        rows, boshqa = [], Counter()
        for k in (2, 3, 4):
            erg = [(d if d in KLAUZA_TURLARI else 'boshqa', l) for r in R if r['k'] == k for d, l in r['ergash']]
            boshqa.update(d for r in R if r['k'] == k for d, _ in r['ergash'] if d not in KLAUZA_TURLARI)
            rows.append({'k': k, 'gap': sum(r['k'] == k for r in R), 'fitga': k in out['E7']['klauza'][kalit]['kataklar'],
                         'ergash': len(erg), 'S_klauza_ortacha': float(np.mean([l for _, l in erg])) if erg else None,
                         'S_E7': e7j[k]['S'] if k in e7j else None,
                         'turlar': _turlar_jadvali(erg, KLAUZA_TURLARI + ('boshqa',))})
        res['klauza'][kalit] = {'jadval': rows, 'boshqa_deprel': dict(boshqa.most_common())}
    rows = {x: [] for x in range(2, 6)}
    komp = Counter()
    for _, raw in Tk:
        g, t = tozala_tok(raw)
        if g != 'yaroqli':
            continue
        a = A[t]
        if a['unk'] or not a['teng'] or not all(a['score']):
            continue
        m = a['score']
        if len(m) not in rows:
            continue
        mg = morf_grafemalari(T.norm(t), m)
        for kod, l in zip(kodlar[t][1:], mg[1:]):
            tur = QOSHIMCHA_TURI.get(kod, 'boshqa')
            rows[len(m)].append((tur, l))
            if tur == 'boshqa' and '+' in (kod or ''):
                komp[len(m)] += 1
    res['morfema']['jadval'] = [{'x': x, 'token': len(v) // (x - 1), 'qoshimcha': len(v),
                                 'S_ortacha': float(np.mean([l for _, l in v])) if v else None,
                                 'boshqa_ichida_kompozit': komp[x], 'turlar': _turlar_jadvali(v, QOSHIMCHA_TURLARI)}
                                for x, v in rows.items()]
    e1j = {r['x']: r for r in out['E1']['max(score)']['jadval']}
    for r in res['morfema']['jadval']:                         # nazorat: S(x) E1 bilan aynan
        if abs(r['S_ortacha'] - e1j[r['x']]['qoshimcha']) > 1e-12:
            raise SystemExit("TO'XTA — E8g: qo'shimcha o'rtachasi E1 S(x) dan farq qiladi")
    res['morfema']['kod_turi'] = {**QOSHIMCHA_TURI, 'qolgan kodlar (A1–A6, AG, T, U, U1–U4, kompozit «+»)': 'boshqa'}
    return res


def e8h(tb, Tk, A, nat):
    import ud_tools as U
    import iq
    import naqsh_kesh as NK
    Y = json.loads((T.SUPP / 'data' / 'ud_system_output.json').read_text(encoding='utf-8'))['sentences']
    G = {(g['tb'], g['sent_id']): g for t in U.TREEBANK for g in U.load_treebank(t)}
    c = Counter()
    for y in Y:
        g = G[(y['tb'], y['sent_id'])]
        s = iq.soz_spanlari(g['text'])
        of = NK.ofsetlar(g['text'], g['tokenlar'])
        ud = [o for t, o in zip(g['tokenlar'], of) if t['upos'] != 'PUNCT']
        c['ud_nonpunct'] += len(ud)
        c['ud_punct'] += len(g['tokenlar']) - len(ud)
        qop = Counter()
        for w, a, b in s:
            k = [i for i, (p, q) in enumerate(ud) if p < b and a < q]
            for i in k:
                qop[i] += 1
            c['tizim_soz'] += 1
            if not T.sozmi(w):
                c['tizim_soz_harfsiz'] += 1
                c['tizim_soz_harfsiz_ud_nonpunct_bor'] += bool(k)
                continue
            c['tizim_soz_harfli'] += 1
            if len(k) == 0:
                c['harfli_ud_nonpunct_0'] += 1
            elif len(k) >= 2:
                c['harfli_ud_nonpunct_2plus'] += 1
                c['ortiqcha_ud_token'] += len(k) - 1
                c['2plus_defisli'] += any(d in w for d in T.DEFIS)
                c['2plus_apostrofli'] += any(ch in w for ch in "'ʻʼ‘’`´")
        c['ud_nonpunct_qoplanmagan'] += sum(1 for i in range(len(ud)) if qop[i] == 0)
        c['ud_nonpunct_2_sozda'] += sum(1 for i in range(len(ud)) if qop[i] >= 2)
    mwt = sum(1 for rels in U.TREEBANK.values() for r in rels
              for l in (U.UD_DIR / r).read_text(encoding='utf-8').splitlines() if l[:1].isdigit() and '-' in l.split('\t')[0])
    yig = {k: int(round(sum(r['n'] * r['x'] * r['y'] for r in nat['qatorlar'][k]['jadval'])))
           for k in ('Q1 treebank tor', 'Q1 treebank keng', 'Q4b A: treebank V0')}
    tenglik = c['tizim_soz_harfli'] + c['ortiqcha_ud_token'] - c['harfli_ud_nonpunct_0'] + c['tizim_soz_harfsiz_ud_nonpunct_bor']
    h1 = {**dict(c), 'ud_mwt_qatori': mwt, 'jadval_katak_yigindisi_sum_n_x_y': yig,
          'tenglik_harfli + ortiqcha − nol + harfsiz_ud_bor': tenglik, 'tenglik_ud_nonpunct_ga_teng': tenglik == c['ud_nonpunct'],
          'natija_treebank_kirish': nat['tokenlar']['treebank']['kirish']}
    # (2) ng: tahlil.q2_q3 — B = [] (noma'lum / yuza teng emas / bo'sh morfema) -> grafemalar(w, []) -> ng har doim 1
    ng = Counter()
    for _, raw in Tk:
        g, t = tozala_tok(raw)
        if g != 'yaroqli':
            continue
        a, w = A[t], T.norm(t)
        if a['unk']:
            gr, B = "noma'lum", []
        elif not a['teng'] or not all(a['score']):
            gr, B = 'yuza teng emas', []
        else:
            gr, B = 'Q2 namunasi', T.morf_chegaralari(a['score'])
        n_ng = sum(1 for i in range(len(w) - 1) if w[i:i + 2] == 'ng')
        if not n_ng:
            continue
        ikki = sum(1 for i in range(len(w) - 1) if w[i:i + 2] == 'ng' and (i + 1) in set(B))
        ng[gr, 'token'] += 1
        ng[gr, 'ng'] += n_ng
        ng[gr, 'ng_2_grafema'] += ikki
    h2 = {'qoida_kodi': "tahlil.q2_q3: B = [] (noma'lum, yuza teng emas, bo'sh morfema); Q2 namunasida B = "
                        "morf_chegaralari(score); Q3: gr = grafemalar(w, B); grafemalar: ng — chegara (i+1) ∈ B bo'lmasa 1 grafema",
          'tahlil_qilinmagan': "har doim 1 (B bo'sh -> ng hech qachon bo'linmaydi)",
          'sanoq': {f'{g} · {k}': v for (g, k), v in sorted(ng.items())}}
    # (3) prereg Q5 modeli
    git = lambda *a: subprocess.run(['git', *a], cwd=REPO, capture_output=True, text=True).stdout  # noqa: E731
    prereg = str((SIKL / 'prereg.md').relative_to(REPO))
    pr = git('show', f'f3bbe32:{prereg}')
    q5 = [l for l in pr.splitlines() if l.startswith('**Q5')]
    h3 = {'f3bbe32_Q5_sarlavha_Benesova_Cech': bool(q5) and 'Benešová & Čech' in q5[0],
          'f3bbe32_asl_variant_tashlangan_deb_qayd': '**Asl Q5 nega tashlandi' in pr,
          'prereg_commitlari': git('log', '--format=%h', '--', prereg).split(),
          'joriy_prereg_f3bbe32_bilan_aynan': hashlib.sha256(pr.encode('utf-8')).hexdigest() == sha256(SIKL / 'prereg.md')}
    return {'1_tokenlar': h1, '2_ng': h2, '3_prereg_q5': h3}


def e8i(nat):
    out = {}
    for k in ('Q1 treebank keng', 'Q1 K1 VDU', 'Q1 K2 VDU'):
        q = nat[k]
        a, b = q['fit']['sodda']['p']
        out[k] = {'a': a, 'b': b, 'jadval': [{'x': r['x'], 'n': r['n'], 'y': r['y'], 'sd': r['sd'], 'fitga': r['fitga'],
                                              'm': a * r['x'] ** b} for r in q['jadval']]}
    return out


def e8k(B, r):
    """E8c 1-variant va E8b (iii) taqqoslovi: havzalar, simulyatsiya kataklari o'rtachasi, kutilma, y_mix (iii)."""
    R = [g for g in B['tor'] if g['k'] and g['M'] is not None]
    K = np.array([g['k'] for g in R])
    M = np.array([g['M'] for g in R], float)
    Sp = np.array([l for g in R for _, l in g['ergash']], float)
    Y = np.array([g['y'] for g in R], float)
    kat = r['c']['kataklar']
    nn = np.bincount(K)[kat].astype(float)
    ch = np.cumsum(np.concatenate([[0], K - 1]))
    rng = np.random.default_rng(SEED_8C)                       # E8c 1-variant bilan aynan tasodifiy ketma-ketlik
    YY, b = [], []
    for _ in range(TAKROR_8C):
        Mv = rng.permutation(M)
        cs = np.concatenate([[0.0], np.cumsum(rng.permutation(Sp))])
        ss = np.bincount(K, weights=(Mv + cs[ch[1:]] - cs[ch[:-1]]) / K)[kat]
        YY.append(ss / nn)
        b.append(_b_fit(kat, nn, ss))
    if float(np.median(b)) != r['c']['bosh va ergash almashtirilgan']['mediana']:
        raise SystemExit("TO'XTA — E8k: simulyatsiya E8c 1-variantini takrorlamadi")
    YY = np.array(YY)
    Mh, Sh = float(M.mean()), float(Sp.mean())
    m4 = np.isin(K, kat)
    Sk = np.array([l for g in R if g['k'] in kat for _, l in g['ergash']], float)
    Sg = np.array([np.mean([l for _, l in g['ergash']]) for g in R if g['k'] in kat and g['ergash']], float)
    kut = lambda p0, s0: [(p0 + (k - 1) * s0) / k for k in kat]  # noqa: E731
    iii = r['b']['klauza · tor']['iii']
    return {'havza': {'bosh_klauza': len(M), 'ergash_klauza': len(Sp), 'gap_k_ge_5': int((K > kat[-1]).sum()),
                      'ergash_k_ge_5': int((K[K > kat[-1]] - 1).sum()), 'usul': "permutatsiya (qaytarmasdan), har takrorda ikkala havza",
                      'y': "y = (M' + Σ S')/k har gapda; ȳ(k) — katak o'rtachasi; fit k = 1…4 (n ≥ 30), n-vaznli"},
            'M_hamma': Mh, 'S_hamma_klauza': Sh, 'M_kataklar': float(M[m4].mean()), 'S_kataklar_klauza': float(Sk.mean()),
            'S_kataklar_gap_vaznli': float(Sg.mean()), 'iii_yangi': {'P0': iii['P0'], 'S0': iii['S0'], 'b_mix': iii['b_mix']},
            'b_sim_mediana': float(np.median(b)), 'b_kutilma_havza': _b(kat, np.array(kut(Mh, Sh)), nn)[1],
            'b_kutilma_gap_vaznli': _b(kat, np.array(kut(float(M[m4].mean()), float(Sg.mean()))), nn)[1],
            'jadval': [{'k': k, 'n': int(nn[i]), 'y': float(np.bincount(K, weights=Y)[k] / nn[i]), 'y_sim': float(YY[:, i].mean()),
                        'y_sim_95': _ci(YY[:, i]), 'y_kutilma_havza': kut(Mh, Sh)[i], 'y_mix_iii_yangi': iii['jadval'][i]['y_mix'],
                        'y_mix_iii_eski': kut(float(M[m4].mean()), float(Sg.mean()))[i]} for i, k in enumerate(kat)]}


def _yaqin(a, b, tol=1e-9):
    """JSON tuzilmalari teng (sonlar tol gacha)."""
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_yaqin(a[k], b[k], tol) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_yaqin(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        return abs(a - b) <= tol
    return a == b


def e8(tb, K, Tk, A, out, q2, q3, kodlar):
    nat = json.loads((NATIJA / 'natija.json').read_text(encoding='utf-8'))
    Q = nat['qatorlar']
    B, _ = e5_birliklar(tb)
    r = {}
    r['a'] = e8a(tokenlar_gap(tb, K, Tk), A, q2, q3, Q)
    r['b'] = e8b(qism_massivlari(B, Tk, A), out)
    r['c'] = e8c(B, tb, {**Q, 'Q5': nat['Q5']})
    r['d'] = e8d(tb, Q, out['E3'])
    r['e'] = e8e(tb, q2, q3, Q)
    r['f'] = e8f(Q)
    r['g'] = e8g(B, Tk, A, kodlar, out)
    r['h'] = e8h(tb, Tk, A, nat)
    r['i'] = e8i(Q)
    r['k'] = e8k(B, r)
    return r


def _ci_md(c):
    return f"[{f(c[0])}; {f(c[1])}]" if c else '—'


def e8_md(o):
    E = o['E8']
    s = ['## E8 (post hoc 4)', '']
    a = E['a']
    s += ['### E8a — klasterli bootstrap (gap bo\'yicha)', '',
          f"Gaplar qaytarib tanlanadi (kamida bitta kuzatuvli gaplar — klaster), 1 000 takror, seed {SEED_8A}; kataklar va "
          "fit tahlil.py dagidek (n ≥ 30, n-vaznli NLS, sodda model). Token oralig'i — natija.json. Gap ID: "
          + '; '.join(f"{k} — {v}" for k, v in a['gap_id'].items()) + '.', '',
          '| daraja | N | klaster (K1 / K2 / treebank) | klaster hajmi o\'rtacha / max | b | 95 % (klaster) | 95 % (token) | '
          'kenglik nisbati | yaqinlashmagan |', '|---|---|---|---|---|---|---|---|---|']
    for nom in ('Q2 standart (max score)', 'Q3'):
        r = a[nom]
        km = r['klaster_manba']
        s.append(f"| {nom} | {r['N']} | {r['klaster']} ({km.get('K1', 0)} / {km.get('K2', 0)} / {km.get('treebank', 0)}) | "
                 f"{f(r['klaster_hajmi_ortacha'], 1)} / {r['klaster_hajmi_max']} | {f(r['b'])} | {_ci_md(r['b_95'])} | "
                 f"{_ci_md(r['b_95_token'])} | {f(r['kenglik_nisbati'], 2)} | {r['yaqinlashmagan']} |")
    s.append('')
    if 'b' in E:
        s += ['### E8b — sof aralashma tayanch sezgirligi (E7)', '',
              'y_mix(x) = [P₀ + (x − 1)·S₀]/x. Tayanch: (i) P₀ = P(1), S₀ = S(2) — asosiy (E7 b_sof bilan aynan, tekshirilgan); '
              '(ii) P₀ = P(1), S₀ = S(3); (iii) P₀ = P̄ (n ≥ 30 kataklardagi barcha kuzatuvlar bo\'yicha bosh qism o\'rtachasi), '
              'S₀ = S̄ (x ≥ 2 kataklarda tobe qism birligi bo\'yicha o\'rtacha: klauza — har ergash klauza, morfema — har qo\'shimcha; '
              'E8k tuzatishidan oldin klauzada gap ichidagi o\'rtachalar o\'rtachasi edi). P = M (klauza) yoki R (morfema). '
              'Pasayish ulushi = [y_mix(1) − y_mix(x_oxirgi)] / [ȳ(1) − ȳ(x_oxirgi)], x_oxirgi — oxirgi n ≥ 30 katak. '
              f'95 % — bootstrap (klauza: gap, morfema: token; 1 000, seed {SEED}).', '',
              '| daraja | umumiy b | tayanch | P₀ [95 %] | S₀ [95 %] | b_mix [95 %] | pasayish ulushi [95 %] |',
              '|---|---|---|---|---|---|---|']
        for nom, r in E['b'].items():
            for v in ('i', 'ii', 'iii'):
                d = r[v]
                s.append(f"| {nom} | {f(r['umumiy_b'])} | ({v}) | {f(d['P0'])} {_ci_md(d['P0_95'])} | {f(d['S0'])} {_ci_md(d['S0_95'])} | "
                         f"{f(d['b_mix'])} {_ci_md(d['b_mix_95'])} | {f(d['pasayish_ulushi'])} {_ci_md(d['pasayish_ulushi_95'])} |")
        s.append('')
        for nom, r in E['b'].items():
            s += [f"**{nom}** — kataklar {r['kataklar']}, x_oxirgi = {r['x_oxirgi']}", '',
                  '| x | n | ȳ | y_mix (i) | ȳ − y_mix (i) [95 %] | y_mix (ii) | ȳ − y_mix (ii) [95 %] | y_mix (iii) | ȳ − y_mix (iii) [95 %] |',
                  '|---|---|---|---|---|---|---|---|---|']
            for j, row in enumerate(r['i']['jadval']):
                c = [r[v]['jadval'][j] for v in ('i', 'ii', 'iii')]
                s.append(f"| {row['x']} | {row['n']} | {f(row['y'])} | " + ' | '.join(
                    f"{f(z['y_mix'])} | {f(z['farq'])} {_ci_md(z['farq_95'])}" for z in c) + ' |')
            s.append('')
    if 'c' in E:
        c = E['c']
        s += ['### E8c — turlarni saqlovchi tasodifiy model va B&Č (klauza, tor)', '',
              f"Namuna: E5/E7 dagi gaplar (bosh klauzasida so'z bor), N = {c['N']} (bosh klauzasi so'zsiz chiqarilgan gap "
              f"{c['gap_bosh_klauzasi_sozsiz_chiqarildi']}), ergash klauza {c['ergash_klauza']}, kataklar {c['kataklar']}. "
              f"Haqiqiy b shu namunada {f(c['b_haqiqiy_shu_namunada'])} (Q1 tor, barcha gaplar: {f(c['b_haqiqiy_Q1'])}). "
              f"Har takror: k ketma-ketligi asl; ergash klauza uzunliklari korpus bo'ylab almashtiriladi (qaytarmasdan) va har gapga "
              f"k − 1 tadan beriladi; bosh klauza — (1) bosh klauzalar bo'ylab almashtiriladi yoki (2) gapning o'zinikida qoladi. "
              f"{TAKROR_8C} takror, seed {SEED_8C} (ikkala variant bir xil seed). B&Č — tahlil.bc_model, {TAKROR_8C} takror, "
              f"seed {SEED_8C_BC}; ijobiy nazorat: seed {SEED} bilan 100 takror natija.json Q5 bilan aynan — "
              f"{'ha' if c['B&Č 1 000']['nazorat_q5_100_aynan'] else 'yo' + chr(39) + 'q'}.", '',
              '| model | takror (fit) | b mediana | 95 % | min / max | b < 0 | b ≤ haqiqiy b | ȳ qat\'iy monoton |',
              '|---|---|---|---|---|---|---|---|']
        for nom in ('bosh va ergash almashtirilgan', "o'z bosh klauzasi, ergash almashtirilgan", 'B&Č 1 000'):
            d = c[nom]
            s.append(f"| {nom} | {d['takror']} ({d['muvaffaqiyatli']}) | {f(d['mediana'])} | {_ci_md(d['95'])} | "
                     f"{f(d['min_max'][0])} / {f(d['min_max'][1])} | {d['b_manfiy']} | {d['b_le_haqiqiy']} | {d['monoton']} |")
        s += ['', f"«b ≤ haqiqiy b»: turlarni saqlovchi modelda haqiqiy b = {f(c['b_haqiqiy_shu_namunada'])} (shu namuna), "
              f"B&Č da {f(c['B&Č 1 000']['b_haqiqiy'])} (Q1 tor).", '']
    if 'd' in E:
        d = E['d']
        s += ['### E8d — chegara sezgirligi (Q1 treebank, tor)', '',
              'tahlil.qator, n-chegara faqat jarayon xotirasida o\'zgartirildi (T.NMIN); bootstrap 1 000, seed 20261021. '
              'n ≥ 30 qatori natija.json bilan aynan (tekshirilgan).', '',
              '| chegara | kataklar | b | 95 % | monoton | §4.4 hukm |', '|---|---|---|---|---|---|']
        for n, r in d['chegara'].items():
            s.append(f"| n ≥ {n} | {r['kataklar']} | {f(r['b'])} | {_ci_md(r['b_95'])} | "
                     f"{'ha' if r['monoton'] else 'yo' + chr(39) + 'q'} | {r['hukm']} |")
        u = d['UT_UzUDT_uch_katak']
        s += ['', f"UzUDT UT bilan bir xil kataklarda ({u['kataklar']}; UzUDT dan boshqa katakdagi {u['UzUDT_chiqarilgan_gap']} gap "
              "chiqarildi, bootstrap qolgan gaplarda):", '',
              '| qator | N | kataklar | b | 95 % | monoton |', '|---|---|---|---|---|---|']
        for nom in ('UT', 'UzUDT (UT kataklari)', 'UzUDT (barcha n ≥ 30 kataklar)'):
            r = u[nom]
            s.append(f"| {nom} | {r['N']} | {r['kataklar']} | {f(r['b'])} | {_ci_md(r['b_95'])} | "
                     f"{'ha' if r['monoton'] else 'yo' + chr(39) + 'q'} |")
        dd = u['UT_minus_UzUDT']
        s += ['', f"Δb UT − UzUDT (uch katak): {f(dd['nuqta'])} {_ci_md(dd['oraliq'])} (mustaqil bootstrap, {dd['takror']} juft takror).", '']
    if 'e' in E:
        s += ['### E8e — vaznsiz NLS (faqat taqqoslash; prereg — n-vaznli)', '',
              'a·x^b kataklar o\'rtachalariga sigma siz (curve_fit); kataklar va bootstrap indekslari tahlil.qator dagidek (1 000, seed 20261021).', '',
              '| daraja | N | kataklar | b (vaznsiz) | 95 % | b (vaznli, prereg) | 95 % | yaqinlashmagan |', '|---|---|---|---|---|---|---|---|']
        for nom, r in E['e'].items():
            s.append(f"| {nom} | {r['N']} | {r['kataklar']} | {f(r['b'])} | {_ci_md(r['b_95'])} | {f(r['b_vaznli'])} | "
                     f"{_ci_md(r['b_vaznli_95'])} | {r['yaqinlashmagan']} |")
        s.append('')
    if 'f' in E:
        s += ['### E8f — ΔAIC = AIC(to\'liq) − AIC(sodda)', '',
              'AIC = K·ln(WRSS/K) + 2p (n-vaznli, n ≥ 30 kataklarda; tahlil.fit). Qiymatlar natija.json dan, qayta hisob bilan tekshirilgan. '
              '«afzal»: to\'liq, agar ΔAIC < −2.', '',
              '| qator | K | AIC (sodda) | AIC (to\'liq) | ΔAIC | c (to\'liq) | afzal |', '|---|---|---|---|---|---|---|']
        for k, r in E['f'].items():
            if 'aniqlanmadi' in r:
                s.append(f"| {k} | {r['K']} | — | — | aniqlanmadi ({r['aniqlanmadi']}) | — | — |")
            else:
                s.append(f"| {k} | {r['K']} | {f(r['aic_sodda'], 2)} | {f(r['aic_toliq'], 2)} | {f(r['delta_aic'], 2)} | "
                         f"{f(r['c_toliq'])} | {r['afzal']} |")
        s.append('')
    if 'g' in E:
        g = E['g']
        s += ['### E8g — ikkinchi darajali aralashma', '',
              'Klauza: E5 birliklari (ergash klauza = bosh tokeni deprel asosi); ulush — shu k dagi ergash klauzalar ichida; '
              'o\'rtacha — klauza darajasida (E7 S(k) esa gap ichidagi o\'rtachalarning o\'rtachasi).', '']
        for kalit, v in g['klauza'].items():
            T_ = KLAUZA_TURLARI + ('boshqa',)
            s += [f'**{kalit}**', '', '| k | gap | fitga | ergash klauza | S(k) klauza o\'rt. | S(k) E7 | '
                  + ' | '.join(f'{t}: n · ulush · o\'rt.' for t in T_) + ' |', '|' + '---|' * (6 + len(T_))]
            for r in v['jadval']:
                s.append(f"| {r['k']} | {r['gap']} | {'ha' if r['fitga'] else '—'} | {r['ergash']} | {f(r['S_klauza_ortacha'])} | "
                         f"{f(r['S_E7'])} | " + ' | '.join(
                             f"{r['turlar'][t]['n']} · {f(100 * r['turlar'][t]['ulush'], 1) if r['turlar'][t]['ulush'] is not None else '—'} % · "
                             f"{f(r['turlar'][t]['ortacha'])}" for t in T_) + ' |')
            s += ['', f"«boshqa» deprel (k = 2–4): " + (', '.join(f'{d} {n}' for d, n in v['boshqa_deprel'].items()) or "yo'q") + '.', '']
        m = g['morfema']
        s += ['Morfema: Q2 namunasi, standart (max score) tahlil; qo\'shimcha turi analizator element kodidan (kontekstli tur, '
              '`_resolve_affix_type`): ' + ', '.join(f'{k} → {v}' for k, v in m['kod_turi'].items()) +
              '. Uzunlik — grafema (E1 dagi taqsimot; S(x) E1 bilan aynan, tekshirilgan).', '',
              '| x | token | qo\'shimcha | S(x) | ' + ' | '.join(f'{t}: n · ulush · o\'rt.' for t in QOSHIMCHA_TURLARI)
              + ' | boshqa ichida kompozit |', '|' + '---|' * (5 + len(QOSHIMCHA_TURLARI))]
        for r in m['jadval']:
            s.append(f"| {r['x']} | {r['token']} | {r['qoshimcha']} | {f(r['S_ortacha'])} | " + ' | '.join(
                f"{r['turlar'][t]['n']} · {f(100 * r['turlar'][t]['ulush'], 1)} % · {f(r['turlar'][t]['ortacha'])}"
                for t in QOSHIMCHA_TURLARI) + f" | {r['boshqa_ichida_kompozit']} |")
        s.append('')
    if 'h' in E:
        h = E['h']
        t1 = h['1_tokenlar']
        s += ['### E8h — uch aniqlik', '', '**(1) Treebank tokenlari: 11 072 va 1-jadval katak yig\'indisi**', '',
              '| o\'lcham | qiymat |', '|---|---|',
              f"| UD non-PUNCT token (natija.json `kirish`) | {t1['ud_nonpunct']} ({t1['natija_treebank_kirish']}) |",
              f"| UD PUNCT token | {t1['ud_punct']} |",
              f"| UD ko'p so'zli token (range) qatori | {t1['ud_mwt_qatori']} |",
              f"| tizim so'zi (bo'shliq-bo'lak, chetdagi tinish olingan) | {t1['tizim_soz']} |",
              f"| — harf-raqamsiz (PUNCT siz so'z emas, Q1 ga kirmaydi) | {t1['tizim_soz_harfsiz']} (UD non-PUNCT bilan ustma-ust: {t1['tizim_soz_harfsiz_ud_nonpunct_bor']}) |",
              f"| — harf-raqamli (Q1 so'zi) | {t1['tizim_soz_harfli']} |",
              f"| 1-jadval Σ n·x·ȳ: tor / keng / V0 | {' / '.join(str(v) for v in t1['jadval_katak_yigindisi_sum_n_x_y'].values())} |",
              f"| harfli so'z, ≥ 2 UD non-PUNCT tokenga to'g'ri keladi | {t1.get('harfli_ud_nonpunct_2plus', 0)} (ortiqcha token {t1.get('ortiqcha_ud_token', 0)}; "
              f"defisli {t1.get('2plus_defisli', 0)}, apostrofli {t1.get('2plus_apostrofli', 0)}) |",
              f"| harfli so'z, UD non-PUNCT tokeni yo'q (faqat PUNCT bilan ustma-ust) | {t1.get('harfli_ud_nonpunct_0', 0)} |",
              f"| UD non-PUNCT, hech bir so'zga tushmagan / 2 so'zga tushgan | {t1.get('ud_nonpunct_qoplanmagan', 0)} / {t1.get('ud_nonpunct_2_sozda', 0)} |",
              f"| tenglik: harfli + ortiqcha − nolli + harfsiz∩UD = UD non-PUNCT | {t1['tenglik_harfli + ortiqcha − nol + harfsiz_ud_bor']} — "
              f"{'ha' if t1['tenglik_ud_nonpunct_ga_teng'] else 'yo' + chr(39) + 'q'} |", '']
        t2 = h['2_ng']
        s += ['**(2) Tahlil qilinmagan tokenlarda ng**', '', f"- Kod: {t2['qoida_kodi']}.", f"- Javob: **{t2['tahlil_qilinmagan']}**.", '',
              '| guruh · o\'lcham | son |', '|---|---|'] + [f'| {k} | {v} |' for k, v in t2['sanoq'].items()] + ['']
        t3 = h['3_prereg_q5']
        s += ['**(3) prereg.md, commit f3bbe32 — Q5 modeli**', '',
              f"- f3bbe32 dagi Q5 sarlavhasi Benešová & Čech modeli: **{'ha' if t3['f3bbe32_Q5_sarlavha_Benesova_Cech'] else 'yo' + chr(39) + 'q'}**; "
              f"«qayta kesish» asl varianti tashlangani o'sha faylda qayd etilgan: {'ha' if t3['f3bbe32_asl_variant_tashlangan_deb_qayd'] else 'yo' + chr(39) + 'q'}.",
              f"- prereg.md ga tegilgan commitlar: {', '.join(t3['prereg_commitlari'])}; joriy fayl f3bbe32 dagi bilan aynan: "
              f"{'ha' if t3['joriy_prereg_f3bbe32_bilan_aynan'] else 'yo' + chr(39) + 'q'}. Keyin almashtirilmagan.", '']
    if 'i' in E:
        s += ['### E8i — Ilova A1-jadvali (natija.json)', '',
              'm(x) = a·x^b — sodda model qiymati (natija.json dagi a, b; fit n ≥ 30 kataklarda, «fitga» — ha). SD — kuzatuvlar standart og\'ishi.', '']
        for k, v in E['i'].items():
            s += [f"**{k}** — a = {f(v['a'])}, b = {f(v['b'])}", '', '| x | n | ȳ | SD | m(x) | fitga |', '|---|---|---|---|---|---|']
            for r in v['jadval']:
                s.append(f"| {r['x']} | {r['n']} | {f(r['y'])} | {f(r['sd'])} | {f(r['m'])} | {'ha' if r['fitga'] else '—'} |")
            s.append('')
    if 'k' in E:
        k = E['k']
        h = k['havza']
        s += ['### E8k — E8c 1-variant va E8b (iii) nomuvofiqligi', '',
              f"E8c 1-variant: bosh klauza havzasi {h['bosh_klauza']} (barcha gaplar), ergash klauza havzasi {h['ergash_klauza']}; "
              f"{h['usul']}; k ≥ 5 gaplar ({h['gap_k_ge_5']} ta, {h['ergash_k_ge_5']} ergash klauza) havzaga kiradi va yig'iladi, fitga kirmaydi; "
              f"{h['y']}.", '',
              '| o\'lcham | qiymat |', '|---|---|',
              f"| M̄ — barcha 1 182 bosh klauza (simulyatsiya havzasi) | {f(k['M_hamma'])} |",
              f"| S̄ — barcha ergash klauzalar, klauza-vaznli (simulyatsiya havzasi) | {f(k['S_hamma_klauza'])} |",
              f"| P̄ — k = 1…4 gaplardagi bosh klauza ((iii), eski va yangi) | {f(k['M_kataklar'])} |",
              f"| S̄ — k = 2…4, gap-vaznli ((iii) ESKI, xato) | {f(k['S_kataklar_gap_vaznli'])} |",
              f"| S̄ — k = 2…4, klauza-vaznli ((iii) YANGI) | {f(k['S_kataklar_klauza'])} |",
              f"| b: simulyatsiya medianasi / havza kutilmasi [M̄ + (k − 1)·S̄]/k | {f(k['b_sim_mediana'])} / {f(k['b_kutilma_havza'])} |",
              f"| b_mix (iii): eski / yangi | {f(k['b_kutilma_gap_vaznli'])} / {f(k['iii_yangi']['b_mix'])} |", '',
              '| k | n | kuzatilgan ȳ | simulyatsiya ȳ (1 000 o\'rt.) [2,5–97,5 %] | kutilma (havza M̄, S̄) | y_mix (iii) eski | y_mix (iii) yangi |',
              '|---|---|---|---|---|---|---|']
        for r in k['jadval']:
            s.append(f"| {r['k']} | {r['n']} | {f(r['y'])} | {f(r['y_sim'])} {_ci_md(r['y_sim_95'])} | {f(r['y_kutilma_havza'])} | "
                     f"{f(r['y_mix_iii_eski'])} | {f(r['y_mix_iii_yangi'])} |")
        if 'iii_eski' in k:
            s += ['', 'E8b (iii) klauza qatorlari — eski (avvalgi posthoc.json) va yangi:', '',
                  '| daraja | P₀ | S₀ eski → yangi | b_mix eski → yangi | pasayish ulushi eski → yangi |', '|---|---|---|---|---|']
            for n, e in k['iii_eski'].items():
                y = E['b'][n]['iii']
                s.append(f"| {n} | {f(y['P0'])} | {f(e['S0'])} → {f(y['S0'])} | {f(e['b_mix'])} {_ci_md(e['b_mix_95'])} → "
                         f"{f(y['b_mix'])} {_ci_md(y['b_mix_95'])} | {f(e['pasayish_ulushi'])} → {f(y['pasayish_ulushi'])} "
                         f"{_ci_md(y['pasayish_ulushi_95'])} |")
        s.append('')
    return s


# ---------------------------------------------------------------- E10
def e10a():
    """tahlil.fit dagi AIC satrlari (koddan, o'zgarishsiz)."""
    import inspect
    kalit = ('K = len(x)', 'sigma=1 / np.sqrt(n)', 'wrss = ', 'aic = ', "out['delta_aic", "out['afzal'] = 'toliq'")
    return {'kod': [l.strip() for l in inspect.getsource(T.fit).splitlines() if any(k in l for k in kalit)]}


def _icc(y, g):
    """Bir yo'nalishli ANOVA ICC(1), muvozanatsiz guruhlar (n₀ bilan)."""
    gid = {}
    gi = np.array([gid.setdefault(z, len(gid)) for z in g])
    G, N = len(gid), len(y)
    ni = np.bincount(gi).astype(float)
    mi = np.bincount(gi, weights=y) / ni
    msb = (ni * (mi - y.mean()) ** 2).sum() / (G - 1)
    msw = ((y - mi[gi]) ** 2).sum() / (N - G)
    n0 = (N - (ni ** 2).sum() / N) / (G - 1)
    return {'icc': float((msb - msw) / (msb + (n0 - 1) * msw)), 'n0': float(n0), 'msb': float(msb), 'msw': float(msw)}


def e10b(Tg, A, q2, q3, nat, e8a):
    o2, o3 = q2_q3_gap(Tg, A, q2, q3)
    out = {}
    for nom, o, qq in (('Q2 standart (max score)', o2, 'Q2 jami (max score)'), ('Q3', o3, 'Q3 jami')):
        x, y = np.asarray(o['x'], int), np.asarray(o['y'], float)
        hajm = np.array(list(Counter(o['g']).values()))
        J = {r['x']: r['y'] for r in T.jadval(x, y)}
        gap = _klaster_boot(x, y, o['g'], SEED_8A)
        if gap['b_95'] != e8a[nom]['b_95']:
            raise SystemExit(f"TO'XTA — E10b {nom}: gap-klaster E8a dan farq qiladi")
        tok = _klaster_boot(x, y, [('token', i) for i in range(len(x))], SEED_8A)
        tok21 = _klaster_boot(x, y, [('token', i) for i in range(len(x))], SEED)
        out[nom] = {'N': len(x), 'klaster': len(hajm), 'hajm_min': int(hajm.min()), 'hajm_median': float(np.median(hajm)),
                    'hajm_max': int(hajm.max()), 'bir_tokenli_klaster': int((hajm == 1).sum()),
                    'icc_y': _icc(y, o['g']), 'icc_y_minus_katak': _icc(y - np.array([J[v] for v in x]), o['g']),
                    'b': gap['b'], 'b_95_gap': gap['b_95'], 'b_95_token_seed_8a': tok['b_95'],
                    'b_95_token_seed_21': tok21['b_95'], 'b_95_natija_token': nat[qq]['oraliq']['sodda']['b']}
    return out


def _klauza_massiv(R):
    return (np.array([r['k'] for r in R]), np.array([r['y'] for r in R], float), np.array([r['M'] for r in R], float),
            np.array([sum(l for _, l in r['ergash']) for r in R], float), np.array([len(r['ergash']) for r in R], float))


def _ajratish(X, Y, P, Q, Qn, nom_p):
    q = T.qator(X, Y, 'E10')
    s = q['fit']['sodda']
    qi = _qism(X, Y, P, Q, Qn, nom_p, 'S')
    ta = _tayanch(X, Y, P, Q, Qn)
    yo = lambda d, k: ({'b': d[k]['b'], 'b_95': d[k]['b_95']} if d[k] else None)  # noqa: E731
    return {'N': int(len(X)), 'kataklar': q['fit_kataklar'], 'b': s['p'][1], 'b_95': q['oraliq']['sodda']['b'],
            'b_P': yo(qi, 'b_' + nom_p), 'b_S': yo(qi, 'b_S'),
            'b_S_qayd': None if qi['b_S'] else f"aniqlanmadi: x ≥ 2 kataklar {[x for x in qi['kataklar'] if x >= 2]} (< 3)",
            'b_mix_i': ta['i']['b_mix'], 'b_mix_i_95': ta['i']['b_mix_95'],
            'pasayish_ulushi_i': ta['i']['pasayish_ulushi'], 'pasayish_ulushi_i_95': ta['i']['pasayish_ulushi_95']}


def e10c(tb, B, e3):
    out = {}
    for t in ('UT', 'UzUDT'):
        R = [r for g, r in zip(tb, B['tor']) if g['tb'] == t and r['k'] and r['M'] is not None]
        out[t] = _ajratish(*_klauza_massiv(R), 'M')
        if abs(out[t]['b'] - e3['qatorlar'][t]['fit']['sodda']['p'][1]) > 1e-12:
            raise SystemExit(f"TO'XTA — E10c {t}: b E3 dan farq qiladi")
    return out


def _q2_namuna(Tk, A):
    for _, raw in Tk:
        g, t = tozala_tok(raw)
        if g != 'yaroqli':
            continue
        a = A[t]
        if a['unk'] or not a['teng'] or not all(a['score']):
            continue
        yield t, a['score'], morf_grafemalari(T.norm(t), a['score'])


def e10d(Tk, A, kodlar):
    c = defaultdict(list)
    for t, m, mg in _q2_namuna(Tk, A):
        if len(m) <= 4:
            c[kodlar[t][0], len(m)].append(mg[0])
            c['hammasi', len(m)].append(mg[0])

    def qator(k, x):
        v = np.array(c[k, x], float)
        if not len(v):
            return {'x': x, 'n': 0, 'R': None, 'R_95': None}
        rng = np.random.default_rng(SEED)
        return {'x': x, 'n': int(len(v)), 'R': float(v.mean()),
                'R_95': _ci([v[rng.integers(0, len(v), len(v))].mean() for _ in range(BOOT)])}
    return {tur: [qator(k, x) for x in range(1, 5)] for tur, k in (('ot (C)', 'C'), ("fe'l (G)", 'G'), ('hammasi', 'hammasi'))}


def e10e(Tk, A):
    kor = {}
    for t, m, mg in _q2_namuna(Tk, A):
        kor.setdefault(t, (len(m), sum(mg) / len(m), mg[0], sum(mg[1:]), len(m) - 1))
    v = list(kor.values())
    X = np.array([z[0] for z in v])
    return {'tip': len(v), **_ajratish(X, *(np.array([z[i] for z in v], float) for i in range(1, 5)), 'R')}


def e10f(K, nat):
    """Eng katta x gaplari: surat tokenlari va asl manba qatori (faqat sonlar). Surat va JSON `sentence` maydonida . ! ? yo'q,
    shuning uchun K1 asl qatori (JSON meta.corpus_path) harf-raqam kaliti bilan topiladi; K2 manbasi PDF — repo tashqarisida."""
    import re
    from gap_model_ierarxiya import UZEN_JSON, TAGOR_JSON
    kalit = lambda t: re.sub(r'\W', '', (t or '').lower())  # noqa: E731
    manba = {}
    for k, pj in (('K1', UZEN_JSON), ('K2', TAGOR_JSON)):
        yol = Path(json.loads(Path(pj).read_text(encoding='utf-8'))['meta']['corpus_path'])
        manba[k] = {'tur': yol.suffix, 'repo_ichida': REPO in yol.parents, 'qatorlar': None}
        if manba[k]['repo_ichida'] and yol.suffix != '.pdf' and yol.exists():
            manba[k]['qatorlar'] = yol.read_text(encoding='utf-8').splitlines()
    sanoq = {}
    for k in ('K1', 'K2'):
        sanoq[k] = {'gap': len(K[k]), 'surat_matnida_belgili_gap': sum(bool(re.search('[.!?]', g['text'])) for g in K[k])}
        Lq = manba[k]['qatorlar']
        if Lq is not None:
            sanoq[k]['manba_qator'] = len(Lq)
            sanoq[k]['manba_ichki_belgili_qator'] = sum(bool(re.search(r'[.!?]+["»”)\']*\s+\S', l)) for l in Lq)
    out = []
    for k, xs in (('K1', (13,)), ('K2', (16, 18))):
        for g in K[k]:
            u, _ = T.klauza_uzunliklari(g['words'], g['v0'])
            if len(u) not in xs:
                continue
            w = g['words']
            r = {'korpus': k, 'x': len(u), 'token': len(w), 'soz': sum(map(T.sozmi, w)), 'birlikdagi_soz': sum(u),
                 'ybar': sum(u) / len(u), 'surat_belgili_token': sum(any(ch in z for ch in '.!?') for z in w)}
            Lq = manba[k]['qatorlar']
            if Lq is None:
                r['manba'] = f"aniqlanmadi: manba {manba[k]['tur']} (repo ichida: {'ha' if manba[k]['repo_ichida'] else 'yo' + chr(39) + 'q'})"
            else:
                mos = [l for l in Lq if kalit(g['text']) and kalit(g['text']) in kalit(l)]
                r['manba_mos_qator'] = len(mos)
                if len(mos) == 1:
                    r['manba_belgi'] = sum(mos[0].count(c) for c in '.!?')
                    r['manba_ichki_belgi'] = len(re.findall(r'[.!?]+["»”)\']*\s+(?=\S)', mos[0]))
            out.append(r)
    for r in out:                                              # natija.json jadvali bilan moslik (n = 1 kataklar)
        j = {q['x']: q for q in nat[f"Q1 {r['korpus']} VDU"]['jadval']}[r['x']]
        if j['n'] != 1 or abs(j['y'] - r['ybar']) > 1e-12:
            raise SystemExit("TO'XTA — E10f: katak natija.json bilan mos emas")
    return {'gaplar': out, 'korpus': sanoq}


def e10g(B, tb, c8):
    """2-rasm uchun takror b qiymatlari: E8c 1-variant va B&Č (o'sha seedlar; medianalar E8c bilan aynan bo'lishi shart)."""
    R = [r for r in B['tor'] if r['k'] and r['M'] is not None]
    K = np.array([r['k'] for r in R])
    M = np.array([r['M'] for r in R], float)
    Sp = np.array([l for r in R for _, l in r['ergash']], float)
    kat = c8['kataklar']
    nn = np.bincount(K)[kat].astype(float)
    ch = np.cumsum(np.concatenate([[0], K - 1]))
    rng = np.random.default_rng(SEED_8C)
    tur = []
    for _ in range(TAKROR_8C):
        Mv = rng.permutation(M)
        cs = np.concatenate([[0.0], np.cumsum(rng.permutation(Sp))])
        tur.append(_b_fit(kat, nn, np.bincount(K, weights=(Mv + cs[ch[1:]] - cs[ch[:-1]]) / K)[kat]))
    _, _, L, _ = T.q1_xy(tb, 'tor')
    rng = np.random.default_rng(SEED_8C_BC)
    bc = []
    for _ in range(TAKROR_8C):
        kx, ky = T.bc_model(L, rng)
        J = [r for r in T.jadval(kx, ky) if r['fitga']]
        s = T.fit(np.array([r['x'] for r in J], float), [r['y'] for r in J], [r['n'] for r in J])['sodda']
        bc.append(s['p'][1] if isinstance(s, dict) else None)
    if (float(np.median(tur)) != c8['bosh va ergash almashtirilgan']['mediana']
            or float(np.median([b for b in bc if b is not None])) != c8['B&Č 1 000']['mediana']):
        raise SystemExit("TO'XTA — E10g: takrorlar E8c medianalari bilan aynan emas")
    return {'turlarni_saqlovchi_b': tur, 'bc_b': bc, 'b_haqiqiy': c8['B&Č 1 000']['b_haqiqiy']}


def e10(tb, K, Tk, A, kodlar, out, q2, q3):
    nat = json.loads((NATIJA / 'natija.json').read_text(encoding='utf-8'))['qatorlar']
    B, _ = e5_birliklar(tb)
    return {'a': e10a(), 'b': e10b(tokenlar_gap(tb, K, Tk), A, q2, q3, nat, out['E8']['a']), 'c': e10c(tb, B, out['E3']),
            'd': e10d(Tk, A, kodlar), 'e': e10e(Tk, A), 'f': e10f(K, nat), 'g': e10g(B, tb, out['E8']['c'])}


def e10_md(o):
    E = o['E10']
    f4 = lambda c: f"[{f(c[0], 4)}; {f(c[1], 4)}]" if c else '—'  # noqa: E731
    s = ['## E10', '', '### E10a — AIC formulasi (tahlil.fit, koddan)', '', '```python', *E['a']['kod'], '```', '',
         'K — fitga kirgan kataklar soni (n ≥ 30); qoldiq — n-vaznli RSS: WRSS = Σ n_x·(ȳ_x − f(x))² (curve_fit sigma = 1/√n bilan bir xil '
         'vazn); likelihood — Gauss, σ² ning ML bahosi WRSS/K o\'rniga qo\'yilgan, doimiy hadlar tashlangan: AIC = K·ln(WRSS/K) + 2p; '
         'p — model parametrlari (sodda 2: a, b; to\'liq 3: a, b, c), σ sanalmaydi (ikkala modelga bir xil qo\'shiladi, ΔAIC ga ta\'sir '
         'qilmaydi). ΔAIC = AIC(to\'liq) − AIC(sodda); afzal = to\'liq, agar ΔAIC < −2.', '',
         '### E10b — klaster diagnostikasi', '',
         'ICC(1) — bir yo\'nalishli ANOVA (muvozanatsiz, n₀): y bo\'yicha va y − ȳ(x) (katak o\'rtachasi ayirilgan) bo\'yicha. Nazorat: har token '
         f'o\'z klasteri — bir xil seed ({SEED_8A}) bilan; shuningdek seed {SEED} bilan (natija.json token oralig\'i bilan solishtirish).', '',
         '| daraja | N | klaster | hajm min / median / max | 1 tokenli klaster | ICC(y) | ICC(y − ȳ(x)) | n₀ |', '|---|---|---|---|---|---|---|---|']
    for nom, r in E['b'].items():
        s.append(f"| {nom} | {r['N']} | {r['klaster']} | {r['hajm_min']} / {f(r['hajm_median'], 1)} / {r['hajm_max']} | "
                 f"{r['bir_tokenli_klaster']} | {f(r['icc_y']['icc'], 4)} | {f(r['icc_y_minus_katak']['icc'], 4)} | {f(r['icc_y']['n0'], 2)} |")
    s += ['', f'| daraja | b | 95 % gap-klaster (seed {SEED_8A}) | 95 % token-klaster (seed {SEED_8A}) | 95 % token-klaster (seed {SEED}) | '
          '95 % natija.json token |', '|---|---|---|---|---|---|']
    for nom, r in E['b'].items():
        s.append(f"| {nom} | {f(r['b'], 4)} | {f4(r['b_95_gap'])} | {f4(r['b_95_token_seed_8a'])} | {f4(r['b_95_token_seed_21'])} | "
                 f"{f4(r['b_95_natija_token'])} |")
    s += ['', '### E10c — ajratish treebank bo\'yicha (klauza, tor; E7 usuli)', '',
          '| treebank | N | kataklar | b [95 %] | b_M [95 %] | b_S [95 %] | b_mix (i) [95 %] | pasayish ulushi (i) [95 %] |',
          '|---|---|---|---|---|---|---|---|']
    for t, r in E['c'].items():
        bs = f"{f(r['b_S']['b'])} {_ci_md(r['b_S']['b_95'])}" if r['b_S'] else r['b_S_qayd']
        s.append(f"| {t} | {r['N']} | {r['kataklar']} | {f(r['b'])} {_ci_md(r['b_95'])} | {f(r['b_P']['b'])} {_ci_md(r['b_P']['b_95'])} | "
                 f"{bs} | {f(r['b_mix_i'])} {_ci_md(r['b_mix_i_95'])} | {f(r['pasayish_ulushi_i'])} {_ci_md(r['pasayish_ulushi_i_95'])} |")
    s += ['', '### E10d — o\'zak uzunligi R(x) turkum bo\'yicha (Q2 namunasi, standart tahlil)', '',
          'Turkum — analizator o\'zak kodi (C = ot, G = fe\'l; `kkt_code_for_word_type`). 95 % — token bootstrap (1 000).', '',
          '| x | ot: n | R | 95 % | fe\'l: n | R | 95 % | hammasi: n | R |', '|---|---|---|---|---|---|---|---|---|']
    for i in range(4):
        a, b, c = (E['d'][k][i] for k in ('ot (C)', "fe'l (G)", 'hammasi'))
        s.append(f"| {a['x']} | {a['n']} | {f(a['R'])} | {_ci_md(a['R_95'])} | {b['n']} | {f(b['R'])} | {_ci_md(b['R_95'])} | {c['n']} | {f(c['R'])} |")
    e = E['e']
    s += ['', '### E10e — Q2 noyob so\'z shakllari (tiplar) bo\'yicha', '',
          f"Har tip (tozalangan token) bir marta; N = {e['tip']} tip. Bootstrap tip darajasida (1 000, seed {SEED}).", '',
          '| N | kataklar | b [95 %] | b_R [95 %] | b_S [95 %] | b_mix (i) [95 %] | pasayish ulushi (i) [95 %] |', '|---|---|---|---|---|---|---|',
          f"| {e['N']} | {e['kataklar']} | {f(e['b'])} {_ci_md(e['b_95'])} | {f(e['b_P']['b'])} {_ci_md(e['b_P']['b_95'])} | "
          f"{f(e['b_S']['b']) + ' ' + _ci_md(e['b_S']['b_95']) if e['b_S'] else e['b_S_qayd']} | {f(e['b_mix_i'])} {_ci_md(e['b_mix_i_95'])} | "
          f"{f(e['pasayish_ulushi_i'])} {_ci_md(e['pasayish_ulushi_i_95'])} |", '',
          '### E10f — K1 x = 13, K2 x = 16, 18 gaplari (matn chop etilmaydi)', '',
          'Surat tokenlari va JSON `sentence` maydonida . ! ? olib tashlangan; K1 asl qatori (JSON meta.corpus_path) harf-raqam kaliti '
          'bilan topildi.', '',
          '| korpus | gap | surat matnida . ! ? li gap | asl manba qatori | ichida . ! ? (oxiridan tashqari) bor qator |', '|---|---|---|---|---|']
    for k, c in E['f']['korpus'].items():
        s.append(f"| {k} | {c['gap']} | {c['surat_matnida_belgili_gap']} | {c.get('manba_qator', '—')} | {c.get('manba_ichki_belgili_qator', '—')} |")
    s += ['', '| korpus | x | token | so\'z (harfli) | ȳ | surat: . ! ? li token | asl qator: mos | . ! ? jami | ichki . ! ? |',
          '|---|---|---|---|---|---|---|---|---|']
    for r in E['f']['gaplar']:
        if 'manba' in r:
            m = f"{r['manba']} | — | — "
        else:
            m = f"{r['manba_mos_qator']} | {r.get('manba_belgi', '—')} | {r.get('manba_ichki_belgi', '—')} "
        s.append(f"| {r['korpus']} | {r['x']} | {r['token']} | {r['soz']} | {f(r['ybar'])} | {r['surat_belgili_token']} | {m}|")
    g = E['g']
    s += ['', '### E10g — 2-rasm uchun takrorlar', '',
          f"E8c 1-variant va B&Č takrorlari (har biri {len(g['bc_b'])}) posthoc.json da saqlandi; medianalar E8c bilan aynan (tekshirilgan).", '']
    return s


# ---------------------------------------------------------------- E11 (post hoc 5)
SEED_11C, SEED_11 = 20261025, 20261026
ICHKI_BOOT, PERM_11D = 200, 1000


def _q2_massiv(Tk, A, q2):
    """Q2 namunasi (standart tahlil): x, y, har morfema grafema uzunligi, manba; tahlil.q2_q3 bilan aynan bo'lishi shart."""
    mg = [m for _, _, m in _q2_namuna(Tk, A)]
    X = np.array([len(m) for m in mg])
    Y = np.array([sum(m) / len(m) for m in mg], float)
    if X.tolist() != q2['x'] or np.abs(Y - np.array(q2['y'])).max() > 1e-12 or len(q2['korpus']) != len(X):
        raise SystemExit("TO'XTA — E11: Q2 massivlari tahlil.q2_q3 dan farq qiladi")
    return X, Y, mg, np.array(q2['korpus'])


def _qism_q2(X, mg):
    return (X, np.array([sum(m) / len(m) for m in mg], float), np.array([m[0] for m in mg], float),
            np.array([sum(m[1:]) for m in mg], float), (X - 1).astype(float))


def _tip_massivlari(Tk, A):
    """E10e dagidek: har tip (tozalangan token) bir marta."""
    kor = {}
    for t, m, mg in _q2_namuna(Tk, A):
        kor.setdefault(t, (len(m), sum(mg) / len(m), mg[0], sum(mg[1:]), len(m) - 1))
    v = list(kor.values())
    return (np.array([z[0] for z in v]), *(np.array([z[i] for z in v], float) for i in range(1, 5)))


def _giper(kat, yb, nn):
    """y = β + α/x, n-vaznli kichik kvadratlar (parametrlar chiziqli — NLS yechimi aniq) -> (α, β, R² n-vaznli)."""
    x, y, w = (np.asarray(v, float) for v in (kat, yb, nn))
    (al, be), *_ = np.linalg.lstsq(np.column_stack([1 / x, np.ones_like(x)]) * np.sqrt(w)[:, None], y * np.sqrt(w), rcond=None)
    yw = (w * y).sum() / w.sum()
    return float(al), float(be), float(1 - (w * (y - be - al / x) ** 2).sum() / (w * (y - yw) ** 2).sum())


def e11a_qator(X, Y, P, Q, Qn, ref=None):
    from scipy.optimize import curve_fit
    xs = sorted(set(X.tolist()))
    kat = [x for x in xs if (X == x).sum() >= NMIN]
    L = max(xs) + 1

    def hisob(idx):
        Xi = X[idx]
        nn = np.bincount(Xi, minlength=L).astype(float)
        dv = lambda w, d: np.divide(np.bincount(Xi, weights=w[idx], minlength=L), d, out=np.full(L, np.nan),  # noqa: E731
                                    where=d > 0)
        yb, pb = dv(Y, nn), dv(P, nn)
        qb = dv(Q, np.bincount(Xi, weights=Qn[idx], minlength=L))
        al, be, r2 = _giper(kat, yb[kat], nn[kat])
        return {'alfa': al, 'beta': be, 'r2': r2, 'P1': pb[1], 'S2': qb[2], 'P1_minus_S2': pb[1] - qb[2],
                'alfa_minus_P1_S2': al - (pb[1] - qb[2]), 'beta_minus_S2': be - qb[2]}, yb, nn
    a0, yb, nn = hisob(np.arange(len(X)))
    p, _ = curve_fit(lambda x, al, be: be + al / x, np.array(kat, float), yb[kat], p0=(a0['alfa'], a0['beta']),
                     sigma=1 / np.sqrt(nn[kat]), maxfev=20000)
    if abs(p[0] - a0['alfa']) > 1e-6 or abs(p[1] - a0['beta']) > 1e-6:
        raise SystemExit("TO'XTA — E11a: WLS va curve_fit (α, β) farq qiladi")
    if ref is not None and ([r['x'] for r in ref['jadval'] if r['fitga']] != kat
                            or any(abs(yb[r['x']] - r['y']) > 1e-12 for r in ref['jadval'] if r['fitga'])):
        raise SystemExit("TO'XTA — E11a: kataklar tahlil.py (natija.json) dan farq qiladi")
    rng = np.random.default_rng(SEED)
    BB = defaultdict(list)
    for _ in range(BOOT):
        r, _, _ = hisob(rng.integers(0, len(X), len(X)))
        for k, v in r.items():
            BB[k].append(v)
    out = {'N': int(len(X)), 'kataklar': kat}
    for k, v in a0.items():
        out[k] = float(v)
        out[k + '_95'] = _ci(BB[k])
    return out


def e11a(M, tip, nat, e8b):
    out = {}
    for nom, arr, qq in (('klauza · tor', M['klauza · tor'], 'Q1 treebank tor'), ('klauza · keng', M['klauza · keng'], 'Q1 treebank keng'),
                         ('morfema · standart', M['morfema · standart'], 'Q2 jami (max score)'), ('morfema · tiplar', tip, None)):
        r = e11a_qator(*arr, nat[qq] if qq else None)
        if nom in e8b:                                           # P(1), S(2) = E8b (i) tayanchi (o'sha bootstrap indekslari)
            t = e8b[nom]['i']
            if abs(r['P1'] - t['P0']) > 1e-12 or abs(r['S2'] - t['S0']) > 1e-12 or r['P1_95'] != t['P0_95'] or r['S2_95'] != t['S0_95']:
                raise SystemExit(f"TO'XTA — E11a {nom}: P(1), S(2) E8b (i) dan farq qiladi")
        out[nom] = r
    return out


def _mezon(X, Y, rng):
    """prereg mezoni (tahlil.hukm): b < 0; 95 % oraliq (ICHKI_BOOT takrorli kuzatuv bootstrapi) yuqori chegarasi < 0;
    n ≥ 30 kataklarda ȳ qat'iy kamayadi. Nuqta b — tahlil.qator dagidek (jadval o'rtachalari, tahlil.fit)."""
    X, Y = np.asarray(X, int), np.asarray(Y, float)
    J = [r for r in T.jadval(X, Y) if r['fitga']]
    kat = [r['x'] for r in J]
    xs = np.array(kat, float)
    s = T.fit(xs, [r['y'] for r in J], [r['n'] for r in J])['sodda']
    b = s['p'][1] if isinstance(s, dict) else None
    yy = [r['y'] for r in J]
    kod = np.full(X.max() + 1, -1)
    kod[kat] = np.arange(len(kat))
    xk = kod[X]
    m = xk >= 0
    xk_m, y_m = xk[m], Y[m]
    pos = np.full(len(X), -1)
    pos[np.nonzero(m)[0]] = np.arange(m.sum())
    bb = []
    for _ in range(ICHKI_BOOT):
        sel = pos[rng.integers(0, len(X), len(X))]
        sel = sel[sel >= 0]
        n2 = np.bincount(xk_m[sel], minlength=len(kat))
        s2 = np.bincount(xk_m[sel], weights=y_m[sel], minlength=len(kat))
        bor = n2 > 0
        r = T._faqat_sodda(xs[bor], s2[bor] / n2[bor], n2[bor])['sodda']
        if isinstance(r, dict):
            bb.append(r['p'][1])
    hi = float(np.percentile(bb, 97.5)) if bb else None
    sh = {'b_manfiy': b is not None and b < 0, 'oraliq_0siz': hi is not None and hi < 0,
          'monoton': all(q < p for p, q in zip(yy, yy[1:]))}
    return b, sh


def _mezon_yigindi(b, S, b_haq):
    out = _taqsimot(b, b_haq)
    out.update({k: sum(s[k] for s in S) for k in ('b_manfiy', 'oraliq_0siz', 'monoton')})
    out['uchalasi_N'] = sum(all(s.values()) for s in S)
    return out


def e11b(B, tb, out):
    g10, c8 = out['E10']['g'], out['E8']['c']
    R = [r for r in B['tor'] if r['k'] and r['M'] is not None]
    K = np.array([r['k'] for r in R])
    M = np.array([r['M'] for r in R], float)
    Sp = np.array([l for r in R for _, l in r['ergash']], float)
    ch = np.cumsum(np.concatenate([[0], K - 1]))
    res = {'ichki_bootstrap': ICHKI_BOOT, 'ichki_seed': SEED_11}
    rng, ri = np.random.default_rng(SEED_8C), np.random.default_rng(SEED_11)
    b, S = [], []
    for _ in range(TAKROR_8C):
        Mv = rng.permutation(M)
        cs = np.concatenate([[0.0], np.cumsum(rng.permutation(Sp))])
        bb, sh = _mezon(K, (Mv + cs[ch[1:]] - cs[ch[:-1]]) / K, ri)
        b.append(bb)
        S.append(sh)
    fq = max(abs(p - q) for p, q in zip(b, g10['turlarni_saqlovchi_b']))     # nuqta b jadval o'rtachalaridan (curve_fit tol.)
    if fq > 1e-6:
        raise SystemExit(f"TO'XTA — E11b: turlarni saqlovchi takrorlar E10g dan farq qiladi ({fq})")
    res['E10g_max_farq_turlarni_saqlovchi'] = fq
    res['turlarni saqlovchi (E8c 1-variant)'] = {'seed': SEED_8C, **_mezon_yigindi(b, S, c8['b_haqiqiy_Q1'])}
    _, _, L, _ = T.q1_xy(tb, 'tor')
    rng, ri = np.random.default_rng(SEED_8C_BC), np.random.default_rng(SEED_11)
    b, S = [], []
    for _ in range(TAKROR_8C):
        kx, ky = T.bc_model(L, rng)
        bb, sh = _mezon(kx, ky, ri)
        b.append(bb)
        S.append(sh)
    if any((p is None) != (q is None) or (p is not None and abs(p - q) > 1e-6) for p, q in zip(b, g10['bc_b'])):
        raise SystemExit("TO'XTA — E11b: B&Č takrorlari E10g dan farq qiladi")
    res['E10g_max_farq_BC'] = max((abs(p - q) for p, q in zip(b, g10['bc_b']) if p is not None), default=0.0)
    res['klauza-havzali (B&Č)'] = {'seed': SEED_8C_BC, **_mezon_yigindi(b, S, c8['b_haqiqiy_Q1'])}
    return res


def e11c(X, mg, nat):
    roots = np.array([m[0] for m in mg], float)
    suf = np.array([v for m in mg for v in m[1:]], float)
    ch = np.cumsum(np.concatenate([[0], X - 1]))
    bh = nat['Q2 jami (max score)']['fit']['sodda']['p'][1]
    res = {'N': int(len(X)), 'ozak': int(len(roots)), 'qoshimcha': int(len(suf)), 'seed': SEED_11C,
           'ichki_bootstrap': ICHKI_BOOT, 'ichki_seed': SEED_11, 'b_haqiqiy': bh}
    for nom, ozi in (("tasodifiy o'zak + tasodifiy qo'shimchalar", False), ("o'z o'zagi + tasodifiy qo'shimchalar", True)):
        rng, ri = np.random.default_rng(SEED_11C), np.random.default_rng(SEED_11)
        b, S = [], []
        for _ in range(TAKROR_8C):
            Rv = roots if ozi else rng.permutation(roots)
            cs = np.concatenate([[0.0], np.cumsum(rng.permutation(suf))])
            bb, sh = _mezon(X, (Rv + cs[ch[1:]] - cs[ch[:-1]]) / X, ri)
            b.append(bb)
            S.append(sh)
        res[nom] = _mezon_yigindi(b, S, bh)
    return res


def _eta2(x, m):
    _, inv = np.unique(x, return_inverse=True)
    n = np.bincount(inv)
    s = np.bincount(inv, weights=m)
    return float(((s ** 2 / n).sum() - m.sum() ** 2 / len(m)) / ((m - m.mean()) ** 2).sum())


def e11d(tb, X2, mg, q3):
    x1, _, L, _ = T.q1_xy(tb, 'tor')
    m3 = np.array(q3['x']) * np.array(q3['y'])
    if np.abs(m3 - np.round(m3)).max() > 1e-9:
        raise SystemExit("TO'XTA — E11d: Q3 m butun son emas")
    out = {'permutatsiya': PERM_11D, 'seed': SEED_11}
    for nom, x, m in (('klauza · tor (m — so\'z, x — klauza)', x1, [sum(u) for u in L]),
                      ('morfema · standart (m — grafema, x — morfema)', X2, [sum(z) for z in mg]),
                      ("bo'g'in (m — grafema, x — bo'g'in)", q3['x'], np.round(m3))):
        x, m = np.asarray(x), np.asarray(m, float)
        e = _eta2(x, m)
        rng = np.random.default_rng(SEED_11)
        P = np.array([_eta2(x, rng.permutation(m)) for _ in range(PERM_11D)])
        ge = int((P >= e).sum())
        out[nom] = {'N': int(len(x)), 'x_qiymatlar': int(len(set(x.tolist()))), 'eta2': e, 'perm_median': float(np.median(P)),
                    'perm_max': float(P.max()), 'perm_ge_kuzatilgan': ge, 'p': (ge + 1) / (PERM_11D + 1)}
    return out


def e11e(q2, q3, X2, mg, kor):
    import inspect
    out = {'Q2 standart': {}, 'Q3': {}}
    for daraja, q in (('Q2 standart', q2), ('Q3', q3)):
        x, y, k = np.array(q['x']), np.array(q['y'], float), np.array(q['korpus'])
        for m in ('K1', 'K2', 'treebank'):
            out[daraja][m] = _qisqa(T.qator(x[k == m], y[k == m], f'E11e {daraja} {m}'))
    arr = _qism_q2(X2, mg)
    for m in ('K1', 'K2', 'treebank'):
        t = _tayanch(*(a[kor == m] for a in arr))['i']
        out['Q2 standart'][m].update({'b_mix_i': t['b_mix'], 'b_mix_i_95': t['b_mix_95'], 'pasayish_ulushi_i': t['pasayish_ulushi'],
                                      'pasayish_ulushi_i_95': t['pasayish_ulushi_95']})
    out['klaster_qatlamlanganmi'] = {
        'javob': "yo'q",
        'kod': [l.strip() for l in inspect.getsource(_klaster_boot).splitlines() if 'rng.integers' in l or 'G = len(gid)' in l]}
    return out


def e11f():
    import inspect
    src = lambda fn, kk: [l.strip() for l in inspect.getsource(fn).splitlines() if any(k in l for k in kk)]  # noqa: E731
    return {'kod': {'tahlil.q1_xy': src(T.q1_xy, ('y.append',)), 'tahlil.q2_q3': src(T.q2_q3, ("q2['y'].append", "q3['y'].append")),
                    'tahlil.jadval': src(T.jadval, ("'sd'",)), 'tahlil.rasm': src(T.rasm, ('ee = ',))},
            'birlik': "har butunning o'rtachasi (gap / so'z y qiymati), alohida qismlar emas"}


def e11g(tip, out, nat):
    X, Y, P, Q, Qn = tip
    A2 = [{'x': int(x), 'n': int((X == x).sum()), 'y': float(Y[X == x].mean()), 'R': float(P[X == x].mean()),
           'S': float(Q[X == x].sum() / Qn[X == x].sum()) if x >= 2 else None, 'fitga': bool((X == x).sum() >= NMIN)}
          for x in sorted(set(X.tolist()))]
    q3 = {r['x']: r for r in nat['Q3 jami']['jadval']}
    return {'A2': A2, 'A3 klauza tor': out['E7']['klauza']['tor']['jadval'], 'A3 morfema standart': out['E7']['morfema']['max(score)']['jadval'],
            'Q3 y5 y6': [{k: q3[x][k] for k in ('x', 'n', 'y', 'sd', 'fitga')} for x in (5, 6)],
            'Q3 y6_minus_y5': q3[6]['y'] - q3[5]['y']}


def e11h(tb, K):
    import ud_tools as U
    import naqsh_kesh as NK
    k2 = []
    for g in K['K2']:
        s = sum(map(T.sozmi, g['words']))
        if s > 60:
            k2.append({'x': len(T.klauza_uzunliklari(g['words'], g['v0'])[0]), 'token': len(g['words']), 'soz': s})
    Y = json.loads((T.SUPP / 'data' / 'ud_system_output.json').read_text(encoding='utf-8'))['sentences']
    G = {(g['tb'], g['sent_id']): g for t in U.TREEBANK for g in U.load_treebank(t)}
    if len(Y) != len(tb):
        raise SystemExit("TO'XTA — E11h: treebank gaplari soni teng emas")
    c = {v: Counter() for v in ('keng', 'tor')}
    for rec, y in zip(tb, Y):
        g = G[(y['tb'], y['sent_id'])]
        if g['text'] != rec['text']:
            raise SystemExit("TO'XTA — E11h: gap tartibi mos emas")
        toks = [t for t in g['tokenlar'] if t['upos'] != 'PUNCT']
        for v, var in (('keng', T.KENG), ('tor', T.TOR)):
            u = {t: k for k, (_, ids) in enumerate(NK.daraxt_bolinishi(g, var)) for t in ids}
            c[v]['birliksiz_token'] += sum(t['id'] not in u for t in toks)
            for a, b in zip(toks, toks[1:]):
                if u.get(a['id']) != u.get(b['id']):
                    c[v]['chegara'] += 1
                    c[v]['oldida_VERB'] += a['upos'] == 'VERB'
                    c[v]['oldida_VERB_AUX'] += a['upos'] in U.PREDIKAT_UPOS
    ch = {v: {**d, 'ulush_VERB': d['oldida_VERB'] / d['chegara'], 'ulush_VERB_AUX': d['oldida_VERB_AUX'] / d['chegara']}
          for v, d in ((v, dict(d)) for v, d in c.items())}
    return {'K2_60dan_uzun': sorted(k2, key=lambda r: -r['soz']), 'K2_gap': len(K['K2']), 'chegara': ch}


def e11(tb, K, Tk, A, out, q2, q3):
    nat = json.loads((NATIJA / 'natija.json').read_text(encoding='utf-8'))['qatorlar']
    B, _ = e5_birliklar(tb)
    M = qism_massivlari(B, Tk, A)
    X2, _, mg, kor = _q2_massiv(Tk, A, q2)
    tip = _tip_massivlari(Tk, A)
    return {'a': e11a(M, tip, nat, out['E8']['b']), 'b': e11b(B, tb, out), 'c': e11c(X2, mg, nat), 'd': e11d(tb, X2, mg, q3),
            'e': e11e(q2, q3, X2, mg, kor), 'f': e11f(), 'g': e11g(tip, out, nat), 'h': e11h(tb, K)}


def e11_md(o):
    E = o['E11']
    f4 = lambda v: f(v, 4) if v is not None else '—'  # noqa: E731
    ci = lambda c, r=3: f"[{f(c[0], r)}; {f(c[1], r)}]" if c else '—'  # noqa: E731
    ha = lambda v: 'ha' if v else "yo'q"  # noqa: E731
    s = ['## E11 (post hoc 5)', '', '### E11a — giperbola y = β + α/x', '',
         "n-vaznli kichik kvadratlar (n ≥ 30 kataklar, tahlil.py dagi kataklar; parametrlar chiziqli — NLS yechimi aniq, curve_fit bilan "
         f"tekshirilgan). 95 % — kuzatuv bootstrapi ({BOOT}, seed {SEED}; P(1), S(2) E8b (i) bilan aynan). R² — n-vaznli.", '',
         '| qator | N | kataklar | α [95 %] | β [95 %] | R² | P(1) − S(2) [95 %] | S(2) [95 %] | α − (P(1) − S(2)) [95 %] | β − S(2) [95 %] |',
         '|---|---|---|---|---|---|---|---|---|---|']
    for nom, r in E['a'].items():
        s.append(f"| {nom} | {r['N']} | {r['kataklar']} | {f(r['alfa'])} {ci(r['alfa_95'])} | {f(r['beta'])} {ci(r['beta_95'])} | {f(r['r2'], 4)} | "
                 f"{f(r['P1_minus_S2'])} {ci(r['P1_minus_S2_95'])} | {f(r['S2'])} {ci(r['S2_95'])} | "
                 f"{f(r['alfa_minus_P1_S2'])} {ci(r['alfa_minus_P1_S2_95'])} | {f(r['beta_minus_S2'])} {ci(r['beta_minus_S2_95'])} |")
    b = E['b']
    s += ['', '### E11b — prereg mezoni nol modellar ostida (klauza, tor)', '',
          f"Har takrorda: b < 0; 95 % oraliq ({b['ichki_bootstrap']} takrorli kuzatuv bootstrapi, seed {b['ichki_seed']}) yuqori chegarasi < 0 "
          "(tahlil.hukm); n ≥ 30 kataklarda qat'iy kamayish. Takror b qiymatlari E10g bilan teng (max |farq|: turlarni saqlovchi "
          f"{b['E10g_max_farq_turlarni_saqlovchi']:.1e}, B&Č {b['E10g_max_farq_BC']:.1e}; nuqta b jadval o'rtachalaridan, tahlil.qator dagidek).", '',
          '| model | seed | takror | b mediana [95 %] | b < 0 | oraliq 0 siz | monoton | uchalasi (N) |', '|---|---|---|---|---|---|---|---|']
    for nom, r in b.items():
        if isinstance(r, dict):
            s.append(f"| {nom} | {r['seed']} | {r['takror']} | {f(r['mediana'])} {ci(r['95'])} | {r['b_manfiy']} | {r['oraliq_0siz']} | "
                     f"{r['monoton']} | {r['uchalasi_N']} |")
    c = E['c']
    s += ['', '### E11c — morfema nol modeli (standart tahlil)', '',
          f"N = {c['N']} token; o'zak havzasi {c['ozak']}, qo'shimcha havzasi {c['qoshimcha']}; x taqsimoti haqiqiy; {TAKROR_8C} takror, "
          f"seed {c['seed']}; ichki bootstrap {c['ichki_bootstrap']} (seed {c['ichki_seed']}). Kuzatilgan b = {f(c['b_haqiqiy'], 4)}.", '',
          '| variant | b mediana | 95 % | min / max | b < 0 | b ≤ kuzatilgan | oraliq 0 siz | monoton | uchalasi (N) |',
          '|---|---|---|---|---|---|---|---|---|']
    for nom, r in c.items():
        if isinstance(r, dict):
            s.append(f"| {nom} | {f(r['mediana'], 4)} | {ci(r['95'], 4)} | {f(r['min_max'][0], 4)} / {f(r['min_max'][1], 4)} | {r['b_manfiy']} | "
                     f"{r['b_le_haqiqiy']} | {r['oraliq_0siz']} | {r['monoton']} | {r['uchalasi_N']} |")
    d = E['d']
    s += ['', '### E11d — m va x: korrelyatsiya nisbati η²', '',
          f"η² = SS_oraliq(m | x) / SS_jami(m); permutatsiya {d['permutatsiya']} (m aralashtiriladi, seed {d['seed']}); p = (#{{η²_perm ≥ η²}} + 1)/"
          f"({d['permutatsiya']} + 1).", '',
          '| daraja | N | x qiymatlari | η² | permutatsiya mediana | permutatsiya max | ≥ kuzatilgan | p |', '|---|---|---|---|---|---|---|---|']
    for nom, r in d.items():
        if isinstance(r, dict):
            s.append(f"| {nom} | {r['N']} | {r['x_qiymatlar']} | {f(r['eta2'], 4)} | {f(r['perm_median'], 6)} | {f(r['perm_max'], 6)} | "
                     f"{r['perm_ge_kuzatilgan']} | {f(r['p'], 4)} |")
    e = E['e']
    s += ['', '### E11e — manba bo\'yicha', '', f'95 % — token bootstrap (tahlil.qator, {BOOT}, seed {SEED}).', '',
          '| daraja | manba | N | kataklar | b [95 %] | monoton | hukm | b_mix (i) [95 %] | pasayish ulushi (i) [95 %] |',
          '|---|---|---|---|---|---|---|---|---|']
    for daraja in ('Q2 standart', 'Q3'):
        for m, r in e[daraja].items():
            mix = (f"{f(r['b_mix_i'])} {ci(r['b_mix_i_95'])} | {f(r['pasayish_ulushi_i'])} {ci(r['pasayish_ulushi_i_95'])}"
                   if 'b_mix_i' in r else '— | —')
            s.append(f"| {daraja} | {m} | {r['N']} | {r['kataklar']} | {f(r['b'])} {ci(r['b_95'])} | {ha(r['monoton'])} | {r['hukm']} | {mix} |")
    s += ['', f"Klasterli bootstrap (E8a) manba bo'yicha qatlamlangan: **{e['klaster_qatlamlanganmi']['javob']}** — `_klaster_boot`:", '',
          '```python', *e['klaster_qatlamlanganmi']['kod'], '```', '',
          '### E11f — tahlil.py rasmlaridagi xato chiziqlari', '', '```python']
    for fn, kk in E['f']['kod'].items():
        s += [f'# {fn}', *kk]
    s += ['```', '', f"SD birligi: **{E['f']['birlik']}**; xato chizig'i ±1,96·SD/√n, n — katakdagi butunlar soni.", '']
    g = E['g']
    s += ['### E11g — jadvallar', '', '**A2 — Q2 tiplar bo\'yicha kataklar**', '', '| x | n | ȳ | R(x) | S(x) | fitga |', '|---|---|---|---|---|---|']
    s += [f"| {r['x']} | {r['n']} | {f(r['y'])} | {f(r['R'])} | {f(r['S']) if r['S'] is not None else '—'} | {ha(r['fitga'])} |" for r in g['A2']]
    s += ['', '**A3 — klauza tor (E7, yaxlitlanmagan qiymatlardan 3 o\'nlik)**', '', '| k | n | M(k) | S(k) | y(k) | fitga |', '|---|---|---|---|---|---|']
    s += [f"| {r['x']} | {r['n']} | {f(r['M'])} | {f(r['S']) if r['S'] is not None else '—'} | {f(r['y'])} | {ha(r['fitga'])} |" for r in g['A3 klauza tor']]
    s += ['', '**A3 — morfema standart (E7)**', '', '| x | n | R(x) | S(x) | y(x) | fitga |', '|---|---|---|---|---|---|']
    s += [f"| {r['x']} | {r['n']} | {f(r['R'])} | {f(r['S']) if r['S'] is not None else '—'} | {f(r['y'])} | {ha(r['fitga'])} |"
          for r in g['A3 morfema standart']]
    s += ['', '**Q3 y(5), y(6)**', '', '| x | n | ȳ (4 o\'nlik) | SD | fitga |', '|---|---|---|---|---|']
    s += [f"| {r['x']} | {r['n']} | {f4(r['y'])} | {f4(r['sd'])} | {ha(r['fitga'])} |" for r in g['Q3 y5 y6']]
    s += ['', f"y(6) − y(5) = {f(g['Q3 y6_minus_y5'], 6)}", '']
    h = E['h']
    s += ['### E11h — K2 uzun gaplar va chegara to\'liqligi yuqori chegarasi', '',
          f"K2 da 60 so'zdan uzun gaplar: {len(h['K2_60dan_uzun'])} / {h['K2_gap']} (x — V0 birliklari).", '',
          "| # | so'z | token | x |", '|---|---|---|---|']
    s += [f"| {i} | {r['soz']} | {r['token']} | {r['x']} |" for i, r in enumerate(h['K2_60dan_uzun'], 1)]
    s += ['', "Oltin chegaralar (treebank, UD non-PUNCT tokenlar ketma-ketligi, qo'shni tokenlar birligi har xil); oldidagi token UPOS (oltin).", '',
          "| ta'rif | chegara | oldida VERB | ulush | oldida VERB/AUX | ulush | birliksiz token |", '|---|---|---|---|---|---|---|']
    for v in ('keng', 'tor'):
        r = h['chegara'][v]
        s.append(f"| {v} | {r['chegara']} | {r['oldida_VERB']} | {f(100 * r['ulush_VERB'], 1)} % | {r['oldida_VERB_AUX']} | "
                 f"{f(100 * r['ulush_VERB_AUX'], 1)} % | {r.get('birliksiz_token', 0)} |")
    s.append('')
    return s


# ---------------------------------------------------------------- rasm
def rasm_e1(R, yol):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 3, figsize=(15, 4))
    for ax, (nom, jad) in zip(axs, R.items()):
        J = [r for r in jad if r['n'] >= NMIN]
        xx = [r['x'] for r in J]
        ax.plot(xx, [r['y'] for r in J], 'o-', color='#1f4e79', label='kuzatilgan ȳ')
        ax.plot(xx, [r['aralashma'] for r in J], 's--', color='#c0392b', label='aralashma S + (R − S)/x')
        ax.plot(xx, [r['ozak'] for r in J], '^:', color='#27864a', label="o'zak (grafema)")
        ax.plot(xx, [r['qoshimcha'] for r in J], 'v:', color='#8e6c00', label='qo\'shimcha (grafema)')
        for r in J:
            if 'farq_95' in r:
                lo, hi = r['farq_95']
                ax.vlines(r['x'], r['aralashma'] + lo, r['aralashma'] + hi, color='#c0392b', alpha=.35, lw=6)
        ax.set_title(f'Q2 · {nom}', fontsize=10)
        ax.set_xlabel('x = morfema soni')
        ax.set_ylabel('grafema')
        ax.grid(alpha=.3)
        ax.legend(fontsize=7)
    fig.suptitle('E1 (POST HOC) — Q2 ajratish; qizil ustun: kuzatilgan − aralashma, 95 % bootstrap (n ≥ 30, x ≥ 3)', fontsize=10)
    fig.tight_layout()
    fig.savefig(yol, dpi=130)
    plt.close(fig)


def rasm_e2(E, yol):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 4, figsize=(20, 4))
    rang = {'Q2 namunasi': '#1f4e79', "noma'lum": '#c0392b', 'yuza teng emas': '#8e6c00', 'hammasi': '#555555'}
    for ax, korpus in zip(axs, ('jami', 'K1', 'K2', 'treebank')):
        for guruh, J in E[korpus].items():
            J = [r for r in J if r['n'] >= NMIN]
            if J:
                ax.plot([r['x'] for r in J], [r['y'] for r in J], 'o-' if guruh != 'hammasi' else '--',
                        color=rang[guruh], label=guruh, ms=4)
        ax.set_title(f'Q3 · {korpus}', fontsize=10)
        ax.set_xlabel("x = bo'g'in (unli) soni")
        ax.set_ylabel("ȳ = bo'g'indagi o'rtacha grafema")
        ax.grid(alpha=.3)
        if ax.get_legend_handles_labels()[0]:
            ax.legend(fontsize=7)
    fig.suptitle("E2 (POST HOC) — Q3 guruh bo'yicha (faqat n ≥ 30 kataklar)", fontsize=10)
    fig.tight_layout()
    fig.savefig(yol, dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------- hisobot
def hisobot(o):
    s = ['# MENZERATH-1 — POST HOC tekshiruvlar', '',
         '> **POST HOC — prereg\'da yo\'q, natijadan keyin rejalashtirilgan, tasdiqlovchi emas.** Prereg hukmlari '
         '(`natija.md`) o\'zgarmaydi. Barcha raqamlar tavsifiy.', '',
         f"Skript `posthoc.py` sha256 `{o['langar']['posthoc_sha256']}` · `tahlil.py` (import, o'zgarmagan) `{o['langar']['tahlil_sha256'][:12]}…` · "
         f"commit `{o['langar']['commit']}` · DB md5 `{o['langar']['db_md5']}` (oxiri `{o['langar']['db_md5_oxiri']}`) · seed {SEED} · bootstrap {BOOT}", '',
         f"Moslik nazorati: Q2 namunasi N = {o['nazorat']['q2_N']} (natija.json {o['nazorat']['q2_N_natija']}), "
         f"Q3 N = {o['nazorat']['q3_N']} (natija.json {o['nazorat']['q3_N_natija']}), ȳ jadvallari aynan: {o['nazorat']['aynan']}.", '']
    s += ['## E1 (post hoc) — Q2: o\'zak va qo\'shimcha uzunligi, «doimiy R, S» aralashma modeli', '',
          'Aralashma: har so\'z = 1 o\'zak (R grafema) + (x − 1) qo\'shimcha (S grafema) → y(x) = S + (R − S)/x. '
          'R = ȳ(1), S = 2·ȳ(2) − ȳ(1) (model x = 1 va x = 2 dan aniq o\'tadi). Farq = kuzatilgan − aralashma; 95 % — token bootstrap. '
          'R(x), S(x) oraliqlari (post hoc 2) — o\'sha bootstrap takrorlaridan, n ≥ 30 kataklar.', '']
    for nom, v in o['E1'].items():
        s += [f"**{nom}** (N = {v['N']}): R = {f(v['R'])} [{f(v['R_95'][0])}; {f(v['R_95'][1])}], "
              f"S = {f(v['S'])} [{f(v['S_95'][0])}; {f(v['S_95'][1])}]", '',
              "| x | n | o'rtacha o'zak R(x) | 95 % | o'rtacha qo'shimcha S(x) | 95 % | kuzatilgan ȳ | aralashma | farq | 95 % (farq) |",
              '|---|---|---|---|---|---|---|---|---|---|']

        def ci(r, k):
            return f"[{f(r[k][0])}; {f(r[k][1])}]" if k in r else '—'
        for r in v['jadval']:
            s.append(f"| {r['x']} | {r['n']} | {f(r['ozak'])} | {ci(r, 'ozak_95')} | {f(r['qoshimcha'])} | {ci(r, 'qoshimcha_95')} | "
                     f"{f(r['y'])} | {f(r['aralashma'])} | {f(r['farq'])} | {ci(r, 'farq_95')} |")
        s.append('')
    s += ['## E2 (post hoc) — Q3: tahlil qilingan vs noma\'lum so\'zlar', '',
          'Guruhlar: «Q2 namunasi» (tahlil qilingan, yuzaga teng; ng chegarasi analizatordan), «noma\'lum» (UNKNOWN), '
          '«yuza teng emas» (tahlil bor, yuzaga teng emas). Q3 qoidasi tahlil.py dagidek (tuzatish_1 bilan).', '']
    for korpus in ('jami', 'K1', 'K2', 'treebank'):
        E = o['E2'][korpus]
        xs = sorted({r['x'] for J in E.values() for r in J})
        idx = {g: {r['x']: r for r in J} for g, J in E.items()}
        s += [f'**{korpus}**', '', "| x | Q2 namunasi: n | ȳ | noma'lum: n | ȳ | yuza teng emas: n | ȳ | hammasi: n | ȳ |",
              '|---|---|---|---|---|---|---|---|---|']
        for x in xs:
            row = [str(x)]
            for g in ('Q2 namunasi', "noma'lum", 'yuza teng emas', 'hammasi'):
                r = idx[g].get(x)
                row += [str(r['n']) if r else '0', f(r['y']) if r else '—']
            s.append('| ' + ' | '.join(row) + ' |')
        s.append('')
    t = o['E2']['x_ge_7_tarkib']
    jt = sum(t.values())
    s += [f"x ≥ 7 kataklar tarkibi (jami {jt} token): " + ', '.join(f"{g} {n} ({f(100 * n / jt, 1)} %)" for g, n in
                                                                   sorted(t.items(), key=lambda z: -z[1])) + '.', '']
    e3 = o['E3']
    s += ['## E3 (post hoc) — Q1 treebank: UT vs UzUDT; janr', '',
          f"UzUDT janr belgisi: {e3['uzudt_janr_belgisi']}. UT janri sent_id bo'yicha (README): 1–250 yangilik, 251–500 badiiy.", '',
          T.FIT_SARLAVHA]
    for k, q in e3['qatorlar'].items():
        s.append(T.fit_qatori(q))
    s.append('')
    for nom, k in (('UT − UzUDT', 'UT_minus_UzUDT'), ('UT yangilik − UT badiiy', 'yangilik_minus_badiiy')):
        d = e3[k]
        s.append(f"- Δb (sodda) {nom}: {f(d['nuqta'])} [{f(d['oraliq'][0])}; {f(d['oraliq'][1])}] (mustaqil bootstrap, {d['takror']} juft takror)"
                 if d else f'- Δb {nom}: aniqlanmagan')
    s.append('')
    for k, q in e3['qatorlar'].items():
        s += [T.jadval_md(q), '']
    e4 = o['E4']
    s += ['## E4 (post hoc) — Q1 K1 VDU: faqat tutuq belgisidan iborat tokenlar', '',
          f"- K1 da faqat tutuq belgisidan iborat token: {e4['tutuq_token']} ta, {e4['gap']} gapda.",
          f"- Q1 da so'z sifatida sanalganmi: **{'ha' if e4['sozmi_true'] else 'yo' + chr(39) + 'q'}** — so'z sanog'i `sozmi` "
          f"(kamida bitta harf-raqam belgisi) bilan; bunday tokenlardan {e4['sozmi_true']} tasi so'z deb sanalgan.",
          f"- Ularsiz qayta hisob: jadval asl bilan aynan — **{'ha' if e4['tutuqsiz_aynan'] else 'yo' + chr(39) + 'q'}**.",
          f"- Qo'shnilar: oldida so'z {e4['oldin_soz']} ({e4['oldin_o_g']} tasida oldingi so'z o/g bilan tugaydi — o'/g' "
          f"bo'linishi), keyinida so'z {e4['keyin_soz']}. Ya'ni tutuq tokeni ko'pincha bitta so'zni ikki «so'z»ga bo'lgan.",
          f"- Qo'shimcha (so'ralmagan, tavsifiy): so'z + tutuq + so'z → bitta so'z, {e4['birlashtirildi']} birlashtirish.", '',
          T.FIT_SARLAVHA, T.fit_qatori(e4['asl']), T.fit_qatori(e4['tutuqsiz']), T.fit_qatori(e4['birlashtirilgan']), '',
          T.jadval_md(e4['birlashtirilgan']), '',
          *e5_e6_md(o),
          *e7_md(o),
          *(e8_md(o) if 'E8' in o else []),
          *(e10_md(o) if 'E10' in o else []),
          *(e11_md(o) if 'E11' in o else []),
          '## Rasmlar', '', '- `rasm_e1.png` — E1: kuzatilgan ȳ, aralashma bashorati, o\'zak va qo\'shimcha uzunligi (uchala qoida).',
          '- `rasm_e2.png` — E2: Q3 ȳ guruh va korpus bo\'yicha (n ≥ 30 kataklar).',
          '- `rasm_e5.png` — E5: Q1 treebank ȳ, aralashma, bosh klauza M(k) va ergash klauza S(k) (tor, keng).',
          '- `rasm_e7.png` — E7: klauza (tor) va morfema (max(score)): ȳ, sof aralashma, M(k)/R(x), S(k)/S(x).', '']
    return '\n'.join(s)


def e5_e6_md(o):
    s = ['## E5 (post hoc 2) — Q1 treebank: bosh (root) va ergash klauzalar', '',
         'Har gap: M = bosh klauza (bosh tokeni deprel `root`) uzunligi, S = ergash klauzalar o\'rtacha uzunligi (PUNCT siz so\'z). '
         'Aralashma: y(k) = [M + (k − 1)·S]/k, M = ȳ(1), S = 2·ȳ(2) − ȳ(1). 95 % — gap darajasidagi bootstrap (1 000, seed 20261021). '
         'k, ȳ Q1 bilan aynan (tekshirilgan).', '']
    for kalit, v in o['E5'].items():
        s += [f"**{kalit}** (N = {v['N']}; bosh klauzasi so\'zsiz qolgan gap {v['root_bosh_klauza_bosh_qolgan_gap']}): "
              f"M = {f(v['M0'])} [{f(v['M0_95'][0])}; {f(v['M0_95'][1])}], S = {f(v['S0'])} [{f(v['S0_95'][0])}; {f(v['S0_95'][1])}]; "
              f"bosh klauza o\'rtacha {f(v['bosh_klauza_ortacha'])} (SD {f(v['bosh_klauza_sd'])})", '',
              '| k | n | M(k) | 95 % | S(k) | 95 % | kuzatilgan ȳ | aralashma | farq | 95 % (farq) |',
              '|---|---|---|---|---|---|---|---|---|---|']
        for r in v['jadval']:
            c = lambda k: f"[{f(r[k][0])}; {f(r[k][1])}]" if k in r else '—'  # noqa: E731
            s.append(f"| {r['k']} | {r['n']} | {f(r['M'])} | {c('M_95')} | {f(r['S'])} | {c('S_95')} | {f(r['y'])} | "
                     f"{f(r['aralashma'])} | {f(r['farq'])} | {c('farq_95')} |")
        s += ['', f'Ergash klauza uzunligi turi bo\'yicha ({kalit}; bosh tokenining deprel asosi; faqat tavsif):', '',
              '| deprel | n | ulush | o\'rtacha so\'z | SD |', '|---|---|---|---|---|']
        for r in v['ergash_tur']:
            s.append(f"| {r['deprel']} | {r['n']} | {f(100 * r['ulush'], 1)} % | {f(r['ortacha'])} | {f(r['sd'])} |")
        s.append('')
    e6 = o['E6']
    q = e6['qator']
    s += ['## E6 (post hoc 2) — Q3 faqat tahlil qilingan so\'zlarda (Q2 namunasi)', '',
          'Prereg §4 usuli (n-vaznli NLS, bootstrap 1 000, §4.4 mezoni) — **post hoc**, prereg hukmini almashtirmaydi.', '',
          T.FIT_SARLAVHA, T.fit_qatori(q), '',
          f"Hukm (post hoc): **{q['hukm']['hukm']}** — b < 0: {q['hukm'].get('b_manfiy')}, oraliq 0 siz: "
          f"{q['hukm'].get('oraliq_0siz')}, monoton: {q['hukm'].get('monoton')}.", '', T.jadval_md(q), '',
          '1 bo\'g\'inli so\'zlar (x = 1): yopiq bo\'g\'in = oxirgi grafema undosh (a, e, i, o, u, o\' emas). Faqat tavsif.', '',
          '| korpus · guruh | n | yopiq | yopiq ulush | ȳ (yopiq) | ȳ (ochiq) |', '|---|---|---|---|---|---|']
    for k, r in e6['bir_bogin'].items():
        s.append(f"| {k} | {r['n']} | {r['yopiq']} | {f(100 * r['yopiq_ulush'], 1)} % | {f(r['y_yopiq'])} | {f(r['y_ochiq'])} |")
    s.append('')
    return s


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--db', required=True)
    a = p.parse_args()
    m = json.loads((SIKL / 'MANIFEST.json').read_text(encoding='utf-8'))
    ps = sha256(__file__)
    eski = None
    if (NATIJA / 'posthoc.json').exists():                    # run-once — shu VERSIYA uchun (post hoc 2 kengaytmasi)
        eski = json.loads((NATIJA / 'posthoc.json').read_text(encoding='utf-8'))
        if eski['langar']['posthoc_sha256'] == ps:
            raise SystemExit("TO'XTA — posthoc.py ning shu versiyasi allaqachon yurgan (run-once)")
    if f'posthoc.py sha256 {ps}' not in json.dumps(m['bosqichlar'], ensure_ascii=False):
        raise SystemExit("TO'XTA — posthoc.py sha256 MANIFEST bosqichlarida yo'q")
    db0 = T.md5(T.DB)
    if T.md5(a.db) != db0:
        raise SystemExit("TO'XTA — --db nusxasi md5 ishchi DB ga teng emas")
    tb, _ = T.treebank_birliklar()
    K = {k: T.k_birliklar(k)[0] for k in ('K1', 'K2')}
    Tk = T.tokenlar(tb, K)
    turlar = {T.tozala(w) for _, w in Tk}
    turlar = {t for t in turlar if T.tok_toifa(t) is None}
    an = T.Analizator(a.db)
    try:
        A = an.tahlil(turlar)
        kodlar = qoshimcha_kodlari(an, A)                   # E8g: max(score) tahlilining element kodlari
    finally:
        an.yop()
    # moslik nazorati: tahlil.py natijasi bilan
    nat = json.loads((NATIJA / 'natija.json').read_text(encoding='utf-8'))
    _, q2, _, q3, _, _ = T.q2_q3(Tk, A)
    jq2 = T.jadval(q2['x'], q2['y'])
    jq3 = T.jadval(q3['x'], q3['y'])
    aynan = (jq2 == nat['qatorlar']['Q2 jami (max score)']['jadval'] and jq3 == nat['qatorlar']['Q3 jami']['jadval'])
    if not aynan:
        raise SystemExit("TO'XTA — moslik nazorati: Q2/Q3 jadvallari natija.json dan farq qiladi")
    out = {'langar': {'posthoc_sha256': ps, 'tahlil_sha256': sha256(SIKL / 'tahlil.py'), 'db_md5': db0,
                      'commit': subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=REPO, capture_output=True,
                                               text=True).stdout.strip()},
           'nazorat': {'q2_N': len(q2['x']), 'q2_N_natija': nat['qatorlar']['Q2 jami (max score)']['N'],
                       'q3_N': len(q3['x']), 'q3_N_natija': nat['qatorlar']['Q3 jami']['N'], 'aynan': aynan}}
    out['E1'], r1 = e1(Tk, A)
    out['E2'] = e2(Tk, A)
    obs = out['E2'].pop('_obs')
    if out['E2']['N'] != len(q3['x']):
        raise SystemExit("TO'XTA — E2 Q3 N tahlil.py dagidan farq qiladi")
    out['E3'] = e3(tb)
    out['E4'] = e4(K['K1'])
    out['E5'], r5 = e5(tb)
    out['E6'] = e6(obs)
    out['E7'], r7 = e7(tb, Tk, A, out)
    out['E8'] = e8(tb, K, Tk, A, out, q2, q3, kodlar)
    out['E10'] = e10(tb, K, Tk, A, kodlar, out, q2, q3)
    out['E11'] = e11(tb, K, Tk, A, out, q2, q3)
    if eski is not None:                                     # avvalgi versiya bilan: undagi har bo'lim (E1–E7, E8 qismlari) aynan
        bolim = ([k for k in ('E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7') if k in eski] + ['E8' + k for k in eski.get('E8', {})]
                 + ['E10' + k for k in eski.get('E10', {})] + ['E11' + k for k in eski.get('E11', {})])
        ol = lambda d, k: d[k[:3]][k[3:]] if k[:3] in ('E10', 'E11') else (d['E8'][k[2:]] if k.startswith('E8') else d[k])  # noqa: E731
        tuzatilgan = 'k' in eski.get('E8', {})               # E8k tuzatishidan keyingi versiya: hammasi aynan
        if tuzatilgan:
            out['E8']['k']['iii_eski'] = eski['E8']['k']['iii_eski']
        bolim_aynan = [k for k in bolim if tuzatilgan or k != 'E8b']
        ok = all(json.loads(json.dumps(ol(out, k), ensure_ascii=False)) == ol(eski, k) for k in bolim_aynan)
        if 'b' in eski.get('E8', {}) and not tuzatilgan:      # E8k tuzatishi: faqat klauza (iii) o'zgaradi, qolgani 1e-9 gacha
            yb = json.loads(json.dumps(out['E8']['b'], ensure_ascii=False))
            ok = ok and all(_yaqin({v: d for v, d in yb[n].items() if not (n.startswith('klauza') and v == 'iii')},
                                   {v: d for v, d in eski['E8']['b'][n].items() if not (n.startswith('klauza') and v == 'iii')})
                            for n in eski['E8']['b'])
            out['E8']['k']['iii_eski'] = {n: {k: eski['E8']['b'][n]['iii'][k] for k in ('P0', 'S0', 'b_mix', 'b_mix_95',
                                                                                        'pasayish_ulushi', 'pasayish_ulushi_95')}
                                          for n in eski['E8']['b'] if n.startswith('klauza')}
        out['nazorat'] = {k: v for k, v in out['nazorat'].items() if not k.startswith('avvalgi_versiya')}
        out['nazorat']['avvalgi_versiya_aynan_bolimlar'] = bolim
        out['nazorat']['avvalgi_versiya_aynan'] = ok
        out['nazorat']['avvalgi_versiya_sha256'] = eski['langar']['posthoc_sha256']
        if not ok:
            raise SystemExit(f"TO'XTA — {bolim} avvalgi posthoc.json dan farq qiladi")
    if T.md5(T.DB) != db0:
        raise SystemExit("TO'XTA — ishchi DB md5 o'zgardi")
    out['langar']['db_md5_oxiri'] = T.md5(T.DB)
    (NATIJA / 'posthoc.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    rasm_e1(r1, NATIJA / 'rasm_e1.png')
    rasm_e2(out['E2'], NATIJA / 'rasm_e2.png')
    rasm_e5(r5, NATIJA / 'rasm_e5.png')
    rasm_e7(r7, NATIJA / 'rasm_e7.png')
    (NATIJA / 'posthoc.md').write_text(hisobot(out), encoding='utf-8')
    print('tayyor')


if __name__ == '__main__':
    main()
