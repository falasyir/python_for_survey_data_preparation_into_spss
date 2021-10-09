# Python for Survey Data Preparation into SPSS

Pembuatan dokumen ini dilakukan dibuat pada OS Fedora 34 menggunakan package:
1. jupyterlab==3.1.13
2. python==3.9.7
3. pandas==1.3.3
4. pyreadstat==1.1.3
5. numpy==1.21.2

<i>Note : data yang digunakan sebagai contoh adalah data fiktif</i>

## Ketentuan penggunaan reasign_into_spss.py
1. Penamaan kolom data untuk kolom multipleresponse dimulai dengan label data (q1, q2, q3) diikuti dengan keterangan kolom yang sama di setiap label data dan diakhiri dengan nomor urutan. Penulisan dipisahkan dengan tanda <i>underscore</i>. Contoh yang berfungsi : q1_pilihan_1, q1_pilihan_2, q2_pilihan_1, q2_pilihan_2, dst. Contoh yang tidak akan berfungsi : q1pilihan_1, q1pilihan_2 atau q1_1, q1_2, dst.
2. File label jawaban untuk <b>tahapan labeling</b> perlu mengikuti contoh yang ada. Jika ingin menggunakan format lain, dipersilakan untuk merombank isi programnya.
3. File label jawaban untuk <b>tahapan generate syntax SPSS</b> dapat langsung menggunakan file excel dengan mengikuti format tabel <b>label_jawaban_melted</b>.
4. Modul program ini belum dapat dengan baik menangani kolom multirespon dan kolom lainnya dengan jawaban yang masih memiliki nilai seperti "99, Jepara", "99, tidak tahu", atau "99, ..." lainnya (asumsi penggunaan modul program ini ketika data sudah <i>clean</i>).
5. Modul program ini juga belum dapat menangani <i>reassign value</i> pada kolom jawaban yang pola penempatan jawabannya mengikuti/mengacu pada kolom multirespon tertentu. Misalkan untuk kasus pembelian barang dan harganya, ada dua kolom: q1_barang_1, q1_barang_2, q1_barang_3; q2_hrg_brg_1_rp, q2_hrg_brng_2_rp, q2_hrg_brg_2_rp. Jika kolom dengan label <b>q2</b> perlu ditata ulang <i>value</i>-nya, maka modul ini belum dapat memfasilitasinya.

## Note
1. Modul yang ada dapat diterapkan untuk data dengan jumlah baris yang banyak, meskipun pada contohnya hanya menggunakan 10 baris data saja.
2. Bagi siapa saja yang merasa kebutuhannya belum terfasilitasi dengan modul <b>reassign_into_spss.py</b> ini, dipersilakan untuk merombanknya sesuai kebutuhan.
3. Jika ada yang ingin memberikan masukan atau kontribusi program, sangat dipersilakan.
