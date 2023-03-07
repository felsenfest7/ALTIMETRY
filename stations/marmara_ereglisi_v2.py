#-----------------------------------------------------------------------------------------------------------------------
#Tüm verinin okunması için (dataframe'in gözükmesi için) gerekli kodlar
import pandas as pd
import numpy as np

desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',20)
pd.set_option('display.max_rows',5000)

#Dosyanın konumu
import sys
sys.path.insert(1, "/home/furkan/PycharmProjects/pythonProject/venv/ALTIMETRY_PY/GENEL_DOSYALAR")

#Verinin okunması için kütüphaneler
import read_merge_nc as rmn
import plot as pl
import trend_analysis as ta
import plot_revize as pr
import altimetry_functions as af
#-----------------------------------------------------------------------------------------------------------------------
#MARMARA EREĞLİSİ ALES
#Verinin okunması
ales_jason1 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/MARMARA_EREGLISI/MARMARA_EREGLISI_VERİLER/JASON1/JASON1_DATA/*.nc")
ales_jason2 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/MARMARA_EREGLISI/MARMARA_EREGLISI_VERİLER/JASON2/JASON2_DATA/*.nc")
ales_jason3 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/MARMARA_EREGLISI/MARMARA_EREGLISI_VERİLER/JASON3/JASON3_DATA/*.nc")

#Verilerin değerlerinin alınması
ales_jason1 = af.index_sec(ales_jason1, 6)
ales_jason2 = af.index_sec(ales_jason2, 6)
ales_jason3 = af.index_sec(ales_jason3, 6)

#Veriye filter uygulanması
ales_jason1 = af.filter_ales_05(ales_jason1)    # 146 veriden 142 tanesi kullanılabiliyor
ales_jason2 = af.filter_ales_05(ales_jason2)    # 262 veriden 245 tanesi kullanılabiliyor
ales_jason3 = af.filter_ales_05(ales_jason3)    # 87 veriden 84 tanesi kullanılabiliyor

#Verilerin birleştirilmesi
ales_frames = [ales_jason1, ales_jason2, ales_jason3]
ales_veriler = af.merge_df(ales_frames)

#ALES verilerin filter uygulanması
#ales_veriler = af.ales_sla_filter(ales_veriler)

#Günlük, aylık ve yıllık veriler
ales_veriler_gunluk = ales_veriler
ales_veriler_aylik = af.aylik(ales_veriler_gunluk)
ales_veriler_yillik = af.yillik(ales_veriler_gunluk)

#Ortalama koordinat değerinin hesabı
hesaba_girecek_veriler = [ales_jason1, ales_jason2, ales_jason3]
ort_koordinatlar_ales = af.ort_koord(hesaba_girecek_veriler, 10)

enlem_ales = ort_koordinatlar_ales[0]
boylam_ales = ort_koordinatlar_ales[1]

#Ağırlık hesabı ile verilerin yeniden düzenlenmesi
ales_agirliklar = af.agirlik_hesabi(ales_veriler_gunluk, enlem_ales, boylam_ales)

#IDW değerlerinin hesaplanması ile son dataframelerin elde edilmesi
idw_ales = af.idw(ales_agirliklar)

#Zamansal olarak interpolasyonların yapılması
idw_ales = af.dates_interpolation(idw_ales)

#Excel tabloları
ales_aylik_veriler_excel = af.df2excel(idw_ales, "ALES2", "MARMARA_EREGLISI", "marmara_ereglisi_ales_aylik_idw")

#Verilerin çizdirilmesi
aylik_ssh_plot = pr.plot_ssh_aylik_yeni(idw_ales, "Marmara Ereğlisi Aylık Altimetre Verileri")

# ortalama enlem = 41.00051595108696
# ortalama boylam = 28.219866119565214



























