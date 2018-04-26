
import CandidateSet
import CombineScore
import json
import os.path
ScoreTable = []

score_table_file = 'ScoreTable.json'

def createScoreTable(dev_list_EtoV,dev_list_VtoE):
    global ScoreTable
    if os.path.isfile(score_table_file):
        json_data=open(score_table_file).read()
        ScoreTable = json.loads(json_data)
        
    else:
        for i in range(len(dev_list_EtoV)):
            EtoV_sent = dev_list_EtoV[i]
            VtoE_sent = dev_list_VtoE[i]
            candidateSet = CandidateSet.getCandidateSet(EtoV_sent,VtoE_sent)
            score = CombineScore.getScoreDictForSet(candidateSet,EtoV_sent,VtoE_sent)
            ScoreTable.append(score)
        with open(score_table_file,'w',encoding='utf-8') as f:
            json.dump(ScoreTable,f)


def getScoreforOneCandidate(sent_index,candidate_index):

    return ScoreTable[sent_index][candidate_index]