# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 15:48:31 2018

@author: Yash Kumar
"""

#a = "asd"
#print(a[1])
#a = ["dsvskdlvjsl","djksfbakjfa"]
#print(a[0][5])

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("mazeinput")
parser.add_argument("outputfeedback")
parser.add_argument("outputfile")


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
        


robot = constructor(args.mazeinput)

print(robot.maze, robot.types, robot.obstacles, robot.state)

with open(args.outputfile) as f:
    steps = [int(x) for x in f.read().strip().split()]

with open(args.outputfeedback,"w+") as f:
    for  action in steps:
        robot.state, end, reward = robot.step(action)
        f.write(str(robot.state[0])+" "+str(robot.state[1])+" "+str(reward)+" "+str(end)+"\n")