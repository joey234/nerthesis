'''
([],[])
'''
def evaluateSentencePair(predict,true_set):
    '''
    Compare predict set and true set of a sentence pair
    '''
    tp = 0
    predict = sorted(predict, key=lambda tmp: tmp[0])
    for i in range(len(true_set)):
        true_en_begin = true_set[i][0][0]
        # print('True_en_begin ',true_en_begin)
        true_en_end = true_set[i][0][-1]
        # print('True_en_end ',true_en_end)
        sub_predict = []
        for j in range(len(predict)):
            if len(predict[j][0]) < 1:
                continue
            predict_en_begin = predict[j][0][0]
            # print('PredictEnBegin ', predict_en_begin)
            if predict_en_begin == true_en_begin:
                sub_predict.append(predict[j])
        # print('SubPredict ',sub_predict)
        if(len(sub_predict)) > 0:
            for pair in sub_predict:
                # print(pair)
                predict_en_end = pair[0][-1]
                if predict_en_end == true_en_end:
                    if len(pair[1]) < 1:
                        continue
                    predict_vi_begin = pair[1][0]
                    predict_vi_end = pair[1][-1]
                    true_vi_begin = true_set[i][1][0]
                    true_vi_end = true_set[i][1][-1]
                    if true_vi_begin == predict_vi_begin and true_vi_end == predict_vi_end:
                        true_label = true_set[i][2]
                        predict_en_label = pair[2]
                        predict_vi_label = pair[5]
                        if predict_en_label == true_label and predict_vi_label == true_label:
                            tp += 1
                        
    return tp

def evaluate(predict_set,true_set):
    '''
    Compare the whole predict set and true set
    '''
    tp = 0
    total_predict_pairs = 0
    total_true_pairs = 0
    for i in range(len(predict_set)):
        total_predict_pairs += len(predict_set[i])
        total_true_pairs += len(true_set[i])
    
    for i in range(len(predict_set)):
        tp = tp + evaluateSentencePair(predict_set[i],true_set[i])
    
    
    return tp, total_predict_pairs, total_true_pairs
 
def getMetrics(predict_set,true_set):
    '''
    get Metrics Evaluation
    type_mode: 0:Insensitive , 1:Type-Sensitive
    '''
    tp, total_predict_pairs,total_true_pairs = evaluate(predict_set,true_set)
    # print('True Set ',true_set)
    # print('Predict Set ', predict_set)
    # print('TP ', tp)
    recall = tp / (total_true_pairs)
    precision = tp / (total_predict_pairs)
    if recall == 0 and precision == 0:
        f1 = 0
    else:
        f1 = 2*recall*precision/(recall+precision)
    res = {}
    res['R'] = recall
    res['P'] = precision
    res['F1'] = f1

    return res

