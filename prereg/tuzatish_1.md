# MENZERATH-1 — TUZATISH 1 (prereg'ga)

Sana: 2026-10-21 · skriptdan OLDIN · asos: `prereg.md` (sha256 `6b5e3cc3665737d940163a18708e89e006ef6627b939b1a8b57ab1fa5d3ca56f`, commit f3bbe32)

Bu tuzatish foydalanuvchi qarori bilan, tahlil skripti yozilmasdan va birorta y–x qiymati ko'rilmasdan kiritildi.
Prereg'ning boshqa bandlari o'zgarmaydi.

## T1.1 — Q3 namunasidan chiqariladigan so'zlar

Q3 namunasi (prereg §2: «barcha so'zlar») §3 normallashtirishidan keyin quyidagi uch toifani chiqaradi:

| toifa | qoida |
|---|---|
| (a) unlisiz | x = 0, ya'ni a, e, i, o, u, o' unlilaridan birortasi ham yo'q |
| (b) faqat tutuq belgisi | token faqat `'` belgilaridan iborat |
| (c) bir grafemali | §3 bo'yicha grafemalar soni 1 |

- Har toifa uchun chiqarilgan tokenlar soni va Q3 kirishiga nisbatan ulushi korpus bo'yicha (K1, K2, treebank, jami)
  natijada qayd etiladi.
- Toifalar ustma-ust tushishi mumkin, masalan bitta unlidan iborat so'z (c) ga kiradi. Shuning uchun har token
  birinchi mos kelgan toifaga yoziladi: (b) → (c) → (a).
- (a) prereg §2 dagi «unlisi 0 bo'lgan so'zlar chiqariladi» qoidasining o'zi. (b) va (c) — yangi qo'shilgan.
- Tuzatish faqat Q3 ga (va Q3 ning sezgirlik qatoriga) taalluqli. Q2 namunasi o'zgarmaydi.
