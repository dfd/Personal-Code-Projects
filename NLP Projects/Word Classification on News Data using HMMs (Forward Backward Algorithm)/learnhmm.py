# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 09:52:22 2018

@author: Yash Kumar
"""

import numpy as np

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("traininput")
parser.add_argument("indextoword")
parser.add_argument("indextotag")
parser.add_argument("hmmprior")
parser.add_argument("hmmemit")
parser.add_argument("hmmtrans")
args = parser.parse_args()

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
        temp1 = data[i].split()
        a.append(temp1)
    return a

def split_stt(train_data):
    return [tuple(a.split("_"))[0] for a in train_data]

def split_lbl(train_data):
    return [tuple(a.split("_"))[1] for a in train_data]

dic_labels, llabels = dicdata(args.indextotag)
dic_states, _ = dicdata(args.indextoword)

train_data = trainmatrix(args.traininput)
train_states = list(map(split_stt, train_data))
train_labels = list(map(split_lbl, train_data))

in_prob = np.zeros(len(dic_labels))
tran_prob = np.zeros((len(dic_labels),len(dic_labels)))
em_prob = np.zeros((len(dic_labels),len(dic_states)))

for i in range(len(train_labels)):
    in_prob[dic_labels[train_labels[i][0]]]+=1
in_prob = (in_prob+1)/(sum(in_prob)+len(in_prob))

for i in range(len(train_labels)):
    for j in range(len(train_labels[i])-1):
        tran_prob[dic_labels[train_labels[i][j+1]],dic_labels[train_labels[i][j]]]+=1
#tran_prob = tran_prob.T

for i in range(len(dic_labels)):
    tran_prob[:,i] = (tran_prob[:,i]+1)/(sum(tran_prob[:,i])+len(dic_labels))
tran_prob = tran_prob.T

for i in range(len(train_labels)):
    for j in range(len(train_labels[i])):
        em_prob[dic_labels[train_labels[i][j]],dic_states[train_states[i][j]]]+=1
        
for i in range(len(dic_labels)):
    em_prob[i,:] = (em_prob[i,:]+1)/(sum(em_prob[i,:])+len(dic_states))

with open(args.hmmprior,"w+") as f:
    for counter in range(len(in_prob)):
        f.write(str(in_prob[counter])+" ")
        
with open(args.hmmtrans,"w+") as f:
    for counter in range(len(tran_prob)):
        for counter2 in range(len(tran_prob[counter])):
            f.write(str(tran_prob[counter,counter2])+" ")
        f.write("\n")
        
with open(args.hmmemit,"w+") as f:
    for counter in range(len(em_prob)):
        for counter2 in range(len(em_prob[counter])):
            f.write(str(em_prob[counter,counter2])+" ")
        f.write("\n")