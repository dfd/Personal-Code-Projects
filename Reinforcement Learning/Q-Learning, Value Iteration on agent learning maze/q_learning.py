# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 17:34:24 2018

@author: Yash Kumar
"""
import random
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("mazeinput")
parser.add_argument("valuefile")
parser.add_argument("qvaluefile")
parser.add_argument("policyfile")
parser.add_argument("numep")
parser.add_argument("maxeplen")
parser.add_argument("lr")
parser.add_argument("df")
parser.add_argument("epsilon")

args = parser.parse_args()

class constructor:    
    def __init__(self, input_txt):
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
        self.maze = maze
        self.types = types
        self.obstacles = obstacles
        self.state = types["in_pt"]
#        return maze, types, obstacles

    def step(self, action):
        if self.state == self.types["end_pt"]:
            return self.state, 1, 0
        
        if action == 0:
            newstate = (self.state[0], self.state[1]-1)
        elif action == 1:
            newstate = (self.state[0]-1, self.state[1])
        elif action == 2:
            newstate = (self.state[0], self.state[1]+1)
        elif action == 3:
            newstate = (self.state[0]+1, self.state[1])
            
        if (newstate in self.obstacles) or not(0 <= newstate[0] < len(self.maze)) or not(0 <= newstate[1] < len(self.maze[0])):
            newstate = self.state
            
        if newstate == self.types["end_pt"]:
            is_terminal = 1
        else:
            is_terminal = 0
        return newstate, is_terminal, -1
    
    def reset(self):
        self.state = self.types["in_pt"]

robot = constructor(args.mazeinput) #'tiny_maze.txt'
maze = robot.maze
types = robot.types
state = robot.state



q = {}
for i in range(len(robot.maze)):
    for j in range(len(robot.maze[i])):
        if (i, j) not in robot.obstacles:
            q[(i, j)] = [0, 0, 0, 0]

def q_update(s, a, sdash, r, df, lr):
    qmax = q[sdash][q[sdash].index(max(q[sdash]))]
    q[s][a] = (1 - lr)*q[s][a] + lr*(r + df*qmax)


#q_update((1, 0), 0, (1, 0), -1, 0.9, 0.8)


num_ep = int(args.numep)
epsilon = float(args.epsilon)
df = float(args.df)
lr = float(args.lr)
max_length = int(args.maxeplen)

for i in range(num_ep):
    for length in range(max_length):
        act_prob = random.uniform(0, 1)
        actmaxindex = q[robot.state].index(max(q[robot.state]))
        act_possible = list(range(4))
        act_possible.pop(actmaxindex)
        if act_prob < epsilon:
            nextact = random.choice(act_possible)
        else:
            nextact = actmaxindex
        newst, termstate, reward = robot.step(nextact)
        q_update(robot.state, nextact, newst, reward, df, lr)
        robot.state = newst
        state = robot.state
        if termstate == 1:
            break
    robot.reset()
#a = list(range(4))
#a.pop(2)

vfile = {}
for key in q:
    vfile[key] = max(q[key])

policy = {}
for key in q:
    policy[key] = q[key].index(max(q[key]))
    
with open(args.policyfile,"w+") as f:
    for key in policy:
        f.write(str(key[0])+" "+str(key[1])+" "+str(policy[key])+"\n")
    
with open(args.valuefile,"w+") as f:
    for key in vfile:
        f.write(str(key[0])+" "+str(key[1])+" "+str(vfile[key])+"\n")

with open(args.qvaluefile,"w+") as f:
    for key in policy:
        for i in range(4):
            f.write(str(key[0])+" "+str(key[1])+" "+str(i)+" "+str(q[key][i])+"\n")  