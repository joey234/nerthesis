import spacy
import sys
from collections import defaultdict
from nltk.tag.stanford import StanfordNERTagger


path_to_model = '../../stanford-ner-2018-02-27/vietnamese_new.gz'
path_to_jar = '../../stanford-ner-2018-02-27/stanford-ner-3.9.1.jar'
nertagger=StanfordNERTagger(path_to_model, path_to_jar)

nlp = spacy.load('./InitialNER/viNerFull50')

v_sent = None
e_sent = None
v_ent_list = None
e_ent_list = None

def sentToTuple(source_sent):
    '''
    Tokenize the Source sentence into tuple
    Input: English sentence (output of Giza++)
    Output: tp_list = [ (word, ({idx idx})) ,]
    '''
    source_sent_tokens = source_sent.split()
    # print(sent_tokens)
    tp_list = []
    idx_seq = ''
    idx_flag = False
    word = ''
    for i in range(len(source_sent_tokens) ):
        if source_sent_tokens[i] == '({':
            idx_flag = True
            word = source_sent_tokens[i-1]
            continue
        elif source_sent_tokens[i] == '})':
            tp = (word ,idx_seq.strip())
            # print(tp)
            tp_list.append(tp)
            idx_flag = False
            idx_seq = ''
            word = ''
        if idx_flag == True:
            idx_seq += source_sent_tokens[i] + ' '
    # print(tp_list)
    del tp_list[0]
    return tp_list

# e_ent_list  = [ (idx,idx,idx,... , type), ]
def getEntList_Spacy(source_tuple_list):
    '''
    Get the entity list of Source sentence
    Input: Source Sentence
    Output: e_ent_list  = [ ('idx idx idx ... ', type), ]
    '''
    source_sent = ''
    for tp in source_tuple_list:
        if tp['Word'] == 'NULL':
            continue
        e_sent += tp['Word']+ ' '
    source_sent = source_sent.strip()
    # print(e_sent)
    
    doc = nlp(source_sent)
    ent_list = []
    for ent in doc.ents:
        idx_seq = ''
        for i in range(ent.start,ent.end):
            idx_seq += str(i) + ' '
        idx_seq.strip()
        tp = (idx_seq,ent.label_)
        ent_list.append(tp)
    # print(ent_list)
    return ent_list

def getEntList_StanfordNER(source_tuple_list):
    '''
    Get the entity list of Source sentence
    Input: Source Sentence
    Output: e_ent_list  = [ ('idx idx idx ... ', type), ]
    '''
    source_sent = ''
    for tp in source_tuple_list:
        if tp['Word'] == 'NULL':
            continue
        source_sent += tp['Word']+ ' '
    source_sent = source_sent.strip()
    tag_list = nertagger.tag(source_sent.split())
    ent = ()
    ent_list = []
    cur_type = ''
    ent_flag = False
    # idx_seq = ''
    idx_seq = []
    word =''
    for i in range(len(tag_list)):
        if tag_list[i][1] != 'O':
            #ent of different type
            if cur_type != tag_list[i][1] and ent_flag == True:
                for idx in idx_seq:
                    word += tag_list[idx][0] + ' '
                word = word.strip()
                ent = (idx_seq,cur_type,word)
                # idx_seq = str(i)
                idx_seq.append(i)
                ent_list.append(ent)
                cur_type = tag_list[i][1]
                word = ''
            #continue of ent
            elif cur_type == tag_list[i][1] and ent_flag == True:
                # idx_seq +=  ' ' + str(i) 
                idx_seq.append(i)
            #begin of ent
            else:
                ent_flag = True
                cur_type = tag_list[i][1]
                # idx_seq = str(i)
                idx_seq.append(i)
        else:
            if ent_flag == True:
                for idx in idx_seq:
                    word += tag_list[idx][0] + ' '
                word = word.strip()
                ent = (idx_seq, cur_type, word)
                ent_list.append(ent)
                idx_seq = []
                ent_flag = False
                word = ''
            else:
                continue
        # print(ent_list)
    return ent_list

def getCombineNER(tuple_list):
    spacy_list = getEntList_Spacy(tuple_list)
    stanfordner_list = getEntList_StanfordNER(tuple_list)
    return spacy_list + stanfordner_list

def HardAlign(v_sent, e_sent):
    ent_set = getEntSet(v_sent,e_sent)
    for i in range(len(ent_set)):
        for ent in ent_set[i]:
            for j in range(len(ent)):
                if j == len(ent) - 1:
                    break
                if (ent[j] + 1) != (ent[j+1]):
                    return []
    return ent_set


def SoftAlign(v_sent,e_sent):
    ent_set = getEntSet(v_sent,e_sent)
    for i in range(len(ent_set)):
        for ent in ent_set[i]:
            for j in range(len(ent)):
                if j == len(ent) - 1:
                    break
                if (ent[j] + 1) != (ent[j+1]):
                    del ent_set[i]
                    break
    return ent_set


def getTargetEntList(tuple_list, target_sent, source_ent_list):
    '''
    Get the entity list of Target sentence based on word alignment
    Input: Alignment List, Source entity list, Target Sent
    Output: Target entity list
    '''
    target_tokens = target_sent.split()
    target_ent_list = []
    # print(tuple_list[8])
    for source_ent in source_ent_list:
        res = ''
        target_ent_idx = []
        for idx in source_ent[0]:
            idx = idx + 1
            list_idx = tuple_list[int(idx)]['Index']
            for index in list_idx:
                target_ent_idx.append(int(index))

        target_ent_idx = sorted(target_ent_idx, key = int)
            
        for idx in target_ent_idx:
            res += target_tokens[idx-1] + ' '
        res = res.strip()
        
        target_ent_list.append((target_ent_idx,source_ent[1],res))

    
    return target_ent_list

def getEntSet(source_sent,target_sent):
    '''
    [([idx]_en,[idx]_vi,'type',[word_en],[word_vi])]
    '''
    target_sent = ' '.join(target_sent).strip()
    
    source_tuple_list = source_sent
    source_ent_list = getEntList_StanfordNER(source_tuple_list)
    target_ent_list = getTargetEntList(source_tuple_list,target_sent,source_ent_list)
    ent_set = []
    for i in range(len(source_ent_list)):

        tp = (source_ent_list[i][0],target_ent_list[i][0],source_ent_list[i][1],source_ent_list[i][2],target_ent_list[i][2])

        ent_set.append(tp)
    
    return ent_set
def main():
    target_sent = 'The Vietnamese market has several challenges according to HCMC director John Rockhold .'
    source_sent = 'NULL ({ 8 }) Theo ({ 1 }) ông ({ }) John ({ 11 }) Rockhold ({ 4 7 9 10 12 }) thì ({ }) thị ({ 3 }) trường ({ }) Việt ({ 2 }) Nam ({ }) ẩn ({ }) chứa ({ }) nhiều ({ 5 }) thách ({ 6 }) thức ({ }) . ({ 13 })'
    print(getEntSet(source_sent,target_sent))

if __name__ == '__main__':
    main()