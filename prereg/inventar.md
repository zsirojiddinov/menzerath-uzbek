# MENZERATH-1 — INVENTAR

> **Faqat sanash.** Menzerath–Altmann qonuni (qism uzunligi ~ butun uzunligi) bu yerda **hisoblanmaydi** — faqat hajmlar,
> taqsimotlar va qamrov. Prereg shundan keyin yoziladi. Matn chop etilmagan/yozilmagan (faqat sonlar).
>
> Manba: `inventar.py` → `inventar.json` (bu jadvallar o'sha JSON dan). Langar: main `285e5ec`, DB md5
> `732a97a56205a00c1c28a100275782ce` (analizator DB ning scratchpad **nusxasida** yurdi; ishchi DB md5 oldin/keyin teng).
> services, data, DB, pm2 tegilmagan.

## 1. Treebanklar (UD_Uzbek-UT, UzUDT — release 2.18)

Nusxa — Heaps/IJCL paketidagi `analysis/ijcl-paket/supplement/data/ud/` (UT r2.18 test; UzUDT r2.18 train + test);
`analysis/ud-baholash/ud/` dagi nusxa bilan sha256 **teng** (uchala fayl). UT ning r2.15 test fayli (5 850 token) ham
paketda bor — bu yerda ishlatilmadi.

| fayl | sha256 | ud-baholash nusxasi | gap | token | PUNCT siz | MWT | lemma % | FEATS bo'sh emas % | Case % | Case % (NOUN/PROPN/PRON) | MISC kalitlari |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `UD_Uzbek-UT/uz_ut-ud-test.conllu` | `6297430a3ac34275eefeab74d3b074618894704082e73e9d048ade561271a03a` | teng | 500 | 5 930 | 5 070 | 0 | 100,0 | 78,52 | 51,95 | 96,0 | SpaceAfter 831 |
| `UD_Uzbek-UzUDT/uz_uzudt-ud-train.conllu` | `c1fb9548cbba34e3dddd5ca2af7d5eb3e37f1e8a6e640e29061ff5b9e581aa12` | teng | 483 | 5 442 | 4 308 | 0 | 100,0 | 57,99 | 39,55 | 72,28 | SpaceAfter 19, Translit 12, Morf 1, Clitic 1 |
| `UD_Uzbek-UzUDT/uz_uzudt-ud-test.conllu` | `6a191e59b6cbaade250463109581e95350702eb85fff765f407eca00ed1937dc` | teng | 201 | 2 140 | 1 703 | 0 | 100,0 | 61,42 | 42,22 | 79,21 | SpaceAfter 4 |

- **Lemma** — har so'zda bor (100 %). **FEATS** — UT da 78,5 %, UzUDT da 58–61 % so'zda bo'sh emas. **Case** — UT da
  NOUN/PROPN/PRON ning 96 % ida, UzUDT da 72–79 %.
- **Morfema chegarasi — YO'Q.** FEATS faqat xususiyat to'plami beradi; MISC da segmentatsiya kaliti yo'q (UzUDT train da
  `Morf` 1 ta, `Clitic` 1 ta — tizimli emas). Multiword-token (`n-m`) qatorlari 0.
- Takror gaplar (harf+raqam kaliti, `ud_tools.squash`): `UzUDT:s130`, `UzUDT:s132` — maqoladagi 1 182 shulardan keyin.

| treebank | ta'rif | gap | klauza | o'rtacha | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8+ |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| UT | tor | 500 | 742 | 1,484 | 310 | 145 | 39 | 5 | 1 | 0 | 0 | 0 |
| UT | tor_takrorsiz | 500 | 742 | 1,484 | 310 | 145 | 39 | 5 | 1 | 0 | 0 | 0 |
| UT | keng | 500 | 933 | 1,866 | 196 | 201 | 82 | 16 | 5 | 0 | 0 | 0 |
| UT | keng_takrorsiz | 500 | 933 | 1,866 | 196 | 201 | 82 | 16 | 5 | 0 | 0 | 0 |
| UzUDT | tor | 684 | 1 352 | 1,977 | 318 | 188 | 102 | 39 | 28 | 7 | 2 | 0 |
| UzUDT | tor_takrorsiz | 682 | 1 347 | 1,975 | 318 | 187 | 101 | 39 | 28 | 7 | 2 | 0 |
| UzUDT | keng | 684 | 1 628 | 2,38 | 237 | 199 | 122 | 65 | 23 | 23 | 9 | 6 |
| UzUDT | keng_takrorsiz | 682 | 1 623 | 2,38 | 237 | 198 | 121 | 65 | 23 | 23 | 9 | 6 |
| jami | tor | 1 184 | 2 094 | 1,769 | 628 | 333 | 141 | 44 | 29 | 7 | 2 | 0 |
| jami | tor_takrorsiz | 1 182 | 2 089 | 1,767 | 628 | 332 | 140 | 44 | 29 | 7 | 2 | 0 |
| jami | keng | 1 184 | 2 561 | 2,163 | 433 | 400 | 204 | 81 | 28 | 23 | 9 | 6 |
| jami | keng_takrorsiz | 1 182 | 2 556 | 2,162 | 433 | 399 | 203 | 81 | 28 | 23 | 9 | 6 |

Ta'riflar — Heaps kodidagi `ud_tools.klauza_boshlari`: klauza boshi = deprel `root, ccomp, xcomp, advcl, acl, csubj,
parataxis` yoki ikki predikat orasidagi `conj` (predikat = VERB/AUX yoki `cop` bolali). **keng** = `asosiy` (hammasi);
**tor** = `xcomp_aclsiz` (`xcomp` va `acl` klauza emas). Nazorat: tor 2 089 / 1 182 = 1,77 va keng 2,16 — maqoladagi
(4.2, 4.7) qiymatlar bilan aynan.

## 2. K1, K2 (Heaps korpuslari)

K1 = `sentence_matematik_model_kkt_simple.json` (uz-en, yangilik/ilmiy-texnik; sha256 `8b679a8ff8819b90…`),
K2 = `math_models_tagor_kkt_simple.json` (Tagor; sha256 `34930538754cb1bd…`). Kodlar va VDU —
paketdagi `coded_corpus_K*.json`; `common.load_coded` V0 kesimini qayta bajarib saqlangan klauzalar bilan **aynan**
ekanini tekshirdi; matn surati gap soni va har gapdagi so'z = kod soni bo'yicha mos. VDU = fe'l bilan chegaralangan
birlik (V0: har maksimal G zanjiridan keyin kesish).

| korpus | gap | token | VDU | VDU/gap | VDU uzunligi (token) | gap uzunligi (token) | oxirgi kodi G bo'lgan gap | shovqin % (n) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| K1 | 889 | 16 890 | 2 786 | 3,134 | 6,06 | 19,0 | 593 | 4,39 (5/114) |
| K2 | 4 297 | 53 596 | 11 694 | 2,721 | 4,58 | 12,47 | 2 887 | 8,03 (31/386) |

| korpus | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11+ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| K1 | 141 | 202 | 227 | 162 | 80 | 47 | 21 | 4 | 2 | 2 | 1 |
| K2 | 903 | 1 361 | 1 017 | 511 | 271 | 132 | 49 | 31 | 6 | 8 | 8 |

- Shovqin (ma'lum, `results/noise_sample.json`): jami **7,2 %** (36/500 token; Wilson 95 %
  5,25–9,81).
- «oxirgi kodi G» — gap fe'l bilan tugaydi; qolganlarida oxirgi VDU fe'lsiz qoldiq.

**Held-out tekshiruvi** (`held_out.filtr_matn` — gap xeshi + 8-oyna, «qattiq» ∪ «kirish»):

| to'plam | tekshirildi | moslik |
|---|---:|---:|
| K1 | 889 | **0** |
| K2 | 4 297 | **0** |
| treebank (UT + UzUDT, `# text`) | 1 184 | **0** |

ID kaliti (`filtr`) qo'llanmaydi: K1/K2 va treebank gaplari 2 119 ID tizimida emas. Eslatma: paketdagi
`heldout_sentences.json` (K1 53, K2 409) — mualliflarning **eski** held-out to'plamlari bilan kesishma
(maqoladagi «-H» qatorlari); §17 ro'yxati (TOLQIN-2) bilan kesishma 0.

## 3. Morfologik analizator (faqat o'qish)

`MorphologyService._analyze_word_hisobla` (sukut env, DB nusxasi). Kirish — K1/K2 so'zlari (`load_corpus`) va treebank
so'zlari (PUNCT siz); `extract_kkt_pattern._strip_punctuation` + kichik harf (tinish-faqat va bo'linadigan token 0).

| manba | token | tur | tahlil % token | tahlil % tur | UNKNOWN % token | UNKNOWN % tur | UNKNOWN dan raqam (token) |
|---|---:|---:|---:|---:|---:|---:|---:|
| K1 | 16 890 | 7 355 | 82,91 | 75,02 | 17,09 | 24,98 | 225 |
| K2 | 53 596 | 15 760 | 83,65 | 73,79 | 16,35 | 26,21 | 114 |
| treebank | 11 081 | 5 847 | 89,82 | 85,21 | 10,18 | 14,79 | 98 |

| manba | birlik | 0 | 1 | 2 | 3 | 4 | 5 | 6 | o'rtacha |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| K1 | token | 7 199 | 4 352 | 1 949 | 454 | 47 | 2 | 0 | 0,7006 |
| K1 | tur | 1 513 | 2 156 | 1 437 | 365 | 45 | 2 | 0 | — |
| K2 | token | 22 490 | 15 571 | 5 623 | 1 036 | 104 | 6 | 1 | 0,6776 |
| K2 | tur | 2 601 | 4 985 | 3 200 | 759 | 77 | 6 | 1 | — |
| treebank | token | 4 803 | 3 437 | 1 426 | 261 | 25 | 1 | 0 | 0,7211 |
| treebank | tur | 1 537 | 2 002 | 1 172 | 245 | 25 | 1 | 0 | — |

(6 = 6 va undan ko'p.)

- **Chegaralar: HA, alohida.** Natija `elements` = ildiz + har qo'shimcha alohida (`value` — yuzaki satr, `code` —
  qo'shimcha turi ID si, masalan X2/U1/A1), `affixes[]` da har qo'shimcha obyekti. Chegara sanasi = qo'shimchalar soni.
- Ildiz + qo'shimchalar satri so'zga **teng emas** bo'lgan holat (morfofonemik ta'mir: q→g', k→g, unli tushishi,
  fe'l `-a` tushishi, `y` o'tkazgich — ildiz DB shaklida qaytadi):

| manba | ildiz+qo'shimchalar = so'z (token %) | (tur %) | >1 nomzod (token %) | (tur %) | nomzod soni turlar: 0 / 1 / 2 / 3 / 4 / 5+ |
|---|---:|---:|---:|---:|---|
| K1 | 97,25 | 95,92 | 36,03 | 40,4 | 21 / 3 268 / 1 820 / 370 / 33 / 6 |
| K2 | 96,3 | 94,81 | 30,13 | 32,6 | 198 / 7 640 / 3 172 / 568 / 45 / 6 |
| treebank | 93,07 | 93,32 | 35,03 | 36,95 | 41 / 3 100 / 1 460 / 312 / 56 / 13 |

- **Noaniqlik va tanlash qoidasi.** Analizator **bitta** tahlil qaytaradi. `_find_decomposition` barcha dekompozitsiyalarni
  yig'adi, `kkt_order_valid` / `kkt_root_affix_valid` / SHAXS-2 tartibi bilan filtrlaydi va `max(score)` bilan tanlaydi:
  `score = (ildizning haqiqiy tarjimasi bor, ildiz turi–qo'shimcha nomosligi jarimasi, ildiz uzunligi, to'g'ridan-to'g'ri
  DB moslik, prioritetlar kamayish tartibida)`; keyin `_shaxs2_s6_s7` tuzatishi. «>1 nomzod» — eng yuqori darajadagi
  filtrdan o'tgan turli (ildiz, ildiz turi, qo'shimcha zanjiri) soni > 1. Sanash shu jarayonda `max` ni o'rash bilan
  qilindi (fayl o'zgarmagan). «0 nomzod» — tahlil zaxira yo'lidan (`_shaxs2_zaxira` / `_morf2_siz_zaxira`) kelgan.
- K1/K2 JSON larida ajratish paytidagi **eski** qo'shimcha yozuvlari ham bor (`morph_brief.affixes`, `word_details.affixes`)
  — joriy analizator emas; sanalmadi.

## 4. Harf va bo'g'in

- O'zbek lotin digraflari (sh, ch, ng, o', g') uchun harf sanash qoidasi — **yo'q**.
- Bo'g'inga ajratuvchi — **yo'q**.

## 5. Repodagi boshqa o'zbek matn korpuslari

Gap darajasidagi to'plamlar — `analysis/toplam_indeks.py` `matnlar()` (2 119 shular birlashmasidan) + `corpus/` harvest
fayllari. Token = bo'shliq bo'yicha. Held-out moslik — `filtr_matn` chiqargan gap soni. TOLQIN-2 to'plamlarining o'zi
(`a_qavat_400`, FLORES dev — `tolqin-2` branchida; `evaluation/eval72/`, `evaluation/corpus/_flores_cache/` — FLORES
dev/devtest manbasi; `analysis/yoqish-2/held_out.json`, `paket.csv`) — **ishlatilmaydi**, sanalmadi.

| to'plam | manba | gap | token (bo'shliq) | held-out moslik (`filtr_matn`) | belgi |
|---|---|---:|---:|---:|---|
| `oltin_200` | `oltin_korpus_200.json` | 200 | 727 | 12 | eval72 dan 12 gap — **TOLQIN-2 «kirish» (eval72): o'sha 12 ishlatilmaydi** |
| `tashqi50` | `analysis/tashqi50_gaplar.md` | 50 | 481 | 0 |  |
| `inkor_dev` | `analysis/inkor_korpus_v1.json` (INKOR-DEV) | 885 | 15 798 | 1 | 1 moslik — filtr chiqaradi |
| `savol_dev` | `analysis/savol_korpus_v1.json` (SAVOL-DEV) | 110 | 897 | 0 |  |
| `uzen900` | `evaluation/corpus/uz-en.uz` (K1 xom manbasi, 900 qator) | 900 | 20 048 | 0 |  |
| `scitech_dev` | `corpus/uz_en_scitech.dev.json` (inlibrary annotatsiyalari) | 49 | 886 | 0 |  |
| `test100` | `analysis/test100_gaplar.txt` — held-out (diagnoz), faqat xesh | 100 | 758 | 0 |  |
| `cc_probe` | `evaluation/corpus/converb_control_cc.json` | 32 | 118 | 0 |  |
| `train231` | `corpus/uz_en_scitech.train.json` | 231 | 3 946 | 24 | eval72 dan 24 gap — **TOLQIN-2 «kirish» (eval72): o'sha 24 ishlatilmaydi** |
| `tashqi40` | `analysis/tashqi40_gaplar.md` | 40 | 173 | 0 |  |
| `mas_v1` | `evaluation/corpus/mas_corpus_v1.json` | 73 | 257 | 0 |  |
| `mas_v2` | `evaluation/corpus/mas_corpus_v2.json` | 104 | 378 | 0 |  |
| `scitech_test` | `corpus/uz_en_scitech.test.json` — held-out | 49 | 832 | 0 |  |
| `inkor_test` | `analysis/inkor_korpus_v1.json` (INKOR-TEST) — held-out | 590 | 10 091 | 0 |  |
| `savol_test` | `analysis/savol_korpus_v1.json` (SAVOL-TEST) — held-out | 72 | 543 | 0 |  |
| `flores_s50` | `evaluation/corpus/flores_sentence_corpus.json` (FLORES devtest) | 50 | 835 | 50 | **ishlatilmaydi** (TOLQIN-2 «kirish») |
| `flores_t1` | `evaluation/corpus/flores_test_corpus.json` (FLORES devtest) | 50 | 620 | 50 | **ishlatilmaydi** (TOLQIN-2 «kirish») |
| `flores_t2` | `evaluation/corpus/flores_test2_corpus.json` (FLORES devtest) | 50 | 597 | 50 | **ishlatilmaydi** (TOLQIN-2 «kirish») |
| `flores_t3` | `evaluation/corpus/flores_test3_corpus.json` (FLORES devtest) | 50 | 624 | 50 | **ishlatilmaydi** (TOLQIN-2 «kirish») |
| `flores_t4` | `evaluation/corpus/flores_test4_corpus.json` (FLORES devtest) | 50 | 601 | 50 | **ishlatilmaydi** (TOLQIN-2 «kirish») |
| `flores_t5` | `evaluation/corpus/flores_test5_corpus.json` (FLORES devtest) | 60 | 715 | 60 | **ishlatilmaydi** (TOLQIN-2 «kirish») |
| `test6` | `data/test6.json` (FLORES devtest TEST6) | 60 | 723 | 60 | **ishlatilmaydi** (TOLQIN-2 «kirish») |
| `conj_dev` | `analysis/conj-m1/conj_dev.json` | 70 | 1 491 | 0 |  |
| `rol_dev` | `analysis/rol-f3-d2/rol_dev.json` | 70 | 1 505 | 0 |  |
| `predlog_dev_tuzatish` | `analysis/predlog-2/predlog_dev.json` (TUZATISH) | 70 | 1 554 | 1 | 1 moslik — filtr chiqaradi |
| `predlog_dev_baho` | `analysis/predlog-2/predlog_dev.json` (BAHO) | 98 | 2 557 | 1 | 1 moslik — filtr chiqaradi |
| `aligned_pairs` | `corpus/aligned_pairs.jsonl` (inlibrary harvest; train/dev/test shu yerdan) | 615 | 11 600 | 24 | 24 moslik (train231 dagi eval72 gaplari) — **o'sha 24 ishlatilmaydi** |
| `flagged` | `corpus/flagged.jsonl` (harvest, filtrdan o'tmagan juftlar) | 286 | 5 934 | 0 |  |

- `corpus/raw_pairs.jsonl` — 185 maqola yozuvi (`uz_abstract` butun annotatsiya, gapga bo'linmagan) — harvest
  xomi; gap soni yo'q.
- K1 (889) `uzen900` dan (900 − 11), K2 — Tagor; ular yuqoridagi 2-bandda.

## 6. Qayta ishlatiladigan kod

| fayl | funksiyalar | sha256 |
|---|---|---|
| `analysis/ijcl-paket/supplement/scripts/common.py` | heaps_beta, to_blocks (B2/B1), v0_clauses, v0_index_clauses, load_coded, unknown_codes, heldout | `ad448717bc394c6fb1963a7817b5bd07c8a68aa368880b77cf0ec1d1e23ea353` |
| `analysis/ijcl-paket/supplement/scripts/ud_tools.py` | conllu_gaplar, load_treebank, klauza_boshlari (asosiy=keng / xcomp_aclsiz=tor), gap_etaloni, kkt_teg, hizala, tizim_chegara, moslash, prf1, kesim_sinfi, baholash | `0d1dd3665d8abc32352d4948479857a880059a30da2705ff8d35b4c1e3178b4b` |
| `analysis/ijcl-paket/supplement/scripts/s02_random_cut.py` | a0_pieces, a2_pieces, real_spans, run (tasodifiy kesish A0/A1/A2) | `12f5aaea87259eea5e2c17acbd28f0ba1de7a720c876b1169ba0ae1881721135` |
| `analysis/ijcl-paket/supplement/scripts/s03_fragments.py` | muqobil segmentatsiya qoidalari (predikatsiz bo'laklar) | `aa5e80268c87500dae0825e1b489ed41d1785b7c4b240f94fb75a265a12041b5` |
| `analysis/ijcl-paket/supplement/scripts/s11_ud_segmentation.py` | V0 chegaralari vs oltin klauza (P/R, tor/keng) | `353389a564c5b4ed155eb12245c7a06dc2567730b459d66f305e9ddba9246f76` |
| `analysis/ijcl-paket/supplement/scripts/s12_ud_gold.py` | pats, betas, pair_delta, half_interval (1 000 yarim-tanlama), unit_codes | `5755a14ff6aeeb8e712752744f3f3c47577d315bebfcafd790fabcf74422d307` |
| `analysis/ijcl-paket/supplement/scripts/s10_ud_tagging.py` | UD->KKT teg aniqligi | `297350cab64b13b55f5fd74fb721714e6905185203311af4810f1480489f2d76` |
| `analysis/ijcl-paket/supplement/scripts/s14_noise_sample.py` | shovqin namunasi (500 token, Wilson) | `49ff8b10173fd02f03964335dd7ce61ef52abaf7a580b6817c222a1037b6967a` |
| `analysis/ijcl-paket/supplement/data/ud_kkt_mapping.tsv` | UPOS -> KKT teg xaritasi (mapped/excluded/unmappable) | `1686e40f114482ff5bda3971211a609f81e536817b180f49e6e542de104d1e2a` |
| `analysis/ijcl-paket/supplement/data/ud_system_output.json` | tizim tokenlari, teglari, V0 birliklari va oltin klauza proyeksiyasi (1 182 gap) | `259fd5ab7cb3fcde4200aaa858bc38174828364f9fc38e16de98d0a4e06076e9` |
| `analysis/ijcl-m2/iq.py` | soz_spanlari, v0_klauzalar, proyeksiya, v0_chegaralar, b2, b2k, kelishik_va_manba | `f2698f805930fb22c682ba0131036a2523553bf346140a19d1cfe2993a96be7b` |
| `analysis/ijcl-mustahkamlik/hisob.py` | setka, ekk, beta_royxat, yarim_indeks, boot_indeks, juft_delta, oraliq_yarim, oraliq_boot | `ee2f38b8e3ac6e124bcb2c9c2d0198efb31f4457e074376dee6377e86a8c82b5` |
| `analysis/ijcl-nazorat/olchov.py` | a2_qisqa, a2_invariant, a_qism, b_qism (random-cut nazorati, aniq uzunlik) | `83730cdd48ee286e11d17363d68c6709cc79ff980428a47c68e70caf19c50bd6` |
| `analysis/ud-baholash/etalon.py` | conllu_gaplar, klauza_boshlari, gap_etaloni, upos_inventar (ud_tools ning manbasi) | `d5e4161407f46158132abb68c282d77bff933fcd6d4d3e6f5fc29dce61aedac8` |
| `analysis/ud-baholash/seg_baho.py` | yaroqli_kesimlar, klauza_spanlari, tizim_chegara, oltin_provenans, moslash | `28cbcc9cb84f6bff463de63d665dae3d45edfc21c5bbae5ebe3c9cf335d26f0f` |
| `analysis/ud-baholash/teg_baho.py` | squash, ud_chunk_xarita, tizim_chunk_xarita, hizala, prf | `8fd507ee0b60209e1f44b2da075a79d46dd2f4b1b585697c8fa1e60e50f62a7d` |
| `analysis/gap_model_ierarxiya.py` | load_corpus (K1/K2 matn surati), heaps_beta, coverage_curve, UZEN_JSON, TAGOR_JSON | `34c23c7dfb5d57ab1b59c66f65b575c3728faebddf19497dc32fb55445d1e36a` |
| `analysis/ierarxiya_qayta_kodlash.py` | _tahlil (analizator MEMO), _kodla (so'z -> KKT kod) | `340f43bc72a2db74e71d5a1ce47c215b78baab21f39b1fb5ff7a9ab447d36c78` |
| `analysis/toplam_indeks.py` | normallash, xesh, matnlar (2 119 to'plamlari) | `116f6325327cfd5ed916765773599f5af73bad357b0e745c981e4f00bb45de75` |
| `analysis/_konvensiya/held_out.py` | filtr, filtr_matn, norm_tok, gap_xesh, oyna_xeshlar | `558bce2a88753d017b75ad339bd41b95ff49cc058de3c4cfb8b229a3b40f76a2` |

Segmentatsiya (V0) — `common.v0_clauses` / `iq.v0_klauzalar`; treebank mapping — `ud_kkt_mapping.tsv` + `ud_tools.kkt_teg`;
klauza ajratish (oltin) — `ud_tools.klauza_boshlari` / `gap_etaloni`; half-sampling — `s12_ud_gold.half_interval`
(1 000, seed 700000+r), `ijcl-mustahkamlik/hisob.yarim_indeks`; random spans — `s02_random_cut.a0_pieces/a2_pieces`,
`ijcl-nazorat/olchov.a2_qisqa`.
