import pandas as pd 
inputfile = 'count_occ.csv'

data = pd.read_csv(inputfile, sep = ',', encoding = 'utf-8')
# data = data.fillna('NaN')


def getTu(enNE,vnNE):
    tmp = data[(data.NEV == vnNE) & (data.NEE == enNE)].Count
    tmp = tmp.values
    if (len(tmp)) == 0:
        return 0
    else:
        return tmp[0]

def getMau(enNE,vnNE):
    tmp = data[(data.NEE == enNE)].Count.sum()
    return tmp
    
def getCoocurenceProb(NEPair):
    enNE = NEPair[3]
    vnNE = NEPair[4]

    mau = getMau(enNE,vnNE)
    if mau == 0:
        return 0
    return getTu(enNE,vnNE) / mau

