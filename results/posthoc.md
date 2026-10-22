# MENZERATH-1 — POST HOC tekshiruvlar

> **POST HOC — prereg'da yo'q, natijadan keyin rejalashtirilgan, tasdiqlovchi emas.** Prereg hukmlari (`natija.md`) o'zgarmaydi. Barcha raqamlar tavsifiy.

Skript `posthoc.py` sha256 `a83bff2040bea72206c9c23fe7555c86c2e2f0d56d5c778c7f519d5d7dce5ab2` · `tahlil.py` (import, o'zgarmagan) `618d333f287c…` · commit `a2d2db2` · DB md5 `732a97a56205a00c1c28a100275782ce` (oxiri `732a97a56205a00c1c28a100275782ce`) · seed 20261021 · bootstrap 1000

Moslik nazorati: Q2 namunasi N = 66437 (natija.json 66437), Q3 N = 79030 (natija.json 79030), ȳ jadvallari aynan: True.

## E1 (post hoc) — Q2: o'zak va qo'shimcha uzunligi, «doimiy R, S» aralashma modeli

Aralashma: har so'z = 1 o'zak (R grafema) + (x − 1) qo'shimcha (S grafema) → y(x) = S + (R − S)/x. R = ȳ(1), S = 2·ȳ(2) − ȳ(1) (model x = 1 va x = 2 dan aniq o'tadi). Farq = kuzatilgan − aralashma; 95 % — token bootstrap. R(x), S(x) oraliqlari (post hoc 2) — o'sha bootstrap takrorlaridan, n ≥ 30 kataklar.

**max(score)** (N = 66437): R = 4,547 [4,524; 4,569], S = 2,052 [2,017; 2,087]

| x | n | o'rtacha o'zak R(x) | 95 % | o'rtacha qo'shimcha S(x) | 95 % | kuzatilgan ȳ | aralashma | farq | 95 % (farq) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 34502 | 4,547 | [4,524; 4,569] | — | — | 4,547 | 4,547 | 0,000 | — |
| 2 | 21905 | 4,235 | [4,212; 4,259] | 2,364 | [2,351; 2,376] | 3,299 | 3,299 | 0,000 | — |
| 3 | 8211 | 4,306 | [4,272; 4,345] | 2,230 | [2,216; 2,244] | 2,922 | 2,884 | 0,039 | [0,015; 0,063] |
| 4 | 1649 | 4,228 | [4,149; 4,311] | 2,223 | [2,201; 2,243] | 2,725 | 2,676 | 0,049 | [0,017; 0,082] |
| 5 | 162 | 3,796 | [3,578; 4,020] | 2,150 | [2,086; 2,218] | 2,479 | 2,551 | −0,072 | [−0,152; 0,009] |
| 6 | 7 | 3,143 | — | 2,000 | — | 2,190 | 2,468 | −0,277 | — |
| 7 | 1 | 3,000 | — | 2,500 | — | 2,571 | 2,408 | 0,163 | — |

**eng kam morfema** (N = 66437): R = 4,564 [4,542; 4,586], S = 2,253 [2,217; 2,287]

| x | n | o'rtacha o'zak R(x) | 95 % | o'rtacha qo'shimcha S(x) | 95 % | kuzatilgan ȳ | aralashma | farq | 95 % (farq) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 34734 | 4,564 | [4,542; 4,586] | — | — | 4,564 | 4,564 | 0,000 | — |
| 2 | 24833 | 4,333 | [4,310; 4,355] | 2,484 | [2,472; 2,496] | 3,408 | 3,408 | 0,000 | — |
| 3 | 5910 | 4,181 | [4,141; 4,226] | 2,549 | [2,533; 2,567] | 3,093 | 3,023 | 0,070 | [0,047; 0,097] |
| 4 | 836 | 3,888 | [3,789; 4,001] | 2,421 | [2,383; 2,458] | 2,788 | 2,831 | −0,043 | [−0,088; 0,002] |
| 5 | 119 | 3,655 | [3,426; 3,902] | 2,181 | [2,105; 2,262] | 2,476 | 2,715 | −0,239 | [−0,331; −0,147] |
| 6 | 5 | 3,000 | — | 2,160 | — | 2,300 | 2,638 | −0,338 | — |

**eng ko'p morfema** (N = 66437): R = 4,540 [4,519; 4,562], S = 1,875 [1,837; 1,910]

| x | n | o'rtacha o'zak R(x) | 95 % | o'rtacha qo'shimcha S(x) | 95 % | kuzatilgan ȳ | aralashma | farq | 95 % (farq) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 34448 | 4,540 | [4,519; 4,562] | — | — | 4,540 | 4,540 | 0,000 | — |
| 2 | 19805 | 4,210 | [4,186; 4,234] | 2,206 | [2,195; 2,216] | 3,208 | 3,208 | 0,000 | — |
| 3 | 9552 | 4,281 | [4,248; 4,316] | 2,144 | [2,132; 2,156] | 2,856 | 2,764 | 0,093 | [0,069; 0,117] |
| 4 | 2349 | 4,111 | [4,049; 4,181] | 2,134 | [2,116; 2,152] | 2,629 | 2,541 | 0,087 | [0,057; 0,121] |
| 5 | 267 | 3,757 | [3,586; 3,920] | 2,067 | [2,018; 2,117] | 2,405 | 2,408 | −0,003 | [−0,063; 0,058] |
| 6 | 15 | 3,667 | — | 2,013 | — | 2,289 | 2,319 | −0,030 | — |
| 7 | 1 | 3,000 | — | 2,500 | — | 2,571 | 2,256 | 0,315 | — |

## E2 (post hoc) — Q3: tahlil qilingan vs noma'lum so'zlar

Guruhlar: «Q2 namunasi» (tahlil qilingan, yuzaga teng; ng chegarasi analizatordan), «noma'lum» (UNKNOWN), «yuza teng emas» (tahlil bor, yuzaga teng emas). Q3 qoidasi tahlil.py dagidek (tuzatish_1 bilan).

**jami**

| x | Q2 namunasi: n | ȳ | noma'lum: n | ȳ | yuza teng emas: n | ȳ | hammasi: n | ȳ |
|---|---|---|---|---|---|---|---|---|
| 1 | 10110 | 2,734 | 1931 | 2,747 | 3 | 3,000 | 12044 | 2,736 |
| 2 | 26750 | 2,409 | 3133 | 2,576 | 615 | 2,426 | 30498 | 2,426 |
| 3 | 16928 | 2,344 | 2956 | 2,422 | 992 | 2,250 | 20876 | 2,351 |
| 4 | 8238 | 2,278 | 1942 | 2,340 | 581 | 2,260 | 10761 | 2,288 |
| 5 | 2710 | 2,243 | 724 | 2,326 | 150 | 2,305 | 3584 | 2,262 |
| 6 | 674 | 2,234 | 240 | 2,331 | 36 | 2,269 | 950 | 2,260 |
| 7 | 134 | 2,235 | 84 | 2,354 | 7 | 2,265 | 225 | 2,280 |
| 8 | 20 | 2,225 | 26 | 2,380 | 1 | 2,250 | 47 | 2,311 |
| 9 | 5 | 2,311 | 22 | 2,455 | 1 | 2,333 | 28 | 2,425 |
| 10 | 0 | — | 5 | 2,400 | 0 | — | 5 | 2,400 |
| 11 | 0 | — | 7 | 2,455 | 0 | — | 7 | 2,455 |
| 12 | 0 | — | 1 | 2,500 | 0 | — | 1 | 2,500 |
| 13 | 0 | — | 1 | 2,462 | 0 | — | 1 | 2,462 |
| 14 | 0 | — | 1 | 2,857 | 0 | — | 1 | 2,857 |
| 15 | 0 | — | 1 | 2,400 | 0 | — | 1 | 2,400 |
| 16 | 0 | — | 1 | 2,188 | 0 | — | 1 | 2,188 |

**K1**

| x | Q2 namunasi: n | ȳ | noma'lum: n | ȳ | yuza teng emas: n | ȳ | hammasi: n | ȳ |
|---|---|---|---|---|---|---|---|---|
| 1 | 1718 | 2,642 | 294 | 3,432 | 0 | — | 2012 | 2,757 |
| 2 | 4549 | 2,451 | 647 | 2,706 | 67 | 2,425 | 5263 | 2,482 |
| 3 | 3410 | 2,370 | 533 | 2,441 | 110 | 2,215 | 4053 | 2,376 |
| 4 | 2312 | 2,293 | 342 | 2,352 | 132 | 2,271 | 2786 | 2,299 |
| 5 | 1068 | 2,242 | 200 | 2,364 | 52 | 2,285 | 1320 | 2,262 |
| 6 | 347 | 2,232 | 95 | 2,405 | 17 | 2,265 | 459 | 2,269 |
| 7 | 74 | 2,249 | 51 | 2,409 | 3 | 2,381 | 128 | 2,316 |
| 8 | 15 | 2,258 | 25 | 2,380 | 1 | 2,250 | 41 | 2,332 |
| 9 | 4 | 2,333 | 20 | 2,456 | 1 | 2,333 | 25 | 2,431 |
| 10 | 0 | — | 5 | 2,400 | 0 | — | 5 | 2,400 |
| 11 | 0 | — | 7 | 2,455 | 0 | — | 7 | 2,455 |
| 12 | 0 | — | 1 | 2,500 | 0 | — | 1 | 2,500 |
| 13 | 0 | — | 1 | 2,462 | 0 | — | 1 | 2,462 |
| 14 | 0 | — | 1 | 2,857 | 0 | — | 1 | 2,857 |
| 15 | 0 | — | 1 | 2,400 | 0 | — | 1 | 2,400 |
| 16 | 0 | — | 1 | 2,188 | 0 | — | 1 | 2,188 |

**K2**

| x | Q2 namunasi: n | ȳ | noma'lum: n | ȳ | yuza teng emas: n | ȳ | hammasi: n | ȳ |
|---|---|---|---|---|---|---|---|---|
| 1 | 7089 | 2,748 | 1555 | 2,624 | 3 | 3,000 | 8647 | 2,726 |
| 2 | 18376 | 2,390 | 2198 | 2,542 | 447 | 2,414 | 21021 | 2,406 |
| 3 | 10961 | 2,333 | 2075 | 2,418 | 753 | 2,254 | 13789 | 2,341 |
| 4 | 4626 | 2,265 | 1416 | 2,336 | 376 | 2,255 | 6418 | 2,280 |
| 5 | 1200 | 2,241 | 469 | 2,306 | 67 | 2,328 | 1736 | 2,262 |
| 6 | 229 | 2,221 | 118 | 2,280 | 10 | 2,233 | 357 | 2,240 |
| 7 | 40 | 2,179 | 31 | 2,267 | 1 | 2,143 | 72 | 2,216 |
| 8 | 3 | 2,208 | 1 | 2,375 | 0 | — | 4 | 2,250 |
| 9 | 0 | — | 2 | 2,444 | 0 | — | 2 | 2,444 |

**treebank**

| x | Q2 namunasi: n | ȳ | noma'lum: n | ȳ | yuza teng emas: n | ȳ | hammasi: n | ȳ |
|---|---|---|---|---|---|---|---|---|
| 1 | 1303 | 2,774 | 82 | 2,610 | 0 | — | 1385 | 2,765 |
| 2 | 3825 | 2,448 | 288 | 2,542 | 101 | 2,480 | 4214 | 2,456 |
| 3 | 2557 | 2,359 | 348 | 2,420 | 129 | 2,253 | 3034 | 2,361 |
| 4 | 1300 | 2,296 | 184 | 2,349 | 73 | 2,267 | 1557 | 2,301 |
| 5 | 442 | 2,250 | 55 | 2,360 | 31 | 2,290 | 528 | 2,264 |
| 6 | 98 | 2,276 | 27 | 2,290 | 9 | 2,315 | 134 | 2,281 |
| 7 | 20 | 2,293 | 2 | 2,286 | 3 | 2,190 | 25 | 2,280 |
| 8 | 2 | 2,000 | 0 | — | 0 | — | 2 | 2,000 |
| 9 | 1 | 2,222 | 0 | — | 0 | — | 1 | 2,222 |

x ≥ 7 kataklar tarkibi (jami 317 token): Q2 namunasi 159 (50,2 %), noma'lum 149 (47,0 %), yuza teng emas 9 (2,8 %).

## E3 (post hoc) — Q1 treebank: UT vs UzUDT; janr

UzUDT janr belgisi: yo'q (sent_id s1…s684, izoh qatorlari faqat sent_id va text; README: «fiction academic»). UT janri sent_id bo'yicha (README): 1–250 yangilik, 251–500 badiiy.

| qator | N | K | a (sodda) [95 %] | **b (sodda)** [95 %] | R² (sodda) | a (to'liq) | b (to'liq) | c (to'liq) | ΔAIC (to'liq − sodda) | afzal | monoton | hukm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 UT tor | 500 | 3 | 9,470 [9,132; 9,826] | −0,838 [−0,908; −0,755] | 0,999 | — | — | — | — | sodda | ha | **bajarildi** |
| Q1 UzUDT tor | 682 | 4 | 6,264 [5,927; 6,578] | −0,450 [−0,523; −0,378] | 0,981 | 7,767 [6,341; 9,408] | −0,063 [−0,464; 0,334] | 0,221 [0,018; 0,433] | −34,01 | toliq | ha | **bajarildi** |
| Q1 UT yangilik (1–250) tor | 250 | 2 | — | — | — | — | — | — | — | — | — | **aniqlanmagan** |
| Q1 UT badiiy (251–500) tor | 250 | 2 | — | — | — | — | — | — | — | — | — | **aniqlanmagan** |

- Δb (sodda) UT − UzUDT: −0,388 [−0,488; −0,267] (mustaqil bootstrap, 1000 juft takror)
- Δb UT yangilik − UT badiiy: aniqlanmagan

**Q1 UT tor** (N = 500; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 310 | 9,477 | 3,108 | ha |
| 2 | 145 | 5,221 | 1,754 | ha |
| 3 | 39 | 4,026 | 1,217 | ha |
| 4 | 5 | 2,950 | 0,647 | — |
| 5 | 1 | 1,800 | — | — |

**Q1 UzUDT tor** (N = 682; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 318 | 6,226 | 3,191 | ha |
| 2 | 187 | 4,778 | 2,090 | ha |
| 3 | 101 | 3,729 | 1,408 | ha |
| 4 | 39 | 2,942 | 1,215 | ha |
| 5 | 28 | 3,379 | 1,146 | — |
| 6 | 7 | 2,786 | 0,507 | — |
| 7 | 2 | 4,143 | 2,424 | — |

**Q1 UT yangilik (1–250) tor** (N = 250; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 176 | 10,324 | 3,318 | ha |
| 2 | 59 | 6,169 | 1,775 | ha |
| 3 | 15 | 4,889 | 1,096 | — |

**Q1 UT badiiy (251–500) tor** (N = 250; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 134 | 8,366 | 2,402 | ha |
| 2 | 86 | 4,570 | 1,417 | ha |
| 3 | 24 | 3,486 | 0,963 | — |
| 4 | 5 | 2,950 | 0,647 | — |
| 5 | 1 | 1,800 | — | — |

## E4 (post hoc) — Q1 K1 VDU: faqat tutuq belgisidan iborat tokenlar

- K1 da faqat tutuq belgisidan iborat token: 194 ta, 119 gapda.
- Q1 da so'z sifatida sanalganmi: **yo'q** — so'z sanog'i `sozmi` (kamida bitta harf-raqam belgisi) bilan; bunday tokenlardan 0 tasi so'z deb sanalgan.
- Ularsiz qayta hisob: jadval asl bilan aynan — **ha**.
- Qo'shnilar: oldida so'z 127 (13 tasida oldingi so'z o/g bilan tugaydi — o'/g' bo'linishi), keyinida so'z 157. Ya'ni tutuq tokeni ko'pincha bitta so'zni ikki «so'z»ga bo'lgan.
- Qo'shimcha (so'ralmagan, tavsifiy): so'z + tutuq + so'z → bitta so'z, 90 birlashtirish.

| qator | N | K | a (sodda) [95 %] | **b (sodda)** [95 %] | R² (sodda) | a (to'liq) | b (to'liq) | c (to'liq) | ΔAIC (to'liq − sodda) | afzal | monoton | hukm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 K1 VDU (asl) | 889 | 6 | 10,882 [10,157; 11,622] | −0,514 [−0,576; −0,452] | 0,974 | 9,900 [9,279; 10,509] | −0,767 [−0,960; −0,561] | −0,115 [−0,184; −0,042] | −5,37 | toliq | ha | **bajarildi** |
| Q1 K1 VDU (tutuq tokenlarisiz) | 889 | 6 | 10,882 [10,157; 11,622] | −0,514 [−0,576; −0,452] | 0,974 | 9,900 [9,279; 10,509] | −0,767 [−0,960; −0,561] | −0,115 [−0,184; −0,042] | −5,37 | toliq | ha | **bajarildi** |
| Q1 K1 VDU (tutuq bilan bo'lingan so'zlar birlashtirilgan) | 889 | 6 | 10,876 [10,154; 11,613] | −0,516 [−0,578; −0,454] | 0,974 | 9,895 [9,273; 10,532] | −0,767 [−0,965; −0,557] | −0,115 [−0,185; −0,041] | −5,18 | toliq | ha | **bajarildi** |

**Q1 K1 VDU (tutuq bilan bo'lingan so'zlar birlashtirilgan)** (N = 889; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 143 | 11,133 | 4,979 | ha |
| 2 | 208 | 7,236 | 3,157 | ha |
| 3 | 226 | 5,929 | 2,087 | ha |
| 4 | 160 | 5,758 | 1,639 | ha |
| 5 | 79 | 4,934 | 1,194 | ha |
| 6 | 46 | 4,732 | 1,291 | ha |
| 7 | 18 | 4,556 | 0,732 | — |
| 8 | 5 | 4,975 | 0,681 | — |
| 9 | 3 | 4,111 | 0,801 | — |
| 13 | 1 | 6,538 | — | — |

## E5 (post hoc 2) — Q1 treebank: bosh (root) va ergash klauzalar

Har gap: M = bosh klauza (bosh tokeni deprel `root`) uzunligi, S = ergash klauzalar o'rtacha uzunligi (PUNCT siz so'z). Aralashma: y(k) = [M + (k − 1)·S]/k, M = ȳ(1), S = 2·ȳ(2) − ȳ(1). 95 % — gap darajasidagi bootstrap (1 000, seed 20261021). k, ȳ Q1 bilan aynan (tekshirilgan).

**tor** (N = 1182; bosh klauzasi so'zsiz qolgan gap 0): M = 7,831 [7,568; 8,147], S = 2,112 [1,637; 2,607]; bosh klauza o'rtacha 6,523 (SD 3,671)

| k | n | M(k) | 95 % | S(k) | 95 % | kuzatilgan ȳ | aralashma | farq | 95 % (farq) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 628 | 7,831 | [7,568; 8,147] | — | — | 7,831 | 7,831 | 0,000 | — |
| 2 | 332 | 5,596 | [5,293; 5,925] | 4,346 | [4,041; 4,683] | 4,971 | 4,971 | 0,000 | — |
| 3 | 140 | 4,279 | [3,804; 4,727] | 3,579 | [3,335; 3,856] | 3,812 | 4,018 | −0,206 | [−0,570; 0,147] |
| 4 | 44 | 3,705 | [2,800; 4,834] | 2,689 | [2,453; 2,977] | 2,943 | 3,541 | −0,598 | [−1,071; −0,102] |
| 5 | 29 | 5,172 | — | 2,862 | — | 3,324 | 3,255 | 0,069 | — |
| 6 | 7 | 2,857 | — | 2,771 | — | 2,786 | 3,065 | −0,279 | — |
| 7 | 2 | 1,000 | — | 4,667 | — | 4,143 | 2,929 | 1,214 | — |

Ergash klauza uzunligi turi bo'yicha (tor; bosh tokenining deprel asosi; faqat tavsif):

| deprel | n | ulush | o'rtacha so'z | SD |
|---|---|---|---|---|
| advcl | 548 | 60,4 % | 3,066 | 2,258 |
| ccomp | 127 | 14,0 % | 4,236 | 2,602 |
| conj | 102 | 11,2 % | 4,137 | 2,442 |
| parataxis | 93 | 10,3 % | 5,000 | 3,618 |
| csubj | 37 | 4,1 % | 4,865 | 3,137 |

**keng** (N = 1182; bosh klauzasi so'zsiz qolgan gap 0): M = 7,136 [6,805; 7,489], S = 2,072 [1,605; 2,535]; bosh klauza o'rtacha 5,630 (SD 3,269)

| k | n | M(k) | 95 % | S(k) | 95 % | kuzatilgan ȳ | aralashma | farq | 95 % (farq) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 433 | 7,136 | [6,805; 7,489] | — | — | 7,136 | 7,136 | 0,000 | — |
| 2 | 399 | 5,351 | [5,079; 5,660] | 3,857 | [3,639; 4,091] | 4,604 | 4,604 | 0,000 | — |
| 3 | 203 | 4,305 | [3,974; 4,634] | 3,150 | [2,927; 3,385] | 3,535 | 3,760 | −0,225 | [−0,538; 0,065] |
| 4 | 81 | 3,864 | [3,349; 4,375] | 2,881 | [2,676; 3,099] | 3,127 | 3,338 | −0,211 | [−0,589; 0,142] |
| 5 | 28 | 3,429 | — | 2,420 | — | 2,621 | 3,085 | −0,463 | — |
| 6 | 23 | 3,522 | — | 2,504 | — | 2,674 | 2,916 | −0,242 | — |
| 7 | 9 | 2,889 | — | 2,907 | — | 2,905 | 2,795 | 0,110 | — |
| 8 | 5 | 7,800 | — | 2,571 | — | 3,225 | 2,705 | 0,520 | — |
| 11 | 1 | 1,000 | — | 1,600 | — | 1,545 | 2,532 | −0,987 | — |

Ergash klauza uzunligi turi bo'yicha (keng; bosh tokenining deprel asosi; faqat tavsif):

| deprel | n | ulush | o'rtacha so'z | SD |
|---|---|---|---|---|
| advcl | 548 | 39,9 % | 2,869 | 2,020 |
| acl | 270 | 19,7 % | 2,922 | 1,855 |
| xcomp | 197 | 14,3 % | 2,640 | 1,986 |
| ccomp | 127 | 9,2 % | 3,811 | 2,319 |
| conj | 102 | 7,4 % | 3,725 | 2,208 |
| parataxis | 93 | 6,8 % | 4,624 | 3,426 |
| csubj | 37 | 2,7 % | 4,459 | 3,088 |

## E6 (post hoc 2) — Q3 faqat tahlil qilingan so'zlarda (Q2 namunasi)

Prereg §4 usuli (n-vaznli NLS, bootstrap 1 000, §4.4 mezoni) — **post hoc**, prereg hukmini almashtirmaydi.

| qator | N | K | a (sodda) [95 %] | **b (sodda)** [95 %] | R² (sodda) | a (to'liq) | b (to'liq) | c (to'liq) | ΔAIC (to'liq − sodda) | afzal | monoton | hukm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E6 Q3 · faqat Q2 namunasi (post hoc) | 65569 | 7 | 2,678 [2,670; 2,686] | −0,126 [−0,129; −0,123] | 0,917 | 2,590 [2,582; 2,599] | −0,237 [−0,247; −0,225] | −0,050 [−0,053; −0,046] | −8,02 | toliq | yo'q | **bajarilmadi** |

Hukm (post hoc): **bajarilmadi** — b < 0: True, oraliq 0 siz: True, monoton: False.

**E6 Q3 · faqat Q2 namunasi (post hoc)** (N = 65569; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 10110 | 2,734 | 0,566 | ha |
| 2 | 26750 | 2,409 | 0,421 | ha |
| 3 | 16928 | 2,344 | 0,329 | ha |
| 4 | 8238 | 2,278 | 0,281 | ha |
| 5 | 2710 | 2,243 | 0,237 | ha |
| 6 | 674 | 2,234 | 0,213 | ha |
| 7 | 134 | 2,235 | 0,200 | ha |
| 8 | 20 | 2,225 | 0,175 | — |
| 9 | 5 | 2,311 | 0,214 | — |

1 bo'g'inli so'zlar (x = 1): yopiq bo'g'in = oxirgi grafema undosh (a, e, i, o, u, o' emas). Faqat tavsif.

| korpus · guruh | n | yopiq | yopiq ulush | ȳ (yopiq) | ȳ (ochiq) |
|---|---|---|---|---|---|
| jami · Q2 namunasi | 10110 | 7758 | 76,7 % | 2,955 | 2,004 |
| jami · noma'lum | 1931 | 1049 | 54,3 % | 3,210 | 2,196 |
| jami · yuza teng emas | 3 | 0 | 0,0 % | — | 3,000 |
| jami · hammasi | 12044 | 8807 | 73,1 % | 2,985 | 2,057 |
| K1 · Q2 namunasi | 1718 | 1096 | 63,8 % | 2,998 | 2,014 |
| K1 · noma'lum | 294 | 209 | 71,1 % | 3,789 | 2,553 |
| K1 · hammasi | 2012 | 1305 | 64,9 % | 3,125 | 2,079 |
| K2 · Q2 namunasi | 7089 | 5629 | 79,4 % | 2,943 | 2,000 |
| K2 · noma'lum | 1555 | 791 | 50,9 % | 3,070 | 2,164 |
| K2 · yuza teng emas | 3 | 0 | 0,0 % | — | 3,000 |
| K2 · hammasi | 8647 | 6420 | 74,2 % | 2,958 | 2,057 |
| treebank · Q2 namunasi | 1303 | 1033 | 79,3 % | 2,977 | 2,000 |
| treebank · noma'lum | 82 | 49 | 59,8 % | 3,000 | 2,030 |
| treebank · hammasi | 1385 | 1082 | 78,1 % | 2,978 | 2,003 |

## E7 (post hoc 3) — qism turi ichidagi ko'rsatkichlar

Har qism uchun a·x^b (n-vaznli NLS, n ≥ 30 kataklar; bosh qism x = 1… , ergash/qo'shimcha x = 2…). «Sof aralashma»: y_sof(x) = [P(1) + (x − 1)·S(2)]/x, P(1) = M(1) yoki R(1), S(2) — kuzatilgan o'rtachalar; b_sof — y_sof ga o'sha kataklarda fit. 95 % — bootstrap (klauza: gap, morfema: token; 1 000, seed 20261021). Umumiy b — prereg natijasi (natija.json).

### (c) Taqqoslov jadvali

| daraja | umumiy b (prereg) [95 %] | b_M / b_R [95 %] | b_S [95 %] | b_sof (sof aralashma) [95 %] |
|---|---|---|---|---|
| Q1 klauza · tor | −0,662 [−0,718; −0,607] | −0,517 [−0,592; −0,446] | −0,569 [−0,763; −0,383] | −0,333 [−0,373; −0,288] |
| Q1 klauza · keng | −0,628 [−0,690; −0,569] | −0,440 [−0,513; −0,374] | −0,458 [−0,621; −0,303] | −0,339 [−0,375; −0,300] |
| Q2 morfema · max(score) | −0,427 [−0,434; −0,421] | −0,070 [−0,078; −0,063] | −0,120 [−0,135; −0,104] | −0,368 [−0,372; −0,364] |
| Q2 morfema · eng kam morfema | −0,395 [−0,402; −0,388] | −0,082 [−0,090; −0,074] | 0,020 [0,004; 0,037] | −0,353 [−0,356; −0,349] |
| Q2 morfema · eng ko'p morfema | −0,450 [−0,457; −0,444] | −0,075 [−0,082; −0,068] | −0,060 [−0,073; −0,047] | −0,395 [−0,398; −0,392] |

Bootstrap yaqinlashmagan fitlar: yo'q.

### (a) Klauza (treebank)

**tor** — kataklar [1, 2, 3, 4]

| k | n | M(k) | S(k) | kuzatilgan ȳ | y_sof | farq | 95 % (farq) |
|---|---|---|---|---|---|---|---|
| 1 | 628 | 7,831 | — | 7,831 | 7,831 | 0,000 | — |
| 2 | 332 | 5,596 | 4,346 | 4,971 | 6,089 | −1,117 | — |
| 3 | 140 | 4,279 | 3,579 | 3,812 | 5,508 | −1,696 | [−2,044; −1,358] |
| 4 | 44 | 3,705 | 2,689 | 2,943 | 5,218 | −2,274 | [−2,673; −1,862] |
| 5 | 29 | 5,172 | 2,862 | 3,324 | 5,043 | −1,719 | — |
| 6 | 7 | 2,857 | 2,771 | 2,786 | 4,927 | −2,141 | — |
| 7 | 2 | 1,000 | 4,667 | 4,143 | 4,844 | −0,701 | — |

**keng** — kataklar [1, 2, 3, 4]

| k | n | M(k) | S(k) | kuzatilgan ȳ | y_sof | farq | 95 % (farq) |
|---|---|---|---|---|---|---|---|
| 1 | 433 | 7,136 | — | 7,136 | 7,136 | 0,000 | — |
| 2 | 399 | 5,351 | 3,857 | 4,604 | 5,497 | −0,893 | — |
| 3 | 203 | 4,305 | 3,150 | 3,535 | 4,950 | −1,415 | [−1,673; −1,164] |
| 4 | 81 | 3,864 | 2,881 | 3,127 | 4,677 | −1,550 | [−1,833; −1,284] |
| 5 | 28 | 3,429 | 2,420 | 2,621 | 4,513 | −1,892 | — |
| 6 | 23 | 3,522 | 2,504 | 2,674 | 4,404 | −1,730 | — |
| 7 | 9 | 2,889 | 2,907 | 2,905 | 4,326 | −1,421 | — |
| 8 | 5 | 7,800 | 2,571 | 3,225 | 4,267 | −1,042 | — |
| 11 | 1 | 1,000 | 1,600 | 1,545 | 4,155 | −2,610 | — |

### (b) Morfema (Q2 namunasi)

**max(score)** — kataklar [1, 2, 3, 4, 5]

| x | n | R(x) | S(x) | kuzatilgan ȳ | y_sof | farq | 95 % (farq) |
|---|---|---|---|---|---|---|---|
| 1 | 34502 | 4,547 | — | 4,547 | 4,547 | 0,000 | — |
| 2 | 21905 | 4,235 | 2,364 | 3,299 | 3,455 | −0,156 | — |
| 3 | 8211 | 4,306 | 2,230 | 2,922 | 3,092 | −0,169 | [−0,187; −0,151] |
| 4 | 1649 | 4,228 | 2,223 | 2,725 | 2,910 | −0,185 | [−0,211; −0,158] |
| 5 | 162 | 3,796 | 2,150 | 2,479 | 2,800 | −0,321 | [−0,400; −0,245] |
| 6 | 7 | 3,143 | 2,000 | 2,190 | 2,728 | −0,537 | — |
| 7 | 1 | 3,000 | 2,500 | 2,571 | 2,676 | −0,104 | — |

**eng kam morfema** — kataklar [1, 2, 3, 4, 5]

| x | n | R(x) | S(x) | kuzatilgan ȳ | y_sof | farq | 95 % (farq) |
|---|---|---|---|---|---|---|---|
| 1 | 34734 | 4,564 | — | 4,564 | 4,564 | 0,000 | — |
| 2 | 24833 | 4,333 | 2,484 | 3,408 | 3,524 | −0,116 | — |
| 3 | 5910 | 4,181 | 2,549 | 3,093 | 3,177 | −0,084 | [−0,104; −0,061] |
| 4 | 836 | 3,888 | 2,421 | 2,788 | 3,004 | −0,216 | [−0,256; −0,173] |
| 5 | 119 | 3,655 | 2,181 | 2,476 | 2,900 | −0,424 | [−0,509; −0,333] |
| 6 | 5 | 3,000 | 2,160 | 2,300 | 2,831 | −0,531 | — |

**eng ko'p morfema** — kataklar [1, 2, 3, 4, 5]

| x | n | R(x) | S(x) | kuzatilgan ȳ | y_sof | farq | 95 % (farq) |
|---|---|---|---|---|---|---|---|
| 1 | 34448 | 4,540 | — | 4,540 | 4,540 | 0,000 | — |
| 2 | 19805 | 4,210 | 2,206 | 3,208 | 3,373 | −0,165 | — |
| 3 | 9552 | 4,281 | 2,144 | 2,856 | 2,984 | −0,127 | [−0,144; −0,111] |
| 4 | 2349 | 4,111 | 2,134 | 2,629 | 2,789 | −0,161 | [−0,184; −0,138] |
| 5 | 267 | 3,757 | 2,067 | 2,405 | 2,673 | −0,267 | [−0,320; −0,212] |
| 6 | 15 | 3,667 | 2,013 | 2,289 | 2,595 | −0,306 | — |
| 7 | 1 | 3,000 | 2,500 | 2,571 | 2,539 | 0,032 | — |

## E8 (post hoc 4)

### E8a — klasterli bootstrap (gap bo'yicha)

Gaplar qaytarib tanlanadi (kamida bitta kuzatuvli gaplar — klaster), 1 000 takror, seed 20261022; kataklar va fit tahlil.py dagidek (n ≥ 30, n-vaznli NLS, sodda model). Token oralig'i — natija.json. Gap ID: K1 — bor (surat gapi indeksi, held-out filtridan keyin); K2 — bor (surat gapi indeksi, held-out filtridan keyin); treebank — bor (ud_system_output gapi indeksi, held-out filtridan keyin).

| daraja | N | klaster (K1 / K2 / treebank) | klaster hajmi o'rtacha / max | b | 95 % (klaster) | 95 % (token) | kenglik nisbati | yaqinlashmagan |
|---|---|---|---|---|---|---|---|---|
| Q2 standart (max score) | 66437 | 6363 (889 / 4292 / 1182) | 10,4 / 75 | −0,427 | [−0,434; −0,421] | [−0,434; −0,421] | 0,92 | 0 |
| Q3 | 79030 | 6368 (889 / 4297 / 1182) | 12,4 / 85 | −0,122 | [−0,125; −0,119] | [−0,125; −0,119] | 1,02 | 0 |

### E8b — sof aralashma tayanch sezgirligi (E7)

y_mix(x) = [P₀ + (x − 1)·S₀]/x. Tayanch: (i) P₀ = P(1), S₀ = S(2) — asosiy (E7 b_sof bilan aynan, tekshirilgan); (ii) P₀ = P(1), S₀ = S(3); (iii) P₀ = P̄ (n ≥ 30 kataklardagi barcha kuzatuvlar bo'yicha bosh qism o'rtachasi), S₀ = S̄ (x ≥ 2 kataklarda tobe qism birligi bo'yicha o'rtacha: klauza — har ergash klauza, morfema — har qo'shimcha; E8k tuzatishidan oldin klauzada gap ichidagi o'rtachalar o'rtachasi edi). P = M (klauza) yoki R (morfema). Pasayish ulushi = [y_mix(1) − y_mix(x_oxirgi)] / [ȳ(1) − ȳ(x_oxirgi)], x_oxirgi — oxirgi n ≥ 30 katak. 95 % — bootstrap (klauza: gap, morfema: token; 1 000, seed 20261021).

| daraja | umumiy b | tayanch | P₀ [95 %] | S₀ [95 %] | b_mix [95 %] | pasayish ulushi [95 %] |
|---|---|---|---|---|---|---|
| klauza · tor | −0,662 | (i) | 7,831 [7,568; 8,147] | 4,346 [4,041; 4,683] | −0,333 [−0,373; −0,288] | 0,535 [0,472; 0,597] |
| klauza · tor | −0,662 | (ii) | 7,831 [7,568; 8,147] | 3,579 [3,335; 3,856] | −0,425 [−0,460; −0,386] | 0,653 [0,594; 0,727] |
| klauza · tor | −0,662 | (iii) | 6,589 [6,375; 6,825] | 3,763 [3,585; 3,966] | −0,318 [−0,348; −0,288] | 0,434 [0,388; 0,484] |
| klauza · keng | −0,628 | (i) | 7,136 [6,805; 7,489] | 3,857 [3,639; 4,091] | −0,339 [−0,375; −0,300] | 0,613 [0,558; 0,665] |
| klauza · keng | −0,628 | (ii) | 7,136 [6,805; 7,489] | 3,150 [2,927; 3,385] | −0,432 [−0,470; −0,395] | 0,746 [0,689; 0,803] |
| klauza · keng | −0,628 | (iii) | 5,746 [5,558; 5,949] | 3,357 [3,227; 3,501] | −0,300 [−0,327; −0,272] | 0,447 [0,404; 0,492] |
| morfema · standart | −0,427 | (i) | 4,547 [4,524; 4,569] | 2,364 [2,351; 2,376] | −0,368 [−0,372; −0,364] | 0,845 [0,813; 0,877] |
| morfema · standart | −0,427 | (ii) | 4,547 [4,524; 4,569] | 2,230 [2,216; 2,244] | −0,396 [−0,399; −0,392] | 0,896 [0,864; 0,932] |
| morfema · standart | −0,427 | (iii) | 4,404 [4,390; 4,420] | 2,295 [2,286; 2,304] | −0,367 [−0,369; −0,365] | 0,816 [0,787; 0,849] |
| morfema · eng kam | −0,395 | (i) | 4,564 [4,542; 4,586] | 2,484 [2,472; 2,496] | −0,353 [−0,356; −0,349] | 0,797 [0,766; 0,834] |
| morfema · eng kam | −0,395 | (ii) | 4,564 [4,542; 4,586] | 2,549 [2,533; 2,567] | −0,340 [−0,344; −0,336] | 0,772 [0,740; 0,807] |
| morfema · eng kam | −0,395 | (iii) | 4,433 [4,419; 4,449] | 2,496 [2,486; 2,505] | −0,336 [−0,338; −0,333] | 0,742 [0,713; 0,776] |
| morfema · eng ko'p | −0,450 | (i) | 4,540 [4,519; 4,562] | 2,206 [2,195; 2,216] | −0,395 [−0,398; −0,392] | 0,875 [0,853; 0,898] |
| morfema · eng ko'p | −0,450 | (ii) | 4,540 [4,519; 4,562] | 2,144 [2,132; 2,156] | −0,408 [−0,411; −0,405] | 0,898 [0,875; 0,922] |
| morfema · eng ko'p | −0,450 | (iii) | 4,386 [4,372; 4,401] | 2,167 [2,159; 2,174] | −0,387 [−0,389; −0,385] | 0,832 [0,811; 0,854] |

**klauza · tor** — kataklar [1, 2, 3, 4], x_oxirgi = 4

| x | n | ȳ | y_mix (i) | ȳ − y_mix (i) [95 %] | y_mix (ii) | ȳ − y_mix (ii) [95 %] | y_mix (iii) | ȳ − y_mix (iii) [95 %] |
|---|---|---|---|---|---|---|---|---|
| 1 | 628 | 7,831 | 7,831 | 0,000 [0,000; 0,000] | 7,831 | 0,000 [0,000; 0,000] | 6,589 | 1,242 [1,054; 1,451] |
| 2 | 332 | 4,971 | 6,089 | −1,117 [−1,338; −0,902] | 5,705 | −0,734 [−0,997; −0,446] | 5,176 | −0,205 [−0,381; −0,034] |
| 3 | 140 | 3,812 | 5,508 | −1,696 [−2,044; −1,358] | 4,996 | −1,184 [−1,357; −1,000] | 4,705 | −0,893 [−1,116; −0,671] |
| 4 | 44 | 2,943 | 5,218 | −2,274 [−2,673; −1,862] | 4,642 | −1,699 [−2,089; −1,248] | 4,470 | −1,527 [−1,849; −1,172] |

**klauza · keng** — kataklar [1, 2, 3, 4], x_oxirgi = 4

| x | n | ȳ | y_mix (i) | ȳ − y_mix (i) [95 %] | y_mix (ii) | ȳ − y_mix (ii) [95 %] | y_mix (iii) | ȳ − y_mix (iii) [95 %] |
|---|---|---|---|---|---|---|---|---|
| 1 | 433 | 7,136 | 7,136 | 0,000 [0,000; 0,000] | 7,136 | 0,000 [0,000; 0,000] | 5,746 | 1,391 [1,147; 1,652] |
| 2 | 399 | 4,604 | 5,497 | −0,893 [−1,121; −0,670] | 5,143 | −0,539 [−0,804; −0,273] | 4,551 | 0,053 [−0,087; 0,199] |
| 3 | 203 | 3,535 | 4,950 | −1,415 [−1,673; −1,164] | 4,479 | −0,944 [−1,102; −0,783] | 4,153 | −0,618 [−0,773; −0,471] |
| 4 | 81 | 3,127 | 4,677 | −1,550 [−1,833; −1,284] | 4,147 | −1,020 [−1,291; −0,750] | 3,954 | −0,827 [−1,045; −0,632] |

**morfema · standart** — kataklar [1, 2, 3, 4, 5], x_oxirgi = 5

| x | n | ȳ | y_mix (i) | ȳ − y_mix (i) [95 %] | y_mix (ii) | ȳ − y_mix (ii) [95 %] | y_mix (iii) | ȳ − y_mix (iii) [95 %] |
|---|---|---|---|---|---|---|---|---|
| 1 | 34502 | 4,547 | 4,547 | 0,000 [0,000; 0,000] | 4,547 | 0,000 [0,000; 0,000] | 4,404 | 0,142 [0,128; 0,157] |
| 2 | 21905 | 3,299 | 3,455 | −0,156 [−0,172; −0,140] | 3,389 | −0,089 [−0,108; −0,070] | 3,350 | −0,050 [−0,062; −0,040] |
| 3 | 8211 | 2,922 | 3,092 | −0,169 [−0,187; −0,151] | 3,003 | −0,080 [−0,095; −0,066] | 2,998 | −0,076 [−0,089; −0,063] |
| 4 | 1649 | 2,725 | 2,910 | −0,185 [−0,211; −0,158] | 2,810 | −0,085 [−0,111; −0,059] | 2,822 | −0,098 [−0,121; −0,074] |
| 5 | 162 | 2,479 | 2,800 | −0,321 [−0,400; −0,245] | 2,694 | −0,215 [−0,291; −0,135] | 2,717 | −0,238 [−0,315; −0,161] |

**morfema · eng kam** — kataklar [1, 2, 3, 4, 5], x_oxirgi = 5

| x | n | ȳ | y_mix (i) | ȳ − y_mix (i) [95 %] | y_mix (ii) | ȳ − y_mix (ii) [95 %] | y_mix (iii) | ȳ − y_mix (iii) [95 %] |
|---|---|---|---|---|---|---|---|---|
| 1 | 34734 | 4,564 | 4,564 | 0,000 [0,000; 0,000] | 4,564 | 0,000 [0,000; 0,000] | 4,433 | 0,131 [0,116; 0,145] |
| 2 | 24833 | 3,408 | 3,524 | −0,116 [−0,132; −0,101] | 3,557 | −0,148 [−0,167; −0,130] | 3,465 | −0,056 [−0,067; −0,047] |
| 3 | 5910 | 3,093 | 3,177 | −0,084 [−0,104; −0,061] | 3,221 | −0,128 [−0,143; −0,111] | 3,142 | −0,049 [−0,063; −0,031] |
| 4 | 836 | 2,788 | 3,004 | −0,216 [−0,256; −0,173] | 3,053 | −0,265 [−0,306; −0,225] | 2,980 | −0,193 [−0,230; −0,154] |
| 5 | 119 | 2,476 | 2,900 | −0,424 [−0,509; −0,333] | 2,952 | −0,477 [−0,565; −0,385] | 2,883 | −0,408 [−0,492; −0,315] |

**morfema · eng ko'p** — kataklar [1, 2, 3, 4, 5], x_oxirgi = 5

| x | n | ȳ | y_mix (i) | ȳ − y_mix (i) [95 %] | y_mix (ii) | ȳ − y_mix (ii) [95 %] | y_mix (iii) | ȳ − y_mix (iii) [95 %] |
|---|---|---|---|---|---|---|---|---|
| 1 | 34448 | 4,540 | 4,540 | 0,000 [0,000; 0,000] | 4,540 | 0,000 [0,000; 0,000] | 4,386 | 0,154 [0,141; 0,169] |
| 2 | 19805 | 3,208 | 3,373 | −0,165 [−0,182; −0,149] | 3,342 | −0,134 [−0,153; −0,116] | 3,276 | −0,069 [−0,081; −0,058] |
| 3 | 9552 | 2,856 | 2,984 | −0,127 [−0,144; −0,111] | 2,943 | −0,086 [−0,100; −0,074] | 2,907 | −0,050 [−0,062; −0,039] |
| 4 | 2349 | 2,629 | 2,789 | −0,161 [−0,184; −0,138] | 2,743 | −0,115 [−0,138; −0,091] | 2,722 | −0,093 [−0,113; −0,074] |
| 5 | 267 | 2,405 | 2,673 | −0,267 [−0,320; −0,212] | 2,623 | −0,218 [−0,273; −0,163] | 2,611 | −0,205 [−0,260; −0,151] |

### E8c — turlarni saqlovchi tasodifiy model va B&Č (klauza, tor)

Namuna: E5/E7 dagi gaplar (bosh klauzasida so'z bor), N = 1182 (bosh klauzasi so'zsiz chiqarilgan gap 0), ergash klauza 907, kataklar [1, 2, 3, 4]. Haqiqiy b shu namunada −0,662 (Q1 tor, barcha gaplar: −0,662). Har takror: k ketma-ketligi asl; ergash klauza uzunliklari korpus bo'ylab almashtiriladi (qaytarmasdan) va har gapga k − 1 tadan beriladi; bosh klauza — (1) bosh klauzalar bo'ylab almashtiriladi yoki (2) gapning o'zinikida qoladi. 1000 takror, seed 20261023 (ikkala variant bir xil seed). B&Č — tahlil.bc_model, 1000 takror, seed 20261024; ijobiy nazorat: seed 20261021 bilan 100 takror natija.json Q5 bilan aynan — ha.

| model | takror (fit) | b mediana | 95 % | min / max | b < 0 | b ≤ haqiqiy b | ȳ qat'iy monoton |
|---|---|---|---|---|---|---|---|
| bosh va ergash almashtirilgan | 1000 (1000) | −0,333 | [−0,393; −0,279] | −0,426 / −0,233 | 1000 | 0 | 834 |
| o'z bosh klauzasi, ergash almashtirilgan | 1000 (1000) | −0,695 | [−0,708; −0,682] | −0,722 / −0,674 | 1000 | 1000 | 807 |
| B&Č 1 000 | 1000 (1000) | 0,001 | [−0,068; 0,063] | −0,132 / 0,092 | 489 | 0 | 46 |

«b ≤ haqiqiy b»: turlarni saqlovchi modelda haqiqiy b = −0,662 (shu namuna), B&Č da −0,662 (Q1 tor).

### E8d — chegara sezgirligi (Q1 treebank, tor)

tahlil.qator, n-chegara faqat jarayon xotirasida o'zgartirildi (T.NMIN); bootstrap 1 000, seed 20261021. n ≥ 30 qatori natija.json bilan aynan (tekshirilgan).

| chegara | kataklar | b | 95 % | monoton | §4.4 hukm |
|---|---|---|---|---|---|
| n ≥ 20 | [1, 2, 3, 4, 5] | −0,650 | [−0,704; −0,596] | yo'q | bajarilmadi |
| n ≥ 25 | [1, 2, 3, 4, 5] | −0,650 | [−0,704; −0,596] | yo'q | bajarilmadi |
| n ≥ 30 | [1, 2, 3, 4] | −0,662 | [−0,718; −0,607] | ha | bajarildi |

UzUDT UT bilan bir xil kataklarda ([1, 2, 3]; UzUDT dan boshqa katakdagi 76 gap chiqarildi, bootstrap qolgan gaplarda):

| qator | N | kataklar | b | 95 % | monoton |
|---|---|---|---|---|---|
| UT | 500 | [1, 2, 3] | −0,838 | [−0,908; −0,755] | ha |
| UzUDT (UT kataklari) | 606 | [1, 2, 3] | −0,427 | [−0,503; −0,344] | ha |
| UzUDT (barcha n ≥ 30 kataklar) | 682 | [1, 2, 3, 4] | −0,450 | [−0,523; −0,378] | ha |

Δb UT − UzUDT (uch katak): −0,411 [−0,521; −0,296] (mustaqil bootstrap, 1000 juft takror).

### E8e — vaznsiz NLS (faqat taqqoslash; prereg — n-vaznli)

a·x^b kataklar o'rtachalariga sigma siz (curve_fit); kataklar va bootstrap indekslari tahlil.qator dagidek (1 000, seed 20261021).

| daraja | N | kataklar | b (vaznsiz) | 95 % | b (vaznli, prereg) | 95 % | yaqinlashmagan |
|---|---|---|---|---|---|---|---|
| Q1 treebank tor | 1182 | [1, 2, 3, 4] | −0,678 | [−0,731; −0,623] | −0,662 | [−0,718; −0,607] | 0 |
| Q2 standart (max score) | 66437 | [1, 2, 3, 4, 5] | −0,379 | [−0,389; −0,369] | −0,427 | [−0,434; −0,421] | 0 |
| Q3 | 79030 | [1, 2, 3, 4, 5, 6, 7, 8] | −0,086 | [−0,092; −0,080] | −0,122 | [−0,125; −0,119] | 0 |

### E8f — ΔAIC = AIC(to'liq) − AIC(sodda)

AIC = K·ln(WRSS/K) + 2p (n-vaznli, n ≥ 30 kataklarda; tahlil.fit). Qiymatlar natija.json dan, qayta hisob bilan tekshirilgan. «afzal»: to'liq, agar ΔAIC < −2.

| qator | K | AIC (sodda) | AIC (to'liq) | ΔAIC | c (to'liq) | afzal |
|---|---|---|---|---|---|---|
| Q1 treebank tor | 4 | 0,71 | −0,21 | −0,92 | 0,045 | sodda |
| Q1 treebank keng | 4 | 1,25 | 1,32 | 0,07 | −0,036 | sodda |
| Q1 K1 VDU | 6 | 20,43 | 15,06 | −5,37 | −0,115 | toliq |
| Q1 K2 VDU | 8 | 36,45 | 19,36 | −17,09 | −0,154 | toliq |
| Q2 jami (max score) | 5 | 23,88 | 11,39 | −12,48 | −0,131 | toliq |
| Q3 jami | 8 | 25,45 | 12,03 | −13,42 | −0,046 | toliq |
| Q4b A: treebank V0 | 4 | 10,10 | 0,68 | −9,42 | −0,170 | toliq |
| Q4c eng kam morfema | 5 | 22,88 | 17,33 | −5,55 | −0,118 | toliq |
| Q4c eng ko'p morfema | 5 | 26,19 | 16,85 | −9,35 | −0,151 | toliq |

### E8g — ikkinchi darajali aralashma

Klauza: E5 birliklari (ergash klauza = bosh tokeni deprel asosi); ulush — shu k dagi ergash klauzalar ichida; o'rtacha — klauza darajasida (E7 S(k) esa gap ichidagi o'rtachalarning o'rtachasi).

**tor**

| k | gap | fitga | ergash klauza | S(k) klauza o'rt. | S(k) E7 | advcl: n · ulush · o'rt. | ccomp: n · ulush · o'rt. | conj: n · ulush · o'rt. | parataxis: n · ulush · o'rt. | csubj: n · ulush · o'rt. | boshqa: n · ulush · o'rt. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 332 | ha | 332 | 4,346 | 4,346 | 190 · 57,2 % · 3,663 | 52 · 15,7 % · 5,000 | 41 · 12,3 % · 5,488 | 31 · 9,3 % · 5,516 | 18 · 5,4 % · 5,056 | 0 · 0,0 % · — |
| 3 | 140 | ha | 280 | 3,579 | 3,579 | 170 · 60,7 % · 3,006 | 40 · 14,3 % · 4,000 | 25 · 8,9 % · 3,880 | 32 · 11,4 % · 5,156 | 13 · 4,6 % · 5,308 | 0 · 0,0 % · — |
| 4 | 44 | ha | 132 | 2,689 | 2,689 | 77 · 58,3 % · 2,364 | 19 · 14,4 % · 3,211 | 16 · 12,1 % · 2,250 | 16 · 12,1 % · 3,938 | 4 · 3,0 % · 3,250 | 0 · 0,0 % · — |

«boshqa» deprel (k = 2–4): yo'q.

**keng**

| k | gap | fitga | ergash klauza | S(k) klauza o'rt. | S(k) E7 | advcl: n · ulush · o'rt. | ccomp: n · ulush · o'rt. | conj: n · ulush · o'rt. | parataxis: n · ulush · o'rt. | csubj: n · ulush · o'rt. | boshqa: n · ulush · o'rt. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 399 | ha | 399 | 3,857 | 3,857 | 127 · 31,8 % · 3,496 | 40 · 10,0 % · 5,025 | 23 · 5,8 % · 5,087 | 24 · 6,0 % · 4,833 | 11 · 2,8 % · 5,091 | 174 · 43,6 % · 3,477 |
| 3 | 203 | ha | 406 | 3,150 | 3,150 | 159 · 39,2 % · 2,836 | 42 · 10,3 % · 3,619 | 38 · 9,4 % · 4,079 | 29 · 7,1 % · 5,000 | 14 · 3,4 % · 4,500 | 124 · 30,5 % · 2,524 |
| 4 | 81 | ha | 243 | 2,881 | 2,881 | 111 · 45,7 % · 2,838 | 17 · 7,0 % · 2,588 | 15 · 6,2 % · 2,267 | 17 · 7,0 % · 4,529 | 8 · 3,3 % · 4,250 | 75 · 30,9 % · 2,613 |

«boshqa» deprel (k = 2–4): acl 221, xcomp 152.

Morfema: Q2 namunasi, standart (max score) tahlil; qo'shimcha turi analizator element kodidan (kontekstli tur, `_resolve_affix_type`): X3 → kelishik, X → ko'plik, X2 → egalik, U5 → shaxs, qolgan kodlar (A1–A6, AG, T, U, U1–U4, kompozit «+») → boshqa. Uzunlik — grafema (E1 dagi taqsimot; S(x) E1 bilan aynan, tekshirilgan).

| x | token | qo'shimcha | S(x) | kelishik: n · ulush · o'rt. | ko'plik: n · ulush · o'rt. | egalik: n · ulush · o'rt. | shaxs: n · ulush · o'rt. | boshqa: n · ulush · o'rt. | boshqa ichida kompozit |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 21905 | 21905 | 2,364 | 7066 · 32,3 % · 2,337 | 1286 · 5,9 % · 2,964 | 2853 · 13,0 % · 1,395 | 212 · 1,0 % · 1,514 | 10488 · 47,9 % · 2,589 | 595 |
| 3 | 8211 | 16422 | 2,230 | 4590 · 28,0 % · 2,319 | 1914 · 11,7 % · 2,995 | 3724 · 22,7 % · 1,321 | 802 · 4,9 % · 1,837 | 5392 · 32,8 % · 2,571 | 272 |
| 4 | 1649 | 4947 | 2,223 | 1099 · 22,2 % · 2,301 | 878 · 17,7 % · 2,995 | 1024 · 20,7 % · 1,262 | 139 · 2,8 % · 1,705 | 1807 · 36,5 % · 2,386 | 48 |
| 5 | 162 | 648 | 2,150 | 121 · 18,7 % · 2,421 | 59 · 9,1 % · 2,983 | 104 · 16,0 % · 1,240 | 18 · 2,8 % · 1,333 | 346 · 53,4 % · 2,228 | 5 |

### E8h — uch aniqlik

**(1) Treebank tokenlari: 11 072 va 1-jadval katak yig'indisi**

| o'lcham | qiymat |
|---|---|
| UD non-PUNCT token (natija.json `kirish`) | 11072 (11072) |
| UD PUNCT token | 2426 |
| UD ko'p so'zli token (range) qatori | 0 |
| tizim so'zi (bo'shliq-bo'lak, chetdagi tinish olingan) | 11039 |
| — harf-raqamsiz (PUNCT siz so'z emas, Q1 ga kirmaydi) | 44 (UD non-PUNCT bilan ustma-ust: 0) |
| — harf-raqamli (Q1 so'zi) | 10995 |
| 1-jadval Σ n·x·ȳ: tor / keng / V0 | 10995 / 10995 / 10995 |
| harfli so'z, ≥ 2 UD non-PUNCT tokenga to'g'ri keladi | 76 (ortiqcha token 79; defisli 73, apostrofli 18) |
| harfli so'z, UD non-PUNCT tokeni yo'q (faqat PUNCT bilan ustma-ust) | 2 |
| UD non-PUNCT, hech bir so'zga tushmagan / 2 so'zga tushgan | 0 / 0 |
| tenglik: harfli + ortiqcha − nolli + harfsiz∩UD = UD non-PUNCT | 11072 — ha |

**(2) Tahlil qilinmagan tokenlarda ng**

- Kod: tahlil.q2_q3: B = [] (noma'lum, yuza teng emas, bo'sh morfema); Q2 namunasida B = morf_chegaralari(score); Q3: gr = grafemalar(w, B); grafemalar: ng — chegara (i+1) ∈ B bo'lmasa 1 grafema.
- Javob: **har doim 1 (B bo'sh -> ng hech qachon bo'linmaydi)**.

| guruh · o'lcham | son |
|---|---|
| Q2 namunasi · ng | 4677 |
| Q2 namunasi · ng_2_grafema | 594 |
| Q2 namunasi · token | 4631 |
| noma'lum · ng | 1059 |
| noma'lum · ng_2_grafema | 0 |
| noma'lum · token | 1041 |
| yuza teng emas · ng | 194 |
| yuza teng emas · ng_2_grafema | 0 |
| yuza teng emas · token | 191 |

**(3) prereg.md, commit f3bbe32 — Q5 modeli**

- f3bbe32 dagi Q5 sarlavhasi Benešová & Čech modeli: **ha**; «qayta kesish» asl varianti tashlangani o'sha faylda qayd etilgan: ha.
- prereg.md ga tegilgan commitlar: f3bbe32; joriy fayl f3bbe32 dagi bilan aynan: ha. Keyin almashtirilmagan.

### E8i — Ilova A1-jadvali (natija.json)

m(x) = a·x^b — sodda model qiymati (natija.json dagi a, b; fit n ≥ 30 kataklarda, «fitga» — ha). SD — kuzatuvlar standart og'ishi.

**Q1 treebank keng** — a = 7,131, b = −0,628

| x | n | ȳ | SD | m(x) | fitga |
|---|---|---|---|---|---|
| 1 | 433 | 7,136 | 3,494 | 7,131 | ha |
| 2 | 399 | 4,604 | 1,674 | 4,615 | ha |
| 3 | 203 | 3,535 | 1,310 | 3,577 | ha |
| 4 | 81 | 3,127 | 0,924 | 2,986 | ha |
| 5 | 28 | 2,621 | 0,663 | 2,596 | — |
| 6 | 23 | 2,674 | 0,643 | 2,315 | — |
| 7 | 9 | 2,905 | 1,268 | 2,101 | — |
| 8 | 5 | 3,225 | 0,920 | 1,932 | — |
| 11 | 1 | 1,545 | — | 1,582 | — |

**Q1 K1 VDU** — a = 10,882, b = −0,514

| x | n | ȳ | SD | m(x) | fitga |
|---|---|---|---|---|---|
| 1 | 143 | 11,154 | 4,982 | 10,882 | ha |
| 2 | 202 | 7,181 | 3,079 | 7,618 | ha |
| 3 | 226 | 6,003 | 2,114 | 6,184 | ha |
| 4 | 164 | 5,733 | 1,656 | 5,333 | ha |
| 5 | 78 | 4,954 | 1,180 | 4,755 | ha |
| 6 | 48 | 4,705 | 1,328 | 4,329 | ha |
| 7 | 19 | 4,541 | 0,726 | 3,999 | — |
| 8 | 4 | 5,125 | 0,771 | 3,734 | — |
| 9 | 3 | 4,444 | 0,556 | 3,514 | — |
| 10 | 1 | 3,200 | — | 3,329 | — |
| 13 | 1 | 6,692 | — | 2,908 | — |

**Q1 K2 VDU** — a = 6,484, b = −0,339

| x | n | ȳ | SD | m(x) | fitga |
|---|---|---|---|---|---|
| 1 | 903 | 6,766 | 3,011 | 6,484 | ha |
| 2 | 1361 | 4,752 | 2,023 | 5,126 | ha |
| 3 | 1017 | 4,385 | 1,537 | 4,467 | ha |
| 4 | 511 | 4,218 | 1,271 | 4,052 | ha |
| 5 | 271 | 4,179 | 1,217 | 3,756 | ha |
| 6 | 132 | 4,154 | 1,065 | 3,531 | ha |
| 7 | 49 | 4,289 | 1,094 | 3,351 | ha |
| 8 | 31 | 4,294 | 1,044 | 3,203 | ha |
| 9 | 6 | 4,370 | 0,960 | 3,077 | — |
| 10 | 8 | 4,638 | 0,980 | 2,969 | — |
| 11 | 4 | 4,045 | 0,563 | 2,875 | — |
| 12 | 2 | 5,542 | 2,298 | 2,791 | — |
| 16 | 1 | 4,188 | — | 2,532 | — |
| 18 | 1 | 3,833 | — | 2,433 | — |

### E8k — E8c 1-variant va E8b (iii) nomuvofiqligi

E8c 1-variant: bosh klauza havzasi 1182 (barcha gaplar), ergash klauza havzasi 907; permutatsiya (qaytarmasdan), har takrorda ikkala havza; k ≥ 5 gaplar (38 ta, 163 ergash klauza) havzaga kiradi va yig'iladi, fitga kirmaydi; y = (M' + Σ S')/k har gapda; ȳ(k) — katak o'rtachasi; fit k = 1…4 (n ≥ 30), n-vaznli.

| o'lcham | qiymat |
|---|---|
| M̄ — barcha 1 182 bosh klauza (simulyatsiya havzasi) | 6,523 |
| S̄ — barcha ergash klauzalar, klauza-vaznli (simulyatsiya havzasi) | 3,622 |
| P̄ — k = 1…4 gaplardagi bosh klauza ((iii), eski va yangi) | 6,589 |
| S̄ — k = 2…4, gap-vaznli ((iii) ESKI, xato) | 3,997 |
| S̄ — k = 2…4, klauza-vaznli ((iii) YANGI) | 3,763 |
| b: simulyatsiya medianasi / havza kutilmasi [M̄ + (k − 1)·S̄]/k | −0,333 / −0,332 |
| b_mix (iii): eski / yangi | −0,287 / −0,318 |

| k | n | kuzatilgan ȳ | simulyatsiya ȳ (1 000 o'rt.) [2,5–97,5 %] | kutilma (havza M̄, S̄) | y_mix (iii) eski | y_mix (iii) yangi |
|---|---|---|---|---|---|---|
| 1 | 628 | 7,831 | 6,527 [6,322; 6,741] | 6,523 | 6,589 | 6,589 |
| 2 | 332 | 4,971 | 5,072 [4,863; 5,250] | 5,072 | 5,293 | 5,176 |
| 3 | 140 | 3,812 | 4,591 [4,333; 4,845] | 4,589 | 4,861 | 4,705 |
| 4 | 44 | 2,943 | 4,334 [3,932; 4,722] | 4,347 | 4,645 | 4,470 |

E8b (iii) klauza qatorlari — eski (avvalgi posthoc.json) va yangi:

| daraja | P₀ | S₀ eski → yangi | b_mix eski → yangi | pasayish ulushi eski → yangi |
|---|---|---|---|---|
| klauza · tor | 6,589 | 3,997 → 3,763 | −0,287 [−0,321; −0,254] → −0,318 [−0,348; −0,288] | 0,398 → 0,434 [0,388; 0,484] |
| klauza · keng | 5,746 | 3,531 → 3,357 | −0,274 [−0,303; −0,243] → −0,300 [−0,327; −0,272] | 0,414 → 0,447 [0,404; 0,492] |

## E10

### E10a — AIC formulasi (tahlil.fit, koddan)

```python
K = len(x)
p, _ = curve_fit(f, x, ybar, p0=p0, sigma=1 / np.sqrt(n), maxfev=20000)
wrss = float((n * (ybar - f(x, *p)) ** 2).sum())
aic = K * np.log(wrss / K) + 2 * len(p) if wrss > 0 else float('-inf')
out['delta_aic_toliq_minus_sodda'] = t['aic'] - s['aic']
out['afzal'] = 'toliq' if t['aic'] < s['aic'] - 2 else 'sodda'
```

K — fitga kirgan kataklar soni (n ≥ 30); qoldiq — n-vaznli RSS: WRSS = Σ n_x·(ȳ_x − f(x))² (curve_fit sigma = 1/√n bilan bir xil vazn); likelihood — Gauss, σ² ning ML bahosi WRSS/K o'rniga qo'yilgan, doimiy hadlar tashlangan: AIC = K·ln(WRSS/K) + 2p; p — model parametrlari (sodda 2: a, b; to'liq 3: a, b, c), σ sanalmaydi (ikkala modelga bir xil qo'shiladi, ΔAIC ga ta'sir qilmaydi). ΔAIC = AIC(to'liq) − AIC(sodda); afzal = to'liq, agar ΔAIC < −2.

### E10b — klaster diagnostikasi

ICC(1) — bir yo'nalishli ANOVA (muvozanatsiz, n₀): y bo'yicha va y − ȳ(x) (katak o'rtachasi ayirilgan) bo'yicha. Nazorat: har token o'z klasteri — bir xil seed (20261022) bilan; shuningdek seed 20261021 bilan (natija.json token oralig'i bilan solishtirish).

| daraja | N | klaster | hajm min / median / max | 1 tokenli klaster | ICC(y) | ICC(y − ȳ(x)) | n₀ |
|---|---|---|---|---|---|---|---|
| Q2 standart (max score) | 66437 | 6363 | 1 / 9,0 / 75 | 50 | 0,0332 | 0,0402 | 10,44 |
| Q3 | 79030 | 6368 | 1 / 11,0 / 85 | 1 | −0,0065 | −0,0055 | 12,41 |

| daraja | b | 95 % gap-klaster (seed 20261022) | 95 % token-klaster (seed 20261022) | 95 % token-klaster (seed 20261021) | 95 % natija.json token |
|---|---|---|---|---|---|
| Q2 standart (max score) | −0,4275 | [−0,4335; −0,4211] | [−0,4334; −0,4212] | [−0,4343; −0,4209] | [−0,4343; −0,4209] |
| Q3 | −0,1217 | [−0,1246; −0,1186] | [−0,1248; −0,1186] | [−0,1246; −0,1187] | [−0,1246; −0,1187] |

### E10c — ajratish treebank bo'yicha (klauza, tor; E7 usuli)

| treebank | N | kataklar | b [95 %] | b_M [95 %] | b_S [95 %] | b_mix (i) [95 %] | pasayish ulushi (i) [95 %] |
|---|---|---|---|---|---|---|---|
| UT | 500 | [1, 2, 3] | −0,838 [−0,908; −0,755] | −0,738 [−0,843; −0,629] | aniqlanmadi: x ≥ 2 kataklar [2, 3] (< 3) | −0,385 [−0,426; −0,341] | 0,564 [0,503; 0,626] |
| UzUDT | 682 | [1, 2, 3, 4] | −0,450 [−0,523; −0,378] | −0,295 [−0,395; −0,199] | −0,424 [−0,668; −0,170] | −0,260 [−0,329; −0,191] | 0,522 [0,404; 0,652] |

### E10d — o'zak uzunligi R(x) turkum bo'yicha (Q2 namunasi, standart tahlil)

Turkum — analizator o'zak kodi (C = ot, G = fe'l; `kkt_code_for_word_type`). 95 % — token bootstrap (1 000).

| x | ot: n | R | 95 % | fe'l: n | R | 95 % | hammasi: n | R |
|---|---|---|---|---|---|---|---|---|
| 1 | 11140 | 5,217 | [5,181; 5,252] | 3352 | 3,937 | [3,887; 3,986] | 34502 | 4,547 |
| 2 | 9833 | 4,887 | [4,851; 4,921] | 10027 | 3,604 | [3,579; 3,630] | 21905 | 4,235 |
| 3 | 4306 | 4,873 | [4,823; 4,931] | 3278 | 3,607 | [3,567; 3,651] | 8211 | 4,306 |
| 4 | 886 | 4,734 | [4,614; 4,848] | 553 | 3,584 | [3,483; 3,702] | 1649 | 4,228 |

### E10e — Q2 noyob so'z shakllari (tiplar) bo'yicha

Har tip (tozalangan token) bir marta; N = 16916 tip. Bootstrap tip darajasida (1 000, seed 20261021).

| N | kataklar | b [95 %] | b_R [95 %] | b_S [95 %] | b_mix (i) [95 %] | pasayish ulushi (i) [95 %] |
|---|---|---|---|---|---|---|
| 16916 | [1, 2, 3, 4, 5] | −0,617 [−0,630; −0,604] | −0,240 [−0,253; −0,227] | −0,163 [−0,187; −0,139] | −0,453 [−0,460; −0,446] | 0,807 [0,787; 0,829] |

### E10f — K1 x = 13, K2 x = 16, 18 gaplari (matn chop etilmaydi)

Surat tokenlari va JSON `sentence` maydonida . ! ? olib tashlangan; K1 asl qatori (JSON meta.corpus_path) harf-raqam kaliti bilan topildi.

| korpus | gap | surat matnida . ! ? li gap | asl manba qatori | ichida . ! ? (oxiridan tashqari) bor qator |
|---|---|---|---|---|
| K1 | 889 | 0 | 900 | 19 |
| K2 | 4297 | 0 | — | — |

| korpus | x | token | so'z (harfli) | ȳ | surat: . ! ? li token | asl qator: mos | . ! ? jami | ichki . ! ? |
|---|---|---|---|---|---|---|---|---|
| K1 | 13 | 90 | 87 | 6,692 | 0 | 1 | 1 | 0 |
| K2 | 18 | 69 | 69 | 3,833 | 0 | aniqlanmadi: manba .pdf (repo ichida: yo'q) | — | — |
| K2 | 16 | 67 | 67 | 4,188 | 0 | aniqlanmadi: manba .pdf (repo ichida: yo'q) | — | — |

### E10g — 2-rasm uchun takrorlar

E8c 1-variant va B&Č takrorlari (har biri 1000) posthoc.json da saqlandi; medianalar E8c bilan aynan (tekshirilgan).

## E11 (post hoc 5)

### E11a — giperbola y = β + α/x

n-vaznli kichik kvadratlar (n ≥ 30 kataklar, tahlil.py dagi kataklar; parametrlar chiziqli — NLS yechimi aniq, curve_fit bilan tekshirilgan). 95 % — kuzatuv bootstrapi (1000, seed 20261021; P(1), S(2) E8b (i) bilan aynan). R² — n-vaznli.

| qator | N | kataklar | α [95 %] | β [95 %] | R² | P(1) − S(2) [95 %] | S(2) [95 %] | α − (P(1) − S(2)) [95 %] | β − S(2) [95 %] |
|---|---|---|---|---|---|---|---|---|---|
| klauza · tor | 1182 | [1, 2, 3, 4] | 5,981 [5,461; 6,521] | 1,869 [1,564; 2,186] | 0,9963 | 3,485 [3,034; 3,905] | 4,346 [4,041; 4,683] | 2,496 [2,149; 2,867] | −2,478 [−2,837; −2,127] |
| klauza · keng | 1182 | [1, 2, 3, 4] | 5,285 [4,720; 5,847] | 1,873 [1,593; 2,154] | 0,9979 | 3,279 [2,862; 3,701] | 3,857 [3,639; 4,091] | 2,006 [1,684; 2,329] | −1,984 [−2,301; −1,655] |
| morfema · standart | 66437 | [1, 2, 3, 4, 5] | 2,465 [2,426; 2,508] | 2,080 [2,056; 2,104] | 0,9997 | 2,183 [2,158; 2,209] | 2,364 [2,351; 2,376] | 0,282 [0,260; 0,305] | −0,284 [−0,307; −0,262] |
| morfema · tiplar | 16916 | [1, 2, 3, 4, 5] | 4,431 [4,321; 4,541] | 1,622 [1,574; 1,669] | 0,9994 | 3,558 [3,482; 3,633] | 2,510 [2,486; 2,536] | 0,873 [0,827; 0,923] | −0,889 [−0,943; −0,837] |

### E11b — prereg mezoni nol modellar ostida (klauza, tor)

Har takrorda: b < 0; 95 % oraliq (200 takrorli kuzatuv bootstrapi, seed 20261026) yuqori chegarasi < 0 (tahlil.hukm); n ≥ 30 kataklarda qat'iy kamayish. Takror b qiymatlari E10g bilan teng (max |farq|: turlarni saqlovchi 3.4e-09, B&Č 0.0e+00; nuqta b jadval o'rtachalaridan, tahlil.qator dagidek).

| model | seed | takror | b mediana [95 %] | b < 0 | oraliq 0 siz | monoton | uchalasi (N) |
|---|---|---|---|---|---|---|---|
| turlarni saqlovchi (E8c 1-variant) | 20261023 | 1000 | −0,333 [−0,393; −0,279] | 1000 | 1000 | 834 | 834 |
| klauza-havzali (B&Č) | 20261024 | 1000 | 0,001 [−0,068; 0,063] | 489 | 28 | 46 | 6 |

### E11c — morfema nol modeli (standart tahlil)

N = 66437 token; o'zak havzasi 66437, qo'shimcha havzasi 43963; x taqsimoti haqiqiy; 1000 takror, seed 20261025; ichki bootstrap 200 (seed 20261026). Kuzatilgan b = −0,4275.

| variant | b mediana | 95 % | min / max | b < 0 | b ≤ kuzatilgan | oraliq 0 siz | monoton | uchalasi (N) |
|---|---|---|---|---|---|---|---|---|
| tasodifiy o'zak + tasodifiy qo'shimchalar | −0,3668 | [−0,3725; −0,3606] | −0,3758 / −0,3567 | 1000 | 0 | 1000 | 996 | 996 |
| o'z o'zagi + tasodifiy qo'shimchalar | −0,4273 | [−0,4274; −0,4272] | −0,4274 / −0,4271 | 1000 | 0 | 1000 | 1000 | 1000 |

### E11d — m va x: korrelyatsiya nisbati η²

η² = SS_oraliq(m | x) / SS_jami(m); permutatsiya 1000 (m aralashtiriladi, seed 20261026); p = (#{η²_perm ≥ η²} + 1)/(1000 + 1).

| daraja | N | x qiymatlari | η² | permutatsiya mediana | permutatsiya max | ≥ kuzatilgan | p |
|---|---|---|---|---|---|---|---|
| klauza · tor (m — so'z, x — klauza) | 1182 | 7 | 0,2263 | 0,004545 | 0,021415 | 0 | 0,0010 |
| morfema · standart (m — grafema, x — morfema) | 66437 | 7 | 0,4263 | 0,000079 | 0,000417 | 0 | 0,0010 |
| bo'g'in (m — grafema, x — bo'g'in) | 79030 | 16 | 0,8766 | 0,000179 | 0,001102 | 0 | 0,0010 |

### E11e — manba bo'yicha

95 % — token bootstrap (tahlil.qator, 1000, seed 20261021).

| daraja | manba | N | kataklar | b [95 %] | monoton | hukm | b_mix (i) [95 %] | pasayish ulushi (i) [95 %] |
|---|---|---|---|---|---|---|---|---|
| Q2 standart | K1 | 13625 | [1, 2, 3, 4, 5] | −0,430 [−0,443; −0,415] | ha | bajarildi | −0,404 [−0,412; −0,397] | 0,896 [0,840; 0,961] |
| Q2 standart | K2 | 43191 | [1, 2, 3, 4, 5] | −0,422 [−0,429; −0,414] | ha | bajarildi | −0,352 [−0,356; −0,348] | 0,816 [0,781; 0,853] |
| Q2 standart | treebank | 9621 | [1, 2, 3, 4] | −0,450 [−0,466; −0,434] | ha | bajarildi | −0,379 [−0,388; −0,370] | 0,886 [0,849; 0,920] |
| Q3 | K1 | 16104 | [1, 2, 3, 4, 5, 6, 7, 8] | −0,119 [−0,127; −0,112] | yo'q | bajarilmadi | — | — |
| Q3 | K2 | 52046 | [1, 2, 3, 4, 5, 6, 7] | −0,125 [−0,129; −0,122] | ha | bajarildi | — | — |
| Q3 | treebank | 10880 | [1, 2, 3, 4, 5, 6] | −0,126 [−0,134; −0,118] | yo'q | bajarilmadi | — | — |

Klasterli bootstrap (E8a) manba bo'yicha qatlamlangan: **yo'q** — `_klaster_boot`:

```python
G = len(gid)
w = np.bincount(rng.integers(0, G, G), minlength=G).astype(float)
```

### E11f — tahlil.py rasmlaridagi xato chiziqlari

```python
# tahlil.q1_xy
y.append(sum(u) / len(u))
# tahlil.q2_q3
q2['y'].append(ng / len(a['score']))
q3['y'].append(len(gr) / v)
# tahlil.jadval
'sd': float(yy.std(ddof=1)) if m.sum() > 1 else None, 'fitga': bool(m.sum() >= NMIN)})
# tahlil.rasm
ee = [1.96 * r['sd'] / np.sqrt(r['n']) if r['sd'] is not None else 0 for r in R]
```

SD birligi: **har butunning o'rtachasi (gap / so'z y qiymati), alohida qismlar emas**; xato chizig'i ±1,96·SD/√n, n — katakdagi butunlar soni.

### E11g — jadvallar

**A2 — Q2 tiplar bo'yicha kataklar**

| x | n | ȳ | R(x) | S(x) | fitga |
|---|---|---|---|---|---|
| 1 | 3743 | 6,068 | 6,068 | — | ha |
| 2 | 7078 | 3,812 | 5,113 | 2,510 | ha |
| 3 | 4729 | 3,102 | 4,661 | 2,322 | ha |
| 4 | 1224 | 2,813 | 4,391 | 2,287 | ha |
| 5 | 134 | 2,543 | 3,963 | 2,188 | ha |
| 6 | 7 | 2,190 | 3,143 | 2,000 | yo'q |
| 7 | 1 | 2,571 | 3,000 | 2,500 | yo'q |

**A3 — klauza tor (E7, yaxlitlanmagan qiymatlardan 3 o'nlik)**

| k | n | M(k) | S(k) | y(k) | fitga |
|---|---|---|---|---|---|
| 1 | 628 | 7,831 | — | 7,831 | ha |
| 2 | 332 | 5,596 | 4,346 | 4,971 | ha |
| 3 | 140 | 4,279 | 3,579 | 3,812 | ha |
| 4 | 44 | 3,705 | 2,689 | 2,943 | ha |
| 5 | 29 | 5,172 | 2,862 | 3,324 | yo'q |
| 6 | 7 | 2,857 | 2,771 | 2,786 | yo'q |
| 7 | 2 | 1,000 | 4,667 | 4,143 | yo'q |

**A3 — morfema standart (E7)**

| x | n | R(x) | S(x) | y(x) | fitga |
|---|---|---|---|---|---|
| 1 | 34502 | 4,547 | — | 4,547 | ha |
| 2 | 21905 | 4,235 | 2,364 | 3,299 | ha |
| 3 | 8211 | 4,306 | 2,230 | 2,922 | ha |
| 4 | 1649 | 4,228 | 2,223 | 2,725 | ha |
| 5 | 162 | 3,796 | 2,150 | 2,479 | ha |
| 6 | 7 | 3,143 | 2,000 | 2,190 | yo'q |
| 7 | 1 | 3,000 | 2,500 | 2,571 | yo'q |

**Q3 y(5), y(6)**

| x | n | ȳ (4 o'nlik) | SD | fitga |
|---|---|---|---|---|
| 5 | 3584 | 2,2622 | 0,2486 | ha |
| 6 | 950 | 2,2598 | 0,2252 | ha |

y(6) − y(5) = −0,002396

### E11h — K2 uzun gaplar va chegara to'liqligi yuqori chegarasi

K2 da 60 so'zdan uzun gaplar: 4 / 4297 (x — V0 birliklari).

| # | so'z | token | x |
|---|---|---|---|
| 1 | 86 | 86 | 12 |
| 2 | 69 | 69 | 18 |
| 3 | 67 | 67 | 16 |
| 4 | 63 | 63 | 10 |

Oltin chegaralar (treebank, UD non-PUNCT tokenlar ketma-ketligi, qo'shni tokenlar birligi har xil); oldidagi token UPOS (oltin).

| ta'rif | chegara | oldida VERB | ulush | oldida VERB/AUX | ulush | birliksiz token |
|---|---|---|---|---|---|---|
| keng | 2026 | 1138 | 56,2 % | 1174 | 57,9 % | 0 |
| tor | 1269 | 739 | 58,2 % | 770 | 60,7 % | 0 |

## Rasmlar

- `rasm_e1.png` — E1: kuzatilgan ȳ, aralashma bashorati, o'zak va qo'shimcha uzunligi (uchala qoida).
- `rasm_e2.png` — E2: Q3 ȳ guruh va korpus bo'yicha (n ≥ 30 kataklar).
- `rasm_e5.png` — E5: Q1 treebank ȳ, aralashma, bosh klauza M(k) va ergash klauza S(k) (tor, keng).
- `rasm_e7.png` — E7: klauza (tor) va morfema (max(score)): ȳ, sof aralashma, M(k)/R(x), S(k)/S(x).
