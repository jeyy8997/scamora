"""Membuat data/dataset_awasin_v3.csv = data formal (v2) + variasi informal sintetis. Kolom: teks,label,sumber."""
import pandas as pd, random, re
random.seed(11)
V=dict(h=["mobil","motor","iphone 15","uang 50 juta","paket umroh","emas 10 gram"],a=["500rb","1 juta","2jt","250rb","100rb"],
 rek=["6374684234","1234567890","9081726354","7788990011"],b=["BRI","BCA","Mandiri","Telkomsel","DANA","Shopee"],
 lnk=["bit.ly/klaimku","http://klaim-bank.xyz","https://cair-dana.top","bit.ly/v3rif"],tel=["0812-9988-7766","0856-1122-3344"],
 g=["3","4","6","8"],c=["Quotex","Binomo","kripto","robot forex"],m=["Shopee","Tokopedia","OLX","FB Marketplace"],x=["3","5","7"],
 p=["kampus","kantin","perpus","lab"],j=["8","9","10","13","15"])
T={'phishing_hadiah':["kamu dapet hadiah {h} dr {b}, buat ngeklaim transfer {a} dulu ke norek {rek}","selamat no kamu kepilih menang {h}. buka {lnk} isi data sama kode otp ya","anda menang undian {b} hadiah {h}, tf biaya admin {a} dlu biar cair","wa kamu terpilih dpt {h}, hubungi admin {tel} skrg juga sblm hangus","km pemenang giveaway {h}! klik {lnk} trus kirim pin ya"],
'fake_call_center':["halo kak ini cs {b}, akun kakak mau diblokir, tolong kasih kode otp yg masuk ya","kartu kamu bermasalah, klik {lnk} buat update data m-banking segera","info {b}: ada transaksi aneh di rekening, konfirmasi pin dlu biar aman","biaya admin {b} naik jd 150rb, klik {lnk} kalo mau tetep pake tarif lama","bapak/ibu kami dari {b}, mohon sebutkan otp utk membatalkan transaksi"],
'lowongan_kerja_palsu':["loker wfh gaji {g}jt/bln gampang cuma like youtube, daftar {lnk}, bayar seragam {a} dulu","butuh admin online no exp dibayar harian, chat {lnk}, ada biaya daftar {a}","kerja sampingan dr rumah komisi {g}jt, deposit dulu {a} buat modal tugas","info loker part time gaji {g}jt tanpa syarat, tf {a} utk pelatihan"],
'investasi_bodong':["modal {a} bisa jd 5jt seminggu, profit pasti, tf ke norek {rek} buat daftar","join grup trading {c}, untung dijamin tiap hari, depo awal {a}","{c} auto cuan, ga mungkin rugi, kirim {a} ke {rek}","ajak teman dpt bonus referral, setor {a} langsung return mingguan"],
'pinjol_ilegal':["bayar hutangmu skrg atau foto ktp kamu kita sebar ke semua kontak, tf ke {rek}","kami kolektor, telat {x} hari, kami hubungi keluarga + kantor kamu kalo ga lunas","pinjaman kamu nunggak, segera lunasi {a} ke {rek}, kalo ngga data disebar","tagihan {b} menunggak {x} hari, bayar hari ini atau kontak darurat kami teror"],
'marketplace_palsu':["kak barangnya udah aku bayar, dananya tertahan, klik {lnk} buat cairin, masukin pin","pembeli {m} sudah transfer, tinggal verifikasi {lnk} + otp biar masuk saldo","aku mau beli, kirim dulu no rek + kode otp buat konfirmasi {m}","admin {m}: dana belum cair, tf {a} biaya verifikasi dulu"],
'aman':["makasih ya udah tf patungan kemarin, aku udah terima","jgn kasih tau kode otp kamu ke siapa pun ya, lagi rame penipuan","besok ketemuan di {p} jam {j} ya, jangan lupa bawa laptop","hadiah ulang tahun buat adik udah aku beli, tinggal bungkus","link zoom kuliahnya: https://zoom.us/j/123456789 jam {j}","nanti aku transfer uang kos {a} ya, kirim no rek kamu","gaji bulan ini udah masuk, makan di luar yuk","info lowongan magang di kampus udah dibuka, cek di web resmi jurusan","tolong kirim tugasnya lewat email dulu ya","promo {m} lagi diskon, mau beli bareng?","tagihan wifi bulan ini {a} ya, nanti aku tf ke kamu","bayar kos udah belum? aku mau tf sekarang","kamu udah makan? aku bawain nasi ke {p}"]}
def noise(s):
    if random.random()<.5: s=s.lower()
    if random.random()<.3: s=re.sub(r"[,.!?]","",s)
    if random.random()<.2: s=s.replace("a","aa",1)
    return s
d=pd.read_csv('data/dataset_formal_v2.csv');d['sumber']='template_formal'
rows=[]
for k,ts in T.items():
    seen=set()
    for _ in range(3000):
        if len(seen)>=55: break
        s=random.choice(ts)
        s=re.sub(r"\{(\w+)\}",lambda m:random.choice(V[m.group(1)]),s);s=noise(s)
        seen.add(s)
    rows+=[(s,k,'template_informal') for s in seen]
o=pd.concat([d,pd.DataFrame(rows,columns=['teks','label','sumber'])]).drop_duplicates('teks').sample(frac=1,random_state=3)
o.to_csv('data/dataset_awasin_v3.csv',index=False);print(o.shape,o.label.value_counts().to_dict())
