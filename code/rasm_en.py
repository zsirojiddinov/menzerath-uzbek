# -*- coding: utf-8 -*-
"""MENZERATH-1 — rasmlar inglizcha yorliqlar bilan (HISOB YO'Q).

Ishlatish (repo ildizidan):
    python3 analysis/menzerath-1/rasm_en.py      # -> natija/fig1.png … fig6.png (300 dpi)

Faqat `natija/natija.json` va `natija/posthoc.json` dan o'qiydi; raqamlar o'sha fayllardagi qiymatlar, qayta hisoblanmaydi.
Oraliqlar: kataklarda ±1,96·SD/√n (natija.md dagi rasmlar bilan bir xil); E7 da kuzatilgan − y_sof ning 95 % bootstrap oralig'i
(x ≥ 2, E8b (i) dan). fig2 — klauza-havzali qayta yig'ish (B&Č) va turlarni saqlovchi model, 1 000 takrordan (posthoc.json E10g).
fig1 = Q1 (2×2) · fig2 = Q5 / E8c · fig3 = Q2 · fig4 = Q3 · fig5 = Q4(b) (umumiy y o'qi) · fig6 = E7.
Rasm ichida umumiy sarlavha yo'q; formulalar mathtext; x o'qida faqat butun belgilar; shrift ≥ 11 pt.
Yorliqlar `EN` lug'atida; `rasm_uz.py` shu funksiyalarni o'zbekcha lug'at bilan chaqiradi.
"""
import json
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt                                   # noqa: E402
from matplotlib.ticker import FuncFormatter, MaxNLocator          # noqa: E402

SIKL = Path(__file__).resolve().parent
NATIJA = SIKL / 'natija'
DPI = 300
KOK, KUL, QIZIL, YASHIL, SARIQ = '#1f4e79', '#9aa5b1', '#c0392b', '#27864a', '#8e6c00'
SHRIFT = {'font.size': 12, 'axes.titlesize': 13, 'axes.labelsize': 12, 'xtick.labelsize': 11, 'ytick.labelsize': 11,
          'legend.fontsize': 11, 'mathtext.fontset': 'dejavusans'}

EN = {
    'vergul': False,
    'fig1': ('Treebank, narrow', 'Treebank, broad', 'K1, automatic units', 'K2, automatic units'),
    'fig1_o': ('Number of clauses', 'Mean clause length (words)'),
    'fig1_ob': ('Number of units', 'Mean unit length (words)'),
    'fig2_o': ('Exponent $b$', 'Replications'), 'fig2_tas': 'Pooled-clause reassembly (1,000)',
    'fig2_tur': 'Type-preserving model (1,000)', 'fig2_haq': 'Observed $b$ = {b}',
    'fig3': ('Word → morpheme → grapheme', 'Number of morphemes', 'Mean morpheme length (graphemes)'),
    'fig4': ('Word → syllable → grapheme', 'Number of syllables', 'Mean syllable length (graphemes)'),
    'fig5': ('Gold clauses', 'Automatic units'), 'fig5_o': ('Number of units', 'Mean unit length (words)'),
    'fig6': (('Clause level', 'Number of clauses', 'Mean length (words)', 'main clause $M(k)$', 'subordinate clause $S(k)$'),
             ('Morpheme level', 'Number of morphemes', 'Mean length (graphemes)', 'root $R(x)$', 'suffix $S(x)$')),
    'fig6_l': ('observed', 'pure mixture', '95 % interval (observed − pure mixture)'),
    'n': ('$n \\geq 30$', '$n < 30$'),
    'nomlar': {f'fig{i}': f'fig{i}.png' for i in range(1, 7)},
}


def yukla():
    nat = json.loads((NATIJA / 'natija.json').read_text(encoding='utf-8'))
    ph = json.loads((NATIJA / 'posthoc.json').read_text(encoding='utf-8'))
    return nat, ph


def son(v, Y):
    s = f'{v:.3f}'.replace('-', '−')
    return s.replace('.', ',') if Y['vergul'] else s


def panel(ax, q, Y, sarlavha, xlabel, ylabel):
    """Kataklar (n ≥ 30 to'ldirilgan, n < 30 bo'sh), ±1,96·SD/√n, sodda va to'liq MA egri chiziqlari."""
    for fitga in (True, False):
        R = [r for r in q['jadval'] if r['fitga'] == fitga]
        if not R:
            continue
        ee = [1.96 * r['sd'] / np.sqrt(r['n']) if r['sd'] is not None else 0 for r in R]
        ax.errorbar([r['x'] for r in R], [r['y'] for r in R], yerr=ee, fmt='o', color=KOK if fitga else KUL,
                    mfc=KOK if fitga else 'none', capsize=3, label=Y['n'][0] if fitga else Y['n'][1])
    kat = q['fit_kataklar']
    if kat:
        xg = np.linspace(min(kat), max(kat), 200)
        s, t = q['fit'].get('sodda'), q['fit'].get('toliq')
        if isinstance(s, dict):
            a, b = s['p']
            ax.plot(xg, a * xg ** b, '-', color=QIZIL, label=f'$a\\cdot x^{{b}}$ ($b$ = {son(b, Y)})')
        if isinstance(t, dict):
            a, b, c = t['p']
            ax.plot(xg, a * xg ** b * np.exp(-c * xg), '--', color=YASHIL,
                    label=f'$a\\cdot x^{{b}}\\cdot e^{{-cx}}$ ($b$ = {son(b, Y)})')
    ax.set_title(sarlavha)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=.3)
    ax.legend()


def saqla(fig, yol, Y):
    if Y['vergul']:                                              # o'q belgilarida o'nli vergul
        fmt = FuncFormatter(lambda v, _: f'{v:g}'.replace('.', ',').replace('-', '−'))
        for ax in fig.axes:
            ax.xaxis.set_major_formatter(fmt)
            ax.yaxis.set_major_formatter(fmt)
    fig.tight_layout()
    fig.savefig(yol, dpi=DPI)
    plt.close(fig)


def fig1(nat, Y, yol):
    Q = nat['qatorlar']
    fig, axs = plt.subplots(2, 2, figsize=(12, 9))
    for ax, k, s in zip(axs.flat, ('Q1 treebank tor', 'Q1 treebank keng', 'Q1 K1 VDU', 'Q1 K2 VDU'), Y['fig1']):
        panel(ax, Q[k], Y, s, *(Y['fig1_ob'] if 'VDU' in k else Y['fig1_o']))
    saqla(fig, yol, Y)


def fig2(nat, ph, Y, yol):
    """B&Č va turlarni saqlovchi model (E8c 1-variant), har biri 1 000 takror (posthoc.json E10g), bitta o'qda."""
    g = ph['E10']['g']
    bc = [b for b in g['bc_b'] if b is not None]
    tur = [b for b in g['turlarni_saqlovchi_b'] if b is not None]
    fig, ax = plt.subplots(figsize=(8, 4.8))
    chegara = np.linspace(min(bc + tur + [g['b_haqiqiy']]) - .02, max(bc + tur) + .02, 60)
    hb, _, _ = ax.hist(bc, bins=chegara, color=KUL, edgecolor='white', lw=.3, label=Y['fig2_tas'])   # ingichka chet: 1 takrorli
    h, _, _ = ax.hist(tur, bins=chegara, color=SARIQ, alpha=.75, edgecolor='white', lw=.3, label=Y['fig2_tur'])  # ustun ko'rinsin
    if hb.sum() != len(bc) or h.sum() != len(tur):
        raise SystemExit("TO'XTA — fig2: gistogramma diapazoni barcha takrorlarni qamramaydi")
    ax.set_ylim(0, 1.45 * max(h.max(), np.histogram(bc, bins=chegara)[0].max()))   # legend ustunlarni yopmasin
    ax.axvline(g['b_haqiqiy'], color=QIZIL, lw=2, label=Y['fig2_haq'].format(b=son(g['b_haqiqiy'], Y)))
    ax.axvline(0, color='black', lw=.8, ls=':')
    ax.set_xlabel(Y['fig2_o'][0])
    ax.set_ylabel(Y['fig2_o'][1])
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend()
    saqla(fig, yol, Y)


def fig3(nat, Y, yol):
    fig, ax = plt.subplots(figsize=(6.5, 4.8))
    panel(ax, nat['qatorlar']['Q2 jami (max score)'], Y, *Y['fig3'])
    saqla(fig, yol, Y)


def fig4(nat, Y, yol):
    fig, ax = plt.subplots(figsize=(6.5, 4.8))
    panel(ax, nat['qatorlar']['Q3 jami'], Y, *Y['fig4'])
    saqla(fig, yol, Y)


def fig5(nat, Y, yol):
    Q = nat['qatorlar']
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)
    for ax, k, s in zip(axs, ('Q1 treebank tor', 'Q4b A: treebank V0'), Y['fig5']):
        panel(ax, Q[k], Y, s, *Y['fig5_o'])
    axs[1].set_ylabel('')
    axs[1].tick_params(labelleft=True)
    saqla(fig, yol, Y)


def fig6(ph, Y, yol):
    E = ph['E7']
    E8b = ph['E8']['b']                                          # x ≥ 2 dagi oraliq — E8b (i) (y_mix (i) ≡ E7 y_sof)
    fig, axs = plt.subplots(1, 2, figsize=(13, 6))
    for ax, q, q8, p, (sarl, xl, yl, lp, ls) in zip(axs, (E['klauza']['tor'], E['morfema']['max(score)']),
                                                    (E8b['klauza · tor']['i'], E8b['morfema · standart']['i']), ('M', 'R'),
                                                    Y['fig6']):
        J = [r for r in q['jadval'] if r['fitga']]
        band = {r['x']: r for r in q8['jadval']}
        for r in J:
            if abs(band[r['x']]['y_mix'] - r['y_sof']) > 1e-9 or ('farq_95' in r and band[r['x']]['farq_95'] != r['farq_95']):
                raise SystemExit("TO'XTA — fig6: E8b (i) E7 bilan mos emas")
        xx = [r['x'] for r in J]
        ax.plot(xx, [r['y'] for r in J], 'o-', color=KOK, label=Y['fig6_l'][0])
        ax.plot(xx, [r['y_sof'] for r in J], 's--', color=QIZIL, label=Y['fig6_l'][1])
        ax.plot(xx, [r[p] for r in J], '^:', color=YASHIL, label=lp)
        J2 = [r for r in J if r['S'] is not None]
        ax.plot([r['x'] for r in J2], [r['S'] for r in J2], 'v:', color=SARIQ, label=ls)
        birinchi = True
        for r in J:
            if r['x'] >= 2:
                lo, hi = band[r['x']]['farq_95']
                ax.vlines(r['x'], r['y_sof'] + lo, r['y_sof'] + hi, color=QIZIL, alpha=.35, lw=6,
                          label=Y['fig6_l'][2] if birinchi else None)
                birinchi = False
        ax.set_title(sarl)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xlabel(xl)
        ax.set_ylabel(yl)
        ax.grid(alpha=.3)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.16), ncol=2, frameon=False)
    saqla(fig, yol, Y)


def chiz(Y, papka):
    nat, ph = yukla()
    papka.mkdir(exist_ok=True)
    N = Y['nomlar']
    with plt.rc_context(SHRIFT):
        fig1(nat, Y, papka / N['fig1'])
        fig2(nat, ph, Y, papka / N['fig2'])
        fig3(nat, Y, papka / N['fig3'])
        fig4(nat, Y, papka / N['fig4'])
        fig5(nat, Y, papka / N['fig5'])
        fig6(ph, Y, papka / N['fig6'])


def main():
    chiz(EN, NATIJA)
    print('tayyor')


if __name__ == '__main__':
    main()
