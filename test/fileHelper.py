def getData(path):
    dataFile = open(path, 'r');
    seqDatabase = []
    for line in dataFile:
        s = line.strip()[1:-1]
        i = 0
        seq = [];
        while i < len(s):
            start = s.find('{', i)
            end = s.find('}', i)
            itemset = getItems(s[start + 1:end])
            seq.append(itemset)
            i = end + 1
        seqDatabase.append(seq)

    return seqDatabase


def getItems(string):
    string = string.replace(',', '')
    items = [];
    splits = string.split();
    for num in splits:
        items.append(int(num))
    return items

def getParamaters(path):
    paramsFile = open(path, 'r');
    MIS = {}
    SDC = 0.0
    for line in paramsFile:
        splits = line.split('=')
        if 'SDC' not in splits[0]:
            key = splits[0][splits[0].find('(')+1: splits[0].find(')')]
            value = float(splits[1].strip())
            MIS[int(key)] = value
        else:
            SDC = float(splits[1].strip())
    return MIS, SDC