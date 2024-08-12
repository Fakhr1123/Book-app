import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from mlxtend.frequent_patterns import association_rules, apriori 
from datetime import datetime

DATASET= pd.read_excel('DATA PENELITIAN4.xlsx')
DATASET.columns=['no', 'Transaksi', 'Judul', 'Nama_Anggota', 'Tahun_Masuk', 'Fakultas', 'Hari']

Judul_Buku= pd.read_excel('JUDUL BUKU.xlsx')
judul=Judul_Buku['Judul'].values.tolist()

import pandas as pd

st.title("Association Rules dengan algoritma Apriori")

#kelompok inputan
def get_data(Tahun_Masuk= '', Fakultas= '', Hari= ''):
    data= DATASET.copy()
    filtered= data.loc[
        (data["Tahun_Masuk"].str.contains(Tahun_Masuk))&
        (data["Fakultas"].str.contains(Fakultas))&
        (data["Hari"].str.contains(Hari))
    ]
    return filtered if filtered.shape[0] else "No Result!"

def User_input_features():
    Judul= st.selectbox("JUDUL", judul)
    Tahun_Masuk= st.selectbox("Tahun_Masuk", ["2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022","2023"])
    Fakultas= st.selectbox("Fakultas", ["FIP", "FBS", "FMIPA", "FIS", "FT", "FIK", "FPP", "FPS", "OTHERS"])
    Hari= st.select_slider("Hari", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], value= "Saturday")

    return Judul, Tahun_Masuk, Fakultas, Hari

DATASET['Tahun_Masuk'] = DATASET['Tahun_Masuk'].astype(str)
Judul, Tahun_Masuk, Fakultas, Hari= User_input_features()

DATASET= get_data(Tahun_Masuk, Fakultas, Hari)


def encode(x):
    if x <= 0:
        return 0
    elif x >= 1:
        return 1

if type(DATASET)!= type("No Result"):
    item_count1= DATASET.groupby(["Transaksi", "Judul"])["Judul"].count().reset_index(name="Jumlah")
    item_count_pivot = item_count1.pivot_table(index='Transaksi', columns='Judul', values='Jumlah', aggfunc='sum').fillna(0)
    item_count_pivot= item_count_pivot.applymap(encode) 
    
    support= 0.0009
    frequent_items= apriori(item_count_pivot, min_support= support, use_colnames=True)
    metric= "lift"
    min_threshold= 1
    rules1= association_rules(frequent_items, metric= metric, min_threshold= min_threshold)[["antecedents", "consequents", "support", "confidence", "lift"]]
    rules1.sort_values('confidence', ascending= False, inplace= True)

def parse_list(x):
    x= list(x)
    if len(x)== 1:
        return x[0]
    elif len(x)> 1:
        return ", ".join(x)

def return_item_data_bread(item_antecedents):
    data= rules1[["antecedents", "consequents"]].copy()

    data["antecedents"]= data["antecedents"].apply(parse_list)
    data["consequents"]= data["consequents"].apply(parse_list)

    return list(data.loc[data["antecedents"]== item_antecedents].iloc[0,:])

if type(data)!= type("No Result!"):
    st.markdown("HASIL REKOMENDASI : ")
    st.success(f"Jika konsumen membeli **{Judul}**, maka meminjam judul **{return_item_data_bread(Judul)[1]}** secara bersamaan")
