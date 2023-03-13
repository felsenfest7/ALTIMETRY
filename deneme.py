from netCDF4 import Dataset as dt
import xarray as xr
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import geopy.distance

#Dosyanın konumu
import sys
sys.path.insert(1, "/home/furkan/PycharmProjects/pythonProject/venv/ALTIMETRY_PY/GENEL_DOSYALAR")

import xtrack_functions as xf
import plot_revize as pr
import juliandate as jd
from datetime import datetime

desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',30)
pd.set_option('display.max_rows',9000)
#-----------------------------------------------------------------------------------------------------------------------
"""
lrm_data = "/home/furkan/deus/ALTIMETRY/processler/XTRACK/XTRACK_DATA/ctoh.sla.ref.TP+J1+J2+J3.medsea.068.nc"
sar_data = "/home/furkan/deus/ALTIMETRY/processler/XTRACK/XTRACK_DATA/S3A_XTRACK_DATA/ctoh.sla.ref.S3A.medsea.500.nc"

#lrm_dataset = xf.read_xtrack(lrm_data, 36.5637203, 34.25539255)
#lrm_dataset = xf.aylik(lrm_dataset)

data = xr.open_dataset(sar_data, decode_times = False)
df = data.to_dataframe()
df2 = df.reset_index()
df2 = df2.dropna(0)

jday4713 = [i + 2433282.50000 for i in df2["time"]]
df2.insert(loc = 21, column="jday4713", value = jday4713)

# Calendar date'e çevirme
cdate = [jd.to_gregorian(i) for i in df2["jday4713"]]
df2.insert(loc = 22, column= "cdate", value = cdate)

cdate_2 = []

for i in cdate:
    dt_obj = datetime(*i)
    x = dt_obj.strftime("%Y-%m-%d")
    cdate_2.append(x)
df2.insert(loc=23, column="cdate_t", value=cdate_2)

# Pandasta çalışması için şu komut girilmeli
df2["cdate_t"] = pd.to_datetime(df2["cdate_t"])

print(df2)

#plot = pr.plot_xtrack(lrm_dataset, sar_dataset, "Deneme")


"""







"""
data =  "/home/furkan/deus/ALTIMETRY/processler/XTRACK/XTRACK_DATA/S3A_XTRACK_DATA/ctoh.sla.ref.S3A.medsea.500.nc"
data = xr.open_dataset(data, decode_times = False)

df = data.to_dataframe()
df2 = df.reset_index()
ist_koord = (36.5637203, 34.25539255 )

df2["distance2coast"] = df2.apply(lambda row: geopy.distance.distance((row["lat"], row["lon"]), ist_koord).km, axis=1)

df2["distance2coast"] = df2[["distance2coast"]].min(axis=1).min()
df2 = df2[df2.lat > 36.50]
print(df2["lat"].min())
"""
import math as m

def read_xtrack(data, ist_enlem, ist_boylam, delta):
    """
        --> XTRACK verilerinin okunması için oluşturulmuş fonksiyon.

        input: data olarak xtrack verisi, ist_enlem ve ist_boylam ise istasyonun koordinatlarıdır
        oytput: dataframe
    """

    # Dataset xarray kütüphanesi ile açılır
    dataset = xr.open_dataset(data, decode_times=False)

    # Ardından dataframe'e dönüştürülür
    df = dataset.to_dataframe()

    # Ardından yeni bir dataframe oluşturulur ve multiindex yapıdaki veri resetlenerek single index yapılır
    df2 = df.reset_index()

    # input olarak girilen istasyon koordinatları yardımıyla her row için koordinatların hesaplanması
    ist_koord = (ist_enlem, ist_boylam)
    df2["distance2coast"] = df2.apply(lambda row: geopy.distance.distance((row["lat"], row["lon"]), ist_koord).km,
                                      axis=1)

    # İstasyona minimum uzaklıkların hesabı
    df2["distance2coast"] = df2[["distance2coast"]].min(axis=1).min()

    df2["ssh"] = df2["mssh"] + df2["sla"]

    # Buraya daha kod geliştirmesi yapmadım, ana amacım en yakın olan noktayı seçebilmek bunu da elle yaptım
    df2 = df2[(df2.lat > (ist_enlem - delta)) & (df2.lat < (ist_enlem))]


    if np.isnan(df2["ssh"]):
        return df2[df2[(df2.lat > (ist_enlem - delta - 1)) & (df2.lat < (ist_enlem))]]["ssh"]
    else:
        return "zort"




    # İstasyon verinin altındaysa bunu kullan:
    # df2 = df2[(df2.lat > (ist_enlem)) & (df2.lat < (ist_enlem + delta))]

    # Nan değerlerin elimine edilmesi
    #df2 = df2.dropna(0)
    """
    # Jülyen tarihlerini grogaryan tarihine çevirme
    ##XTRACK verileri "days since 1950-1-1" olarak tanımlanmakta ve bu tarih 2433282.50000 Jülyen tarihine gelmekte (MÖ 4713'e göre)
    # Elimdeki julian günlerini bu date ile toplarsam aslında epok kaydırma yapmış olurum, bu sayede BC 4713'e göre tarih bulurum.
    # Ardından yeni epokları gregoryana çevirebilirim
    jday4713 = [i + 2433282.50000 for i in df2["time"]]
    df2.insert(loc=22, column="jday4713", value=jday4713)

    # Calendar date'e çevirme
    cdate = [jd.to_gregorian(i) for i in df2["jday4713"]]
    df2.insert(loc=23, column="cdate", value=cdate)

    # Datetime'a çevirme
    cdate_2 = []

    for i in cdate:
        dt_obj = datetime(*i)
        x = dt_obj.strftime("%Y-%m-%d")
        cdate_2.append(x)
    df2.insert(loc=24, column="cdate_t", value=cdate_2)

    # Pandasta çalışması için şu komut girilmeli
    df2["cdate_t"] = pd.to_datetime(df2["cdate_t"])
    """
    # XTRACK verileri T/P elipsoitinde elde edildiği için buradan elde edilen SSH değerleri WGS84 datumuna çevrilmelidir.
    # Bunun içinde T/P ve WGS84 elipsoitlerine ait bazı bilgilerin bilinmesi gerekmektedir.

    # WGS84 için veriler şu siteden alındı: https://www.unoosa.org/pdf/icg/2012/template/WGS_84.pdf, erişim tarihi 10 Mart Cuma
    a_wgs84 = 6378137.0  # metre
    b_wgs84 = 6356752.3142  # metre

    # T/P için bilgiler şı siteden alondı https://imos.org.au/fileadmin/user_upload/shared/SRS/Calval/1994_White_etal_JGR_94JC01382.pdf
    a_tp = 6378136.3
    b_tp = 6356751.56

    delta_a = a_wgs84 - a_tp
    delta_b = b_wgs84 - b_tp

    # İlk olarak SSH değerleri ham veride hesaplanacak


    # Ardından formül uygulanacak

    df2["lat_radyan"] = (df2["lat"] * m.pi) / 180
    df2["lon_radyan"] = (df2["lon"] * m.pi) / 180

    # WGS84 datumundaki koordinatlaron elde edilmesi
    df2["ssh_wgs84"] = df2.apply(lambda x: (
                x["ssh"] - (delta_a * ((m.cos(x["lat_radyan"])) ** 2)) + (delta_b * ((m.sin(x["lat_radyan"])) ** 2))),
                                 axis=1)

    # -----------------------------------------------
    #df2.set_index("cdate_t", inplace=True)

    return df2

lrm_data = "/home/furkan/deus/ALTIMETRY/processler/XTRACK/XTRACK_DATA/ctoh.sla.ref.TP+J1+J2+J3.medsea.068.nc"
lrm_dataset = read_xtrack(lrm_data, 36.5637203, 34.25539255, 0.05)
#lrm_dataset_aylik = xf.aylik(lrm_dataset)

print(lrm_dataset[["lat", "lon", "ssh", "ssh_wgs84", "mssh", "sla"]])