# MENZERATH-1 — PREREG

Sana: 2026-10-21 · natijadan OLDIN · inventar: `inventar.md` (commit 913db25)

Bu hujjat hech qanday y–x hisobi, fit yoki jadvaldan oldin yozildi. Skript shu matn bo'yicha yoziladi,
sha256 i MANIFEST ga qotiriladi va **bir marta** yuritiladi. Prereg'dan har qanday chetlanish hisobotda
«chetlanish» deb alohida qayd etiladi.

---

## 1. Savollar va bashoratlar

| # | daraja | x | y | bashorat |
|---|---|---|---|---|
| Q1 | gap → klauza → so'z | gapdagi klauza soni | klauzaning o'rtacha so'z soni (PUNCT siz) | b < 0 |
| Q2 | so'z → morfema → grafema | morfema soni (o'zak + qo'shimchalar) | morfemaning o'rtacha grafema soni | b < 0 |
| Q3 | so'z → bo'g'in → grafema | bo'g'in soni (= unli harflar soni) | bo'g'inning o'rtacha grafema soni | b < 0 |

**Q1 asosiy qatori:** treebank, tor ta'rif (`xcomp_aclsiz`), 1 182 gap. Q1 qo'shimcha qatorlari: K1 va K2,
birlik = avtomatik VDU (V0). Hukm har qator uchun alohida beriladi.

**Q4 — birlik ta'rifiga bog'liqlik**
- (a) Klauza ta'rifi: tor (`xcomp_aclsiz`) va keng (`asosiy`), treebankda.
- (b) Oltin klauza va avtomatik VDU, treebank gaplarida (Heaps A/B sharoitlari).
  - A = V0 birliklari (`ud_system_output.json` → `v0_units`).
  - B = oltin tor klauza (`gold_unit`).
  - Bashorat: Δb = b_A − b_B < 0. Ya'ni avtomatik VDU b ni manfiyroq qiladi (ortiqcha kesish).
- (c) Morfema tanlash qoidasi:
  - `max(score)` (analizator sukuti);
  - eng kam morfemali nomzod;
  - eng ko'p morfemali nomzod.
  - Bashorat: parametrlar o'zgaradi, b ishorasi o'zgarmaydi.

**Q5 — tasodifiy nazorat (Benešová & Čech random modeli).** Q1 asosiy qatoridagi (treebank, tor) barcha
klauzalarning uzunligi saqlanadi.
1. Klauzalar korpus bo'ylab tasodifiy aralashtiriladi (UT + UzUDT birga).
2. Ular gaplarga ketma-ket yig'iladi. Har gapning asl k soni saqlanadi, shuning uchun k taqsimoti aynan
   bir xil qoladi.
3. Q1 qayta hisoblanadi.
4. Bu 100 marta takrorlanadi; seed `20261021`.

Bashorat: tasodifiy modelda b 0 ga yaqinlashadi yoki ishorasini yo'qotadi.

> **Asl Q5 nega tashlandi (hisobdan oldin almashtirildi).** Asl variantda har gap o'sha sonda tasodifiy
> nuqtalarda (so'z chegaralarida) qayta kesilardi. Oltin klauzalar gapning har so'zini bitta klauzaga
> bog'laydi (`gold_unit`, bo'linma). Shuning uchun gapdagi m so'z va k klauza uchun y = m/k bo'ladi, va bu
> qiymat qayta kesishda o'zgarmaydi. Natijada b_tasodifiy ≡ b, ya'ni nazorat analitik jihatdan bo'sh.
> Almashtirish foydalanuvchi qarori bilan, birorta y–x qiymati ko'rilmasdan, 2026-10-21 da qilindi.

---

## 2. Materiallar

- **Treebanklar:** UD r2.18, `analysis/ijcl-paket/supplement/data/ud/`.
  - sha256: UT `6297430a…`, UzUDT train `c1fb9548…`, UzUDT test `6a191e59…` (to'liq qiymatlar `inventar.json` da).
  - Takror gaplar s130 va s132 chiqariladi (`squash(text)` bo'yicha, s11 dagi qoida) → 1 182 gap.
- **K1, K2:** `coded_corpus_K1.json`, `coded_corpus_K2.json` (Heaps paketi; sha256 `inventar.json` da).
- **Held-out:** inventar bo'yicha moslik 0. Shunga qaramay skript har korpusga
  `analysis/_konvensiya/held_out.filtr_matn` ni qo'llaydi. Chiqarilgan gaplar soni hisobotga yoziladi
  (kutilgan qiymat 0).
- **Q2 va Q3 tokenlari:** K1 + K2 + treebank. PUNCT, raqamli tokenlar va §3 dagi alifbodan tashqari
  tokenlar chiqariladi; har sababdan chiqarilganlar soni qayd etiladi.
  - **Q2 namunasi:** analizator tahlil qilgan va o'zak + qo'shimchalar yig'indisi tokenga aynan teng
    bo'lgan so'zlar (§3 normallashtirishdan keyin). Tushib qolganlarning ulushi korpus bo'yicha qayd etiladi.
  - **Q3 namunasi:** barcha so'zlar. Unlisi 0 bo'lgan so'zlar chiqariladi va soni qayd etiladi.
- **Birlik darajasi:** Q2 va Q3 da birlik token (so'z ishlatilishi), tip emas.
- **Analizator:** `services/morphology_service.py`, faqat o'qiladi. U `instance/new_phd.db` ning md5 i teng
  scratchpad nusxasida yuritiladi; ishchi DB md5 oldin va keyin tekshiriladi (inventar.py dagi tartib).
  Q4(c) uchun nomzodlar `_find_decomposition` ichida, `max(score)` qo'llanadigan joyda, xotirada ushlanadi.
  Hech bir fayl o'zgartirilmaydi.

---

## 3. Ta'riflar

- **Normallashtirish:**
  - Kichik harfga o'tkaziladi.
  - Apostrof shakllari (ʻ ʼ ' ' ` ´) bitta `'` ga keltiriladi.
  - Defis olib tashlanadi (grafema emas).
- **Grafema:**
  - `sh`, `ch`, `o'`, `g'` — har biri bitta birlik.
  - `ng` faqat bitta morfema ichida bitta birlik. Morfema chegarasidagi n + g ikkita birlik.
  - Qolgan har harf bitta birlik. Bunga `o'`/`g'` dan tashqaridagi tutuq belgisi `'` ham kiradi; u bitta
    grafema, lekin unli emas.
  - Ruxsat etilgan alifbo: a–z va `'`. Boshqa belgili token chiqariladi.
- **`ng` ning chegarasini qayerdan olamiz:**
  - Q2 da chegara analizatordan olinadi.
  - Q3 da chegara analizatordan faqat Q2 sharti bajarilgan so'zlar uchun olinadi. Qolgan so'zlarda `ng`
    bitta birlik hisoblanadi (morfema ichida deb qabul qilinadi).
- **Unlilar:** a, e, i, o, u, o'. `o'` bitta unli; `o` dan keyin `'` kelsa, u alohida `o` bo'lib sanalmaydi.
- **Klauza:** `ud_tools.klauza_boshlari` ning `xcomp_aclsiz` (tor) va `asosiy` (keng) variantlari.
  - Klauzaga so'z berish `ud_system_output.json` dagi `gold_unit` bilan qilinadi (tor). Keng ta'rif uchun xuddi
    shu tartib `asosiy` boshlari bilan quriladi.
  - Uzilgan (discontinuous) klauza bitta klauza sanaladi.
  - So'z soni: UPOS ≠ PUNCT bo'lgan tokenlar.
  - PUNCT siz so'zi 0 bo'lgan klauza x ga kirmaydi, soni qayd etiladi.
- **VDU (K1, K2, Q4b A):** V0 birligi; so'z soni = faqat tinish belgisidan iborat bo'lmagan tokenlar.
  Q4(b) da A va B bitta token ro'yxatida (`ud_system_output.json` → `words`) va bitta PUNCT qoidasi bilan sanaladi.
- **Morfema:** analizator chiqishi (`elements`). O'zak — 1 morfema, har qo'shimcha — 1 morfema.
  - Tahlil qilingan, lekin qo'shimchasiz so'z: x = 1.
  - Q2 da y = so'zning grafemalari soni / x.

---

## 4. Tahlil (muzlatiladigan skript)

### 4.1 Jadval
Har daraja va har qator uchun x bo'yicha jadval tuziladi: x, n, o'rtacha y, SD.
- x katagi faqat n ≥ 30 bo'lsa fitga kiradi.
- Qolgan kataklar jadvalda ko'rsatiladi, lekin fitga kirmaydi.
- Katak to'plami asl namunadan bir marta aniqlanadi va bootstrapda o'zgarmaydi.

### 4.2 Fit
- **Modellar:**
  - to'liq MA: y = a·x^b·e^(−cx);
  - soddalashtirilgan: y = a·x^b.
- **Usul:** n bilan vaznlangan NLS, ya'ni Σ n_x·(ȳ_x − f(x))² minimallashtiriladi (`scipy.optimize.curve_fit`,
  sigma = 1/√n_x). Parametrlar cheklanmaydi.
- **Boshlang'ich qiymatlar:** log ȳ ~ log x vaznlangan OLS dan olinadi, c₀ = 0.
- **Shart:** model faqat fitga kirgan kataklar soni parametrlar sonidan katta bo'lsa (to'liq MA ≥ 4 katak,
  soddalashtirilgan ≥ 3 katak) yuritiladi. Aks holda natija «aniqlanmagan».
- **AIC:** AIC = K·ln(WRSS/K) + 2p, bu yerda K — kataklar soni, p — parametrlar soni. ΔAIC < 2 bo'lsa sodda
  model afzal ko'riladi.
- **R²:** vaznlangan R² hisobot qilinadi, lekin mezon emas.

### 4.3 Noaniqlik
- **Bootstrap:** 1 000 takror, seed `20261021`.
  - Q1 va Q4(a, b): gaplar qayta tanlanadi.
  - Q2, Q3, Q4(c): tokenlar qayta tanlanadi.
- **Natija:** a, b, c uchun 95 % percentile oralig'i.
- **Fit yaqinlashmagan takrorlar:** soni hisobot qilinadi; oraliq muvaffaqiyatlilardan olinadi. 5 % dan ko'p
  bo'lsa, qatorga «beqaror» belgisi qo'yiladi.

### 4.4 «Qonun bajarildi» mezoni
Har qator uchun hukm uchala shart bajarilganda «bajarildi», aks holda «bajarilmadi» bo'ladi:
1. b < 0, b esa **soddalashtirilgan** modeldan olinadi. Bu asosiy b: 4–5 katakda to'liq MA da b va c bir-biriga
   bog'liq bo'lib qoladi.
2. b ning 95 % bootstrap oralig'i 0 ni o'z ichiga olmaydi.
3. n ≥ 30 kataklarda ȳ x bo'yicha qat'iy monoton kamayadi.

To'liq MA ning b va c qiymatlari ikkinchi darajali bo'lib, o'sha shart bilan hisobot qilinadi.

### 4.5 Q4 va Q5
- **Q4(a, b):** parametrlar farqi Δb, Δa juft bootstrap bilan baholanadi (bir xil qayta tanlangan gaplar). 95 %
  oraliq hisoblanadi. Q4(b) bashorati Δb < 0 va oraliq 0 ni o'z ichiga olmasa tasdiqlangan hisoblanadi.
- **Q4(c):** uch qoida bitta token namunasida solishtiriladi: Q2 namunasi `max(score)` ostida.
  - Muqobil qoida nomzodlari filtrdan o'tgan va yuzaga teng nomzodlar ichidan olinadi. Bunday nomzod bo'lmasa,
    so'z `max(score)` tahlilida qoladi.
  - `_shaxs2_s6_s7` tuzatishi uchala qoidaga bir xil qo'llanadi.
  - Bashorat: uchala b ning ishorasi bir xil.
- **Q5:**
  - haqiqiy b va 100 tasodifiy b taqsimoti (mediana, 2,5–97,5 %);
  - tasodifiy b ≤ haqiqiy b bo'lgan takrorlar ulushi;
  - tasodifiy takrorlarning qanchasida §4.4 mezoni bajarilgani.

### 4.6 Sezgirlik
Sezgirlik tahlillari hukmni o'zgartirmaydi va faqat hisobot qilinadi:
- fit diapazoni: oxirgi n ≥ 30 katak chiqariladi;
- Q1: K1 va K2 alohida; treebank UT va UzUDT alohida;
- Q2 noma'lum so'zlar bo'yicha:
  - (i) noma'lum so'zlar x = 1 deb qo'shiladi;
  - (ii) K1, K2 va treebank alohida, chunki noma'lum ulushi har xil: 17 / 16 / 10 %;
- Q3: `ng` har doim bitta birlik.

---

## 5. Cheklovlar (oldindan)

- Treebank kichik (1 182 gap) va janri aralash. Q1 da n ≥ 30 kataklar soni oz, shuning uchun to'liq MA zaif
  aniqlanadi.
- K1 va K2 — tarjima matn, avtomatik kodlash shovqini 7,2 % (36/500).
- Morfemalar analizatorning tanlash qoidasiga bog'liq (> 1 nomzod 30–36 % tokenda) → Q4(c).
- Grafema fonemaning faqat yaqinlashuvi (`ng`, tutuq belgisi, o'zlashma imlo).
- «Bo'g'in = unli soni» qoidasining chegaralari bor: o'zlashma so'zlardagi unli ketma-ketligi, va bo'g'in hosil
  qiluvchi undosh hisobga olinmaydi.
- Q1 da per-gap y = m/k. Shuning uchun Q1 dagi b gap uzunligining klauza soniga bog'lanishini aks ettiradi; Q5 shu
  bog'lanishni uzadigan nazorat.

---

## 6. Tartib

1. Shu prereg commit qilinadi.
2. Skript yoziladi va uning sha256 i MANIFEST ga yoziladi.
3. Skript bir marta yuritiladi.
4. Natija yoziladi.

Hisobot bosqichida natijalar foydalanuvchi bilan to'liq baham ko'riladi; bu siklda ko'rlik yo'q. services/,
data/, DB va production ga tegilmaydi.
