#from jarowinkler import similarity as sim
from pyjarowinkler import distance as sim
from numba import jit
import pandas as pd
import os
import re
# from numba import cuda
dir_path = os.path.dirname(os.path.realpath(__file__))

#open(dir_path + '/' + 'data.json')

def load_data():
    abjad = "ZABCDEFGHIJKLMNOPQRSTUVWXY"
    dc = "_dictionary"
    dfr = "_df"

    #f = pd.read_excel("A-G.xlsx", )
    kata = []
    replace = []
    for key, huruf in enumerate(abjad):
        #print(huruf, key)
        f = pd.read_excel(dir_path + '/' +"data/kata_typo.xlsx", sheet_name = huruf)
        f_1 = f['kata'].tolist()
        f_2 = f['ganti'].tolist()
        kata +=f_1
        replace+=f_2

    #print(len(kata))
    #print(len(replace))
    with open(dir_path + '/' +'data/_kata_.txt', 'w') as f:
        for item in kata:
            f.write("%s\n" % item)
    with open(dir_path + '/' +'data/_replace_.txt', 'w') as f:
        for item in replace:
            f.write("%s\n" % item)
#load_data()
# @cuda.jit(device=True)
def reduksi_huruf(kata):
#kata = 'siiiiiiapaaaa'
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

def read_text(alamat):
    lineList = list()
    with open(alamat, encoding = "ISO-8859-1") as f:
        for line in f:
            lineList.append(line.rstrip('\n'))
    return lineList

kata_ = getData('data/_kata_.txt')
ganti_ = getData('data/_replace_.txt')

#print(len(ganti_))
#print(len(kata_))

if len(ganti_)!= len(kata_):
    load_data()
    print("Load data ulang")
    kata_ = getData('data/_kata_.txt')
    ganti_ = getData('data/_replace_.txt')
    print("Load data berhasil")

# @cuda.jit(device=True)  
def simJaro(kata1,kata2):
    return sim.get_jaro_distance(kata1, kata2, winkler=True, scaling=0.01)

# @cuda.jit(device=True)
def distinc_huruf(kata, jm=3):
    #kata = just_get_text(kata)
    if len(kata)==0:
        return kata
    n_kata = list()
    if kata[0].isalpha() or kata[0].isnumeric():
        pass
    else:
        if (kata[1].isalpha() or kata[1].isnumeric()) and kata[1] not in n_kata:
            n_kata.append(kata[1])
    try:
        if kata[0]=='a' or kata[0]=='m' or kata[0]=='p'or kata[0]=='b':#or kata[1]=='a' or kata[1]=='m' or kata[1]=='p':
            if (kata[0].isalpha() or kata[0].isnumeric()):
                n_kata.append(kata[0])
            if kata[1] not in n_kata and (kata[1].isalpha() or kata[1].isnumeric()):
                n_kata.append(kata[1])
    except:
        pass
    for hr in kata:
        if hr not in n_kata and hr != 'a' and hr != 'm' and hr != 'p'and hr != 'b':
            if hr.isalpha() or hr.isnumeric():
                n_kata.append(hr)
    if len(n_kata)>jm:
        return "".join(n_kata[:jm])
    else:
        return "".join(n_kata)
    #if jm == 1:
        #return "".join(n_kata[0])
    #elif jm==2:
        #return "".join(n_kata[:2])
def new_corpus_k(kata, jm):
    corpus = list()
    #if len(kata)==0:
        #return []
    for i in distinc_huruf(kata, jm=jm):
        x = i
        i = "k_"+x+'_'
        #j = "r_"+x+'_'
        #print(i)
        f = getData('data/kata/'+i+'.txt')
        #f=open('data/kata/'+i+'.txt')
        #f=f.read()
        #f=f.split()
        corpus+=f
    return corpus

def new_corpus_r(kata, jm):
    corpus = list()
    #if len(kata)==0:
        #return []
    for j in distinc_huruf(kata, jm=jm):
        x = j
        #i = "k_"+x+'_'
        j = "r_"+x+'_'
        #print(i)
        f = getData('data/kata/'+j+'.txt')
        #f=open('data/kata/'+i+'.txt')
        #f=f.read()
        #f=f.split()
        corpus+=f
    return corpus
# @cuda.jit(device=True)
def save_gdiganti():
    with open(dir_path + '/' +"data/g_diganti.txt", "w") as f:
        for s in g_diganti:
            f.write(str(s) +"\n")     
    with open(dir_path + '/' +"data/last_use_k.txt", "w") as f:
        for s in last_use_k:
            f.write(str(s) +"\n")
    with open(dir_path + '/' +"data/last_use_r.txt", "w") as f:
        for s in last_use_r:
            f.write(str(s) +"\n")
    with open(dir_path + '/' +"data/last_use_s.txt", "w") as f:
        for s in last_use_s:
            f.write(str(s) +"\n")


last_use_k = getData('data/last_use_k.txt')
last_use_r = getData('data/last_use_r.txt')
last_use_s = getData('data/last_use_s.txt')

kbbi = getData('data/kata_kbbi_new.txt')
g_diganti = getData('data/g_diganti.txt')

# @cuda.jit(device=True)
def norm_typo(komentar, jm=3):
    if type(komentar)!=list:
        komentar_split = komentar.split()
    for indx, kt in enumerate(komentar_split):
        kttr = kt
        kt = reduksi_huruf(kt)
        komentar_split[indx] = kt
        kata_ = new_corpus_k(kt, jm)
        ganti_ = new_corpus_r(kt, jm)
        cek = True
        if kttr in kbbi or kttr in g_diganti:
            #print("<<kbbi>>")
            continue
        elif kt in last_use_k or kttr in last_use_k:
            last_use_k_index = last_use_k.index(kt)
            komentar_split[indx] = last_use_r[last_use_k_index]
            # print("<<last use>>")
        elif kt in kata_ or kttr in kata_:
            komentar_split[indx]= "" if ganti_[kata_.index(kt)] == 'nan' else ganti_[kata_.index(kt)]
            last_use_k.append(kt)
            last_use_r.append(komentar_split[indx])
            #print("<<<ada>>>")
            #continue
        else:
            list_kemiripan = []
            for ix, sl in enumerate(kata_):
                list_kemiripan.append(simJaro(kt, sl)) 
                if simJaro(kt, sl) >= .96:
                    komentar_split[indx]="" if ganti_[ix] == 'nan' else ganti_[ix]
                    #print("similarity-> "+kt+"|"+sl+" ->", simJaro(kt, sl))
                    last_use_k.append(kt)
                    last_use_r.append(komentar_split[indx])
                    last_use_s.append(simJaro(kt, sl))
                    cek = False
                    break
            if max(list_kemiripan)>=.90 and cek== True:
                #print("similarity",kt, str(max(list_kemiripan)))
                #print("similarity =>",kt,"|",kata_[list_kemiripan.index(max(list_kemiripan))],"=>", str(max(list_kemiripan)))
                komentar_split[indx]= "" if ganti_[list_kemiripan.index(max(list_kemiripan))] == 'nan' else ganti_[list_kemiripan.index(max(list_kemiripan))] #'Yes' if fruit == 'Apple' else 'No'
                last_use_k.append(kt)
                last_use_r.append(komentar_split[indx])
                last_use_s.append(max(list_kemiripan))
                
            else:
                if cek == True:
                    if kt not in g_diganti:
                        g_diganti.append(kt)
                    pass
                    #print("similarity =>",kt,"|",kata_[list_kemiripan.index(max(list_kemiripan))],"=>", str(max(list_kemiripan)))
    ret = re.sub(' +', ' '," ".join(komentar_split))
    # save_gdiganti()
    return ret.strip()
