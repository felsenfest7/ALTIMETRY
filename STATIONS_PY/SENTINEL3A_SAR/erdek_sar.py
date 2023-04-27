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
import harmonik_analiz as ha
#-----------------------------------------------------------------------------------------------------------------------
#BOZYAZI GELENEKSEL VERİLER
#Verinin okunması
gel_s3a = rmn.merge_nc_ssh("/home/furkan/deus/ALTIMETRY/processler/SSH_VERİLERİ/ERDEK/ERDEK_VERİLER/SENTINEL3A/SENTINEL3A_DATA/*.nc")

#Verilerin değerlerinin alınması
gel_s3a = af.index_sec(gel_s3a, 0)

#Ortalama koordinat değerinin hesabı
gel_hesaba_girecek_veriler = [gel_s3a]
gel_ort_koordinatlar = rmn.gel_ort_koord(gel_hesaba_girecek_veriler)

gel_enlem = gel_ort_koordinatlar[0]
gel_boylam = gel_ort_koordinatlar[1]

#Ağırlık hesabı ile verilerin yeniden düzenlenmesi
gel_sar_agirliklar = rmn.agirlik_hesabi(gel_s3a, gel_enlem, gel_boylam)

#IDW değerlerinin hesaplanması ile son dataframelerin elde edilmesi
gel_idw_sar = rmn.gel_idw(gel_sar_agirliklar)

#IQR HESABI
filtered_idw_gel = af.iqr(gel_idw_sar)

#Zamansal olarak interpolasyonların yapılması
filtered_idw_gel = rmn.dates_interpolation(filtered_idw_gel)

#Verilerin çizdirilmesi
#gel_aylik_ssh_plot = pr.plot_ssh_aylik_yeni(filtered_idw_gel, "Erdek SAR Altimetre Verileri")

#nx3'lük matrisin oluşturulması
wish = af.df2newdf_gel(filtered_idw_gel)

#Excele aktarılması
wish_table = af.df2excel3(wish, "ALES3", "ERDEK", "erdek_sar_ssh_weight")

haa = ha.harmonik_analiz2(wish, "Erdek SAR", "erdek", "sar")
print(haa)


