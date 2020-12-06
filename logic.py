#15000 emails
#TrainingData = 10000 
#TestingData = 5000 

import collections
import numpy.matlib 
import numpy as np 

f1 = open("trainingData_data.txt", "r")
contents =f1.readlines()
trainingData = []
testingData = []
isSpam = []

for i in range(len(contents)):
    if i < 10000:
        trainingData.append(contents[i])
    else:
        testingData.append(contents[i])

   
def getUnusedVocab():
    unusedVocab = set()
    vocab = GenerateDictionaries()[1]
    for word in vocab: 
        if vocab[word] >= 30:
            unusedVocab.add(word)
    return unusedVocab
    

def GenerateDictionaries(): 
    allDict = list() # Get  list of dictionaries for each email
    vocab = collections.Counter() # Get total dictionary for all words
    for email in trainingData:
        emailDict = dict()
        split = email.split()
        for i in range(len(split)):
            if i == 0:
                if split[i] == "0": # not spam
                    isSpam.append(-1)
                else:
                    isSpam.append(1)
                continue
            if split[i] not in emailDict: #if we have not already seen it before
                vocab[split[i]] += 1
                emailDict[split[i]] = 1
            else: 
                emailDict[split[i]] += 1
        allDict.append(emailDict)
    return allDict, vocab 

#build vocabulary list
def BuildVocabVectors():
    #ignore all words that appear in fewer than 30 emails
    allDict = GenerateDictionaries()[0]
    unusedVocab = getUnusedVocab()
    
    #make the dictionaries for each email
    featureVectors = []
    for email in allDict:
        emailVector = []
        for word in unusedVocab:
            if word in email:
                emailVector.append(1)
            else:
                emailVector.append(0)
        # print(emailVector)
        featureVectors.append(np.array(emailVector))

    return unusedVocab, np.array(featureVectors)
        
        

# def emailVector(notIgnoredSet):
    # make dictionary of each word in notIgnoredSet and then check if its in the individual email 

    #for each 

def train_perceptron():
    unusedVocab, featureVectors = BuildVocabVectors()
    w = np.zeros(len(unusedVocab))
    print(len(featureVectors))
    # keep updating until the weight does not need to be modified
    
    numMistakes = 0
    numUpdates = 0
    numIterations = 0
    while (True):
        numIterations += 1
        numUpdates = 0
        for i in range(len(featureVectors)):
            dot = np.dot(w, featureVectors[i])
            if dot == 0: 
                dot = 1
            # check for sign agreement
            sign = isSpam[i] * dot
            if sign <= 0: 
                numMistakes += 1
                numUpdates += 1
            #modify weight accordingly
                w = np.add(w, np.multiply(isSpam[i],featureVectors[i]))
        if numUpdates == 0:
            break

    # return the number of mistakes, the number of iterations and the weight array
    return w, numMistakes, numIterations

def test_perceptron(w, data):
    print("hiiii")
    dataIsSpam = [] # saves the spam values for the data given as parameter
    dataDict = list()
    for email in data:
        emailDict = dict()
        split = email.split()
        for i in range(len(split)): #iterating over each word
            if i == 0:
                if split[i] == "0": # not spam
                    dataIsSpam.append(-1)
                else:
                    dataIsSpam.append(1)
                continue
            if split[i] not in emailDict: #if we have not already seen it before
                emailDict[split[i]] = 1
            else: 
                emailDict[split[i]] += 1
        dataDict.append(emailDict)
    
    unusedVocab = BuildVocabVectors()[0]
    featureVectors = []
    print("wop")
    for email in dataDict:
        emailVector = []
        for word in unusedVocab:
            if word in email:
                emailVector.append(1)
            else:
                emailVector.append(0)
        # print(emailVector)
        featureVectors.append(np.array(emailVector))
    
    numMistakes = 0
    numIterations = 0
    print("oh hi")
    for i in range(len(featureVectors)):
        dot = np.dot(w, featureVectors[i])
        if dot == 0: 
            dot = 1
        # check for sign agreement
        sign = isSpam[i] * dot
        if sign <= 0: 
            numMistakes += 1
        numIterations += 1
    print(numMistakes)
    print(numIterations)
    return numMistakes/numIterations
    
    
w, numMistakes, numIterations = train_perceptron()

print(w, numMistakes, numIterations)
print(test_perceptron(w, trainingData))
print(test_perceptron(w, testingData))
