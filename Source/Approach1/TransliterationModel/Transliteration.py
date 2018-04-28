
def getTransliterationProb(NEPair,VtoE_sent):
    enNE = NEPair[3]
    vnNE = NEPair[4]
    n = len(enNE.split())
    word_count = 0
    enNE = enNE.lower()
    vnNE = vnNE.lower()
    # Count Word 
    for enword in enNE.split():
        for vnword in vnNE.split():
            if (enword == vnword):
                word_count += 1
                break
    if n == 0:
        return 0.0
    return word_count / n
