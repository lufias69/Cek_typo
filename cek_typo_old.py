#from jarowinkler import similarity as sim
from pyjarowinkler import distance as sim
from numba import jit
import pandas as pd
import os
import re
# from numba import cuda
dir_path = os.path.dirname(os.path.realpath(__file__))

#open(dir_path + '/' + 'data.json')

# def load_data():
#     abjad = "ZABCDEFGHIJKLMNOPQRSTUVWXY"
#     # dc = "_dictionary"
#     # dfr = "_df"

#     #f = pd.read_excel("A-G.xlsx", )
#     kata = []
#     replace = []
#     for key, huruf in enumerate(abjad):
#         #print(huruf, key)
#         f = pd.read_excel(dir_path + '/' +"data/kata_typo.xlsx", sheet_name = huruf)
#         f_1 = f['kata'].tolist()
#         f_2 = f['ganti'].tolist()
#         kata +=f_1
#         replace+=f_2
#         key+=1

    #print(len(kata))
    #print(len(replace))
#     with open(dir_path + '/' +'data/_kata_.txt', 'w') as f:
#         for item in kata:
#             f.write("%s\n" % item)
#     with open(dir_path + '/' +'data/_replace_.txt', 'w') as f:
#         for item in replace:
#             f.write("%s\n" % item)
# #load_data()
# @cuda.jit(device=True)
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

def read_text(alamat):
    lineList = list()
    with open(alamat, encoding = "ISO-8859-1") as f:
        for line in f:
            lineList.append(line.rstrip('\n'))
    return lineList
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
def distinc_huruf(kata, jm=5):
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
# def new_corpus(kata, hr, jm):



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
            
def clean():
    g_diganti = list()
    with open(dir_path + '/' +"data/g_diganti.txt", "w") as f:
        for s in g_diganti:
            f.write(str(s) +"\n")   
    
    last_use_k = list()
    with open(dir_path + '/' +"data/last_use_k.txt", "w") as f:
        for s in last_use_k:
            f.write(str(s) +"\n")
            
    last_use_r = list()
    with open(dir_path + '/' +"data/last_use_r.txt", "w") as f:
        for s in last_use_r:
            f.write(str(s) +"\n")
            
    last_use_s = list()
    with open(dir_path + '/' +"data/last_use_s.txt", "w") as f:
        for s in last_use_s:
            f.write(str(s) +"\n")

def new_corpus(kata, jm):
    corpus = list()
    #if len(kata)==0:
        #return []
    huruf = 'abcdefghijklmnopqrstufwxyz1234567890'
    # for i in distinc_huruf(kata, jm=jm):
    kata = list(set(kata))
    for i in kata:
        if i not in huruf:
            i = 'a'
        x = i
        i = "k"+"_"+x+'_'
        #j = "r_"+x+'_'
        #print(i)
        f = getData('data/kata/'+i+'.txt')
        #f=open('data/kata/'+i+'.txt')
        #f=f.read()
        #f=f.split()
        corpus+=f
    return corpus

def new_corpus(kata, courpus_):
    huruf = 'abcdefghijklmnopqrstufwxyz1234567890'
    new_dict = dict()
    kata = list(set(kata))
    for i in kata:
        if i not in huruf:
            i = 'a'
        x = i
        #i = "k_"+x+'_'
        j = "k_"+x+'_'
        # #print(i)
        # # f = getData('data/kata/'+j+'.txt')
        # f = courpus_[j]
        new_dict.update(courpus_[j])
        # corpus+=f
    return new_dict

def get_data(name):
    with open(dir_path+"/"+str(name), "r") as filename:
        return json.load(filename)
def save_data(name, data):
    with open(dir_path+"/"+str(name), "w") as filename:
        json.dump(data, filename)

las_use    = get_data("data/last_use.json")
courpus_   = get_data("data/kata.json")
# last_use_k = getData('data/last_use_k.txt')
# last_use_r = getData('data/last_use_r.txt')
# last_use_s = getData('data/last_use_s.txt')

kbbi = getData('data/kata_kbbi_new.txt')
g_diganti = getData('data/g_diganti.txt')

kata_ = getData('data/_kata_.txt')
ganti_ = getData('data/_replace_.txt')


# @cuda.jit(device=True)
def typo (komentar):
    if type(komentar)!=list:
        komentar_split = komentar.split()
    for indx, kt_ in enumerate(komentar_split):
        if type(komentar) == str:
            kt_ = kt_.lower()
        kttr = kt_
        kt_ = reduksi_huruf(kt_)
        komentar_split[indx] = kt_
        kata_ = new_corpus(kt_, courpus_)
        cek = True
        
        if kttr in kbbi or kttr in g_diganti:
            continue



def norm_typo(komentar, jm=5):
    if type(komentar)!=list:
        komentar_split = komentar.split()
    for indx, kt in enumerate(komentar_split):
        if type(komentar) == str:
            kt = kt.lower()
        kttr = kt
        kt = reduksi_huruf(kt)
        komentar_split[indx] = kt
        kata_ = new_corpus(kt, courpus_)
        cek = True
        if kttr in kbbi or kttr in g_diganti:
            continue
        elif kt in last_use or kttr in last_use:
            komentar_split[indx] = las_use [kt]
        elif kt in kata_ or kttr in kata_:
            komentar_split[indx]= "" if kata_[kt] == 'nan' else kata_[kt]
            las_use[kt] = kata_[kt]
        else:
            list_kemiripan = []
            loop_kata = list()
            for kt, value in kata_.items():
                loop_kata.append(key)
                list_kemiripan.append(simJaro(kt, sl))
                simJaro0 = simJaro(kt, sl)
                if len(kt)<5:
                    if simJaro0 >= .98:
                        komentar_split[indx]="" if kt == 'nan' else kt
                        las_use[kt] = value#kata_[kt]
                        print("similarity-> "+kt+"|"+value+" ->", simJaro0)
                        cek = False
                        break
                else:
                    if simJaro0 >= .98:
                        komentar_split[indx]="" if ganti_[ix] == 'nan' else ganti_[ix]
                        las_use[kt] = value#kata_[kt]
                        print("similarity-> "+kt+"|"+value+" ->", simJaro0)
                        cek = False
                        break
            max_sim = max(list_kemiripan)
            idx = list_kemiripan.index(max_sim)
            katanya = loop_kata[idx]
            if len(kt)<5:
                if max_sim>=.98 and cek== True:
                    print("similarity",kt, str(max_sim))
                    print("similarity =>",kt,"|",kata_[list_kemiripan.index(max_sim)],"=>", str(max_sim))
                    komentar_split[indx]= "" if ganti_[list_kemiripan.index(max_sim)] == 'nan' else ganti_[list_kemiripan.index(max_sim)] #'Yes' if fruit == 'Apple' else 'No'
                    last_use_k.append(kt)
                    last_use_r.append(komentar_split[indx])
                    last_use_s.append(max(list_kemiripan))

                else:
                    if cek == True:
                        if kt not in g_diganti:
                            g_diganti.append(kt)
                        pass
            else:
                if max(list_kemiripan)>=.98 and cek== True:
                    print("similarity",kt, str(max(list_kemiripan)))
                    print("similarity =>",kt,"|",kata_[list_kemiripan.index(max(list_kemiripan))],"=>", str(max(list_kemiripan)))
                    komentar_split[indx]= "" if ganti_[list_kemiripan.index(max(list_kemiripan))] == 'nan' else ganti_[list_kemiripan.index(max(list_kemiripan))] #'Yes' if fruit == 'Apple' else 'No'
                    last_use_k.append(kt)
                    last_use_r.append(komentar_split[indx])
                    last_use_s.append(max(list_kemiripan))
                    # print("similarity =>",kt,"|",kata_[list_kemiripan.index(max(list_kemiripan))],"=>", str(max(list_kemiripan)))
                
                else:
                    print("similarity =>",kt,"|",kata_[list_kemiripan.index(max(list_kemiripan))],"=>", str(max(list_kemiripan)))
                    if cek == True:
                        if kt not in g_diganti:
                            g_diganti.append(kt)
                            pass
                    
                    
    ret = re.sub(' +', ' '," ".join(komentar_split))
    try:
        save_gdiganti()
    except:
        pass
    return ret.strip()
