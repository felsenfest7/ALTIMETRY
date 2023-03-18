from netCDF4 import Dataset as dt
import xarray as xr
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import geopy.distance
import juliandate as jd
from datetime import datetime

#Dosyanın konumu
import sys
sys.path.insert(1, "/home/furkan/PycharmProjects/pythonProject/venv/ALTIMETRY_PY/GENEL_DOSYALAR")

import xtrack_functions as xf
import xtrack_plot as xp

desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',30)
pd.set_option('display.max_rows',500000)
#-----------------------------------------------------------------------------------------------------------------------
#ANTALYA
"""
lrm_data = "/home/furkan/deus/ALTIMETRY/processler/XTRACK/XTRACK_DATA/ctoh.sla.ref.TP+J1+J2+J3.medsea.007.nc"
lrm_dataset = xf.read_xtrack(lrm_data, 36.83042146, 30.60868263, 0.05)
#lrm_dataset_aylik = xf.aylik(lrm_dataset)
print(lrm_dataset)
#plot = xp.plot_xtrack(lrm_dataset_aylik, "Antalya X-TRACK Verileri", "1995-10-28")
"""
lrm_data = "/home/furkan/deus/ALTIMETRY/processler/XTRACK/XTRACK_DATA/ctoh.sla.ref.TP+J1+J2+J3.medsea.007.nc"
data = xr.open_dataset(lrm_data, decode_times = False)
df = data.to_dataframe()
df2 = df.reset_index()
df2 = df2.dropna(0)

jday4713 = [i + 2433282.50000 for i in df2["time"]]
df2.insert(loc = 21, column="jday4713", value = jday4713)

# Calendar date'e çevirme
cdate = [jd.to_gregorian(i) for i in df2["jday4713"]]
df2.insert(loc = 22, column= "cdate", value = cdate)

ist_enlem = 36.83042146
ist_boylam = 30.60868263
delta = 0.3
ist_koord = (ist_enlem, ist_boylam)

df2["distance2coast"] = df2.apply(lambda row: geopy.distance.distance((row["lat"], row["lon"]), ist_koord).km, axis=1)
#df2["distance2coast"] = df2[["distance2coast"]].min(axis=1).min()

#df2 = df2[(df2.lat > (ist_enlem - delta)) & (df2.lat < (ist_enlem))]
#df2 = df2[df2["lat"] == 36.804829]
df2 = df2[(df2.lat > 36.80000) & (df2.lat < 36.81)]

"""
cdate_2 = []

for i in cdate:
    dt_obj = datetime(*i)
    x = dt_obj.strftime("%Y-%m-%d")
    cdate_2.append(x)
df2.insert(loc=24, column="cdate_t", value=cdate_2)

#Pandasta çalışması için şu komut girilmeli
df2["cdate_t"] = pd.to_datetime(df2["cdate_t"])
"""
#İlk olarak SSH değerleri ham veride hesaplanacak
df2["ssh"] = df2["mssh"] + df2["sla"]

#print(df2["cdate"])
"""
tuplex = (1993, 3, 20, 21, 29, 46, 420485)
new_tuple = tuplex[:3]
mydate = datetime(*new_tuple)
print(mydate)
"""
new_tuple = list()

for i in cdate:
    year = i[0]
    month = i[1]
    day = i[2]

    string_format = f"{year}-{month}-{day}"
    #date_time_obj = datetime.strptime(string_format,'%Y-%m-%d')
    print(string_format)


#print(new_tuple)


















