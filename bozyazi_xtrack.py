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

desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',30)
pd.set_option('display.max_rows',30000)
#-----------------------------------------------------------------------------------------------------------------------

lrm_data = "/home/furkan/deus/ALTIMETRY/processler/XTRACK/XTRACK_DATA/ctoh.sla.ref.TP+J1+J2+J3.medsea.083.nc"

lrm_dataset = xf.read_xtrack(lrm_data, 36.09619554, 32.94011772, 0.05)
lrm_dataset_aylik = xf.aylik(lrm_dataset)

plot = xp.plot_xtrack(lrm_dataset_aylik, "Bozyazı X-TRACK Verileri", "2008-08-01")

