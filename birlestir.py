# Birleştirilecek dosya adları
ftb = 'ftb.m3u'
r = 'r.m3u'
r2 = 'r2.m3u'
inn = 'inn.m3u'
selcuk = 'selcuk.m3u'
an = 'an.m3u'
kbl = 'kbl.m3u'
gl = 'gl.m3u'
cikis_dosyasi = 'man26.m3u'

# M3U dosyalarının içeriğini oku
def oku_m3u(dosya_adi):
    with open(dosya_adi, 'r', encoding='utf-8') as f:
        return [satir.strip() for satir in f if satir.strip()]

# İçerikleri oku
ftb_icerik = oku_m3u(ftb)
r_icerik = oku_m3u(r)
r2_icerik = oku_m3u(r2)
inn_icerik = oku_m3u(inn)
selcuk_icerik = oku_m3u(selcuk)
an_icerik = oku_m3u(an)
kbl_icerik = oku_m3u(kbl)
gl_icerik = oku_m3u(gl)


# Birleştir
birlesik_icerik = kbl_icerik + ftb_icerik + r_icerik + r2_icerik + inn_icerik + selcuk_icerik + an_icerik + gl_icerik 

# Yeni dosyaya yaz
with open(cikis_dosyasi, 'w', encoding='utf-8') as f:
    for satir in birlesik_icerik:
        f.write(satir + '\n')

print(f"{cikis_dosyasi} dosyası başarıyla oluşturuldu.")
