import operator
import copy

#Function for Level 2 candidate generation for SPM
def candidateGenLevel2(L, S, MS, sdc):
    #Joining s1 and s2
    C2, CTemp, CTemp1, CTemp2 = [], [], [], []
    for index, element in enumerate(L):
        for other in L[index:]:
            if element != other:
                CTemp.append([[element, other]])
            CTemp1.append([element])
            CTemp1.append([other])
            CTemp2.append([other])
            CTemp2.append([element])
            if CTemp1 not in CTemp:
                CTemp.append(CTemp1)
            if CTemp2 not in CTemp:
                CTemp.append(CTemp2)
            CTemp1, CTemp2 = [], []

    C2.append(CTemp)

    #Pruning step
    C2Prune = []
    for j, value in enumerate(C2[0]):
        count = 0
        for transaction in S:
            subsetCount = verifySubset(value, transaction, index=0, count=0)
            if subsetCount:
                C2Prune.append(C2[0][j])
                break

    #Verifying the sdc value
    removeArray = []
    for each in C2Prune:
        sdcCheck = checkSDC(each, sdc, MS)
        if not sdcCheck:
            removeArray.append(each)

    for each in removeArray:
        C2Prune.remove(each)
    return C2Prune

#Function to check if candidate is a subset of seq Level 2, true if it is a subset
def verifySubset(value, transaction, index, count):
    if transaction:
        for i, each in enumerate(transaction):

            if set(value[index]).issubset(set(each)):
                count += 1
                if index != len(value) - 1:
                    index += 1
                    verifySubset(value, transaction[i + 1:], index, count)

        if count >= len(value):
            return True
    return False

#Calculates the SDC value and verify if it satisfies
def checkSDC(seq, sdc, MS):
    size = len(seq)
    count = 0
    MSArray = []
    if size == 1:
        for each in seq[0]:
            count += 1
            MSArray.append(MS[each])
        length = count
    else:
        for each in seq:
            if len(each) == 1:
                count += 1
                MSArray.append(MS[each[0]])
            else:
                for every in each:
                    count += 1
                    MSArray.append(MS[every])
        length = count

    maximumVal = max(MSArray)
    minimumVal = min(MSArray)
    if maximumVal - minimumVal > sdc:
        return False

    return True