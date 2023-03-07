clc, clear, close all

%MARMARİSE AİT VERİLER

ales_veriler = readtable("/home/furkan/deus/ALTIMETRY/processler/ALES2/MARMARİS/marmaris_ales_aylik_idw.xlsx");

%TUDES istasyonlarına ait bilgier
istasyonlar = readtable("/home/furkan/deus/ALTIMETRY/processler/EXCELLER/istasyonlarin_konumlari.xlsx");

%Verilerin çizdirilmesi

figure;
geoscatter(istasyonlar.Latitude, istasyonlar.Longitude, "filled", "^", "MarkerEdgeColor", "r",...
            "MarkerFaceColor", "r", "DisplayName", "TUDES İstasyonu");

hold on

geoscatter(ales_veriler.glat_00, ales_veriler.glon_00, "filled", "o", "MarkerEdgeColor", "#0d88e6", ...
           "MarkerFaceColor","#0d88e6", "DisplayName", "ALES Verileri");

hold on;

geobasemap satellite;
title("Marmaris Aylık ALES Verilerinin Dağılımları");
legend();
grid on;

%İstasyonların isimlerinin haritaya yazdırılması
txt = strcat(istasyonlar.Station);
text(istasyonlar.Latitude-0.01,istasyonlar.Longitude-0.01,txt, "Color", "white", "FontWeight", "Bold");

ales_lat_ort = 36.753829885245906;
ales_lon_ort = 28.57312370765027;

geoscatter(ales_lat_ort, ales_lon_ort, "filled", "square", "MarkerEdgeColor", "#e6d800", "MarkerFaceColor", "#e6d800", "DisplayName", "Ortalama Koordinat");


