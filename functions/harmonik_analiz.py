import pandas as pd
import numpy as np
import math as m
from numpy.linalg import inv

import sys
import numpy
numpy.set_printoptions(threshold=sys.maxsize)

def harmonik_analiz(df):

    # In nomine Patris, et Fiili, et Spiritus Sancti. Amen.

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
    v = Ax - l

    #STOKASTİK MODEL
    ##Varyansın hesabı

    for i in v:
        if i > 10:
            print(i)

            #20DEN BÜYÜK OLANLARI 0LAYACAKSIN BURADA KALDIN


















