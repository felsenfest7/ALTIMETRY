import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Dosyanın konumu
import sys
sys.path.insert(1, "/home/furkan/PycharmProjects/pythonProject/venv/ALTIMETRY_PY/GENEL_DOSYALAR/TUDES")
import tudes_functions as tf
#--------------------------------------------------
desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',20)
pd.set_option('display.max_rows',10000)
#--------------------------------------------------
#15 ve 60dklık verilerin birleştirilerek kullanılması gerekiliyor. Çünkü veriler arası zaman farklılıkları var.
#Bunları tespit ederken ben elimle txt filedan düzelttim ve ona göre verileri düzenleyerek buraya aktardım.
path1 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/ANTALYA/ANTALYA_60DK/17_12_1998-17_12_2003.txt" #60dk
path2 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/ANTALYA/ANTALYA_15DK/21_06_2001-01_03_2006.txt" #15dk
path3 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/ANTALYA/ANTALYA_15DK/01_03_2006-01_03_2011.txt" #15dk
path4 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/ANTALYA/ANTALYA_15DK/01_03_2011-01_03_2016.txt" #15dk
path5 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/ANTALYA/ANTALYA_15DK/01_03_2016-15_01_2018.txt" #15dk
path6 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/ANTALYA/ANTALYA_R/26_02_2019-13_11_2019.txt"    #15dk R

#Dataframelerin oluşturulması
df1 = tf.tudes_oku(path1)
df2 = tf.tudes_oku(path2)
df3 = tf.tudes_oku(path3)
df4 = tf.tudes_oku(path4)
df5 = tf.tudes_oku(path5)
df6 = tf.tudes_oku(path6)

#Günlük verilerin elde edilmesi
frames_15dk = [df2, df3, df4, df5]
df_15dk = tf.tudes_15dk_birlestir(frames_15dk)

frames_60dk = [df1]
df_60dk = tf.tudes_60dk_birlestir(frames_60dk)

#İki veri grubunun birleştirilmesi ve aylık verilerin elde edilmesi
frames_merged = [df_15dk, df_60dk]
df_aylik = tf.birlestir_1560(frames_merged)

#Harmonik analiz hesabı
ha = tf.harmonik_analiz_tudes(df_aylik, "Antalya", "antalya", "tudes")
print(ha)









