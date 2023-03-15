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
#ERDEMLİ ALES
#Verinin okunması
ales_jason1 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES2/ERDEMLİ/ERDEMLİ_VERİLER/JASON1/JASON1_DATA/*.nc")
ales_jason2 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES2/ERDEMLİ/ERDEMLİ_VERİLER/JASON2/JASON2_DATA/*.nc")
ales_jason3 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES2/ERDEMLİ/ERDEMLİ_VERİLER/JASON3/JASON3_DATA/*.nc")

#Verilerin değerlerinin alınması
ales_jason1 = af.index_sec(ales_jason1, 0)
ales_jason2 = af.index_sec(ales_jason2, 0)
ales_jason3 = af.index_sec(ales_jason3, 0)

#Veriye filter uygulanması
ales_jason1 = af.filter_ales_05(ales_jason1)
ales_jason2 = af.filter_ales_05(ales_jason2)
ales_jason3 = af.filter_ales_05(ales_jason3)

#Verilerin birleştirilmesi
ales_frames = [ales_jason1, ales_jason2, ales_jason3]
ales_veriler = af.merge_df(ales_frames)

#Günlük, aylık ve yıllık veriler
ales_veriler_gunluk = ales_veriler
ales_veriler_aylik = af.aylik(ales_veriler_gunluk)
ales_veriler_yillik = af.yillik(ales_veriler_gunluk)

#Ortalama koordinat değerinin hesabı
hesaba_girecek_veriler = [ales_jason1, ales_jason2, ales_jason3]
ort_koordinatlar_ales = af.ort_koord(hesaba_girecek_veriler, 17)

enlem_ales = ort_koordinatlar_ales[0]
boylam_ales = ort_koordinatlar_ales[1]

#Ağırlık hesabı ile verilerin yeniden düzenlenmesi
ales_agirliklar = af.agirlik_hesabi(ales_veriler_gunluk, 36.520397, 34.390459)

#IDW değerlerinin hesaplanması ile son dataframelerin elde edilmesi
idw_ales = af.idw(ales_agirliklar)

#IQR HESABI
filtered_idw_ales = af.iqr(idw_ales)

#Ufak noiseların yok edilmesi gerekmekte
filtered_idw_ales = filtered_idw_ales[filtered_idw_ales["ssh_idw"] > 25.10]
filtered_idw_ales = filtered_idw_ales[filtered_idw_ales["ssh_idw"] < 25.50]
filtered_idw_ales = filtered_idw_ales[filtered_idw_ales["distance.00"] < 19.60]
print(filtered_idw_ales)
#Zamansal olarak interpolasyonların yapılması
filtered_idw_ales = af.dates_interpolation(filtered_idw_ales)

#Excel tabloları
#ales_aylik_veriler_excel = af.df2excel(filtered_idw_ales, "ALES2", "ERDEMLİ", "erdemli_ales_aylik_idw")

#Verilerin çizdirilmesi
#aylik_ssh_plot = pr.plot_ssh_aylik_yeni(filtered_idw_ales, "Erdemli Aylık Altimetre Verileri")

#pr.distance_plot(filtered_idw_ales, 36.5637203, 34.25539255, enlem_ales, boylam_ales, "Erdemli")




































