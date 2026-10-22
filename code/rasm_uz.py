# -*- coding: utf-8 -*-
"""MENZERATH-1 — rasmlar o'zbekcha yorliqlar bilan (HISOB YO'Q).

Ishlatish (repo ildizidan):
    python3 analysis/menzerath-1/rasm_uz.py      # -> natija/rasm_uz/rasm_q1, q5, q2, q3, q4b, e7.png (300 dpi)

`rasm_en.py` dagi chizish funksiyalari o'zbekcha yorliqlar lug'ati bilan chaqiriladi; faqat `natija/natija.json` va
`natija/posthoc.json` o'qiladi. `tahlil.py` dagi asl rasm_*.png lar o'zgarmaydi.
"""
import importlib.util
from pathlib import Path

SIKL = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('rasm_en', SIKL / 'rasm_en.py')
R = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R)

OK, TUTUQ = '\u02bb', '\u02bc'                                  # oʻ/gʻ — U+02BB, tutuq — U+02BC


def _uz(t):
    """ASCII apostrof -> oʻ/gʻ (U+02BB) yoki tutuq (U+02BC)."""
    return ''.join((OK if i and t[i - 1] in 'oOgG' else TUTUQ) if ch == "'" else ch for i, ch in enumerate(t))


def _uz_hammasi(v):
    if isinstance(v, str):
        return _uz(v)
    if isinstance(v, tuple):
        return tuple(_uz_hammasi(z) for z in v)
    return v


UZ = {k: (_uz_hammasi(v) if k not in ('nomlar', 'vergul') else v) for k, v in {
    'vergul': True,
    'fig1': ("Treebank, tor ta'rif", "Treebank, keng ta'rif", 'K1, avtomatik birliklar', 'K2, avtomatik birliklar'),
    'fig1_o': ('Klauzalar soni', "O'rtacha klauza uzunligi (so'z)"),
    'fig1_ob': ('Birliklar soni', "O'rtacha birlik uzunligi (so'z)"),
    'fig2_o': ("Ko'rsatkich $b$", 'Takrorlar'), 'fig2_tas': "Klauza-havzali qayta yig'ish (1 000)",
    'fig2_tur': 'Turlarni saqlovchi model (1 000)', 'fig2_haq': 'Kuzatilgan $b$ = {b}',
    'fig3': ("So'z → morfema → grafema (standart tahlil)", 'Morfemalar soni', "O'rtacha morfema uzunligi (grafema)"),
    'fig4': ("So'z → bo'g'in → grafema", "Bo'g'inlar soni", "O'rtacha bo'g'in uzunligi (grafema)"),
    'fig5': ('Oltin klauzalar', 'Avtomatik birliklar'), 'fig5_o': ('Birliklar soni', "O'rtacha birlik uzunligi (so'z)"),
    'fig6': (('Klauza darajasi', 'Klauzalar soni', "O'rtacha uzunlik (so'z)", 'bosh klauza $M(k)$', 'ergash klauza $S(k)$'),
             ('Morfema darajasi', 'Morfemalar soni', "O'rtacha uzunlik (grafema)", "o'zak $R(x)$", "qo'shimcha $S(x)$")),
    'fig6_l': ('kuzatilgan', 'sof aralashma', '95 % oraliq (kuzatilgan − sof aralashma)'),
    'n': ('$n \\geq 30$', '$n < 30$'),
    'nomlar': {'fig1': 'rasm_q1.png', 'fig2': 'rasm_q5.png', 'fig3': 'rasm_q2.png', 'fig4': 'rasm_q3.png',
               'fig5': 'rasm_q4b.png', 'fig6': 'rasm_e7.png'},
}.items()}


def main():
    R.chiz(UZ, R.NATIJA / 'rasm_uz')
    print('tayyor')


if __name__ == '__main__':
    main()
