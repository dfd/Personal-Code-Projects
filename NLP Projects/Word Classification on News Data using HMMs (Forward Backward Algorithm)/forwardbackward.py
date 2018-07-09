# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 10:28:40 2018

@author: Yash Kumar
"""

import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("testinput")
parser.add_argument("indextoword")
parser.add_argument("indextotag")
parser.add_argument("hmmprior")
parser.add_argument("hmmemit")
parser.add_argument("hmmtrans")
parser.add_argument("predictedfile")
args = parser.parse_args()

def txttomatrix(input_txt):
    f = open(input_txt)
    data = [l.strip() for l in f.readlines()]
#    print(data)
    a = []
    for i in range(len(data)):
        temp1 = data[i].split()
        a.append(temp1)
    new = np.empty((len(a),len(a[0])))
    for i in range(len(a)):
        for j in range(len(a[0])):
            new[i,j] = np.float64(a[i][j])
    return new

def txttoarray(input_txt):
    f = open(input_txt)
    data = [l.strip() for l in f.readlines()]
    a = []
    for i in range(len(data)):
        temp1 = data[i].split()
        a.append(temp1)
    new = np.empty(len(a[0]))
    for i in range(len(a[0])):
        new[i] = np.float64(a[0][i])
    return new    

in_prob = txttoarray(args.hmmprior)
tran_prob = txttomatrix(args.hmmtrans)
em_prob = txttomatrix(args.hmmemit)

def dicdata(input_txt):
    f = open(input_txt)
    data = [l.strip() for l in f.readlines()]
    dicword = {}
    for i,v in enumerate(data):
        dicword[v] = i
    return dicword, data

def trainmatrix(input_txt):
    f = open(input_txt)
    data = [l.strip() for l in f.readlines()]
    a = []
    for i in range(len(data)):
        temp1 = data[i].split(" ")
        a.append(temp1)
    return a

def split_stt(train_data):
    return [tuple(a.split("_"))[0] for a in train_data]

def split_lbl(train_data):
    return [tuple(a.split("_"))[1] for a in train_data]        

dic_labels, llabels = dicdata(args.indextotag)
dic_states, _ = dicdata(args.indextoword)

#train_data = trainmatrix("trainwords.txt")
#train_states = list(map(split_stt, train_data))
#train_labels = list(map(split_lbl, train_data))
        
test_data = trainmatrix(args.testinput)
test_states = list(map(split_stt, test_data))
test_labels = list(map(split_lbl, test_data))

def alpha(j, t, sentence, dic_a):
    if (j, t) in dic_a:
        return dic_a[(j, t)]
    elif t == 0:
        dic_a[(j, t)] = in_prob[j]*em_prob[j,dic_states[sentence[0]]]
        return dic_a[(j, t)]
    else:
        newsum = 0
        for k in range(len(dic_labels)):
            if (k, t-1) in dic_a:
                newsum += tran_prob[k,j]*dic_a[(k, t-1)]
            else:
                dic_a[(k, t-1)] = alpha(k, t-1, sentence, dic_a)
                newsum += tran_prob[k,j]*dic_a[(k, t-1)]
        dic_a[(j, t)] = newsum*em_prob[j,dic_states[sentence[t]]]
        return dic_a[(j, t)]
    
def beta(j, t, sentence, dic_b):
    if (j, t) in dic_b:
        return dic_b[(j, t)]
    elif t == len(sentence)-1:
        dic_b[(j, t)] = 1
        return 1
    else:
        newsum = 0
        for k in range(len(dic_labels)):
            if (k, t+1) in dic_b:
                newsum += em_prob[k, dic_states[sentence[t+1]]]*dic_b[(k, t+1)]*tran_prob[j,k]
            else:
                dic_b[(k, t+1)] = beta(k, t+1, sentence, dic_b)
                newsum += em_prob[k, dic_states[sentence[t+1]]]*dic_b[(k, t+1)]*tran_prob[j,k]
        dic_b[(j, t)] = newsum
        return dic_b[(j, t)]

def alphabeta(j, t, sentence, dic_a, dic_b):
#    dic_a = {}
#    dic_b = {}
    return alpha(j, t, sentence, dic_a)*beta(j, t, sentence, dic_b)

def argmax(t, sentence):
    dic_a = {}
    dic_b = {}
    args = []
    for j in range(len(dic_labels)):
        args.append(alphabeta(j, t, sentence, dic_a, dic_b))
    return llabels[args.index(max(args))]

def full_sentence(sentence):
    label = []
    for num in range(len(sentence)):
        label.append(argmax(num, sentence))
    return label

chk_labels = []
for i in range(len(test_states)):
    chk_labels.append(full_sentence(test_states[i]))
    
with open(args.predictedfile,"w+") as f:
    for counter in range(len(chk_labels)):
        for counter2 in range(len(chk_labels[counter])):
            f.write(str(test_states[counter][counter2])+"_"+str(chk_labels[counter][counter2])+" ")
        f.write("\n")