import pandas as pd
from util import read_align_file
inputfile = 'Result.actual.ti.final'
align_file = ''

data = pd.read_csv(inputfile, sep = ' ', encoding = 'utf-8')
data = data.fillna('NaN')

align_list = read_align_file(align_file)

def getWordTranslationProb(vnword, enword):
    result = data[(data.VN == vnword) & (data.EN == enword)].Prob
    tmp = result.values
    if (len(tmp)) == 0:
        return 0
    else:
        return tmp[0]

def getNETranslationProb(align_index, NEPair):
    '''
    NEPair: ([index],[index])

    Align element:
    [
{
     'Source_length':15,
     'Target_length':14,
     'Score':7.84741e-23,
     'Target':[words],
     'Source':
     [
               {
                    'Word':''
                    'Align':[...]
               }
     ]
}
]
    '''
    res = 0.0
    enNE = NEPair[3]
    vnNE = NEPair[4]
    # cur_align_sent = a lign_list[align_index]
    for enWord in enNE:
        sum = 0
        for vnWord in vnNE:
            sum += getWordTranslationProb(vnWord,enWord)
        res *= sum
    res = res / (len(enNE)**len(vnWord))
    return res