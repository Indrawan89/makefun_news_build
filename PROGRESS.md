# news-image-20261123-dense — PROGRESS

## Status: BUILD SELESAI + TERUJI (23 Nov 2026, ~15:30 WIB)

Poster padat "THE WORLD TODAY — Monday 23 November 2026", tindak lanjut
riset ATM 20-50 (~/workspace/makefun/ATM-top20-50-20261123.md §1).
Resubmit target: sebelum blind round 1 jam 19:00 WIB hari ini.

## Isi
- 33 berita ber-tanggal dari 7 region (target 32-36): lead COP31 (1) +
  Europe 4 + Middle East 4 + Asia 5 + Americas 4 + Africa 4 +
  Oceania 3 + Sport/Tech 4 + Also today 4.
- Lead COP31 dipertahankan + panel termometer 1.5C; 4 kartu lama
  dipertahankan (kapal kargo Rusia, Dymer/Kyiv, Hormuz, menteri Korsel)
  + strip Also today lama (Lisbon, India 720/9d) + 20 berita baru.
- Tiap berita: 1 baris judul + 1 baris sub-judul + angka spesifik
  (korban, skor, jumlah, waktu).

## File
- main.py — Python stdlib murni, font bitmap 5x7, encoder PNG sendiri,
  1024x1024, deterministik.
- output/entry.png — 31.407 byte, sha256
  c981ff3216e186e96e8494e3f33b6dccbdcca4c198fcf3846baa5044a84a81e9
  (2x run byte-identical).
- README.md (3 badge make.fun, repo makefun_news_build), LICENSE (MIT,
  SPDX), .makefun/owner.json (wallet 6JPei...Msg3h).

## Catatan ukuran file
- 31 KB, BUKAN 200-400 KB seperti target heuristik. Itu hanya efisiensi
  kompresi PNG (warna datar + teks) — bukan kurang padat. Yang dinilai
  juri adalah gambarnya (33 berita di 1024x1024), bukan byte. Batas
  1 MiB jauh.

## Check kit (tanpa transcripts — bundle oleh parent)
- PASS: competition_open, snapshot, license_osi, entrypoint.
- FAIL: transcripts_present (wajar — belum ada bundle).
- SKIP x14: semua check transcript (butuh bundle).
- SUBMISSION x5: repo_public, repo_owner, repo_created_after_open,
  commit_in_repo, duplicate_snapshot (lolos setelah push ke
  makefun_news_build, dibuat 23 Nov 01:04Z sesudah opening 00:00Z).

## Visual check
- Dicek 2x via render: masthead tidak tumpang tindih (judul scale 6),
  semua 33 berita 1 baris judul + 1 baris deck, tidak ada teks
  terpotong / keluar panel. Kolom kiri berakhir y=974, kanan y=908,
  footer y=1008.

## Yang belum (tugas parent)
- Bundle transcripts (v1) + check dengan --transcripts.
- Push ke repo makefun_news_build (HAPUS dulu file entry lama? TIDAK —
  repo ini berisi entry Frank Pendulum; parent yang putuskan: ganti isi
  repo dengan folder dense ini, lalu submit sebelum 19:00 WIB).
- Loop EVAL ke user + submit.
