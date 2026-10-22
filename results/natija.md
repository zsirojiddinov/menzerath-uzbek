# MENZERATH-1 — NATIJA (bir martalik yurish)

Skript `tahlil.py` sha256 `618d333f287cd3b5e9a4b87fc5f842b853f46cd0e4676b64302d29a2a53f4b4f` · prereg `6b5e3cc36657…` · tuzatish_1 `066652538d5e…` · commit `4ca1569` · DB md5 `732a97a56205a00c1c28a100275782ce` (oxiri `732a97a56205a00c1c28a100275782ce`)
seed 20261021 · bootstrap 1000 · B&Č 100 · fit kataklari n ≥ 30 · numpy 2.0.2 · scipy 1.13.1 · matplotlib 3.9.4

## 0. Materiallar va namunalar

- Treebank: 1182 gap; held-out (`filtr_matn`) chiqarildi 0; ijobiy nazorat (qayta qurilgan tor proyeksiya = `gold_unit`) 1182/1182.
- K1: 889 gap, held-out chiqarildi 0; K2: 4297 gap, held-out chiqarildi 0.

| korpus | kirish token | tinish | raqam | alifbodan tashqari | yaroqli | Q2: noma'lum | Q2: yuza teng emas | Q2: bo'sh morfema | **Q2 namuna** | Q3: faqat tutuq | Q3: 1 grafema | Q3: unlisiz | **Q3 namuna** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | 16890 | 67 | 296 | 9 | 16324 | 2316 (14,19 %) | 383 (2,35 %) | 0 | **13625 (83,47 %)** | 194 (1,17 %) | 137 (0,83 %) | 83 (0,50 %) | **16104 (97,49 %)** |
| K2 | 53596 | 4 | 150 | 2 | 53439 | 8591 (16,08 %) | 1657 (3,10 %) | 0 | **43191 (80,82 %)** | 1 (0,00 %) | 1376 (2,57 %) | 17 (0,03 %) | **52046 (97,39 %)** |
| treebank | 11072 | 0 | 102 | 8 | 10962 | 995 (9,08 %) | 346 (3,16 %) | 0 | **9621 (87,77 %)** | 0 (0,00 %) | 74 (0,68 %) | 8 (0,07 %) | **10880 (99,25 %)** |
| jami | 81558 | 71 | 548 | 19 | 80725 | 11902 (14,74 %) | 2386 (2,96 %) | 0 | **66437 (82,30 %)** | 195 (0,24 %) | 1587 (1,96 %) | 108 (0,13 %) | **79030 (97,66 %)** |

Q2 ulushlari yaroqli tokenlarga nisbatan; Q3 ulushlari Q3 kirishiga (yaroqli + faqat tutuq, tuzatish_1) nisbatan. Faqat tutuq belgisidan iborat token tozalashdan OLDIN ajratiladi (tinish deb sanalmaydi).

## 1. Fitlar va hukmlar (asosiy qatorlar)

b — **sodda** model y = a·x^b dan (§4.4 asosiy b); [95 %] — bootstrap percentile oralig'i. To'liq MA y = a·x^b·e^(−cx) ikkinchi darajali. K — fitga kirgan kataklar. Hukm: b < 0 · oraliq 0 siz · n ≥ 30 kataklarda qat'iy monoton kamayish.

| qator | N | K | a (sodda) [95 %] | **b (sodda)** [95 %] | R² (sodda) | a (to'liq) | b (to'liq) | c (to'liq) | ΔAIC (to'liq − sodda) | afzal | monoton | hukm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 treebank tor | 1182 | 4 | 7,835 [7,572; 8,145] | −0,662 [−0,718; −0,607] | 0,999 | 8,190 [7,164; 9,486] | −0,587 [−0,845; −0,314] | 0,045 [−0,093; 0,198] | −0,92 | sodda | ha | **bajarildi** |
| Q1 treebank keng | 1182 | 4 | 7,131 [6,816; 7,478] | −0,628 [−0,690; −0,569] | 0,999 | 6,886 [6,224; 7,717] | −0,690 [−0,933; −0,438] | −0,036 [−0,149; 0,090] | 0,07 | sodda | ha | **bajarildi** |
| Q1 K1 VDU | 889 | 6 | 10,882 [10,157; 11,622] | −0,514 [−0,576; −0,452] | 0,974 | 9,900 [9,279; 10,509] | −0,767 [−0,960; −0,561] | −0,115 [−0,184; −0,042] | −5,37 | toliq | ha | **bajarildi** |
| Q1 K2 VDU | 4297 | 8 | 6,484 [6,306; 6,678] | −0,339 [−0,368; −0,312] | 0,882 | 5,761 [5,619; 5,910] | −0,689 [−0,758; −0,612] | −0,154 [−0,178; −0,130] | −17,09 | toliq | yo'q | **bajarilmadi** |
| Q2 jami (max score) | 66437 | 5 | 4,533 [4,511; 4,554] | −0,427 [−0,434; −0,421] | 0,992 | 3,989 [3,945; 4,036] | −0,648 [−0,674; −0,623] | −0,131 [−0,143; −0,118] | −12,48 | toliq | ha | **bajarildi** |
| Q3 jami | 79030 | 8 | 2,684 [2,675; 2,693] | −0,122 [−0,125; −0,119] | 0,927 | 2,604 [2,597; 2,612] | −0,227 [−0,236; −0,217] | −0,046 [−0,050; −0,043] | −13,42 | toliq | yo'q | **bajarilmadi** |
| Q4b A: treebank V0 | 1182 | 4 | 6,867 [6,589; 7,178] | −0,539 [−0,595; −0,483] | 0,990 | 5,826 [5,247; 6,552] | −0,831 [−1,058; −0,598] | −0,170 [−0,286; −0,049] | −9,42 | toliq | ha | **bajarildi** |
| Q4c eng kam morfema | 66437 | 5 | 4,552 [4,531; 4,574] | −0,395 [−0,402; −0,388] | 0,992 | 4,054 [4,002; 4,103] | −0,586 [−0,613; −0,561] | −0,118 [−0,133; −0,105] | −5,55 | toliq | ha | **bajarildi** |
| Q4c eng ko'p morfema | 66437 | 5 | 4,522 [4,501; 4,543] | −0,450 [−0,457; −0,444] | 0,989 | 3,903 [3,862; 3,945] | −0,710 [−0,736; −0,688] | −0,151 [−0,163; −0,139] | −9,35 | toliq | ha | **bajarildi** |

**Q1 asosiy qatori — treebank, tor.** Hukm: **bajarildi**. Q2: **bajarildi**. Q3: **bajarilmadi**.

Bootstrap yaqinlashmaganlar (sodda / to'liq):

- Q1 treebank tor: sodda 0/1000, to'liq 0/1000; bo'sh (0 so'zli) birlik 0, x ga kirmagan gap 0
- Q1 treebank keng: sodda 0/1000, to'liq 0/1000; bo'sh (0 so'zli) birlik 0, x ga kirmagan gap 0
- Q4b A: treebank V0: sodda 0/1000, to'liq 0/1000; bo'sh (0 so'zli) birlik 0, x ga kirmagan gap 0
- Q1 K1 VDU: sodda 0/1000, to'liq 0/1000; bo'sh (0 so'zli) birlik 12, x ga kirmagan gap 0
- Q1 K2 VDU: sodda 0/1000, to'liq 0/1000; bo'sh (0 so'zli) birlik 0, x ga kirmagan gap 0
- Q2 jami (max score): sodda 0/1000, to'liq 0/1000
- Q4c eng kam morfema: sodda 0/1000, to'liq 0/1000
- Q4c eng ko'p morfema: sodda 0/1000, to'liq 0/1000
- Q3 jami: sodda 0/1000, to'liq 0/1000

## 2. Jadvallar (har daraja: x, n, o'rtacha y, SD)

**Q1 treebank tor** (N = 1182; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 628 | 7,831 | 3,543 | ha |
| 2 | 332 | 4,971 | 1,960 | ha |
| 3 | 140 | 3,812 | 1,360 | ha |
| 4 | 44 | 2,943 | 1,159 | ha |
| 5 | 29 | 3,324 | 1,163 | — |
| 6 | 7 | 2,786 | 0,507 | — |
| 7 | 2 | 4,143 | 2,424 | — |

**Q1 treebank keng** (N = 1182; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 433 | 7,136 | 3,494 | ha |
| 2 | 399 | 4,604 | 1,674 | ha |
| 3 | 203 | 3,535 | 1,310 | ha |
| 4 | 81 | 3,127 | 0,924 | ha |
| 5 | 28 | 2,621 | 0,663 | — |
| 6 | 23 | 2,674 | 0,643 | — |
| 7 | 9 | 2,905 | 1,268 | — |
| 8 | 5 | 3,225 | 0,920 | — |
| 11 | 1 | 1,545 | — | — |

**Q1 K1 VDU** (N = 889; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 143 | 11,154 | 4,982 | ha |
| 2 | 202 | 7,181 | 3,079 | ha |
| 3 | 226 | 6,003 | 2,114 | ha |
| 4 | 164 | 5,733 | 1,656 | ha |
| 5 | 78 | 4,954 | 1,180 | ha |
| 6 | 48 | 4,705 | 1,328 | ha |
| 7 | 19 | 4,541 | 0,726 | — |
| 8 | 4 | 5,125 | 0,771 | — |
| 9 | 3 | 4,444 | 0,556 | — |
| 10 | 1 | 3,200 | — | — |
| 13 | 1 | 6,692 | — | — |

**Q1 K2 VDU** (N = 4297; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 903 | 6,766 | 3,011 | ha |
| 2 | 1361 | 4,752 | 2,023 | ha |
| 3 | 1017 | 4,385 | 1,537 | ha |
| 4 | 511 | 4,218 | 1,271 | ha |
| 5 | 271 | 4,179 | 1,217 | ha |
| 6 | 132 | 4,154 | 1,065 | ha |
| 7 | 49 | 4,289 | 1,094 | ha |
| 8 | 31 | 4,294 | 1,044 | ha |
| 9 | 6 | 4,370 | 0,960 | — |
| 10 | 8 | 4,638 | 0,980 | — |
| 11 | 4 | 4,045 | 0,563 | — |
| 12 | 2 | 5,542 | 2,298 | — |
| 16 | 1 | 4,188 | — | — |
| 18 | 1 | 3,833 | — | — |

**Q4b A: treebank V0** (N = 1182; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 432 | 6,903 | 3,233 | ha |
| 2 | 448 | 4,616 | 1,633 | ha |
| 3 | 226 | 3,845 | 1,158 | ha |
| 4 | 54 | 3,722 | 1,148 | ha |
| 5 | 16 | 3,900 | 1,341 | — |
| 6 | 4 | 3,667 | 0,871 | — |
| 8 | 1 | 4,250 | — | — |
| 10 | 1 | 3,200 | — | — |

**Q2 jami (max score)** (N = 66437; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 34502 | 4,547 | 1,932 | ha |
| 2 | 21905 | 3,299 | 0,978 | ha |
| 3 | 8211 | 2,922 | 0,685 | ha |
| 4 | 1649 | 2,725 | 0,528 | ha |
| 5 | 162 | 2,479 | 0,475 | ha |
| 6 | 7 | 2,190 | 0,178 | — |
| 7 | 1 | 2,571 | — | — |

**Q4c eng kam morfema** (N = 66437; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 34734 | 4,564 | 1,943 | ha |
| 2 | 24833 | 3,408 | 1,019 | ha |
| 3 | 5910 | 3,093 | 0,722 | ha |
| 4 | 836 | 2,788 | 0,566 | ha |
| 5 | 119 | 2,476 | 0,486 | ha |
| 6 | 5 | 2,300 | 0,431 | — |

**Q4c eng ko'p morfema** (N = 66437; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 34448 | 4,540 | 1,925 | ha |
| 2 | 19805 | 3,208 | 0,939 | ha |
| 3 | 9552 | 2,856 | 0,660 | ha |
| 4 | 2349 | 2,629 | 0,534 | ha |
| 5 | 267 | 2,405 | 0,453 | ha |
| 6 | 15 | 2,289 | 0,336 | — |
| 7 | 1 | 2,571 | — | — |

**Q3 jami** (N = 79030; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 12044 | 2,736 | 0,629 | ha |
| 2 | 30498 | 2,426 | 0,428 | ha |
| 3 | 20876 | 2,351 | 0,335 | ha |
| 4 | 10761 | 2,288 | 0,284 | ha |
| 5 | 3584 | 2,262 | 0,249 | ha |
| 6 | 950 | 2,260 | 0,225 | ha |
| 7 | 225 | 2,280 | 0,223 | ha |
| 8 | 47 | 2,311 | 0,212 | ha |
| 9 | 28 | 2,425 | 0,216 | — |
| 10 | 5 | 2,400 | 0,212 | — |
| 11 | 7 | 2,455 | 0,157 | — |
| 12 | 1 | 2,500 | — | — |
| 13 | 1 | 2,462 | — | — |
| 14 | 1 | 2,857 | — | — |
| 15 | 1 | 2,400 | — | — |
| 16 | 1 | 2,188 | — | — |

## 3. Q4 — birlik ta'rifiga bog'liqlik

| taqqoslash | Δb (sodda) | 95 % | Δa (sodda) | 95 % | juft takror |
|---|---|---|---|---|---|
| (a) keng − tor | 0,034 | [−0,006; 0,078] | −0,704 | [−0,892; −0,531] | 1000 |
| (b) A (V0) − B (oltin tor) | 0,122 | [0,064; 0,184] | −0,968 | [−1,230; −0,734] | 1000 |
| (c) Q4c eng kam morfema − max score | 0,033 | [0,031; 0,034] | 0,020 | [0,017; 0,022] | 1000 |
| (c) Q4c eng ko'p morfema − max score | −0,023 | [−0,024; −0,021] | −0,011 | [−0,013; −0,009] | 1000 |

- Q4(b) bashorati (Δb < 0, oraliq 0 siz): **tasdiqlanmadi**.
- Q4(c) bashorati (uchala qoidada b ishorasi bir xil): **tasdiqlandi**. Tahlili o'zgargan tokenlar: eng kam 4117, eng ko'p 2910 (Q2 namunasidan).

## 4. Q5 — B&Č tasodifiy model (treebank, tor)

- haqiqiy b (sodda) = −0,662
- tasodifiy b: mediana −0,004, 2,5–97,5 % [−0,063; 0,053], min–max [−0,123; 0,074] (100/100 fit)
- tasodifiy b ≤ haqiqiy b ulushi: 0,0 %; tasodifiy b < 0 ulushi: 55,0 %
- §4.4 mezoni bajarilgan tasodifiy takrorlar: 0/100

## 5. Sezgirlik (hukmni o'zgartirmaydi)

| qator | N | K | a (sodda) [95 %] | **b (sodda)** [95 %] | R² (sodda) | a (to'liq) | b (to'liq) | c (to'liq) | ΔAIC (to'liq − sodda) | afzal | monoton | hukm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 treebank tor · oxirgi katak (x = 4) chiqarilgan | 1138 | 3 | 7,831 [7,562; 8,096] | −0,655 [−0,716; −0,597] | 1,000 | — | — | — | — | sodda | ha | **bajarildi** |
| Q1 treebank keng · oxirgi katak (x = 4) chiqarilgan | 1101 | 3 | 7,138 [6,785; 7,446] | −0,636 [−0,700; −0,566] | 1,000 | — | — | — | — | sodda | ha | **bajarildi** |
| Q1 K1 VDU · oxirgi katak (x = 6) chiqarilgan | 841 | 5 | 10,911 [10,224; 11,688] | −0,522 [−0,590; −0,459] | 0,974 | 9,629 [8,912; 10,354] | −0,823 [−1,054; −0,602] | −0,145 [−0,237; −0,057] | −5,30 | toliq | ha | **bajarildi** |
| Q1 K2 VDU · oxirgi katak (x = 8) chiqarilgan | 4266 | 7 | 6,500 [6,326; 6,681] | −0,345 [−0,370; −0,319] | 0,891 | 5,708 [5,547; 5,860] | −0,709 [−0,790; −0,636] | −0,165 [−0,192; −0,138] | −15,58 | toliq | yo'q | **bajarilmadi** |
| Q2 jami (max score) · oxirgi katak (x = 5) chiqarilgan | 66275 | 4 | 4,533 [4,512; 4,551] | −0,428 [−0,435; −0,422] | 0,992 | 3,952 [3,903; 4,000] | −0,663 [−0,689; −0,635] | −0,140 [−0,153; −0,126] | −13,65 | toliq | ha | **bajarildi** |
| Q3 jami · oxirgi katak (x = 8) chiqarilgan | 78983 | 7 | 2,684 [2,676; 2,693] | −0,122 [−0,125; −0,119] | 0,929 | 2,604 [2,596; 2,611] | −0,227 [−0,237; −0,218] | −0,046 [−0,050; −0,043] | −11,38 | toliq | yo'q | **bajarilmadi** |
| Q1 UT tor | 500 | 3 | 9,470 [9,132; 9,826] | −0,838 [−0,908; −0,755] | 0,999 | — | — | — | — | sodda | ha | **bajarildi** |
| Q1 UzUDT tor | 682 | 4 | 6,264 [5,927; 6,578] | −0,450 [−0,523; −0,378] | 0,981 | 7,767 [6,341; 9,408] | −0,063 [−0,464; 0,334] | 0,221 [0,018; 0,433] | −34,01 | toliq | ha | **bajarildi** |
| Q2 (i) noma'lum so'zlar x = 1 | 78339 | 5 | 5,017 [4,995; 5,039] | −0,549 [−0,556; −0,543] | 0,986 | 3,959 [3,917; 4,006] | −0,948 [−0,971; −0,924] | −0,240 [−0,252; −0,227] | −11,88 | toliq | ha | **bajarildi** |
| Q2 (ii) K1 | 13625 | 5 | 5,078 [5,028; 5,127] | −0,430 [−0,443; −0,415] | 0,995 | 4,593 [4,471; 4,718] | −0,606 [−0,664; −0,545] | −0,103 [−0,132; −0,072] | −9,18 | toliq | ha | **bajarildi** |
| Q2 (ii) K2 | 43191 | 5 | 4,324 [4,300; 4,348] | −0,422 [−0,429; −0,414] | 0,993 | 3,842 [3,788; 3,894] | −0,624 [−0,652; −0,594] | −0,121 [−0,135; −0,105] | −13,75 | toliq | ha | **bajarildi** |
| Q2 (ii) treebank | 9621 | 4 | 4,705 [4,651; 4,758] | −0,450 [−0,466; −0,434] | 0,993 | 4,108 [3,971; 4,247] | −0,683 [−0,750; −0,617] | −0,139 [−0,173; −0,104] | −17,56 | toliq | ha | **bajarildi** |
| Q3 ng har doim 1 | 79030 | 8 | 2,681 [2,673; 2,690] | −0,122 [−0,125; −0,119] | 0,921 | 2,598 [2,591; 2,606] | −0,232 [−0,241; −0,222] | −0,048 [−0,052; −0,045] | −13,14 | toliq | yo'q | **bajarilmadi** |

**Q1 treebank tor · oxirgi katak (x = 4) chiqarilgan** (N = 1138; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 628 | 7,831 | 3,543 | ha |
| 2 | 332 | 4,971 | 1,960 | ha |
| 3 | 140 | 3,812 | 1,360 | ha |
| 5 | 29 | 3,324 | 1,163 | — |
| 6 | 7 | 2,786 | 0,507 | — |
| 7 | 2 | 4,143 | 2,424 | — |

**Q1 treebank keng · oxirgi katak (x = 4) chiqarilgan** (N = 1101; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 433 | 7,136 | 3,494 | ha |
| 2 | 399 | 4,604 | 1,674 | ha |
| 3 | 203 | 3,535 | 1,310 | ha |
| 5 | 28 | 2,621 | 0,663 | — |
| 6 | 23 | 2,674 | 0,643 | — |
| 7 | 9 | 2,905 | 1,268 | — |
| 8 | 5 | 3,225 | 0,920 | — |
| 11 | 1 | 1,545 | — | — |

**Q1 K1 VDU · oxirgi katak (x = 6) chiqarilgan** (N = 841; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 143 | 11,154 | 4,982 | ha |
| 2 | 202 | 7,181 | 3,079 | ha |
| 3 | 226 | 6,003 | 2,114 | ha |
| 4 | 164 | 5,733 | 1,656 | ha |
| 5 | 78 | 4,954 | 1,180 | ha |
| 7 | 19 | 4,541 | 0,726 | — |
| 8 | 4 | 5,125 | 0,771 | — |
| 9 | 3 | 4,444 | 0,556 | — |
| 10 | 1 | 3,200 | — | — |
| 13 | 1 | 6,692 | — | — |

**Q1 K2 VDU · oxirgi katak (x = 8) chiqarilgan** (N = 4266; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 903 | 6,766 | 3,011 | ha |
| 2 | 1361 | 4,752 | 2,023 | ha |
| 3 | 1017 | 4,385 | 1,537 | ha |
| 4 | 511 | 4,218 | 1,271 | ha |
| 5 | 271 | 4,179 | 1,217 | ha |
| 6 | 132 | 4,154 | 1,065 | ha |
| 7 | 49 | 4,289 | 1,094 | ha |
| 9 | 6 | 4,370 | 0,960 | — |
| 10 | 8 | 4,638 | 0,980 | — |
| 11 | 4 | 4,045 | 0,563 | — |
| 12 | 2 | 5,542 | 2,298 | — |
| 16 | 1 | 4,188 | — | — |
| 18 | 1 | 3,833 | — | — |

**Q2 jami (max score) · oxirgi katak (x = 5) chiqarilgan** (N = 66275; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 34502 | 4,547 | 1,932 | ha |
| 2 | 21905 | 3,299 | 0,978 | ha |
| 3 | 8211 | 2,922 | 0,685 | ha |
| 4 | 1649 | 2,725 | 0,528 | ha |
| 6 | 7 | 2,190 | 0,178 | — |
| 7 | 1 | 2,571 | — | — |

**Q3 jami · oxirgi katak (x = 8) chiqarilgan** (N = 78983; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 12044 | 2,736 | 0,629 | ha |
| 2 | 30498 | 2,426 | 0,428 | ha |
| 3 | 20876 | 2,351 | 0,335 | ha |
| 4 | 10761 | 2,288 | 0,284 | ha |
| 5 | 3584 | 2,262 | 0,249 | ha |
| 6 | 950 | 2,260 | 0,225 | ha |
| 7 | 225 | 2,280 | 0,223 | ha |
| 9 | 28 | 2,425 | 0,216 | — |
| 10 | 5 | 2,400 | 0,212 | — |
| 11 | 7 | 2,455 | 0,157 | — |
| 12 | 1 | 2,500 | — | — |
| 13 | 1 | 2,462 | — | — |
| 14 | 1 | 2,857 | — | — |
| 15 | 1 | 2,400 | — | — |
| 16 | 1 | 2,188 | — | — |

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

**Q2 (i) noma'lum so'zlar x = 1** (N = 78339; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 46404 | 5,034 | 2,572 | ha |
| 2 | 21905 | 3,299 | 0,978 | ha |
| 3 | 8211 | 2,922 | 0,685 | ha |
| 4 | 1649 | 2,725 | 0,528 | ha |
| 5 | 162 | 2,479 | 0,475 | ha |
| 6 | 7 | 2,190 | 0,178 | — |
| 7 | 1 | 2,571 | — | — |

**Q2 (ii) K1** (N = 13625; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 7199 | 5,092 | 2,223 | ha |
| 2 | 4144 | 3,695 | 1,157 | ha |
| 3 | 1815 | 3,251 | 0,765 | ha |
| 4 | 423 | 2,952 | 0,573 | ha |
| 5 | 43 | 2,721 | 0,545 | ha |
| 6 | 1 | 2,167 | — | — |

**Q2 (ii) K2** (N = 43191; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 22501 | 4,336 | 1,799 | ha |
| 2 | 14526 | 3,170 | 0,883 | ha |
| 3 | 5082 | 2,797 | 0,608 | ha |
| 4 | 978 | 2,619 | 0,456 | ha |
| 5 | 97 | 2,375 | 0,412 | ha |
| 6 | 6 | 2,194 | 0,195 | — |
| 7 | 1 | 2,571 | — | — |

**Q2 (ii) treebank** (N = 9621; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 4802 | 4,719 | 1,889 | ha |
| 2 | 3235 | 3,375 | 0,991 | ha |
| 3 | 1314 | 2,952 | 0,697 | ha |
| 4 | 248 | 2,754 | 0,588 | ha |
| 5 | 22 | 2,464 | 0,438 | — |

**Q3 ng har doim 1** (N = 79030; fitga: n ≥ 30)

| x | n | o'rtacha y | SD | fitga |
|---|---|---|---|---|
| 1 | 12044 | 2,736 | 0,629 | ha |
| 2 | 30498 | 2,421 | 0,433 | ha |
| 3 | 20876 | 2,348 | 0,334 | ha |
| 4 | 10761 | 2,287 | 0,283 | ha |
| 5 | 3584 | 2,261 | 0,248 | ha |
| 6 | 950 | 2,259 | 0,226 | ha |
| 7 | 225 | 2,279 | 0,223 | ha |
| 8 | 47 | 2,311 | 0,212 | ha |
| 9 | 28 | 2,425 | 0,216 | — |
| 10 | 5 | 2,400 | 0,212 | — |
| 11 | 7 | 2,455 | 0,157 | — |
| 12 | 1 | 2,500 | — | — |
| 13 | 1 | 2,462 | — | — |
| 14 | 1 | 2,857 | — | — |
| 15 | 1 | 2,400 | — | — |
| 16 | 1 | 2,188 | — | — |

## 6. Amalga oshirish qaydlari

- Q1 so'zlari — tizim so'zlari (`ud_system_output.json` → `words`; bo'shliq-bo'lak, chetdagi tinish olingan); PUNCT siz = kamida bitta harf-raqam belgisi. Keng proyeksiya tor bilan bir xil tartibda (`naqsh_kesh.daraxt_bolinishi` + `iq.proyeksiya`) qurildi; tor qayta qurilishi `gold_unit` ga aynan teng (ijobiy nazorat).
- Q2/Q3 tokenlari: apostrof → `'`, kichik harf, chetdagi tinish olinadi (boshdagi `'` olinadi; oxirgi `'` faqat o/g dan keyin qoladi); defis grafema emas. Analizator kirishi — shu token (defis bilan); yuza tengligi defissiz solishtiriladi.
- Q4(c): nomzodlar depth-0 `max(score)` chaqiruvida; qoida tartibi (morfema soni, keyin score) bo'yicha birinchi yuzaga teng nomzod; bo'lmasa `max(score)` tahlili. `_shaxs2_s6_s7` uchala qoidada bir xil chaqiriladi.
- Juft bootstrap: bir xil N li qatorlar bir xil seed bilan bir xil indekslarni oladi.
- Rasmlar: `rasm_q1.png`, `rasm_q2.png`, `rasm_q3.png`, `rasm_q4b.png`, `rasm_q4c.png`, `rasm_q5.png`. Oraliq ±1,96·SD/√n; to'ldirilmagan nuqta — n < 30 (fitga kirmagan).
