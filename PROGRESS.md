# news-image-20261123-dense-r3 — PROGRESS

## Status: BUILD SELESAI + TERUJI (24 Nov 2026, ~15:30 WIB)

Varian R3 untuk blind round 3 (cutoff 24 Nov 19:00 WIB). Perintah user
verbatim 24 Nov 15:03 WIB: jangan ganti poster total; hanya 1 perubahan
— perbesar judul utama 10-15%, jangan tambah berita baru; resubmit
sebelum 19:00; kalau R3 turun di bawah 50%, final besok pakai versi R2.

## SATU-SATUNYA perubahan: judul utama diperbesar
- Masthead "THE WORLD TODAY": 534x42 px (scale 6) -> 600x47 px.
  **+12,5% lebar, +11,9% tinggi** — di dalam brief 10-15%.
- Cara: metode baru `Page.write_scaled(..., 9, 8)` — render judul di
  scale 6 ke buffer kecil, lalu blit nearest-neighbour 9/8. Scale 7
  (= +16,7%) ditolak: di atas 15% DAN bertabrakan dengan teks kanan
  masthead (judul scale 7 berakhir x=659, teks kanan mulai x=594).
- Penyesuaian spacing yang dipaksa geometri (bukan perubahan konten):
  baris kanan bawah "THE DAY'S WORLD NEWS IN ONE IMAGE" pindah y 46
  -> 67 supaya judul yang melebar (berakhir x=636) tidak menyentuhnya.
  Tidak ada teks lain yang dipindah; tanggal, baris kanan atas, panel
  lead, grid 33 berita, footer — semua tidak disentuh.

## Bukti hanya 1 perubahan
- Pixel-diff poster baru vs dense: 14.576 piksel berbeda, SEMUA di
  y 18..80 (pita masthead saja). Di bawah y=93 — 33 berita, lead,
  termometer, grid, footer — byte-identik dengan versi dense.
- Verifikasi piksel: judul x 36..635 y 18..64; baris kanan atas
  x 654..987 y 20..33 (celah 18 px); baris kanan bawah x 594..987
  y 67..80 (celah 2 px); tanggal x 36..345 y 70..83 (celah 5 px).
  Tidak ada overlap, tidak ada yang terpotong.
- Visual check 2x: crop masthead + poster penuh — judul jelas lebih
  besar, semua teks terbaca, tidak ada huruf yang bersentuhan.

## File
- main.py — sama seperti dense + metode write_scaled + 2 baris
  masthead yang diubah. 33 berita tidak berubah.
- output/entry.png — 31.513 byte, sha256
  e3baac5666e3922693ac704adc3e7ed89155d78372f53c666eb976e0ae002ab6
  (2x run byte-identical).
- README.md (3 badge make.fun, repo makefun_news_build), LICENSE (MIT,
  SPDX), .makefun/owner.json (wallet 6JPei...Msg3h).

## Check kit (bundle v1, dua sesi)
- Bundle `news-image-20261123-dense-r3-transcripts-v1.tar.gz`
  (225.392 byte, sha256 a324a1c6…), commit lokal 47e874eb.
  Dua sesi: sesi asli poster padat (8e73bbe4) + sesi R3 ini
  (dea3526e); usage row sesi padat terlampir.
- **Check v1: ok true, failed [] — LOLOS PENUH.** thinking_reproduces
  50,0% (294/587 authored, 30 copied — di atas 30% yang disyaratkan);
  thinking_in_window lolos (98 timestamp dalam jendela);
  thinking_priced lolos (1 usage record); thinking_revised lolos
  (main.py dari 7 pesan); thinking_turns 58.
- Catatan: bundle memberi warning 0 usage row untuk sesi R3 ini
  (wajar — row muncul setelah sesi berakhir). Parent re-bundle
  dengan usage row sesi ini sebelum submit; reproduces tidak berubah
  karena itu (usage hanya memengaruhi pricing).

## Yang belum (tugas parent)
- Re-bundle setelah sesi ini berakhir (tambah usage row sesi ini) +
  check ulang.
- Loop EVAL ke user + push ke makefun_news_build + submit sebelum
  cutoff R3 24 Nov 19:00 WIB.
- Keputusan user: kalau R3 < 50%, final R4 besok pakai versi R2
  (Exact Sextant), jangan pakai versi R3.

---

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
