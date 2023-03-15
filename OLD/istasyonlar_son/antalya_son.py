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
#-----------------------------------------------------------------------------------------------------------------------
#ANTALYA ALES
#Verinin okunması
ales_jason1 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/ANTALYA/ANTALYA_VERİLER/JASON1/JASON1_DATA/*.nc")
ales_jason2 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/ANTALYA/ANTALYA_VERİLER/JASON2/JASON2_DATA/*.nc")
ales_jason3 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/ANTALYA/ANTALYA_VERİLER/JASON3/JASON3_DATA/*.nc")
ales_envisat214 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/ANTALYA/ANTALYA_VERİLER/ENVISAT/ENVISAT_214_DATA/*.nc")
ales_envisat141 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/ANTALYA/ANTALYA_VERİLER/ENVISAT/ENVISAT_141_DATA/*.nc")
print(ales_envisat141)
#Verilerin değerlerinin alınması
ales_jason1 = rmn.dort_index(ales_jason1)
ales_jason2 = rmn.dort_index(ales_jason2)
ales_jason3 = rmn.dort_index(ales_jason3)
ales_envisat214 = rmn.sifir_index(ales_envisat214)
ales_envisat141 = rmn.sifir_index(ales_envisat141)

#Veriye filter uygulanması
ales_jason1 = rmn.filter_ales_05(ales_jason1)
ales_jason2 = rmn.filter_ales_05(ales_jason2)
ales_jason3 = rmn.filter_ales_05(ales_jason3)
ales_envisat214 = rmn.filter_ales_05(ales_envisat214)
ales_envisat141 = rmn.filter_ales_05(ales_envisat141)

#Verilerin birleştirilmesi
#Tüm veriler
ales_frames = [ales_jason1, ales_jason2, ales_jason3, ales_envisat214, ales_envisat141]
ales_veriler = rmn.merge_df(ales_frames)

#Jason verileri
jason_frames = [ales_jason1, ales_jason2, ales_jason3]
jason_veriler = rmn.merge_df(jason_frames)

#Envisat verileri
envisat_frames = [ales_envisat214, ales_envisat141]
envisat_veriler = rmn.merge_df(envisat_frames)

#ALES verilerin filter uygulanması
ales_veriler = rmn.ales_sla_filter(ales_veriler)
jason_veriler = rmn.ales_sla_filter(jason_veriler)
envisat_veriler = rmn.ales_sla_filter(envisat_veriler)

#Günlük, aylık ve yıllık veriler
jason_veriler_gunluk = jason_veriler
jason_veriler_aylik = rmn.aylik(jason_veriler_gunluk)
jason_veriler_yillik = rmn.yillik(jason_veriler_gunluk)

envisat_veriler_gunluk = envisat_veriler
envisat_veriler_aylik = rmn.aylik(envisat_veriler_gunluk)
envisat_veriler_yillik = rmn.yillik(envisat_veriler_gunluk)

#Ortalama koordinat değerinin hesabı
hesaba_girecek_veriler_envisat = [ales_envisat214, ales_envisat141]
ort_koordinatlar_envisat = rmn.ort_koord(hesaba_girecek_veriler_envisat, 10)

hesaba_girecek_veriler_jason = [ales_jason1, ales_jason2, ales_jason3]
ort_koordinatlar_jason = rmn.ort_koord(hesaba_girecek_veriler_jason, 8.5)

enlem_envisat = ort_koordinatlar_envisat[0]
boylam_envisat = ort_koordinatlar_envisat[1]

enlem_jason = ort_koordinatlar_jason[0]
boylam_jason = ort_koordinatlar_jason[1]

#Ağırlık hesabı ile verilerin yeniden düzenlenmesi
envisat_agirliklar = rmn.agirlik_hesabi(envisat_veriler_gunluk, enlem_envisat, boylam_envisat)
jason_agirliklar = rmn.agirlik_hesabi(jason_veriler_gunluk, enlem_jason, boylam_jason)

#IDW değerlerinin hesaplanması ile son dataframelerin elde edilmesi
idw_envisat = rmn.idw(envisat_agirliklar)
idw_jason = rmn.idw(jason_agirliklar)

#Zamansal ve verisel olarak interpolasyonların yapılması
idw_envisat = rmn.dates_interpolation(idw_envisat)
idw_envisat = rmn.interpolation_ales(idw_envisat)

idw_jason = rmn.dates_interpolation(idw_jason)
idw_jason = rmn.interpolation_ales(idw_jason)

#İki tane noise var elimine edip tekrar interpole etcem
idw_envisat = idw_envisat[idw_envisat["ssh_idw"] < 26.40]
idw_jason = idw_jason[idw_jason["ssh_idw"] < 26.40]

idw_envisat = rmn.dates_interpolation(idw_envisat)
idw_envisat = rmn.interpolation_ales(idw_envisat)
idw_jason = rmn.dates_interpolation(idw_jason)
idw_jason = rmn.interpolation_ales(idw_jason)

#Excel tabloları
envisat_aylik_veriler_excel = rmn.df2excel(idw_envisat, "ALES", "ANTALYA", "antalya_ales_envisat_idw")
jason_aylik_veriler_excel = rmn.df2excel(idw_jason, "ALES", "ANTALYA", "antalya_ales_jason_idw")

#Verilerin çizdirilmesi
aylik_ssh_plot = pr.plot_ssh_aylik(idw_envisat, idw_jason, "Antalya Aylık Ağırlıklandırılmış Altimetre Verileri")



