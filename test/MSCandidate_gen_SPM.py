import operator
import copy

#Function for MScandidate generation Sequential Pattern Mining
def candidateGen(F, S, MS, sdc):
    CTemp, CTemp1 = [], []
    for index, seq in enumerate(F):
        minimumVal, fItemS1 = smallestMS(seq, MS)

        #MS of first item in s1 is lesser than MS of all other items in s1
        if MSseqFirst(seq, MS):
            s1Subseq = subseq1(copy.deepcopy(seq))
            for other in F[index:]:
                s2Subseq, lItemS2, isSeparateElement = subseq2(copy.deepcopy(other))

                #1: the subsequence obtained by dropping the second item of s1 and the last item of s2 are the same
                #2: the MIS value of the last item of s2 is greater than that of the first item of s1.
                if s1Subseq == s2Subseq and MS[lItemS2] > MS[fItemS1]:
                    sizeS1, lengthS1 = lengthSizeS1(seq)
                    #Last item l in s2 is a separate element appended at the end of s1 as a separate element
                    if isSeparateElement:
                        CTemp1 = copy.deepcopy(seq)
                        CTemp1.append([lItemS2])
                        CTemp.append(CTemp1)
                        #(the length and the size of s1 are both 2) AND (the last item of s2 is greater than the last item of s1); l is added at the end of the last element of s1
                        if sizeS1 == lengthS1 == 2 and lItemS2 > lItem(seq):
                            CTemp1 = copy.deepcopy(seq)
                            CTemp1[-1].append(lItemS2)
                            CTemp.append(CTemp1)
                    #((the length of s1 is 2 and the size of s1 is 1) AND (the last item of s2 is greater than the last item of s1)) OR (the length of s1 is greater than 2); last item in s2 is added at the end of the last element of s1
                    elif ((lengthS1 == 2 and sizeS1 == 1) and (lItemS2 > lItem(seq))) or lengthS1 > 2:
                        CTemp1 = copy.deepcopy(seq)
                        CTemp1[-1].append(lItemS2)
                        CTemp.append(CTemp1)

        #MS of last item in S2 is less than MS of all other items in S2
        elif MSseqLast(seq, MS):
            for other in F[index:]:
                #Removes the first item from S1 and second last item from S2
                s1Subseq = subseq1NormalJoin(copy.deepcopy(seq))
                s2Subseq = subseqSecondlItem(copy.deepcopy(other))
                minimumVal, fItemS1 = smallestMS(seq, MS)
                minimumVal1, fItemS2 = smallestMS(other, MS)
                lItemS2 = lItem(other)

                #Check if first item is separate item in the sequence
                for each in seq:
                    if len(each) == 1:
                        isSeparateElement = True
                        break
                    else:
                        isSeparateElement = False
                        break

                #If both subsequences are equal and MS of last item of S2 is less than MS of first item in S1
                if s1Subseq == s2Subseq and MS[lItemS2] < MS[fItemS1]:
                    sizeS2, lengthS2 = lengthSizeS1(other)
                    #If they are not same, add first item of S1 in front of S2
                    if isSeparateElement:
                        CTemp1 = copy.deepcopy(seq[:1])
                        for n in other:
                            CTemp1.append(n)
                        CTemp.append(CTemp1)
                        #If the size of S2 is equal to length equal to 2 and first item in S1 is less than first item in S2
                        if sizeS2 == lengthS2 == 2 and fItemS1 < fItemS2:
                            CTemp1 = copy.deepcopy(other)
                            CTemp1[0].append(fItemS1)
                            CTemp.append(CTemp1)
                    elif ((lengthS2 == 2 and sizeS2 == 1) and (fItemS2 > fItemS1)) or lengthS2 > 2:
                        CTemp1 = copy.deepcopy(other)
                        CTemp1[0].append(fItemS1)
                        CTemp.append(CTemp1)

        #Join step
        else:
            for other in F[index:]:
                s1Subseq = subseq1NormalJoin(copy.deepcopy(seq))
                s2Subseq, lItemS2, isSeparateElement = subseq2(copy.deepcopy(other))

                if s1Subseq == s2Subseq:
                    if isSeparateElement:
                        CTemp1 = copy.deepcopy(seq)
                        CTemp1.append([lItemS2])
                        CTemp.append(CTemp1)
                    else:
                        lItemSetS1 = lItemSet(seq)
                        lItemSetS2 = lItemSet(other)
                        if len(seq) == 1:
                            sample = list(set(lItemSetS1 + lItemSetS2))
                            CTemp.append([sample])
                        else:
                            sample = list(set(lItemSetS1 + lItemSetS2))
                            CTemp1 = copy.deepcopy(seq[:-1])
                            CTemp1.append(sample)
                            CTemp.append(CTemp1)

    #Repeating for the reversed F string (create combination {a,b} and {b,a})
    F = list(reversed(F))
    for index, seq in enumerate(F):
        minimumVal, fItemS1 = smallestMS(seq, MS)
        if MSseqFirst(seq, MS):
            s1Subseq = subseq1(copy.deepcopy(seq))
            for other in F[index:]:
                s2Subseq, lItemS2, isSeparateElement = subseq2(copy.deepcopy(other))

                if s1Subseq == s2Subseq and MS[lItemS2] > MS[fItemS1]:
                    sizeS1, lengthS1 = lengthSizeS1(seq)
                    if isSeparateElement:
                        CTemp1 = copy.deepcopy(seq)
                        CTemp1.append([lItemS2])
                        CTemp.append(CTemp1)
                        if sizeS1 == lengthS1 == 2 and lItemS2 > lItem(seq):
                            CTemp1 = copy.deepcopy(seq)
                            CTemp1[-1].append(lItemS2)
                            CTemp.append(CTemp1)
                    elif ((lengthS1 == 2 and sizeS1 == 1) and (lItemS2 > lItem(seq))) or lengthS1 > 2:
                        CTemp1 = copy.deepcopy(seq)
                        CTemp1[-1].append(lItemS2)
                        CTemp.append(CTemp1)

        elif MSseqLast(seq, MS):
            for other in F[index:]:
                s1Subseq = subseq1NormalJoin(copy.deepcopy(seq))
                s2Subseq = subseqSecondlItem(copy.deepcopy(other))
                minimumVal, fItemS1 = smallestMS(seq, MS)
                minimumVal1, fItemS2 = smallestMS(other, MS)
                lItemS2 = lItem(other)

                for each in seq:
                    if len(each) == 1:
                        isSeparateElement = True
                        break
                    else:
                        isSeparateElement = False
                        break

                if s1Subseq == s2Subseq and MS[lItemS2] < MS[fItemS1]:
                    sizeS2, lengthS2 = lengthSizeS1(other)
                    if isSeparateElement:
                        CTemp1 = copy.deepcopy(seq[:1])
                        for n in other:
                            CTemp1.append(n)
                        CTemp.append(CTemp1)
                        if sizeS2 == lengthS2 == 2 and fItemS1 < fItemS2:
                            CTemp1 = copy.deepcopy(other)
                            CTemp1[0].append(fItemS1)
                            CTemp.append(CTemp1)
                    elif ((lengthS2 == 2 and sizeS2 == 1) and (fItemS2 > fItemS1)) or lengthS2 > 2:
                        CTemp1 = copy.deepcopy(other)
                        CTemp1[0].append(fItemS1)
                        CTemp.append(CTemp1)

        else:
            for other in F[index:]:
                s1Subseq = subseq1NormalJoin(copy.deepcopy(seq))
                s2Subseq, lItemS2, isSeparateElement = subseq2(copy.deepcopy(other))

                if s1Subseq == s2Subseq:
                    if isSeparateElement:
                        CTemp1 = copy.deepcopy(seq)
                        CTemp1.append([lItemS2])
                        CTemp.append(CTemp1)
                    else:
                        lItemSetS1 = lItemSet(seq)
                        lItemSetS2 = lItemSet(other)
                        if len(seq) == 1:
                            sample = list(set(lItemSetS1 + lItemSetS2))
                            CTemp.append([sample])
                        else:
                            sample = list(set(lItemSetS1 + lItemSetS2))
                            CTemp1 = copy.deepcopy(seq[:-1])
                            CTemp1.append(sample)
                            CTemp.append(CTemp1)

    #Prune step: Prune the C obtained
    F = list(reversed(F))

    #Ordering within itemsets
    for each in CTemp:
        if len(each) == 1:
            each[0].sort()
        else:
            for every in each:
                if len(every) != 1:
                    every.sort()

    CPrune = []
    Ftemp1 = copy.deepcopy(F)
    for candidate in CTemp:
        size, length = lengthSizeS1(candidate)
        CandidateSub = createSubset(copy.deepcopy(candidate), length)
        count = 0
        for each in CandidateSub:
            for transaction in Ftemp1:
                isSubset = checkSubsetLevel3(each, transaction, 0, 0)
                if isSubset:
                    count += 1
                    break
            if count == len(CandidateSub):
                CPrune.append(candidate)

    #Checking the sdc value
    removeArray = []
    for each in CPrune:
        sdcCheck = checkSDC(seq, sdc, MS)
        if not sdcCheck:
            removeArray.append(each)

    for each in removeArray:
        CPrune.remove(each)

    return CPrune

#Checking if the MS of first is smallest
def smallestMS(seq, MS):
    initFlag = True
    minimumVal = 10000
    for each in seq:
        if len(each) != 1:
            for every in each:
                if initFlag:
                    fItem = every
                    initFlag = False
                if MS[every] < minimumVal:
                    minimumVal = MS[every]
        else:
            if MS[each[0]] < minimumVal:
                minimumVal = MS[each[0]]
                if initFlag:
                    fItem = each[0]
                    initFlag = False

    return minimumVal, fItem

#Function to check if first item in sequence has lowest MS than all other items
def MSseqFirst(seq, MS):
    size = len(seq)
    temp = []
    if size == 1:
        for each in seq[0]:
            temp.append(MS[each])
    else:
        for each in seq:
            if len(each) == 1:
                temp.append(MS[each[0]])
            else:
                for every in each:
                    temp.append(MS[every])

    if min(temp) == temp[0]:
        if temp.count(temp[0]) == 1:
            return True

    return False

#Function to check if last item in sequence has lowest MS than all other items
def MSseqLast(seq, MS):
    size = len(seq)
    temp = []
    if size == 1:
        for each in seq[0]:
            temp.append(MS[each])
    else:
        for each in seq:
            if len(each) == 1:
                temp.append(MS[each[0]])
            else:
                for every in each:
                    temp.append(MS[every])

    if min(temp) == temp[-1]:
        if temp.count(temp[-1]) == 1:
            return True

    return False
#Function to remove first item from sequence
def subseq1NormalJoin(seq):
    if len(seq) == 1:
        seq[0].remove(seq[0][0])
    else:
        for each in seq:
            if len(each) == 1:
                seq.remove(each)
                break
            else:
                seq[0].remove(each[0])
                break

    return seq

#Function to create subsequence s2. Drop last item of S2
def subseq2(seq):
    for each in seq:
        if len(seq) == 1:
            lItemS2 = each[-1]
            seq[0].remove(each[-1])
            isSeparateElement = False
            break
        else:
            if len(seq[-1]) == 1:
                lItemS2 = seq[-1][0]
                seq.remove(seq[-1])
                isSeparateElement = True
                break
            else:
                lItemS2 = seq[-1][-1]
                seq[-1].remove(seq[-1][-1])
                isSeparateElement = False
                break

    return seq, lItemS2, isSeparateElement

#Function to return the last item set in a sequence
def lItemSet(seq):
    if len(seq) == 1:
        return seq[0]
    else:
        return seq[-1]


#Function to obtain length and size of a sequence
def lengthSizeS1(seq):
    size = len(seq)
    count = 0
    if size == 1:
        for each in seq[0]:
            count += 1
        length = count
    else:
        for each in seq:
            if len(each) == 1:
                count += 1
            else:
                for every in each:
                    count += 1
        length = count
    return size, length

#Function to create all subsets from a sequence
def createSubset(candidate, length):
    size = len(candidate)
    CandidateSubArray = []
    for index in range(length):
        flag = False
        candidate1 = copy.deepcopy(candidate)
        count = 0
        if size == 1:
            for each in candidate1[0]:
                count += 1
                if count == index + 1:
                    candidate1[0].remove(each)
                    CandidateSubArray.append(candidate1)
                    break
        else:
            for j, each in enumerate(candidate1):
                if len(each) == 1:
                    count += 1
                    if count == index + 1:
                        candidate1.remove(each)
                        CandidateSubArray.append(candidate1)
                        break
                else:
                    for every in each:
                        count += 1
                        if count == index + 1:
                            candidate1[j].remove(every)
                            CandidateSubArray.append(candidate1)
                            flag = True
                            break
                    if flag:
                        break
    return CandidateSubArray

#Function to check if candidate is a subset of sequence Level 3 onwards
def checkSubsetLevel3(value, transaction, index, count):
    if value == transaction:
        return True
    return False

#Calculate SDC value and verify if it satisfies
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
