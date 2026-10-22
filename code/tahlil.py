# -*- coding: utf-8 -*-
"""MENZERATH-1 — TAHLIL (muzlatilgan skript; prereg.md + tuzatish_1.md ni so'zma-so'z amalga oshiradi).

Ishlatish (repo ildizidan, BIR MARTA):
    python3 analysis/menzerath-1/tahlil.py --db NUSXA.db       # -> natija/natija.json, natija.md, rasm_*.png

Himoyalar:
  * run-once — `natija/` mavjud bo'lsa TO'XTA;
  * skript sha256 i MANIFEST bosqichlarida «tahlil.py sha256 <qiymat>» ko'rinishida bo'lishi shart (muzlatilgan holat);
  * prereg.md va tuzatish_1.md sha256 i MANIFEST bosqichlaridagi qiymatlarga teng bo'lishi shart;
  * `--db` — `instance/new_phd.db` NUSXASI (md5 teng); ishchi DB md5 oxirida qayta tekshiriladi.
Analizator (`MorphologyService._analyze_word_hisobla`) faqat o'qiladi; Q4(c) uchun `services.morphology_service.max`
faqat shu jarayon xotirasida o'raladi — fayl o'zgarmaydi. Matn chop etilmaydi va yozilmaydi — faqat sonlar.

Talab: numpy, scipy (`curve_fit`), matplotlib.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import warnings
from collections import Counter
from pathlib import Path

import numpy as np

SIKL = Path(__file__).resolve().parent
REPO = SIKL.parents[1]
SUPP = REPO / 'analysis' / 'ijcl-paket' / 'supplement'
NATIJA = SIKL / 'natija'
DB = REPO / 'instance' / 'new_phd.db'
for _p in (REPO, REPO / 'analysis', REPO / 'analysis' / '_konvensiya', SUPP / 'scripts',
           REPO / 'analysis' / 'ijcl-m2', REPO / 'analysis' / 'ijcl-mustahkamlik'):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

SEED = 20261021
BOOT = 1000
BC_TAKROR = 100
NMIN = 30
TOR, KENG = 'xcomp_aclsiz', 'asosiy'
APOSTROF = {'ʻ': "'", 'ʼ': "'", '‘': "'", '’': "'", '`': "'", '´': "'"}
DEFIS = ('-', '‐', '‑')
ALIFBO = set("abcdefghijklmnopqrstuvwxyz'")
UNLI = {'a', 'e', 'i', 'o', 'u', "o'"}
DIGRAF = ('sh', 'ch', 'ng', "o'", "g'")


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def md5(p):
    return hashlib.md5(Path(p).read_bytes()).hexdigest()


# ---------------------------------------------------------------- §3 normallashtirish va grafema
def apos(s):
    return ''.join(APOSTROF.get(ch, ch) for ch in s)


def tozala(raw):
    """Token -> analizator kirishi: kichik harf, apostrof bitta `'`; chetdagi tinish (Unicode P*, `'` dan
    tashqari) olinadi; boshdagi `'` olinadi; oxirgi `'` faqat o/g dan keyin (o', g') qoladi. Defis qoladi."""
    import unicodedata
    t = apos(raw or '').lower()
    i, j = 0, len(t)
    while i < j and (t[i] == "'" or (unicodedata.category(t[i]).startswith('P') and t[i] not in DEFIS)):
        i += 1
    while j > i and t[j - 1] != "'" and unicodedata.category(t[j - 1]).startswith('P') and t[j - 1] not in DEFIS:
        j -= 1
    t = t[i:j]
    while t.endswith("'") and not (len(t) >= 2 and t[-2] in 'og' and not t.endswith("''")):
        t = t[:-1]
    return t.strip(''.join(DEFIS))


def norm(s):
    """§3: kichik harf, apostrof `'`, defis olib tashlanadi (grafema emas)."""
    t = apos(s or '').lower()
    for d in DEFIS:
        t = t.replace(d, '')
    return t


def grafemalar(soz, chegaralar=()):
    """[grafema] — sh, ch, o', g' har doim bitta; ng faqat chegara (morfema boshi indeksi) n va g orasida
    bo'lmasa bitta. `chegaralar` — normallangan so'zdagi morfema boshlari (0 dan tashqari)."""
    out, i, B = [], 0, set(chegaralar)
    while i < len(soz):
        ikki = soz[i:i + 2]
        if ikki in DIGRAF and not (ikki == 'ng' and (i + 1) in B):
            out.append(ikki)
            i += 2
        else:
            out.append(soz[i])
            i += 1
    return out


def morf_chegaralari(morflar):
    B, k = [], 0
    for m in morflar[:-1]:
        k += len(m)
        B.append(k)
    return B


def unli_soni(gr):
    return sum(1 for g in gr if g in UNLI)


def tok_toifa(t):
    """None = yaroqli; aks holda chiqarish sababi (prereg §2)."""
    n = norm(t)
    if not n:
        return 'tinish'
    if any(ch.isdigit() for ch in n):
        return 'raqam'
    if set(n) - ALIFBO:
        return 'alifbo'
    return None


def sozmi(w):
    """PUNCT siz so'z: kamida bitta harf-raqam belgisi bor."""
    return any(ch.isalnum() for ch in (w or ''))


# ---------------------------------------------------------------- §4.2 fit
def _model_sodda(x, a, b):
    return a * np.power(x, b)


def _model_toliq(x, a, b, c):
    return a * np.power(x, b) * np.exp(-c * x)


def fit(x, ybar, n):
    """Ikkala model, n-vaznli NLS (curve_fit, sigma = 1/sqrt(n)). Natija: {'sodda': {...}|None, 'toliq': ...}."""
    from scipy.optimize import curve_fit, OptimizeWarning
    x, ybar, n = (np.asarray(v, dtype=float) for v in (x, ybar, n))
    K = len(x)
    out = {'K': K}
    ok = (ybar > 0).all()
    if ok and K >= 2:
        w = n / n.sum()
        lx, ly = np.log(x), np.log(ybar)
        mx, my = (w * lx).sum(), (w * ly).sum()
        sxx = (w * (lx - mx) ** 2).sum()
        b0 = (w * (lx - mx) * (ly - my)).sum() / sxx if sxx > 0 else 0.0
        a0 = float(np.exp(my - b0 * mx))
    else:
        a0, b0 = float(ybar.mean()) if K else 1.0, 0.0
    yw = (n * ybar).sum() / n.sum() if K else 0.0
    sst = (n * (ybar - yw) ** 2).sum() if K else 0.0
    for nom, f, p0, kmin in (('sodda', _model_sodda, (a0, b0), 3), ('toliq', _model_toliq, (a0, b0, 0.0), 4)):
        if K < kmin:
            out[nom] = None
            continue
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('error', OptimizeWarning)
                warnings.simplefilter('ignore', RuntimeWarning)
                p, _ = curve_fit(f, x, ybar, p0=p0, sigma=1 / np.sqrt(n), maxfev=20000)
            if not np.all(np.isfinite(p)):
                raise RuntimeError('nochekli')
            wrss = float((n * (ybar - f(x, *p)) ** 2).sum())
            aic = K * np.log(wrss / K) + 2 * len(p) if wrss > 0 else float('-inf')
            out[nom] = {'p': [float(v) for v in p], 'wrss': wrss, 'aic': float(aic),
                        'r2': float(1 - wrss / sst) if sst > 0 else None}
        except (RuntimeError, ValueError, OptimizeWarning, FloatingPointError):
            out[nom] = 'yaqinlashmadi'
    s, t = out.get('sodda'), out.get('toliq')
    if isinstance(s, dict) and isinstance(t, dict):
        out['delta_aic_toliq_minus_sodda'] = t['aic'] - s['aic']
        out['afzal'] = 'toliq' if t['aic'] < s['aic'] - 2 else 'sodda'
    elif isinstance(s, dict):
        out['afzal'] = 'sodda'
    return out


def jadval(x, y):
    x, y = np.asarray(x), np.asarray(y, dtype=float)
    out = []
    for v in sorted(set(x.tolist())):
        m = x == v
        yy = y[m]
        out.append({'x': int(v), 'n': int(m.sum()), 'y': float(yy.mean()),
                    'sd': float(yy.std(ddof=1)) if m.sum() > 1 else None, 'fitga': bool(m.sum() >= NMIN)})
    return out


def qator(x, y, nom, boot=BOOT, toliq_boot=True):
    """Bitta qator: jadval, fit, bootstrap (kuzatuv darajasida qayta tanlash, seed SEED, kataklar asl namunadan),
    §4.4 hukmi. Bir xil N li qatorlar bir xil indekslarni oladi (juft bootstrap)."""
    x = np.asarray(x, dtype=int)
    y = np.asarray(y, dtype=float)
    J = jadval(x, y)
    kat = [r['x'] for r in J if r['fitga']]
    xs = np.array(kat, dtype=float)
    asl = fit(xs, [r['y'] for r in J if r['fitga']], [r['n'] for r in J if r['fitga']])
    kod = np.full(x.max() + 1 if len(x) else 1, -1)
    for i, v in enumerate(kat):
        kod[v] = i
    xk = kod[x]
    m = xk >= 0
    xk_m, y_m = xk[m], y[m]
    idx_all = np.nonzero(m)[0]
    N = len(x)
    rng = np.random.default_rng(SEED)
    B = {'sodda': [], 'toliq': []}
    xato = {'sodda': 0, 'toliq': 0}
    pos = np.full(N, -1)
    pos[idx_all] = np.arange(len(idx_all))
    for _ in range(boot):
        idx = rng.integers(0, N, N)
        sel = pos[idx]
        sel = sel[sel >= 0]
        nn = np.bincount(xk_m[sel], minlength=len(kat))
        ss = np.bincount(xk_m[sel], weights=y_m[sel], minlength=len(kat))
        bor = nn > 0
        r = fit(xs[bor], ss[bor] / nn[bor], nn[bor]) if toliq_boot else _faqat_sodda(xs[bor], ss[bor] / nn[bor], nn[bor])
        for k in ('sodda', 'toliq'):
            v = r.get(k)
            if isinstance(v, dict):
                B[k].append(v['p'])
            elif asl.get(k) is not None and asl.get(k) != 'yaqinlashmadi' and (toliq_boot or k == 'sodda'):
                xato[k] += 1
                B[k].append(None)
            else:
                B[k].append(None)
    oraliq = {}
    for k, nomlar in (('sodda', ('a', 'b')), ('toliq', ('a', 'b', 'c'))):
        P = [p for p in B[k] if p is not None]
        if not P or not isinstance(asl.get(k), dict):
            oraliq[k] = None
            continue
        P = np.array(P)
        oraliq[k] = {nm: [float(np.percentile(P[:, i], 2.5)), float(np.percentile(P[:, i], 97.5))]
                     for i, nm in enumerate(nomlar)}
        oraliq[k]['muvaffaqiyatli'] = len(P)
        oraliq[k]['yaqinlashmagan'] = xato[k]
        oraliq[k]['beqaror'] = xato[k] > 0.05 * boot
    out = {'nom': nom, 'N': int(N), 'jadval': J, 'fit_kataklar': kat, 'fit': asl, 'oraliq': oraliq,
           'hukm': hukm(J, asl, oraliq), '_boot': B}
    return out


def _faqat_sodda(x, ybar, n):
    from scipy.optimize import curve_fit, OptimizeWarning
    if len(x) < 3:
        return {'sodda': None}
    w = n / n.sum()
    lx, ly = np.log(x), np.log(ybar)
    mx, my = (w * lx).sum(), (w * ly).sum()
    sxx = (w * (lx - mx) ** 2).sum()
    b0 = (w * (lx - mx) * (ly - my)).sum() / sxx if sxx > 0 else 0.0
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', OptimizeWarning)
            warnings.simplefilter('ignore', RuntimeWarning)
            p, _ = curve_fit(_model_sodda, x, ybar, p0=(float(np.exp(my - b0 * mx)), b0), sigma=1 / np.sqrt(n), maxfev=20000)
        if not np.all(np.isfinite(p)):
            raise RuntimeError
        return {'sodda': {'p': [float(v) for v in p]}}
    except (RuntimeError, ValueError, OptimizeWarning, FloatingPointError):
        return {'sodda': 'yaqinlashmadi'}


def hukm(J, asl, oraliq):
    """§4.4: b (sodda) < 0, b ning 95 % oralig'i 0 ni o'z ichiga olmaydi, n >= 30 kataklarda y qat'iy kamayadi."""
    s = asl.get('sodda')
    if not isinstance(s, dict) or oraliq.get('sodda') is None:
        return {'hukm': 'aniqlanmagan', 'b_manfiy': None, 'oraliq_0siz': None, 'monoton': None}
    yy = [r['y'] for r in J if r['fitga']]
    mon = all(b < a for a, b in zip(yy, yy[1:]))
    b = s['p'][1]
    lo, hi = oraliq['sodda']['b']
    shart = {'b_manfiy': b < 0, 'oraliq_0siz': hi < 0, 'monoton': mon}
    shart['hukm'] = 'bajarildi' if all(shart.values()) else 'bajarilmadi'
    if oraliq['sodda']['beqaror']:
        shart['beqaror'] = True
    t = asl.get('toliq')
    if isinstance(t, dict) and oraliq.get('toliq'):
        shart['toliq_ikkinchi_daraja'] = {'b_manfiy': t['p'][1] < 0, 'oraliq_0siz': oraliq['toliq']['b'][1] < 0}
    return shart


def delta(q1, q2, k='sodda', i=1):
    """Juft bootstrap farqi q1 − q2 (bir xil N, bir xil seed -> bir xil indekslar)."""
    if q1['N'] != q2['N']:
        raise SystemExit("TO'XTA — juft bootstrap N teng emas")
    f1, f2 = q1['fit'].get(k), q2['fit'].get(k)
    if not (isinstance(f1, dict) and isinstance(f2, dict)):
        return None
    d = [a[i] - b[i] for a, b in zip(q1['_boot'][k], q2['_boot'][k]) if a is not None and b is not None]
    if not d:
        return None
    return {'nuqta': f1['p'][i] - f2['p'][i], 'oraliq': [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))],
            'juft_takror': len(d)}


# ---------------------------------------------------------------- materiallar
def treebank_birliklar():
    """1 182 gap (ud_system_output.json, s130/s132 chiqarilgan): tor (gold_unit) va keng proyeksiya, V0 birliklari.
    Ijobiy nazorat: qayta qurilgan tor proyeksiya `gold_unit` ga AYNAN teng bo'lishi shart."""
    import ud_tools as U
    import iq
    import naqsh_kesh as NK
    import held_out as H
    Y = json.loads((SUPP / 'data' / 'ud_system_output.json').read_text(encoding='utf-8'))['sentences']
    G = {(g['tb'], g['sent_id']): g for tb in U.TREEBANK for g in U.load_treebank(tb)}
    tk = lambda P: {t: k for k, (_, ids) in enumerate(P) for t in ids}        # noqa: E731
    out, nazorat_farq = [], 0
    for y in Y:
        g = G[(y['tb'], y['sent_id'])]
        sozlar = iq.soz_spanlari(g['text'])
        if [s[0] for s in sozlar] != y['words']:
            raise SystemExit(f"TO'XTA — {y['tb']}:{y['sent_id']} so'zlar ud_system_output bilan mos emas")
        of = NK.ofsetlar(g['text'], g['tokenlar'])
        tor, _, _ = iq.proyeksiya(sozlar, g['tokenlar'], of, tk(NK.daraxt_bolinishi(g, TOR)))
        keng, _, _ = iq.proyeksiya(sozlar, g['tokenlar'], of, tk(NK.daraxt_bolinishi(g, KENG)))
        nazorat_farq += tor != y['gold_unit']
        v0 = [0] * len(y['words'])
        for k, idx in enumerate(y['v0_units']):
            for i in idx:
                v0[i] = k
        out.append({'tb': y['tb'], 'text': g['text'], 'words': y['words'], 'tor': y['gold_unit'], 'keng': keng,
                    'v0': v0, 'ud_toks': [t['form'] for t in g['tokenlar'] if t['upos'] != 'PUNCT']})
    if nazorat_farq:
        raise SystemExit(f"TO'XTA — ijobiy nazorat: qayta qurilgan tor proyeksiya {nazorat_farq} gapda gold_unit dan farq qiladi")
    qol = H.filtr_matn(list(range(len(out))), matn=lambda i: out[i]['text'])
    return [out[i] for i in qol], {'gap': len(out), 'held_out_chiqarildi': len(out) - len(qol),
                                   'ijobiy_nazorat_tor_eq_gold_unit': f'{len(out)}/{len(out)}'}


def klauza_uzunliklari(words, birlik):
    """Har birlik (klauza) PUNCT siz so'z soni; 0 so'zli birlik x ga kirmaydi. -> (uzunliklar, bo'sh_birlik_soni)."""
    c = Counter(b for w, b in zip(words, birlik) if sozmi(w))
    return [c[k] for k in sorted(c)], len(set(birlik)) - len(c)


def k_birliklar(k):
    import common as CM
    import held_out as H
    from gap_model_ierarxiya import load_corpus, UZEN_JSON, TAGOR_JSON
    S = load_corpus({'K1': UZEN_JSON, 'K2': TAGOR_JSON}[k])
    R = CM.load_coded(k)
    if len(S) != len(R) or any(len(s['toks']) != len(r['codes']) for s, r in zip(S, R)):
        raise SystemExit(f"TO'XTA — {k}: matn surati va kodlangan korpus mos emas")
    out = []
    for s, r in zip(S, R):
        birlik, i = [0] * len(s['toks']), 0
        for kk, cl in enumerate(r['clauses']):
            for _ in cl:
                birlik[i] = kk
                i += 1
        if i != len(s['toks']):
            raise SystemExit(f"TO'XTA — {k}: V0 birliklari tokenlarni qoplamaydi")
        out.append({'text': s['sent'], 'words': [t['w'] for t in s['toks']], 'v0': birlik})
    qol = H.filtr_matn(list(range(len(out))), matn=lambda i: out[i]['text'])
    return [out[i] for i in qol], {'gap': len(out), 'held_out_chiqarildi': len(out) - len(qol)}


def q1_xy(gaplar, kalit):
    x, y, L, bosh = [], [], [], 0
    for g in gaplar:
        u, b = klauza_uzunliklari(g['words'], g[kalit])
        bosh += b
        if not u:
            continue
        x.append(len(u))
        y.append(sum(u) / len(u))
        L.append(u)
    return x, y, L, bosh


# ---------------------------------------------------------------- analizator
class Analizator:
    """`_analyze_word_hisobla` + depth-0 `max` ustidan tanlash qoidasi (faqat xotirada)."""

    def __init__(self, db_nusxa):
        os.environ['DATABASE_URL'] = 'sqlite:///' + str(Path(db_nusxa).resolve())
        from app import create_app
        import services.morphology_service as MSM
        self.MSM = MSM
        self.app = create_app()
        self.asl_max = max
        self.stek = []
        self.holat = {'rejim': None, 'i': 0, 'ishlatildi': False, 'nomzod': None}
        stek, holat, asl_max = self.stek, self.holat, self.asl_max

        def tanlovchi_max(cands, key):
            if not stek or stek[-1] != 0 or holat['rejim'] is None or holat['ishlatildi']:
                return asl_max(cands, key=key)
            holat['ishlatildi'] = True
            cands = list(cands)
            holat['nomzod'] = len(cands)
            if holat['rejim'] == 'score':
                return asl_max(cands, key=key)
            tart = sorted(cands, key=key, reverse=True)                      # score kamayish (barqaror)
            tart = sorted(tart, key=lambda c: 1 + len(c[2]), reverse=holat['rejim'] == 'kop')
            return tart[min(holat['i'], len(tart) - 1)]

        class Tanlovchi(MSM.MorphologyService):
            def _find_decomposition(self, word, affixes_sorted, memo, depth=0):
                stek.append(depth)
                try:
                    return super()._find_decomposition(word, affixes_sorted, memo, depth)
                finally:
                    stek.pop()

        MSM.max = tanlovchi_max
        self.ms = Tanlovchi()

    def yop(self):
        self.MSM.max = self.asl_max

    def _bir(self, w, aff, rejim, i=0):
        self.holat.update(rejim=rejim, i=i, ishlatildi=False, nomzod=None)
        r = self.ms._analyze_word_hisobla(w, aff)
        n = self.holat['nomzod']
        self.holat['rejim'] = None
        unk = r['rootCode'] == 'UNKNOWN'
        morf = [norm(e['value']) for e in r['elements']]
        return {'unk': unk, 'morf': morf, 'teng': (not unk) and ''.join(morf) == norm(w), 'nomzod': n or 0}

    def tahlil(self, turlar):
        MSM = self.MSM
        out = {}
        with self.app.app_context():
            aff = MSM._affikslar_saralangan(MSM.kesh_manbasi()) if MSM._kesh_ishlaydimi() else \
                sorted(MSM.Affix.query.all(), key=MSM._affiks_saralash_kaliti)
            for w in sorted(turlar):
                r0 = self._bir(w, aff, 'score')
                rec = {'unk': r0['unk'], 'teng': r0['teng'], 'score': r0['morf'] if r0['teng'] else None,
                       'nomzod': r0['nomzod']}
                if r0['teng']:
                    for rejim in ('kam', 'kop'):
                        tanlov = None
                        if r0['nomzod'] > 1:
                            for i in range(r0['nomzod']):
                                r = self._bir(w, aff, rejim, i)
                                if r['teng'] and all(r['morf']):
                                    tanlov = r['morf']
                                    break
                        rec[rejim] = tanlov or r0['morf']
                        rec[rejim + '_ozgardi'] = tanlov is not None and tanlov != r0['morf']
                out[w] = rec
        return out


# ---------------------------------------------------------------- Q2 / Q3 tokenlari
def tokenlar(tb, K):
    """[(korpus, token)] — K1, K2 (surat tokenlari), treebank (UD non-PUNCT); held-out filtrdan o'tgan gaplar."""
    T = []
    for k in ('K1', 'K2'):
        T += [(k, w) for g in K[k] for w in g['words']]
    T += [('treebank', w) for g in tb for w in g['ud_toks']]
    return T


def q2_q3(T, A):
    """Q2 / Q3 / Q4(c) / sezgirlik kuzatuvlari va chiqarish sanoqlari."""
    sanoq = {k: Counter() for k in ('K1', 'K2', 'treebank')}
    q2 = {'x': [], 'y': [], 'korpus': [], 'kam_x': [], 'kam_y': [], 'kop_x': [], 'kop_y': []}
    q2i = {'x': [], 'y': []}
    q3 = {'x': [], 'y': [], 'korpus': []}
    q3ng = {'x': [], 'y': []}
    ozgardi = Counter()
    for korpus, raw in T:
        s = sanoq[korpus]
        s['kirish'] += 1
        if norm(raw).strip() and set(norm(raw).strip()) <= {"'"}:            # tuzatish_1 (b): faqat tutuq belgisi
            s['q3_faqat_tutuq'] += 1
            continue
        t = tozala(raw)
        sabab = tok_toifa(t)
        if sabab:
            s[sabab] += 1
            continue
        s['yaroqli'] += 1
        w = norm(t)
        a = A[t]
        # Q2
        B = []
        if a['unk']:
            s['q2_noma_lum'] += 1
            gr = grafemalar(w)
            q2i['x'].append(1)
            q2i['y'].append(len(gr))
        elif not a['teng']:
            s['q2_yuza_teng_emas'] += 1
        elif not all(a['score']):
            s['q2_bosh_morfema'] += 1
        else:
            s['q2_namuna'] += 1
            B = morf_chegaralari(a['score'])
            ng = len(grafemalar(w, B))
            q2['x'].append(len(a['score']))
            q2['y'].append(ng / len(a['score']))
            q2['korpus'].append(korpus)
            q2i['x'].append(len(a['score']))
            q2i['y'].append(ng / len(a['score']))
            for rejim in ('kam', 'kop'):
                m = a[rejim]
                q2[rejim + '_x'].append(len(m))
                q2[rejim + '_y'].append(len(grafemalar(w, morf_chegaralari(m))) / len(m))
                ozgardi[rejim] += a[rejim + '_ozgardi']
        # Q3 (tuzatish_1: (b) faqat tutuq -> (c) 1 grafema -> (a) unlisiz)
        gr = grafemalar(w, B)
        if len(gr) == 1:
            s['q3_bir_grafema'] += 1
            continue
        v = unli_soni(gr)
        if v == 0:
            s['q3_unlisiz'] += 1
            continue
        s['q3_namuna'] += 1
        q3['x'].append(v)
        q3['y'].append(len(gr) / v)
        q3['korpus'].append(korpus)
        gr1 = grafemalar(w)
        v1 = unli_soni(gr1)
        q3ng['x'].append(v1)
        q3ng['y'].append(len(gr1) / v1)
    return sanoq, q2, q2i, q3, q3ng, ozgardi


# ---------------------------------------------------------------- Q5
def bc_model(L, rng):
    """B&Č: barcha klauza uzunliklari korpus bo'ylab aralashtiriladi va asl k ketma-ketligi bilan gaplarga yig'iladi."""
    k = [len(u) for u in L]
    hamma = np.array([v for u in L for v in u], dtype=float)
    p = rng.permutation(hamma)
    chegara = np.cumsum([0] + k)
    y = [p[chegara[i]:chegara[i + 1]].mean() for i in range(len(k))]
    return k, y


# ---------------------------------------------------------------- hisobot
def f(v, r=3):
    if v is None:
        return '—'
    if isinstance(v, str):
        return v
    return f'{v:.{r}f}'.replace('.', ',').replace('-', '−')


def fit_qatori(q):
    s, t = q['fit'].get('sodda'), q['fit'].get('toliq')
    o = q['oraliq']
    h = q['hukm']

    def par(m, k, i):
        if not isinstance(m, dict):
            return f(m) if isinstance(m, str) else '—'
        lo = o.get(k)
        nm = 'abc'[i]
        ci = f" [{f(lo[nm][0])}; {f(lo[nm][1])}]" if lo else ''
        return f"{f(m['p'][i])}{ci}"
    return (f"| {q['nom']} | {q['N']} | {len(q['fit_kataklar'])} | {par(s, 'sodda', 0)} | {par(s, 'sodda', 1)} | "
            f"{f(s['r2']) if isinstance(s, dict) else '—'} | {par(t, 'toliq', 0)} | {par(t, 'toliq', 1)} | {par(t, 'toliq', 2)} | "
            f"{f(q['fit'].get('delta_aic_toliq_minus_sodda'), 2)} | {q['fit'].get('afzal', '—')} | "
            f"{'ha' if h.get('monoton') else ('yo' + chr(39) + 'q' if h.get('monoton') is False else '—')} | **{h['hukm']}**"
            f"{' (beqaror)' if h.get('beqaror') else ''} |")


FIT_SARLAVHA = ("| qator | N | K | a (sodda) [95 %] | **b (sodda)** [95 %] | R² (sodda) | a (to'liq) | b (to'liq) | c (to'liq) | "
                "ΔAIC (to'liq − sodda) | afzal | monoton | hukm |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|")


def jadval_md(q):
    s = [f"**{q['nom']}** (N = {q['N']}; fitga: n ≥ {NMIN})", '', '| x | n | o\'rtacha y | SD | fitga |', '|---|---|---|---|---|']
    for r in q['jadval']:
        s.append(f"| {r['x']} | {r['n']} | {f(r['y'])} | {f(r['sd'])} | {'ha' if r['fitga'] else '—'} |")
    return '\n'.join(s)


def rasm(qatorlar, yol, sarlavha, xlabel, ylabel):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    n = len(qatorlar)
    fig, axs = plt.subplots(1, n, figsize=(5 * n, 4), squeeze=False)
    for ax, q in zip(axs[0], qatorlar):
        J = q['jadval']
        for fitga, mk in ((True, 'o'), (False, 'o')):
            R = [r for r in J if r['fitga'] == fitga]
            if not R:
                continue
            xx = [r['x'] for r in R]
            yy = [r['y'] for r in R]
            ee = [1.96 * r['sd'] / np.sqrt(r['n']) if r['sd'] is not None else 0 for r in R]
            ax.errorbar(xx, yy, yerr=ee, fmt=mk, color='#1f4e79' if fitga else '#9aa5b1',
                        mfc='#1f4e79' if fitga else 'none', capsize=3, label='n ≥ 30' if fitga else 'n < 30')
        kat = q['fit_kataklar']
        if kat:
            xg = np.linspace(min(kat), max(kat), 200)
            s, t = q['fit'].get('sodda'), q['fit'].get('toliq')
            if isinstance(s, dict):
                ax.plot(xg, _model_sodda(xg, *s['p']), '-', color='#c0392b', label=f"a·x^b (b = {s['p'][1]:.3f})")
            if isinstance(t, dict):
                ax.plot(xg, _model_toliq(xg, *t['p']), '--', color='#27864a', label=f"a·x^b·e^(−cx) (b = {t['p'][1]:.3f})")
        ax.set_title(q['nom'], fontsize=10)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend(fontsize=8)
        ax.grid(alpha=.3)
    fig.suptitle(sarlavha + ' — o\'rtacha y, 95 % oraliq (±1,96·SD/√n)', fontsize=11)
    fig.tight_layout()
    fig.savefig(yol, dpi=130)
    plt.close(fig)


def rasm_q5(b_haqiqiy, b_tas, yol):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist([b for b in b_tas if b is not None], bins=20, color='#9aa5b1', edgecolor='white', label='B&Č tasodifiy (100)')
    ax.axvline(b_haqiqiy, color='#c0392b', lw=2, label=f'haqiqiy b = {b_haqiqiy:.3f}')
    ax.axvline(0, color='black', lw=.8, ls=':')
    ax.set_xlabel('b (y = a·x^b)')
    ax.set_ylabel('takrorlar')
    ax.set_title('Q5 — treebank, tor klauza: haqiqiy b va B&Č tasodifiy b', fontsize=10)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(yol, dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------- main
def tekshir_muzlatish():
    m = json.loads((SIKL / 'MANIFEST.json').read_text(encoding='utf-8'))
    matn = json.dumps(m['bosqichlar'], ensure_ascii=False)
    kut = sha256(__file__)
    if f'tahlil.py sha256 {kut}' not in matn:
        raise SystemExit("TO'XTA — tahlil.py sha256 MANIFEST bosqichlarida yo'q (muzlatilmagan)")
    for fl in ('prereg.md', 'tuzatish_1.md'):
        if sha256(SIKL / fl) not in matn:
            raise SystemExit(f"TO'XTA — {fl} sha256 MANIFEST bosqichlarida yo'q")
    return kut


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--db', required=True)
    a = p.parse_args()
    if NATIJA.exists():
        raise SystemExit("TO'XTA — natija/ mavjud (run-once)")
    skript_sha = tekshir_muzlatish()
    db0 = md5(DB)
    if md5(a.db) != db0:
        raise SystemExit("TO'XTA — --db nusxasi md5 ishchi DB ga teng emas")
    import scipy
    import matplotlib
    commit = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=REPO, capture_output=True, text=True).stdout.strip()
    NATIJA.mkdir()
    out = {'langar': {'db_md5': db0, 'commit': commit, 'tahlil_sha256': skript_sha,
                      'prereg_sha256': sha256(SIKL / 'prereg.md'), 'tuzatish_1_sha256': sha256(SIKL / 'tuzatish_1.md'),
                      'seed': SEED, 'bootstrap': BOOT, 'bc_takror': BC_TAKROR, 'nmin': NMIN,
                      'numpy': np.__version__, 'scipy': scipy.__version__, 'matplotlib': matplotlib.__version__}}

    # --- materiallar
    tb, tb_s = treebank_birliklar()
    K, k_s = {}, {}
    for k in ('K1', 'K2'):
        K[k], k_s[k] = k_birliklar(k)
    out['materiallar'] = {'treebank': tb_s, **k_s}

    # --- Q1, Q4(a), Q4(b)
    Q = {}
    xy = {}
    for nom, gaplar, kalit in (('Q1 treebank tor', tb, 'tor'), ('Q1 treebank keng', tb, 'keng'),
                               ('Q4b A: treebank V0', tb, 'v0'), ('Q1 K1 VDU', K['K1'], 'v0'),
                               ('Q1 K2 VDU', K['K2'], 'v0')):
        x, y, L, bosh = q1_xy(gaplar, kalit)
        xy[nom] = (x, y, L)
        Q[nom] = qator(x, y, nom)
        Q[nom]['bosh_birlik'] = bosh
        Q[nom]['gap_x_ga_kirmadi'] = len(gaplar) - len(x)
    if Q['Q1 treebank tor']['N'] != Q['Q1 treebank keng']['N'] or Q['Q1 treebank tor']['N'] != Q['Q4b A: treebank V0']['N']:
        raise SystemExit("TO'XTA — Q4 juftligi: gaplar soni teng emas")
    out['Q4a_keng_minus_tor'] = {'b': delta(Q['Q1 treebank keng'], Q['Q1 treebank tor']),
                                 'a': delta(Q['Q1 treebank keng'], Q['Q1 treebank tor'], i=0)}
    d = delta(Q['Q4b A: treebank V0'], Q['Q1 treebank tor'])
    out['Q4b_A_minus_B'] = {'b': d, 'a': delta(Q['Q4b A: treebank V0'], Q['Q1 treebank tor'], i=0),
                            'bashorat_tasdiqlandi': bool(d and d['nuqta'] < 0 and d['oraliq'][1] < 0)}

    # --- analizator, Q2, Q3, Q4(c)
    T = tokenlar(tb, K)
    turlar = {tozala(w) for _, w in T}
    turlar = {t for t in turlar if tok_toifa(t) is None}
    an = Analizator(a.db)
    try:
        A = an.tahlil(turlar)
    finally:
        an.yop()
    sanoq, q2, q2i, q3, q3ng, ozgardi = q2_q3(T, A)
    out['tokenlar'] = {k: dict(v) for k, v in sanoq.items()}
    out['Q4c_ozgargan_token'] = dict(ozgardi)
    Q['Q2 jami (max score)'] = qator(q2['x'], q2['y'], 'Q2 jami (max score)')
    Q['Q4c eng kam morfema'] = qator(q2['kam_x'], q2['kam_y'], 'Q4c eng kam morfema')
    Q['Q4c eng ko\'p morfema'] = qator(q2['kop_x'], q2['kop_y'], 'Q4c eng ko\'p morfema')
    Q['Q3 jami'] = qator(q3['x'], q3['y'], 'Q3 jami')
    out['Q4c'] = {}
    for r in ('Q4c eng kam morfema', 'Q4c eng ko\'p morfema'):
        out['Q4c'][r + ' − max score'] = {'b': delta(Q[r], Q['Q2 jami (max score)']),
                                           'a': delta(Q[r], Q['Q2 jami (max score)'], i=0)}
    bl = [Q[r]['fit'].get('sodda') for r in ('Q2 jami (max score)', 'Q4c eng kam morfema', 'Q4c eng ko\'p morfema')]
    out['Q4c']['ishora_bir_xil'] = (all(isinstance(s, dict) for s in bl)
                                    and len({np.sign(s['p'][1]) for s in bl}) == 1)

    # --- Q5
    x, y, L = xy['Q1 treebank tor']
    rng5 = np.random.default_rng(SEED)
    tas = []
    for _ in range(BC_TAKROR):
        kx, ky = bc_model(L, rng5)
        r = qator(kx, ky, 'B&Č', toliq_boot=False)
        s = r['fit'].get('sodda')
        tas.append({'b': s['p'][1] if isinstance(s, dict) else None, 'hukm': r['hukm']['hukm'],
                    'oraliq_b': r['oraliq']['sodda']['b'] if r['oraliq'].get('sodda') else None})
    bh = Q['Q1 treebank tor']['fit']['sodda']['p'][1]
    bt = [t['b'] for t in tas if t['b'] is not None]
    out['Q5'] = {'b_haqiqiy': bh, 'takror': BC_TAKROR, 'muvaffaqiyatli': len(bt),
                 'b_tasodifiy_mediana': float(np.median(bt)), 'b_tasodifiy_2_5_97_5': [float(np.percentile(bt, 2.5)), float(np.percentile(bt, 97.5))],
                 'b_tasodifiy_min_max': [float(min(bt)), float(max(bt))],
                 'ulush_b_tasodifiy_le_b_haqiqiy': sum(b <= bh for b in bt) / len(bt),
                 'ulush_b_tasodifiy_manfiy': sum(b < 0 for b in bt) / len(bt),
                 'mezon_bajarilgan_takror': sum(t['hukm'] == 'bajarildi' for t in tas), 'takrorlar': tas}

    # --- sezgirlik
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
        S[nom + ' · oxirgi katak (x = %d) chiqarilgan' % oxirgi] = qator([x[i] for i in mm], [y[i] for i in mm],
                                                                       nom + ' · oxirgi katak chiqarilgan')
    for tbn in ('UT', 'UzUDT'):
        x, y, _, _ = q1_xy([g for g in tb if g['tb'] == tbn], 'tor')
        S[f'Q1 {tbn} tor'] = qator(x, y, f'Q1 {tbn} tor')
    S['Q2 (i) noma\'lum so\'zlar x = 1'] = qator(q2i['x'], q2i['y'], 'Q2 (i) noma\'lum so\'zlar x = 1')
    for k in ('K1', 'K2', 'treebank'):
        m = [i for i, v in enumerate(q2['korpus']) if v == k]
        S[f'Q2 (ii) {k}'] = qator([q2['x'][i] for i in m], [q2['y'][i] for i in m], f'Q2 (ii) {k}')
    S['Q3 ng har doim 1'] = qator(q3ng['x'], q3ng['y'], 'Q3 ng har doim 1')

    # --- yozish
    tozalash = lambda q: {k: v for k, v in q.items() if k != '_boot'}          # noqa: E731
    out['qatorlar'] = {k: tozalash(v) for k, v in Q.items()}
    out['sezgirlik'] = {k: tozalash(v) for k, v in S.items()}
    if md5(DB) != db0:
        raise SystemExit("TO'XTA — ishchi DB md5 o'zgardi")
    out['langar']['db_md5_oxiri'] = md5(DB)
    out['langar']['nusxa_db_ozgarmadi'] = md5(a.db) == db0
    (NATIJA / 'natija.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

    rasm([Q['Q1 treebank tor'], Q['Q1 treebank keng'], Q['Q1 K1 VDU'], Q['Q1 K2 VDU']], NATIJA / 'rasm_q1.png',
         'Q1 gap → klauza → so\'z', 'x = klauza soni', 'y = klauzadagi o\'rtacha so\'z')
    rasm([Q['Q2 jami (max score)']], NATIJA / 'rasm_q2.png', 'Q2 so\'z → morfema → grafema', 'x = morfema soni',
         'y = morfemadagi o\'rtacha grafema')
    rasm([Q['Q3 jami']], NATIJA / 'rasm_q3.png', 'Q3 so\'z → bo\'g\'in → grafema', 'x = bo\'g\'in (unli) soni',
         'y = bo\'g\'indagi o\'rtacha grafema')
    rasm([Q['Q1 treebank tor'], Q['Q4b A: treebank V0']], NATIJA / 'rasm_q4b.png', 'Q4(b) oltin tor klauza (B) vs V0 (A)',
         'x = birlik soni', 'y = birlikdagi o\'rtacha so\'z')
    rasm([Q['Q2 jami (max score)'], Q['Q4c eng kam morfema'], Q['Q4c eng ko\'p morfema']], NATIJA / 'rasm_q4c.png',
         'Q4(c) morfema tanlash qoidasi', 'x = morfema soni', 'y = morfemadagi o\'rtacha grafema')
    rasm_q5(bh, [t['b'] for t in tas], NATIJA / 'rasm_q5.png')
    (NATIJA / 'natija.md').write_text(hisobot(out), encoding='utf-8')
    print(json.dumps({k: (v['fit'].get('sodda'), v['hukm']['hukm']) for k, v in out['qatorlar'].items()},
                     ensure_ascii=False, default=str)[:3000])


def hisobot(out):
    L = out['langar']
    Qd = out['qatorlar']
    S = out['sezgirlik']
    m = out['materiallar']
    s = ['# MENZERATH-1 — NATIJA (bir martalik yurish)', '',
         f"Skript `tahlil.py` sha256 `{L['tahlil_sha256']}` · prereg `{L['prereg_sha256'][:12]}…` · tuzatish_1 "
         f"`{L['tuzatish_1_sha256'][:12]}…` · commit `{L['commit']}` · DB md5 `{L['db_md5']}` (oxiri `{L['db_md5_oxiri']}`)",
         f"seed {L['seed']} · bootstrap {L['bootstrap']} · B&Č {L['bc_takror']} · fit kataklari n ≥ {L['nmin']} · "
         f"numpy {L['numpy']} · scipy {L['scipy']} · matplotlib {L['matplotlib']}", '',
         '## 0. Materiallar va namunalar', '',
         f"- Treebank: {m['treebank']['gap']} gap; held-out (`filtr_matn`) chiqarildi {m['treebank']['held_out_chiqarildi']}; "
         f"ijobiy nazorat (qayta qurilgan tor proyeksiya = `gold_unit`) {m['treebank']['ijobiy_nazorat_tor_eq_gold_unit']}.",
         f"- K1: {m['K1']['gap']} gap, held-out chiqarildi {m['K1']['held_out_chiqarildi']}; "
         f"K2: {m['K2']['gap']} gap, held-out chiqarildi {m['K2']['held_out_chiqarildi']}.", '',
         '| korpus | kirish token | tinish | raqam | alifbodan tashqari | yaroqli | Q2: noma\'lum | Q2: yuza teng emas | '
         'Q2: bo\'sh morfema | **Q2 namuna** | Q3: faqat tutuq | Q3: 1 grafema | Q3: unlisiz | **Q3 namuna** |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    jami = Counter()
    for k, c in out['tokenlar'].items():
        jami.update(c)
    for k, c in list(out['tokenlar'].items()) + [('jami', jami)]:
        y = c.get('yaroqli', 0)

        def pc(v, asos):
            return f"{v} ({f(100 * v / asos, 2)} %)" if asos else str(v)
        q3k = y + c.get('q3_faqat_tutuq', 0)
        s.append(f"| {k} | {c.get('kirish', 0)} | {c.get('tinish', 0)} | {c.get('raqam', 0)} | {c.get('alifbo', 0)} | {y} | "
                 f"{pc(c.get('q2_noma_lum', 0), y)} | {pc(c.get('q2_yuza_teng_emas', 0), y)} | {c.get('q2_bosh_morfema', 0)} | "
                 f"**{pc(c.get('q2_namuna', 0), y)}** | {pc(c.get('q3_faqat_tutuq', 0), q3k)} | {pc(c.get('q3_bir_grafema', 0), q3k)} | "
                 f"{pc(c.get('q3_unlisiz', 0), q3k)} | **{pc(c.get('q3_namuna', 0), q3k)}** |")
    s += ['', 'Q2 ulushlari yaroqli tokenlarga nisbatan; Q3 ulushlari Q3 kirishiga (yaroqli + faqat tutuq, tuzatish_1) nisbatan. '
          'Faqat tutuq belgisidan iborat token tozalashdan OLDIN ajratiladi (tinish deb sanalmaydi).', '']
    s += ['## 1. Fitlar va hukmlar (asosiy qatorlar)', '',
          'b — **sodda** model y = a·x^b dan (§4.4 asosiy b); [95 %] — bootstrap percentile oralig\'i. To\'liq MA y = a·x^b·e^(−cx) '
          'ikkinchi darajali. K — fitga kirgan kataklar. Hukm: b < 0 · oraliq 0 siz · n ≥ 30 kataklarda qat\'iy monoton kamayish.', '',
          FIT_SARLAVHA]
    for k in ('Q1 treebank tor', 'Q1 treebank keng', 'Q1 K1 VDU', 'Q1 K2 VDU', 'Q2 jami (max score)', 'Q3 jami',
              'Q4b A: treebank V0', 'Q4c eng kam morfema', 'Q4c eng ko\'p morfema'):
        s.append(fit_qatori(Qd[k]))
    s += ['', '**Q1 asosiy qatori — treebank, tor.** '
          f"Hukm: **{Qd['Q1 treebank tor']['hukm']['hukm']}**. Q2: **{Qd['Q2 jami (max score)']['hukm']['hukm']}**. "
          f"Q3: **{Qd['Q3 jami']['hukm']['hukm']}**.", '']
    s += ['Bootstrap yaqinlashmaganlar (sodda / to\'liq):', '']
    for k, q in Qd.items():
        o = q['oraliq']
        s.append(f"- {k}: sodda {o['sodda']['yaqinlashmagan'] if o.get('sodda') else '—'}/{BOOT}, "
                 f"to'liq {o['toliq']['yaqinlashmagan'] if o.get('toliq') else '—'}/{BOOT}"
                 + (f"; bo'sh (0 so'zli) birlik {q['bosh_birlik']}, x ga kirmagan gap {q['gap_x_ga_kirmadi']}" if 'bosh_birlik' in q else ''))
    s += ['', '## 2. Jadvallar (har daraja: x, n, o\'rtacha y, SD)', '']
    for k in ('Q1 treebank tor', 'Q1 treebank keng', 'Q1 K1 VDU', 'Q1 K2 VDU', 'Q4b A: treebank V0', 'Q2 jami (max score)',
              'Q4c eng kam morfema', 'Q4c eng ko\'p morfema', 'Q3 jami'):
        s += [jadval_md(Qd[k]), '']
    s += ['## 3. Q4 — birlik ta\'rifiga bog\'liqlik', '', '| taqqoslash | Δb (sodda) | 95 % | Δa (sodda) | 95 % | juft takror |',
          '|---|---|---|---|---|---|']

    def dq(nom, d):
        b, a_ = d['b'], d['a']
        if not b:
            return f'| {nom} | — | — | — | — | — |'
        return (f"| {nom} | {f(b['nuqta'])} | [{f(b['oraliq'][0])}; {f(b['oraliq'][1])}] | {f(a_['nuqta'])} | "
                f"[{f(a_['oraliq'][0])}; {f(a_['oraliq'][1])}] | {b['juft_takror']} |")
    s.append(dq('(a) keng − tor', out['Q4a_keng_minus_tor']))
    s.append(dq('(b) A (V0) − B (oltin tor)', out['Q4b_A_minus_B']))
    for k, v in out['Q4c'].items():
        if isinstance(v, dict):
            s.append(dq('(c) ' + k, v))
    s += ['', f"- Q4(b) bashorati (Δb < 0, oraliq 0 siz): **{'tasdiqlandi' if out['Q4b_A_minus_B']['bashorat_tasdiqlandi'] else 'tasdiqlanmadi'}**.",
          f"- Q4(c) bashorati (uchala qoidada b ishorasi bir xil): **{'tasdiqlandi' if out['Q4c']['ishora_bir_xil'] else 'tasdiqlanmadi'}**. "
          f"Tahlili o'zgargan tokenlar: eng kam {out['Q4c_ozgargan_token'].get('kam', 0)}, eng ko'p {out['Q4c_ozgargan_token'].get('kop', 0)} "
          f"(Q2 namunasidan).", '']
    q5 = out['Q5']
    s += ['## 4. Q5 — B&Č tasodifiy model (treebank, tor)', '',
          f"- haqiqiy b (sodda) = {f(q5['b_haqiqiy'])}",
          f"- tasodifiy b: mediana {f(q5['b_tasodifiy_mediana'])}, 2,5–97,5 % [{f(q5['b_tasodifiy_2_5_97_5'][0])}; "
          f"{f(q5['b_tasodifiy_2_5_97_5'][1])}], min–max [{f(q5['b_tasodifiy_min_max'][0])}; {f(q5['b_tasodifiy_min_max'][1])}] "
          f"({q5['muvaffaqiyatli']}/{q5['takror']} fit)",
          f"- tasodifiy b ≤ haqiqiy b ulushi: {f(100 * q5['ulush_b_tasodifiy_le_b_haqiqiy'], 1)} %; tasodifiy b < 0 ulushi: "
          f"{f(100 * q5['ulush_b_tasodifiy_manfiy'], 1)} %",
          f"- §4.4 mezoni bajarilgan tasodifiy takrorlar: {q5['mezon_bajarilgan_takror']}/{q5['takror']}", '']
    s += ['## 5. Sezgirlik (hukmni o\'zgartirmaydi)', '', FIT_SARLAVHA]
    for k, q in S.items():
        q = dict(q)
        q['nom'] = k
        s.append(fit_qatori(q))
    s += ['']
    for k, q in S.items():
        s += [jadval_md({**q, 'nom': k}), '']
    s += ['## 6. Amalga oshirish qaydlari', '',
          '- Q1 so\'zlari — tizim so\'zlari (`ud_system_output.json` → `words`; bo\'shliq-bo\'lak, chetdagi tinish olingan); '
          'PUNCT siz = kamida bitta harf-raqam belgisi. Keng proyeksiya tor bilan bir xil tartibda (`naqsh_kesh.daraxt_bolinishi` + '
          '`iq.proyeksiya`) qurildi; tor qayta qurilishi `gold_unit` ga aynan teng (ijobiy nazorat).',
          '- Q2/Q3 tokenlari: apostrof → `\'`, kichik harf, chetdagi tinish olinadi (boshdagi `\'` olinadi; oxirgi `\'` faqat o/g dan keyin qoladi); '
          'defis grafema emas. Analizator kirishi — shu token (defis bilan); yuza tengligi defissiz solishtiriladi.',
          '- Q4(c): nomzodlar depth-0 `max(score)` chaqiruvida; qoida tartibi (morfema soni, keyin score) bo\'yicha birinchi '
          'yuzaga teng nomzod; bo\'lmasa `max(score)` tahlili. `_shaxs2_s6_s7` uchala qoidada bir xil chaqiriladi.',
          '- Juft bootstrap: bir xil N li qatorlar bir xil seed bilan bir xil indekslarni oladi.',
          '- Rasmlar: `rasm_q1.png`, `rasm_q2.png`, `rasm_q3.png`, `rasm_q4b.png`, `rasm_q4c.png`, `rasm_q5.png`. Oraliq ±1,96·SD/√n; '
          'to\'ldirilmagan nuqta — n < 30 (fitga kirmagan).', '']
    return '\n'.join(s)


if __name__ == '__main__':
    main()
