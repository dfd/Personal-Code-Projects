# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 09:52:06 2018

@author: Yash Kumar
"""

#a = "asd"
#print(a[1])
#a = ["dsvskdlvjsl","djksfbakjfa"]
#print(a[0][5])

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("mazeinput")
parser.add_argument("valuefile")
parser.add_argument("qvaluefile")
parser.add_argument("policyfile")
parser.add_argument("numep")
parser.add_argument("df")

args = parser.parse_args()


def createmaze(input_txt):        
    with open(input_txt) as f:
        maze = [l.strip() for l in f.readlines()]
        types = {}
        obstacles = set([])
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j] == "S":
                    types["in_pt"] = (i, j)
                elif maze[i][j] == "*":
                    obstacles.update({(i, j)})
                elif maze[i][j] == "G":
                    types["end_pt"] = (i, j)
    #    types["obstacles"] = obstacles
    return maze, types, obstacles

maze, types, obstacles = createmaze(args.mazeinput)


def step(state, action):
    if state == types["end_pt"]:
        return state, 1, 0
    
    if action == 0:
        newstate = (state[0], state[1]-1)
    elif action == 1:
        newstate = (state[0]-1, state[1])
    elif action == 2:
        newstate = (state[0], state[1]+1)
    elif action == 3:
        newstate = (state[0]+1, state[1])
        
    if (newstate in obstacles) or not(0 <= newstate[0] < len(maze)) or not(0 <= newstate[1] < len(maze[0])):
        newstate = state
        
    if newstate == types["end_pt"]:
        is_terminal = 1
    else:
        is_terminal = 0
        
    return newstate, is_terminal, -1

q = {}
for i in range(len(maze)):
    for j in range(len(maze[i])):
        if (i, j) not in obstacles:
            q[(i, j)] = [0, 0, 0, 0]
            
V = {}
for i in range(len(maze)):
    for j in range(len(maze[i])):
        if (i, j) not in obstacles:
            V[(i, j)] = 0
            
num_epoch = int(args.numep)
df = float(args.df)

for epoch in range(num_epoch):
    for key in q:
        for action in range(4):
            state = key
            newstate, termstate, reward = step(state, action)
            q[state][action] = reward + df*V[newstate]
    for qqq in V:
        V[qqq] = max(q[qqq])

policy = {}
for key in q:
    policy[key] = q[key].index(max(q[key]))
    
with open(args.policyfile,"w+") as f:
    for key in policy:
        f.write(str(key[0])+" "+str(key[1])+" "+str(policy[key])+"\n")

    
with open(args.valuefile,"w+") as f:
    for key in V:
        f.write(str(key[0])+" "+str(key[1])+" "+str(V[key])+"\n")


with open(args.qvaluefile,"w+") as f:
    for key in policy:
        for i in range(4):
            f.write(str(key[0])+" "+str(key[1])+" "+str(i)+" "+str(q[key][i])+"\n")          