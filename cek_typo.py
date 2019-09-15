from pyjarowinkler import distance as sim
from numba import jit
import pandas as pd
import os
import re
import json
from nltk.tokenize import TweetTokenizer
tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)

dir_path = os.path.dirname(os.path.realpath(__file__))
def similarity (kata1,kata2):
    return sim.get_jaro_distance(kata1, kata2, winkler=True, scaling=0.01)
def reduksi_huruf(kata):
    nkata  = list()
    for i,k in enumerate(kata):
        if i>2:
            if kata[i]== kata[i-1] and kata[i] == kata[i-2]:
                continue
            else:
                nkata.append(k)
        else:
            nkata.append(k)
    return "".join(nkata)

def getData(alamat):
    lineList = list()
    with open(dir_path + '/' + alamat, encoding = "ISO-8859-1") as f:
        for line in f:
            lineList.append(line.rstrip('\n'))
    return lineList

def get_data(name):
    with open(dir_path+"/"+str(name), "r") as filename:
        return json.load(filename)
def save_data(name, data):
    with open(dir_path+"/"+str(name), "w") as filename:
        json.dump(data, filename)

def new_corpus(kata, courpus_):
    huruf = 'abcdefghijklmnopqrstufwxyz1234567890'
    new_dict = dict()
    kata = list(set(kata))
    for i in list(reversed(kata)):
        if i not in huruf:
            # i = 'q'
            qq = {i:i}
            new_dict.update(qq)
        else:
            x = i
            j = "k_"+x+'_'
            new_dict.update(courpus_[j])
    return new_dict

corpus   = get_data("data/kata.json")
las_use  = get_data("data/last_use.json")
kbbi     = get_data("data/kata_kbbi_new.json") 
kata_dasar = get_data("data/kata-dasar.json")
failed   = get_data("data/failed_cek.json")

def cek_kata(cek, corpus_ = corpus, toleransi = 0.95):
    c = new_corpus(cek, corpus_)
    if (cek in kbbi) or (cek in kata_dasar) or (cek in failed):
    # if (cek in kbbi) :#or (cek in kata_dasar) or (cek in failed):
        # print("*ada-kbbi-")
        return cek
    elif cek in c :
        las_use[cek] = c[cek]
        # print('**ada', end=" ")
        return c[cek]
    elif cek in las_use:
        # print("**ada di lst", end=" ")
        return las_use[cek]
    temp_kata = list()
    temp_sim  = list()
    for kata, ganti in c.items(): 
        # print(kata, ganti)
        sim = similarity(cek,kata)
        # print("sim", sim)
        if sim > .97:
            las_use[kata] = ganti
            # print(sim)
            # print("sini")
            # print(kata)
            # save_data("data/last_use.json", data=las_use)
            return ganti
        else:
            temp_kata.append(kata)
            temp_sim.append(sim)
    max_ = max(temp_sim)
    # print("max", max_, end=" ")
    # print(max_, toleransi)
    if max_ < toleransi:
        # print(max_)
        if cek not in failed:
            failed.insert(0,cek)
        return cek
    else:
        max_index = temp_sim.index(max_)
        max_kata = temp_kata[max_index]
        las_use[max_kata] = c[max_kata]
        return c[max_kata]

def cek_typo (cek, corpus_ = corpus, toleransi = 0.95):
    if type(cek) != str:
        return "Masukan harus bertipe string"
    # cek = cek.split()
    cek = tknzr.tokenize(cek)
    list_cek=list()
    for k in cek:
        k = reduksi_huruf(k)
        kata_ = cek_kata(k.lower(), corpus_ = corpus, toleransi =toleransi)
        list_cek.append(kata_)
    save_data("data/failed_cek.json", data=failed)
    save_data("data/last_use.json", data=las_use)
    return " ".join(list_cek)