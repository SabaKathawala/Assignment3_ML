import fileHelper
import itertools
import copy

def init_pass(sortedMIS, I, S):
    # step 1: scan S to get support count of each item
    n = float(len(S))
    supportCount = {}
    for item in I:
        count = 0
        for sequence in S:
            for itemset in sequence:
                if item in itemset:
                    count = count + 1;
                    break

        supportCount[item] = count / n

    print supportCount
    L = []

    # step 2: add items with support > min(MIS)
    for item, support in supportCount.iteritems():
        if (support >= sortedMIS[0]):
            L.append(item)

    return L, supportCount

def level2_candidate_gen(L, supportCount, SDC, MS):
    C2 = []
    for index, l in enumerate(L):
        #print l
        if supportCount[l] >= MS[l]:
            for h in L[index+1:]:
                if (supportCount[h] >= MS[l]) & (abs(supportCount[h] - supportCount[l]) <= SDC):
                    #Add <{x, y}>
                    C2.append([[l, h]])
                    #Add < {x}, {y} >
                    C2.append([[l],[h]])
                    #C2.append([h])
                    #Add < {y}, {x} >
                    C2.append([[h],[l]])
                    #C2.append([l])

    print C2
    return C2

def MScandidate_gen_SPM(F, MS):
    C = []
    print(F)
    for index, s1 in enumerate(F):
        if minFirst(s1, MS):
            separate = False
            tempS1 = copy.deepcopy(s1)
            valSecondItem = '';
            # delete second value of s1
            if len(tempS1[0]) > 1:
                valSecondItem = tempS1[0][1]
                del tempS1[0][1]
            else:
                valSecondItem = tempS1[1][0]
                del tempS1[1][0]
            for s2 in F[index+1:]:
                tempS1 = copy.deepcopy(s1)
                #delete last value of s2
                tempS2 = copy.deepcopy(s2)
                valLastItem = ''
                if len(tempS2[-1]) == 1:
                    separate = True
                    valLastItem = tempS2[-1][0]
                    del tempS2[-1][0]

                # check if MIS of last item of s2> MIS of second item of s1
                if (MS[s2[-1][0]] > MS[s1[0][0]]):
                    # check if both sequences same
                    if(isSame(tempS1, tempS2)):

                        #check if last item is separate
                        if(separate):
                            candidate = copy.deepcopy(s1)
                            candidate.append([valLastItem])
                            C.append(candidate)

                            lengthOfS1 = sequenceLen(s1)
                            if (len(s1) == 2) & (lengthOfS1 == 2):
                                if(MS[valLastItem] > MS[s1[1]]):
                                    candidate = copy.deepcopy(s1)
                                    candidate[1].append(valLastItem)
                                    C.append(candidate)

                        #Not separate
                        else:
                            if((len(s1) == 1) & (lengthOfS1== 2)) | (lengthOfS1 > 2):
                                candidate = copy.deepcopy(s1)
                                candidate[1].append(valLastItem)
                                C.append(candidate)

        # Not greater
        elif minLast(s1, MS):
            separate = False

            # Remove first item from S1 and second last item from S2
            s2 = copy.deepcopy(s1)
            secondLastS2 = '';
            lastItemS2 = tempS2[-1][0]
            # delete second last value of s2
            if len(s2[-1]) > 1:
                secondLastItemS2 = s2[-1][-2]
                del s2[-1][2]
            else:
                secondLastItemS2 = s2[-2][0]
                del s2[-2][0]

            for seq in F[index + 1:]:

                # remove first item from s1
                s1_ = copy.deepcopy(seq)
                firstItemS1 = ''
                if len(s1_[0]) == 1:
                    separate = True

                firstItemS1 = s1_[0][0]
                del s1_[0][0]

                # check if MIS of last item of s2 < MIS of first item of s1
                if (MS[lastItemS2] < MS[firstItemS1]):
                    # check if both sequences same
                    lengthOfS2 = sequenceLen(s2)
                    if (isSame(s1_, s2)):

                        # check if last item is separate
                        if (separate):
                            candidate = copy.deepcopy(seq)
                            candidate.insert(0, [firstItemS1])
                            C.append(candidate)

                            # If size of S2 is equal to length equal to 2 and
                            # first item in S1 is greater than first item in S2
                            if (len(s2) == 2) & (lengthOfS2 == 2):
                                if (MS[firstItemS1] > MS[s2[0][1]]):
                                    candidate = copy.deepcopy(seq)
                                    candidate[0].append(s2[0][1])
                                    C.append(candidate)

                        # Not separate
                        else:
                            if ((len(s2) == 1) & (lengthOfS2 == 2) & MS[firstItemS1] > MS[s2[0][1]]) | (lengthOfS2 > 2):
                                candidate = copy.deepcopy(seq)
                                candidate[0].append(s2[0][1])
                                C.append(candidate)

        else:
            candidate_gen_SPM(F[k-1], s1, index, C)

    #Pruning
    FTemp = []
    for candidate in C:
        count = 0
        for element in candidate:
            for i in len(element):
                elCopy = copy.deepcopy(element)
                del elCopy[i]

                if isFrequent(elCopy, F[k-1]):
                    count += 1

        if(count == len(candidate)):
            FTemp.append(candidate)

    F.append(FTemp)


def isFrequent(elCopy, F):
    for seq in F:
        if not isSubSeqList(seq, elCopy):
            return False
    return True

def candidate_gen_SPM(F, s1, index, C):
    s1Copy = copy.deepcopy(s1)
    del s1Copy[0][0]

    for s2 in F[index+1:]:
        s2Copy = copy.deepcopy(s2)
        separate = False
        if(len(s2Copy[-1]) > 1):
            separate = True
        del s2Copy[-1][0]

        if(separate):
            candidate = copy.deepcopy(s1)
            candidate.append([s2[-1][0]])
            C.append(candidate)
        else:
            candidate = copy.deepcopy(s1)
            candidate[-1].append(s2[-1][0])
            C.append(candidate)

    #dropping the first item of s1 and dropping the last item of s2


def minFirst(s, MS):
    flattened = list(itertools.chain(*s))
    first = MS[flattened[0]]
    for i in range(1, len(flattened)):
        if first > flattened[i]:
            return False
    return True

def minLast(s, MS):
    flattened = list(itertools.chain(*s))
    last = MS[flattened[-1]]
    for i in flattened[0:-1]:
        if last > flattened[i]:
            return False
    return True

def isSame(s1, s2):
    flattenedS1 = list(itertools.chain(*s1))
    flattenedS2 = list(itertools.chain(*s2))

    for i,j in zip(flattenedS1, flattenedS2):
        if i != j:
            return False
    return True

def sequenceLen(s):
    flattened = list(itertools.chain(*s))
    return len(flattened)

#Preprocessing
#get data form file
I, S = fileHelper.getData('data-1.txt')      # set of all items and sequence database S

#get MIS and SDC values from file
MS, SDC = fileHelper.getParamaters('para1-1.txt')
# F-> 1
#
#
'''print 'Set of all items: ', I
print 'All sequences: ', S
print 'MIS: ', MS
print 'SDC: ', SDC'''

#start MS-GSP

#Step 1: sort(I, MS);
sortedMIS = MS.values()
sortedMIS.sort()
#print sortedMIS[0]

#Step2: init-pass(M, S);
L, supportCount = init_pass(sortedMIS, I, S)
#print 'L: ', L


# to hold k-length sequence patterns
F =[]
#step 3: fill F1
F1 = []
for item in L:
    if(supportCount[item] >= MS[item]):
        F1.append([item])

#print 'F1: ', F1
F.append(F1)


def findCTemp(C, MIS):
    minMISItem = []
    C_temp = copy.deepcopy(C)
    for index, c in enumerate(C_temp):
        current_min = 10
        min_element = -1
        for i in c:
            for p in i:
                if (MIS[p] < current_min):
                    current_min = MIS[p]
                    min_element = p
        #print min_element
        minMISItem.append(min_element)
        remove(min_element, c)
    return C_temp, minMISItem

def remove(element, seq):
    for i in seq:
        if (element in i):
            i.remove(element)
            break
    if ([] in seq):
        seq.remove([])
    return seq

# [1,2,4,5,6] [2,5,6]
def isSubSeq(super, sub):
    k=0
    for i in super:
        if k == len(sub):
            break
        if sub[k] == i:
            k+=1
    return k == len(sub)

def isSubSeqList(super, sub):
    k=0
    for i in super:
        if k == len(sub):
            break
        if isSubSeq(i, sub[k]):
            k+=1
    return k == len(sub)

k = 1
temp_bol = True

while(F[k-1]):
    print k-1, F[k-1]
    if k == 1:
        C = level2_candidate_gen(L, supportCount, SDC, MS)
    else:
        C = MScandidate_gen_SPM(F[k-1], MS)
        print "C", k, C
    FTemp = []

    if C:
        C_temp, minMISItem = findCTemp(C, MS)
        countCOcc = [0] * len(C)
        countC_tempOcc = [0] * len(C_temp)
        for s in S:
            for index, c in enumerate(C):
                if isSubSeqList(s, c):
                    countCOcc[index] += 1
                if isSubSeqList(s, C_temp[index]):
                    countC_tempOcc[index] += 1

        n = float(len(S))

        for index, count in enumerate(countCOcc):
            if count/n >= MS[minMISItem[index]]:
                FTemp.append(C[index])
    if (FTemp):
        F.append(FTemp)
        k += 1
    else: break
    #print F


    #temp_bol = False

