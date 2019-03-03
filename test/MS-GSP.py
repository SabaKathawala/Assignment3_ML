import operator
import copy
from Level2_candidate_gen_SPM import candidateGenLevel2, verifySubset, checkSDC
from MSCandidate_gen_SPM import candidateGen, smallestMS, MSseqFirst, MSseqLast, subseq1NormalJoin, subseq2, lItemSet, lengthSizeS1, createSubset, checkSubsetLevel3, checkSDC

#Function to calculate minsup and check if it satisfies for all elements
def supCalc(S, C, index, count):
    countArray = []
    for j, value in enumerate(C):
        count = 0
        for transaction in S:
            subsetCount = verifySubset(value, transaction, index=0, count=0)
            if subsetCount:
                count += 1
        #Prune
        countArray.append(count)
    return countArray

#Function to create subsequence of s1. Drop second item of s1
def subseq1(seq):
    for index, each in enumerate(seq):
        if len(each) != 1:
            seq[0].remove(each[1])
            break
        else:
            if len(seq[index + 1]) != 1:
                seq[index + 1].remove(seq[index + 1][0])
                break
            else:
                seq.remove(seq[index + 1])
                break

    return seq

#Function to return last item in a sequence
def lastItem(seq):
    for each in seq:
        if len(seq) == 1:
            lastItem = each[-1]
            break
        else:
            if len(seq[-1]) == 1:
                lastItem = seq[-1][0]
                break
            else:
                lastItem = seq[-1][-1]
                break

    return lastItem

#Function to remove second last item from S2
def subSeqSecondLastItem(seq):
    if len(seq) == 1:
        seq[0].remove(seq[0][-2])
    else:
        if len(seq[-1]) == 1:
            if len(seq[-2]) != 1:
                seq[-2].remove(seq[-2][-1])
            else:
                seq.remove(seq[-2])
        else:
            seq[-1].remove(seq[-1][-2])
    return seq

#Function to calculate support for level 3 and above
def supCalcLevel3(S, C, index, count):
    countArray = []
    for j, value in enumerate(C):
        count = 0
        for transaction in S:
            subsetCount = verifySubset(value, transaction, index=0, count=0)
            if subsetCount:
                count += 1
        # Prune
        countArray.append(count)
    return countArray

#Function to read the input files - data.txt and para.txt
def readFile(path):
    fr = open(path, 'r')
    return fr.readlines()

import fileHelper

if __name__ == '__main__':

    # Preprocessing
    # get data form file
    S = fileHelper.getData('data-1.txt')  # set of all items and sequence database S

    # get MIS and SDC values from file
    MS, sdc = fileHelper.getParamaters('para1-1.txt')

    sortedMS = sorted(MS.items(), key=operator.itemgetter(1))

    #Initializing the L array
    L = []
    for each in sortedMS:
        L.append(each[0])

    #Check minsup
    F = []
    F1 = []
    nTransactions = len(S)
    countArray = []
    for key in L:
        count = 0
        for transaction in S:
            for seq in transaction:
                flag = False
                if key in seq:
                    count += 1
                    flag = True
                    break

        #If support is greater than minsup
        support = float(count) / float(nTransactions)
        if support >= MS[key]:
            countArray.append(count)
            F1.append(key)

    #Frequent candidates array
    F.append(F1)

    outputFile = open('output.txt', 'w')
    #Printing the output in the required format
    output = ('The number of length 1 Frequent Sequence is ' + str(len(F[0])) + '\n')
    outputFile.write(output)
    for index, each in enumerate(F[0]):
        output = '<{' + str(each) + '}> count: ' + str(countArray[index]) + '\n'
        print('<{' + str(each) + '}> count:', countArray[index])
        outputFile.write(output)
    print()
    outputFile.write('\n')

    k = 1
    C = []
    while F[-1]:
        if k == 1:
            C.append(candidateGenLevel2(L, S, MS, sdc))
            countArray = supCalc(S, C[-1], index=0, count=0)
        else:
            C.append(candidateGen(F[-1], S, MS, sdc))
            countArray = supCalcLevel3(S, C[-1], index=0, count=0)

        #Calculates if each sequence satisfies minimum support; c.count/n > MIS(c.minMISItem)
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

        #Ordering the inside datasets
        for each in Ftemp:
            if len(each) == 1:
                each[0].sort()

        #Printing the output to the output.txt file
        if (Ftemp):
            output = 'The number of length ' + str(k + 1) + ' Frequent Sequence is ' + str(len(Ftemp)) + '\n'
            outputFile.write(output)
            print('The number of length ', k + 1, ' Frequent Sequence is ', len(Ftemp))
            for index, each in enumerate(Ftemp):
                value = str(each).replace('[', '', 1).replace('[', '<{').replace(']', '}>').replace('>, <', '').replace(
                    ' ', '')
                output = value[:-2] + ' count: ' + str(outputCountArray[index]) + '\n'
                outputFile.write(output) 
                print(value[:-2], 'count: ' + str(outputCountArray[index]))
            print()
            outputFile.write('\n')

        F.append(Ftemp)
        k += 1

    outputFile.close()