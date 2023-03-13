from netCDF4 import Dataset as dt
import xarray as xr
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import geopy.distance
import juliandate as jd
from datetime import datetime
import math as m

#-----------------------------------------------------------------------------------------------------------------------
def read_xtrack(data, ist_enlem, ist_boylam, delta):

    """
        --> XTRACK verilerinin okunması için oluşturulmuş fonksiyon.

        input: data olarak xtrack verisi, ist_enlem ve ist_boylam ise istasyonun koordinatlarıdır
        oytput: dataframe
    """

    #Dataset xarray kütüphanesi ile açılır
    dataset = xr.open_dataset(data, decode_times = False)

    #Ardından dataframe'e dönüştürülür
    df = dataset.to_dataframe()

    #Ardından yeni bir dataframe oluşturulur ve multiindex yapıdaki veri resetlenerek single index yapılır
    df2 = df.reset_index()

    #input olarak girilen istasyon koordinatları yardımıyla her row için koordinatların hesaplanması
    ist_koord = (ist_enlem, ist_boylam)
    df2["distance2coast"] = df2.apply(lambda row: geopy.distance.distance((row["lat"], row["lon"]), ist_koord).km, axis=1)

    #İstasyona minimum uzaklıkların hesabı
    df2["distance2coast"] = df2[["distance2coast"]].min(axis=1).min()

    #Buraya daha kod geliştirmesi yapmadım, ana amacım en yakın olan noktayı seçebilmek bunu da elle yaptım
    df2 = df2[(df2.lat > (ist_enlem - delta)) & (df2.lat < (ist_enlem))]

    #İstasyon verinin altındaysa bunu kullan:
    #df2 = df2[(df2.lat > (ist_enlem)) & (df2.lat < (ist_enlem + delta))]

    #Nan değerlerin elimine edilmesi
    df2 = df2.dropna(0)

    #Jülyen tarihlerini grogaryan tarihine çevirme
    ##XTRACK verileri "days since 1950-1-1" olarak tanımlanmakta ve bu tarih 2433282.50000 Jülyen tarihine gelmekte (MÖ 4713'e göre)
    # Elimdeki julian günlerini bu date ile toplarsam aslında epok kaydırma yapmış olurum, bu sayede BC 4713'e göre tarih bulurum.
    # Ardından yeni epokları gregoryana çevirebilirim
    jday4713 = [i + 2433282.50000 for i in df2["time"]]
    df2.insert(loc = 22, column="jday4713", value = jday4713)

    # Calendar date'e çevirme
    cdate = [jd.to_gregorian(i) for i in df2["jday4713"]]
    df2.insert(loc = 23, column= "cdate", value = cdate)

    # Datetime'a çevirme
    cdate_2 = []

    for i in cdate:
        dt_obj = datetime(*i)
        x = dt_obj.strftime("%Y-%m-%d")
        cdate_2.append(x)
    df2.insert(loc=24, column="cdate_t", value=cdate_2)

    #Pandasta çalışması için şu komut girilmeli
    df2["cdate_t"] = pd.to_datetime(df2["cdate_t"])

    # XTRACK verileri T/P elipsoitinde elde edildiği için buradan elde edilen SSH değerleri WGS84 datumuna çevrilmelidir.
    # Bunun içinde T/P ve WGS84 elipsoitlerine ait bazı bilgilerin bilinmesi gerekmektedir.

    #WGS84 için veriler şu siteden alındı: https://www.unoosa.org/pdf/icg/2012/template/WGS_84.pdf, erişim tarihi 10 Mart Cuma
    a_wgs84 = 6378137.0 #metre
    b_wgs84 = 6356752.3142 #metre

    #T/P için bilgiler şı siteden alondı https://imos.org.au/fileadmin/user_upload/shared/SRS/Calval/1994_White_etal_JGR_94JC01382.pdf
    a_tp = 6378136.3
    b_tp = 6356751.56

    delta_a = a_wgs84 - a_tp
    delta_b = b_wgs84 - b_tp

    #İlk olarak SSH değerleri ham veride hesaplanacak
    df2["ssh"] = df2["mssh"] + df2["sla"]

    #Ardından formül uygulanacak

    df2["lat_radyan"] = (df2["lat"] * m.pi) / 180
    df2["lon_radyan"] = (df2["lon"] * m.pi) / 180

    #WGS84 datumundaki koordinatlaron elde edilmesi
    df2["ssh_wgs84"] = df2.apply(lambda x: (x["ssh"] - (delta_a * ((m.cos(x["lat_radyan"]))**2)) + (delta_b * ((m.sin(x["lat_radyan"]))**2))), axis=1)



    #-----------------------------------------------
    df2.set_index("cdate_t", inplace=True)



    return df2
#-----------------------------------------------------------------------------------------------------------------------
def aylik(df):

    """
        --> Günlük olarak elde edilen XTRACK verilerinin aylık hale getirilmeis için kullanılmaktadır.

        input: dataframe
        output: dataframe
    """

    df = df.sort_values(by="cdate_t", ascending=True)
    df_aylık = df.resample("MS").mean()
    return df_aylık
#-----------------------------------------------------------------------------------------------------------------------







