import pandas as pd
import numpy as np
import math as m
from numpy.linalg import inv

import sys
import numpy
numpy.set_printoptions(threshold=sys.maxsize)

"""
def harmonik_analiz(df):

    #FONKSİYONEL MODEL
    #Ağırlık matrisinin oluşturulması (numpy array şeklinde)
    boyut = df.shape[0]
    p = np.diag(np.full(boyut, 1))

    #l matrisinin çekilmesi ve numpy arrayine döndürülmesi
    l = df[["ssh_ales"]]
    l.fillna(0, inplace = True) # NaN valuelar matris çarpımında hata verdiği için 0 olarak değiştirildi
    l = l.to_numpy()

    #A matrisinin oluşturulması
    zaman_farkı = df.index[-1]

    #Solar semiannual parametreleri
    cos_radyan_ssa = m.cos((2 * m.pi * 6.00420752964) / 6)
    sin_radyan_ssa = m.sin((2 * m.pi * 6.00420752964) / 6)

    # Solar annual parametreleri
    cos_radyan_sa = m.cos((2 * m.pi * 12.0084151963) / 12)
    sin_radyan_sa = m.sin((2 * m.pi * 12.0084151963) / 12)

    row = [1, zaman_farkı, cos_radyan_ssa, sin_radyan_ssa, cos_radyan_sa, sin_radyan_sa]

    arr = np.array(row)
    A = np.tile(arr, (boyut, 1)) #A matrisi
    A_transpose = np.transpose(A)

    #Dengeleme hesabı
    ##N matrisi
    N = np.matmul(A_transpose, p)
    N = np.matmul(N, A)

    ##N'nin tersi
    N_ters = inv(N)

    ##n matrisi
    n = np.matmul(A_transpose, p)
    n = np.matmul(n, l)

    #x matrisi
    x = np.matmul(N_ters, n)

    #Düzeltmelerin hesaplanması
    #v = Ax - l

    Ax = np.matmul(A, x)
    v = Ax - l  #düzeltmeler

    np.place(v, v > 20, 0)  #bazı veriler doğal olarak hatalı geliyor (Nanlar yüzünden). Bunları 0'la değiştirildi.

    #STOKASTİK MODEL
    ##Varyansın hesabı

    v_transpose = np.transpose(v)

    vtp = np.matmul(v_transpose, p)
    vtpv = np.matmul(vtp, v)    #Pvv

    n = boyut   #bilinenler
    mx = 6      #bilinmeyenler
    f = n - mx  #serbestlik derecesi

    varyans = vtpv / f  #metre kare
    stdv = m.sqrt(varyans) #metre

    #Varyans kovaryans matrisinin oluşturulması
    Cxx = varyans * N_ters  #varyans kovaryans matrisi

    print(x)
"""

def harmonik_analiz2(df):

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

    print(x)



































