import pandas as pd
import numpy as np
import math as m
from numpy.linalg import inv

import sys
import numpy
numpy.set_printoptions(threshold=sys.maxsize)
sys.path.insert(1, "/home/furkan/PycharmProjects/pythonProject/venv/ALTIMETRY_PY/GENEL_DOSYALAR")
import altimetry_functions as af
import plot_revize as pr

def harmonik_analiz2(df, title):

    #NaN olan verilerin droplanması
    df.dropna(inplace = True)

    # FONKSİYONEL MODEL
    # Ağırlık matrisinin oluşturulması (numpy array şeklinde)
    boyut = df.shape[0]
    P = np.diag(np.full(boyut, 1))

    # l matrisinin çekilmesi ve numpy arrayine döndürülmesi
    l = df[["ssh_ales"]]
    l = l.to_numpy()

    #A matrisinin oluşturulması için yapılan işlemler
    ##İşlemler
    df2 = df.copy()
    df2.drop(columns = ["date", "weight"], inplace = True)  #gereksiz columnlar droplandı
    df2.reset_index(inplace = True)     #index sıfırlandı
    df2.rename_axis("index", inplace = True)    #indexi isimlendirme
    df2.rename(columns={"ay": "delta_t"}, inplace=True)     #zaman farklarını delta_t olarak isimlendirdim

    ##Katsayıların hesapları
    df2["Ak1"] = df2.apply(lambda df: m.cos((2 * m.pi * df["delta_t"])/6), axis=1)
    df2["Bk1"] = df2.apply(lambda df: m.sin((2 * m.pi * df["delta_t"])/6), axis=1)

    df2["Ak2"] = df2.apply(lambda df: m.cos((2 * m.pi * df["delta_t"])/12), axis=1)
    df2["Bk2"] = df2.apply(lambda df: m.sin((2 * m.pi * df["delta_t"])/12), axis=1)

    df2["b0_katsayı"] = 1

    ##l matrisini de çekmek lazım
    l = df2[["ssh_ales"]]

    ##Şimdi A katsayı matrisi biçiminde referanslamak için yeni bir dataframee aktararak referanslandırcam
    df3 = df2.copy()
    df3.drop(columns = ["ssh_ales"], inplace = True)    #l matrisini dropluyoruz buradan
    df3 = df3[["b0_katsayı", "delta_t", "Ak1", "Bk1", "Ak2", "Bk2"]]    #orderı düzeltiyorum

    A = df3.to_numpy()  #A matrisi
    l = l.to_numpy()    #l matrisi
    A_transpose = np.transpose(A)   #A transpose matrisi
    N = np.matmul(np.matmul(A_transpose, P), A)     #N matrisi, birimsiz
    n = np.matmul(np.matmul(A_transpose, P), l)     #n matrisi, metre biriminde
    N_ters = inv(N)     #ters N matrisi
    x = np.matmul(N_ters, n)    #x matrisi, metre biriminde

    #Düzeltme denklemlerinin hesabı
    ## v = Ax - l olarak ifade edilir. l matrisi zaten SSH ölçmeleri
    Ax = np.matmul(A, x)
    v = Ax - l  #metre biriminde

    ##Dengelemenin kontrolünün sağlanması
    l_artı_v = l + v    #ölçü + düzeltmesi

    ##Dengelemenin sağlanmasında l+v = Ax kontrolü yapılmalı. Ölçülerde virgülden sonra hata gelebileceği için
    ##milimetre mertebesinde bu kontrolü sağlayacağım.

    l_artı_v_v2 = np.round(l_artı_v, 3)
    Ax_v2 = np.round(Ax, 3)

    ##Dengelemenin kontrolü
    if np.array_equal(l_artı_v_v2, Ax_v2) == True:
        print("Dengeleme doğru !")
    else:
        print("Error 404 !")

    #Stokastik modelin oluşturulması
    v_transpose = np.transpose(v)   #v'nin transposesi
    PVV = np.matmul(np.matmul(v_transpose, P), v)   #metrekare biriminde bir deper döndürdü

    ##Bilinenler, bilinmeyenler ve serbestlik derecesi
    ##Aslında bu önceden belirlenmeliydi fakat ölçü sayısı zaten bilinmeyenlerden fazla gelecek kendi ölçülerimde
    bilinenler = boyut
    bilinmeyenler = 6   #6 tane gelgit bilinmeyni var. b0, b1, Ak1, Bk1, Ak2, Bk2
    serbestlik_derecesi = bilinenler - bilinmeyenler

    varyans = PVV / serbestlik_derecesi  #metrekare
    stdv = m.sqrt(varyans)  #metre

    ##Varyans kovaryans matrisinin oluşturulması ve bilinmeyenlerin doğruluklarının hesaplanması
    varyans_kovaryans_matrisi = varyans * N_ters

    #Trend
    ##Trend b1*t olarak ifade edilen değer.



    #Düzeltilmiş SSH verilerinin excele aktarılması ve plotta çizdirilmesi
    dateler = df[["cdate_t"]]
    corr_ssh = pd.DataFrame(l_artı_v, columns=['SSH'])

    dateler.reset_index(inplace = True)
    dateler.drop(columns=["ay"], inplace=True)

    df_merged = dateler.join(corr_ssh)  #Date ve CORR SSH değerlerinin tek dfte bulunduğu durum

    #Elde edilen df_merged'ün NaN boş aylarını interpole etmek
    df_merged = af.dates_interpolation(df_merged)

    #Plotun çizdirilmesi
    mss = x[0]  #Mean Sea Surface (m) biriminde ama array halinde
    mss = mss[0]  #Burada ise float halinde
    mss = mss.round(3)  #metre

    plot = pr.corr_ssh(df_merged, f"{title} Altimetri Verileri", mss)




































