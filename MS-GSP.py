# MS-GSP algorithm implementation
import operator
import copy


# Function to read the input files
def readFile(path):
    fr = open(path, 'r')
    return fr.readlines()


# Function to check if candidate is a subset of sequence Level 2
# Returns true if subset
def checkSubset(value, transaction, index, count):
    if transaction:
        for i, each in enumerate(transaction):

            if set(value[index]).issubset(set(each)):
                count += 1
                if index != len(value) - 1:
                    index += 1
                    # if count == len(value):
                    #     return True
                    checkSubset(value, transaction[i + 1:], index, count)

        if count >= len(value):
            return True
    return False


# Function to check if candidate is a subset of sequence Level 3 onwards
def checkSubsetLevel3(value, transaction, index, count):
    if value == transaction:
        return True
    return False


# Check if MS of first is smallest
def smallestMS(sequence, MS):
    initialFlag = True
    minValue = 10000
    for each in sequence:
        if len(each) != 1:
            for every in each:
                if initialFlag:
                    firstItem = every
                    initialFlag = False
                if MS[every] < minValue:
                    minValue = MS[every]
        else:
            if MS[each[0]] < minValue:
                minValue = MS[each[0]]
                if initialFlag:
                    firstItem = each[0]
                    initialFlag = False

    return minValue, firstItem


# Function to create subsequence of s1. Drop second item of S1
def subsequence1(sequence):
    for index, each in enumerate(sequence):
        if len(each) != 1:
            sequence[0].remove(each[1])
            break
        else:
            if len(sequence[index + 1]) != 1:
                sequence[index + 1].remove(sequence[index + 1][0])
                break
            else:
                sequence.remove(sequence[index + 1])
                break

    return sequence


# Function to create subsequence s2. Drop last item of S2
def subsequence2(sequence):
    for each in sequence:
        if len(sequence) == 1:
            lastItemS2 = each[-1]
            sequence[0].remove(each[-1])
            isSeparateElement = False
            break
        else:
            if len(sequence[-1]) == 1:
                lastItemS2 = sequence[-1][0]
                sequence.remove(sequence[-1])
                isSeparateElement = True
                break
            else:
                lastItemS2 = sequence[-1][-1]
                sequence[-1].remove(sequence[-1][-1])
                isSeparateElement = False
                break

    return sequence, lastItemS2, isSeparateElement


# Function to return last item in a sequence
def lastItem(sequence):
    for each in sequence:
        if len(sequence) == 1:
            lastItem = each[-1]
            break
        else:
            if len(sequence[-1]) == 1:
                lastItem = sequence[-1][0]
                break
            else:
                lastItem = sequence[-1][-1]
                break

    return lastItem


# Function to obtain length and size of a sequence
def lengthSizeS1(sequence):
    size = len(sequence)
    count = 0
    if size == 1:
        for each in sequence[0]:
            count += 1
        length = count
    else:
        for each in sequence:
            if len(each) == 1:
                count += 1
            else:
                for every in each:
                    count += 1
        length = count
    return size, length


# Function to check if first item in sequence has lowest MS than all other items
def MSSequenceFirst(sequence, MS):
    size = len(sequence)
    temp = []
    if size == 1:
        for each in sequence[0]:
            temp.append(MS[each])
    else:
        for each in sequence:
            if len(each) == 1:
                temp.append(MS[each[0]])
            else:
                for every in each:
                    temp.append(MS[every])

    if min(temp) == temp[0]:
        if temp.count(temp[0]) == 1:
            return True

    return False


# Function to check if last item in sequence has lowest MS than all other items
def MSSequenceLast(sequence, MS):
    size = len(sequence)
    temp = []
    if size == 1:
        for each in sequence[0]:
            temp.append(MS[each])
    else:
        for each in sequence:
            if len(each) == 1:
                temp.append(MS[each[0]])
            else:
                for every in each:
                    temp.append(MS[every])

    if min(temp) == temp[-1]:
        if temp.count(temp[-1]) == 1:
            return True

    return False


# Function to remove first item from sequence
def subsequence1NormalJoin(sequence):
    if len(sequence) == 1:
        sequence[0].remove(sequence[0][0])
    else:
        for each in sequence:
            if len(each) == 1:
                sequence.remove(each)
                break
            else:
                sequence[0].remove(each[0])
                break

    return sequence


# Function to return the last item set in a sequence
def lastItemSet(sequence):
    if len(sequence) == 1:
        return sequence[0]
    else:
        return sequence[-1]


# Function to remove second last item from S2
def subSequenceSecondLastItem(sequence):
    if len(sequence) == 1:
        sequence[0].remove(sequence[0][-2])
    else:
        if len(sequence[-1]) == 1:
            if len(sequence[-2]) != 1:
                sequence[-2].remove(sequence[-2][-1])
            else:
                sequence.remove(sequence[-2])
        else:
            sequence[-1].remove(sequence[-1][-2])
    return sequence


# Function to create all subsets from a sequence
def createSubset(candidate, length):
    size = len(candidate)
    candidateSubsetArray = []
    for index in range(length):
        flag = False
        candidate1 = copy.deepcopy(candidate)
        count = 0
        if size == 1:
            for each in candidate1[0]:
                count += 1
                if count == index + 1:
                    candidate1[0].remove(each)
                    candidateSubsetArray.append(candidate1)
                    break
        else:
            for j, each in enumerate(candidate1):
                if len(each) == 1:
                    count += 1
                    if count == index + 1:
                        candidate1.remove(each)
                        candidateSubsetArray.append(candidate1)
                        break
                else:
                    for every in each:
                        count += 1
                        if count == index + 1:
                            candidate1[j].remove(every)
                            candidateSubsetArray.append(candidate1)
                            flag = True
                            break
                    if flag:
                        break
    return candidateSubsetArray


# Calculate SDC value and verify if it satisfies
def calculateSDC(sequence, sdc, MS):
    size = len(sequence)
    count = 0
    MSArray = []
    if size == 1:
        for each in sequence[0]:
            count += 1
            MSArray.append(MS[each])
        length = count
    else:
        for each in sequence:
            if len(each) == 1:
                count += 1
                MSArray.append(MS[each[0]])
            else:
                for every in each:
                    count += 1
                    MSArray.append(MS[every])
        length = count

    maxValue = max(MSArray)
    minValue = min(MSArray)
    if maxValue - minValue > sdc:
        return False

    return True


# Function for candidate generation for F[k-1]
def candidateGen(F, S, MS, sdc):
    Ctemp, Ctemp1 = [], []
    for index, sequence in enumerate(F):
        minValue, firstItemS1 = smallestMS(sequence, MS)

        # MS of first item in S1 Is lesser than MS of all other items in S1
        if MSSequenceFirst(sequence, MS):
            s1Subsequence = subsequence1(copy.deepcopy(sequence))
            for other in F[index:]:
                s2Subsequence, lastItemS2, isSeparateElement = subsequence2(copy.deepcopy(other))

                # (1) the subsequences obtained by dropping the second item of s1 and the last item of s2 are the same
                # (2) the MIS val- ue of the last item of s2 is greater than that of the first item of s1.
                if s1Subsequence == s2Subsequence and MS[lastItemS2] > MS[firstItemS1]:
                    sizeS1, lengthS1 = lengthSizeS1(sequence)
                    # the last item l in s2 is a separate element
                    # appended at the end of s1 as a separate element
                    if isSeparateElement:
                        Ctemp1 = copy.deepcopy(sequence)
                        Ctemp1.append([lastItemS2])
                        Ctemp.append(Ctemp1)
                        # (the length and the size of s1 are both 2) AND (the last item of s2 is greater than the last item of s1)
                        # l is added at the end of the last element of s1
                        if sizeS1 == lengthS1 == 2 and lastItemS2 > lastItem(sequence):
                            Ctemp1 = copy.deepcopy(sequence)
                            Ctemp1[-1].append(lastItemS2)
                            Ctemp.append(Ctemp1)
                    # ((the length of s1 is 2 and the size of s1 is 1) AND (the last item of s2 is greater than the last item of s1)) OR (the length of s1 is greater than 2)
                    # the last item in s2 is added at the end of the last element of s1
                    elif ((lengthS1 == 2 and sizeS1 == 1) and (lastItemS2 > lastItem(sequence))) or lengthS1 > 2:
                        Ctemp1 = copy.deepcopy(sequence)
                        Ctemp1[-1].append(lastItemS2)
                        Ctemp.append(Ctemp1)

        # MS of last item in S2 is less than MS of all other items in S2
        elif MSSequenceLast(sequence, MS):
            for other in F[index:]:
                # Remove first item from S1 and second last item from S2
                s1Subsequence = subsequence1NormalJoin(copy.deepcopy(sequence))
                s2Subsequence = subSequenceSecondLastItem(copy.deepcopy(other))
                minValue, firstItemS1 = smallestMS(sequence, MS)
                minValue1, firstItemS2 = smallestMS(other, MS)
                lastItemS2 = lastItem(other)

                # Check if first item is separate item
                for each in sequence:
                    if len(each) == 1:
                        isSeparateElement = True
                        break
                    else:
                        isSeparateElement = False
                        break

                # If both subsequence are equal and MS of last item of S2 is less than MS of first item in S1
                if s1Subsequence == s2Subsequence and MS[lastItemS2] < MS[firstItemS1]:
                    sizeS2, lengthS2 = lengthSizeS1(other)
                    # If separate item, add first item of S1 in front of S2
                    if isSeparateElement:
                        Ctemp1 = copy.deepcopy(sequence[:1])
                        for n in other:
                            Ctemp1.append(n)
                        Ctemp.append(Ctemp1)
                        # If size of S2 is equal to length equal to 2 and first item in S1 is less than first item in S2
                        if sizeS2 == lengthS2 == 2 and firstItemS1 < firstItemS2:
                            Ctemp1 = copy.deepcopy(other)
                            Ctemp1[0].append(firstItemS1)
                            Ctemp.append(Ctemp1)
                    elif ((lengthS2 == 2 and sizeS2 == 1) and (firstItemS2 > firstItemS1)) or lengthS2 > 2:
                        Ctemp1 = copy.deepcopy(other)
                        Ctemp1[0].append(firstItemS1)
                        Ctemp.append(Ctemp1)

        # Normal join step
        else:
            for other in F[index:]:
                s1Subsequence = subsequence1NormalJoin(copy.deepcopy(sequence))
                s2Subsequence, lastItemS2, isSeparateElement = subsequence2(copy.deepcopy(other))

                if s1Subsequence == s2Subsequence:
                    if isSeparateElement:
                        Ctemp1 = copy.deepcopy(sequence)
                        Ctemp1.append([lastItemS2])
                        Ctemp.append(Ctemp1)
                    else:
                        lastItemSetS1 = lastItemSet(sequence)
                        lastItemSetS2 = lastItemSet(other)
                        if len(sequence) == 1:
                            sample = list(set(lastItemSetS1 + lastItemSetS2))
                            Ctemp.append([sample])
                        else:
                            sample = list(set(lastItemSetS1 + lastItemSetS2))
                            Ctemp1 = copy.deepcopy(sequence[:-1])
                            Ctemp1.append(sample)
                            Ctemp.append(Ctemp1)

    # Repeat for the reversed F string (create combination {a,b} and {b,a})
    F = list(reversed(F))
    for index, sequence in enumerate(F):
        minValue, firstItemS1 = smallestMS(sequence, MS)
        if MSSequenceFirst(sequence, MS):
            s1Subsequence = subsequence1(copy.deepcopy(sequence))
            for other in F[index:]:
                s2Subsequence, lastItemS2, isSeparateElement = subsequence2(copy.deepcopy(other))

                if s1Subsequence == s2Subsequence and MS[lastItemS2] > MS[firstItemS1]:
                    sizeS1, lengthS1 = lengthSizeS1(sequence)
                    if isSeparateElement:
                        Ctemp1 = copy.deepcopy(sequence)
                        Ctemp1.append([lastItemS2])
                        Ctemp.append(Ctemp1)
                        if sizeS1 == lengthS1 == 2 and lastItemS2 > lastItem(sequence):
                            Ctemp1 = copy.deepcopy(sequence)
                            Ctemp1[-1].append(lastItemS2)
                            Ctemp.append(Ctemp1)
                    elif ((lengthS1 == 2 and sizeS1 == 1) and (lastItemS2 > lastItem(sequence))) or lengthS1 > 2:
                        Ctemp1 = copy.deepcopy(sequence)
                        Ctemp1[-1].append(lastItemS2)
                        Ctemp.append(Ctemp1)

        elif MSSequenceLast(sequence, MS):
            for other in F[index:]:
                s1Subsequence = subsequence1NormalJoin(copy.deepcopy(sequence))
                s2Subsequence = subSequenceSecondLastItem(copy.deepcopy(other))
                minValue, firstItemS1 = smallestMS(sequence, MS)
                minValue1, firstItemS2 = smallestMS(other, MS)
                lastItemS2 = lastItem(other)

                for each in sequence:
                    if len(each) == 1:
                        isSeparateElement = True
                        break
                    else:
                        isSeparateElement = False
                        break

                if s1Subsequence == s2Subsequence and MS[lastItemS2] < MS[firstItemS1]:
                    sizeS2, lengthS2 = lengthSizeS1(other)
                    if isSeparateElement:
                        Ctemp1 = copy.deepcopy(sequence[:1])
                        for n in other:
                            Ctemp1.append(n)
                        Ctemp.append(Ctemp1)
                        if sizeS2 == lengthS2 == 2 and firstItemS1 < firstItemS2:
                            Ctemp1 = copy.deepcopy(other)
                            Ctemp1[0].append(firstItemS1)
                            Ctemp.append(Ctemp1)
                    elif ((lengthS2 == 2 and sizeS2 == 1) and (firstItemS2 > firstItemS1)) or lengthS2 > 2:
                        Ctemp1 = copy.deepcopy(other)
                        Ctemp1[0].append(firstItemS1)
                        Ctemp.append(Ctemp1)

        else:
            for other in F[index:]:
                s1Subsequence = subsequence1NormalJoin(copy.deepcopy(sequence))
                s2Subsequence, lastItemS2, isSeparateElement = subsequence2(copy.deepcopy(other))

                if s1Subsequence == s2Subsequence:
                    if isSeparateElement:
                        Ctemp1 = copy.deepcopy(sequence)
                        Ctemp1.append([lastItemS2])
                        Ctemp.append(Ctemp1)
                    else:
                        lastItemSetS1 = lastItemSet(sequence)
                        lastItemSetS2 = lastItemSet(other)
                        if len(sequence) == 1:
                            sample = list(set(lastItemSetS1 + lastItemSetS2))
                            Ctemp.append([sample])
                        else:
                            sample = list(set(lastItemSetS1 + lastItemSetS2))
                            Ctemp1 = copy.deepcopy(sequence[:-1])
                            Ctemp1.append(sample)
                            Ctemp.append(Ctemp1)

    # Prune the C obtained
    F = list(reversed(F))

    # Order within itemsets
    for each in Ctemp:
        if len(each) == 1:
            each[0].sort()
        else:
            for every in each:
                if len(every) != 1:
                    every.sort()

    CPrune = []
    Ftemp1 = copy.deepcopy(F)
    for candidate in Ctemp:
        size, length = lengthSizeS1(candidate)
        candidateSubset = createSubset(copy.deepcopy(candidate), length)
        count = 0
        for each in candidateSubset:
            for transaction in Ftemp1:
                isSubset = checkSubsetLevel3(each, transaction, 0, 0)
                if isSubset:
                    count += 1
                    break
            if count == len(candidateSubset):
                CPrune.append(candidate)

    # Check sdc value
    removeArray = []
    for each in CPrune:
        sdcCheck = calculateSDC(sequence, sdc, MS)
        if not sdcCheck:
            removeArray.append(each)

    for each in removeArray:
        CPrune.remove(each)

    return CPrune


# Function for candidate generation for level 2
def candidateGenLevel2(L, S, MS, sdc):
    # Joining step
    C2, C2temp, C2temp1, C2temp2 = [], [], [], []
    for index, element in enumerate(L):
        for other in L[index:]:
            if element != other:
                C2temp.append([[element, other]])
            C2temp1.append([element])
            C2temp1.append([other])
            C2temp2.append([other])
            C2temp2.append([element])
            if C2temp1 not in C2temp:
                C2temp.append(C2temp1)
            if C2temp2 not in C2temp:
                C2temp.append(C2temp2)
            C2temp1, C2temp2 = [], []

    C2.append(C2temp)

    # Pruning step
    C2Prune = []
    for j, value in enumerate(C2[0]):
        count = 0
        for transaction in S:
            subsetCount = checkSubset(value, transaction, index=0, count=0)
            if subsetCount:
                C2Prune.append(C2[0][j])
                break

    # Check sdc value
    removeArray = []
    for each in C2Prune:
        sdcCheck = calculateSDC(each, sdc, MS)
        if not sdcCheck:
            removeArray.append(each)

    for each in removeArray:
        C2Prune.remove(each)
    return C2Prune


# Function to calculate minsup and check if it satisfies
def supportCalculation(S, C, index, count):
    countArray = []
    for j, value in enumerate(C):
        count = 0
        for transaction in S:
            subsetCount = checkSubset(value, transaction, index=0, count=0)
            if subsetCount:
                count += 1
        # Trim
        countArray.append(count)
    return countArray


# Function to calculate support for level 3 and above
def supportCalculationsLevel3(S, C, index, count):
    countArray = []
    for j, value in enumerate(C):
        count = 0
        for transaction in S:
            subsetCount = checkSubset(value, transaction, index=0, count=0)
            if subsetCount:
                count += 1
        # Trim
        countArray.append(count)
    return countArray


if __name__ == '__main__':
    # Read data file
    # dataFile = readFile('/Users/abhijithjeevaraj/Downloads/DMTM/Project 1/sampleData')
    dataFile = open('data-1.txt', 'r').readlines();

    # Read parameters file
    # parametersFile = readFile('/Users/abhijithjeevaraj/Downloads/DMTM/Project 1/sampleParameters')
    parametersFile = open('para1-1.txt', 'r').readlines()

    # Open text file
    outputFile = open('output.txt', 'w')

    # Initialise sequence array
    # Extract transaction data as list of list
    S = []
    Stemp1 = []
    for each in dataFile:
        temp = each[each.find("<") + 1:each.find(">")]
        nComponent = temp.count('{')
        tempComponent = []
        for i in range(nComponent):
            component = temp[temp.find("{") + 1:temp.find("}")]
            component = component.split(',')
            Stemp = []
            for every in component:
                every = every.strip()
                Stemp.append(int(every))
            Stemp1.append(Stemp)

            temp = temp[temp.find('}') + 1:]

        S.append(Stemp1)
        Stemp1 = []

    # Initialise parameters dictionary
    # Extract MIS values from parameters file
    MS = {}
    for each in parametersFile:
        if 'SDC' not in each:
            key = each[each.find("(") + 1:each.find(")")]
            value = float(each[each.find("=") + 1:].strip("\n"))
            MS[int(key)] = value
        else:
            sdc = float(each[each.find("=") + 1:].strip("\n"))

    sortedMS = sorted(MS.items(), key=operator.itemgetter(1))

    # Initialise L array
    L = []
    for each in sortedMS:
        L.append(each[0])

    # Check minsup
    F = []
    F1 = []
    nTransactions = len(S)
    countArray = []
    for key in L:
        count = 0
        for transaction in S:
            for sequence in transaction:
                flag = False
                if key in sequence:
                    count += 1
                    flag = True
                    break

        # If support is greater than minsup
        support = float(count) / float(nTransactions)
        if support >= MS[key]:
            countArray.append(count)
            F1.append(key)

    # List of Frequent candidates
    F.append(F1)

    # Print the output in the required format
    output = ('The number of length 1 sequence is ' + str(len(F[0])) + '\n')
    outputFile.write(output)
    for index, each in enumerate(F[0]):
        output = 'Pattern: <{' + str(each) + '}> :Count=' + str(countArray[index]) + '\n'
        print('Pattern: <{' + str(each) + '}> :Count=', countArray[index])
        outputFile.write(output)
    print()
    outputFile.write('\n')

    # Main loop
    k = 1
    C = []
    while F[-1]:
        if k == 1:
            C.append(candidateGenLevel2(L, S, MS, sdc))
            countArray = supportCalculation(S, C[-1], index=0, count=0)
        else:
            C.append(candidateGen(F[-1], S, MS, sdc))
            countArray = supportCalculationsLevel3(S, C[-1], index=0, count=0)

        # Calculate if each sequence satisfies minimum support
        # c.count/n > MIS(c.minMISItem)
        Ftemp = []
        outputCountArray = []
        for i, candidate in enumerate(C[-1]):
            minValue = 100000
            for element in candidate:
                if minValue > MS[element[0]]:
                    minValue = MS[element[0]]
            if (float(countArray[i]) / float(nTransactions)) >= minValue:
                Ftemp.append(candidate)
                outputCountArray.append(countArray[i])

        # Order inside datasets
        for each in Ftemp:
            if len(each) == 1:
                each[0].sort()

        if (Ftemp):
            # Print the output in the required format
            output = 'The number of length ' + str(k + 1) + ' sequence is ' + str(len(Ftemp)) + '\n'
            outputFile.write(output)
            print('The number of length ', k + 1, ' sequence is ', len(Ftemp))
            for index, each in enumerate(Ftemp):
                value = str(each).replace('[', '', 1).replace('[', '<{').replace(']', '}>').replace('>, <', '').replace(
                    ' ', '')
                output = 'Pattern: ' + value[:-2] + ' :Count=' + str(outputCountArray[index]) + '\n'
                outputFile.write(output)
                print('Pattern:', value[:-2], ':Count=' + str(outputCountArray[index]))
            print()
            outputFile.write('\n')

        F.append(Ftemp)
        k += 1

    outputFile.close()