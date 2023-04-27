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
import xtrack_plot as xp
import harmonik_analiz as ha

desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',30)
pd.set_option('display.max_rows',30000)
#-----------------------------------------------------------------------------------------------------------------------
#BOZYAZI
lrm_data = "/home/furkan/deus/ALTIMETRY/processler/XTRACK/XTRACK_DATA/ctoh.sla.ref.TP+J1+J2+J3.medsea.083.nc"
lrm_dataset = xf.read_xtrack(lrm_data, 36.09619554, 32.94011772, 0.05)
lrm_dataset_aylik = xf.aylik(lrm_dataset)

#IQR HESABI
filtered = xf.iqr_xtrack(lrm_dataset_aylik)

#Ufak noiseların yok edilmesi gerekmekte
filtered = filtered[filtered["ssh"] > 26.40]
filtered = filtered[filtered["ssh"] < 26.70]

#Dates interpolation
filtered = xf.dates_interpolation_xtrack(filtered)

#Plotun çizdirilmesi
#plot = xp.plot_xtrack(filtered, "Bozyazı X-TRACK Verileri", "2008-08-01")

#nx3'lük matrisin oluşturulması
wish = xf.df2newdf_xtrack(filtered, "2008-08-01")

#Excele aktarılması
#wish_table = xf.df2excel_xtrack(wish, "XTRACK", "BOZYAZI", "bozyazi_ssh_weight.xlsx")

haa = ha.harmonik_analiz2(wish, "Bozyazı X-TRACK", "bozyazı", "xtrack")
print(haa)