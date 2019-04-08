#from jarowinkler import similarity as sim
from pyjarowinkler import distance as sim
import pandas as pd
import os 
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


def getData(alamat):
    lineList = list()
    with open(dir_path + '/' + alamat) as f:
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
    
def simJaro(kata1,kata2):
    return sim.get_jaro_distance(kata1, kata2, winkler=True, scaling=0.01)

def norm_typo(komentar):
    if type(komentar)!=list:
        komentar_split = komentar.split()
    for indx, kt in enumerate(komentar_split):
        cek = True
        if kt in kata_:
            komentar_split[indx]= "" if ganti_[kata_.index(kt)] == 'nan' else ganti_[kata_.index(kt)]
            print("<<<ada>>>")
            #continue
        else:
            list_kemiripan = []
            for ix, sl in enumerate(kata_):
                list_kemiripan.append(simJaro(kt, sl)) 
                if simJaro(kt, sl) >= .96:
                    komentar_split[indx]="" if ganti_[ix] == 'nan' else ganti_[ix]
                    print("similarity-> "+kt+"|"+sl+" ->", simJaro(kt, sl))
                    cek = False
                    break
            if max(list_kemiripan)>=.88 and cek== True:
                #print("similarity",kt, str(max(list_kemiripan)))
                print("similarity =>",kt,"|",kata_[list_kemiripan.index(max(list_kemiripan))],"=>", str(max(list_kemiripan)))
                komentar_split[indx]= "" if ganti_[list_kemiripan.index(max(list_kemiripan))] == 'nan' else ganti_[list_kemiripan.index(max(list_kemiripan))] #'Yes' if fruit == 'Apple' else 'No'
            else:
                if cek == True:
                    print("similarity =>",kt,"|",kata_[list_kemiripan.index(max(list_kemiripan))],"=>", str(max(list_kemiripan)))
    return " ".join(komentar_split)
