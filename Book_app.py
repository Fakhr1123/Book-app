import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from mlxtend.frequent_patterns import association_rules, apriori 
from datetime import datetime

DATASET= pd.read_excel('DATA PENELITIAN4.xlsx')
DATASET.columns=['no', 'Transaksi', 'Judul', 'Nama_Anggota', 'Tahun_Masuk', 'Fakultas', 'Hari']

st.title("Association Rules dengan algoritma Apriori")

#kelompok inputan
DATASET['Tahun_Masuk'] = DATASET['Tahun_Masuk'].astype(str)
def get_data(Tahun_Masuk= '', Fakultas= '', Hari= ''):
    DATA= DATASET.copy()
    filtered= DATA.loc[
        (DATA["Tahun_Masuk"].str.contains(Tahun_Masuk))&
        (DATA["Fakultas"].str.contains(Fakultas))&
        (DATA["Hari"].str.contains(Hari))
    ]
    return filtered if filtered.shape[0] else "No Result!"

Judul_Buku= pd.read_excel('JUDUL BUKU.xlsx')
Item_options=Judul_Buku['Judul'].values.tolist()

def User_input_features():
    Item= st.selectbox("Item", Item_options)
    Tahun_Masuk= st.selectbox("Tahun_Masuk", ["2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022","2023"])
    Fakultas= st.selectbox("Fakultas", ["FIP", "FBS", "FMIPA", "FIS", "FT", "FIK", "FPP", "FPS", "OTHERS"])
    Hari= st.select_slider("Hari", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], value= "Saturday")

    return Item, Tahun_Masuk, Fakultas, Hari

Judul, Tahun_Masuk, Fakultas, Hari = User_input_features()

DATA= get_data(Tahun_Masuk, Fakultas, Hari)


def encode(x):
    if x <= 0:
        return 0
    elif x >= 1:
        return 1

if type(DATA)!= type("No Result"):
    item_count1= DATA.groupby(["Transaksi", "Judul"])["Judul"].count().reset_index(name="Jumlah")
    item_count_pivot = item_count1.pivot_table(index='Transaksi', columns='Judul', values='Jumlah', aggfunc='sum').fillna(0)
    item_count_pivot= item_count_pivot.map(encode) 
    
    support= 0.0009
    frequent_items= apriori(item_count_pivot, min_support= support, use_colnames=True)

    metric= "lift"
    min_threshold= 1

    rules1= association_rules(frequent_items, metric= metric, min_threshold= min_threshold)[["antecedents", "consequents", "support", "confidence", "lift"]]
    rules1.sort_values('confidence', ascending= False, inplace= True)

def parse_list(x):
    if len(x) == 1:
        return str(x[0])
    elif len(x) > 1:
        return ", ".join(map(str, x))


def return_item_df(item_antecedents):
    DATA= rules1[["antecedents", "consequents"]].copy()

    DATA["antecedents"]= DATA["antecedents"].apply(parse_list)
    DATA["consequents"]= DATA["consequents"].apply(parse_list)

    return list(DATA.loc[DATA["antecedents"]== item_antecedents].iloc[0,:])

if type(DATA)!= type("No Result!"):
    st.markdown("HASIL REKOMENDASI : ")
    st.success(f"Jika konsumen meminjam **{Judul}**, maka meminjam judul **{return_item_df(Judul)[1]}** secara bersamaan")
