##################################################
## Author: Cheng-Yen Yang (1968990)
## Email: cycyang@uw.edu
## Course: EE 562 (Autumn 2020)
## Assignment: Assignment 2
##################################################
import math
from collections import OrderedDict 


# dis() util function return distance of two Point object p1 and p2
def dis(p1, p2):
    return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

# intersect() util function return whether Line(p1,p2) and Line(p3,p4) 
# intersect or not.
# The idea was developed from the reference:
#   - https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def intersect(p1, p2, p3, p4):
    if not (min(p1.x, p2.x) < max(p3.x, p4.x) and \
            min(p3.y, p4.y) < max(p1.y, p2.y) and \
            min(p3.x, p4.x) < max(p1.x, p2.x) and \
            min(p1.y, p2.y) < max(p3.y, p4.y)):
        return False
    elif ((p3.y - p1.y) * (p2.x - p1.x) - (p3.x - p1.x) * (p2.y - p1.y)) * ((p4.y - p1.y) * (p2.x - p1.x) - (p4.x - p1.x) * (p2.y - p1.y)) > 0:
        return False
    return True

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '({},{})'.format(self.x, self.y)

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y

    def __hash__(self):
        return hash((self.x, self.y))

# Each state contains at least the following:
#   - the coordinates of a point
#   - the g-value cost of the path from the initial state to this state
#   - the h-value that estimates the cost from this state to the goal
#   - the f-value that is the sum of these two
#   - a list of the successors of this state (will be empty till the state is expanded)
#   - the parent state
class State(object):
    def __init__(self, point, g, h, children, parent):
        self.point = point 
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.children = children
        self.parent = parent

    def __repr__(self):
        return '({},{},{},{},{})'.format(self.point, self.g, self.h, self.children, self.parent)


# aStarSearch is a object that take the txt file as input and run a-star search with following processes:
# 0) Initialize all member object (e.g., open list and close list)
# 1) Parse the txt file (e.g., starting point, ending point, obstacle locations)
# 2) Run a-star search
# 3) Print the corresponding output in desired format
# The idea was developed from the reference:
#   - https://www.geeksforgeeks.org/a-search-algorithm/
#   - https://homes.cs.washington.edu/~shapiro/EE562/hw2/index.html
class aStarSearch(object):
    def __init__(self, fname, verbose=False):
        self.fname = fname
        self.verbose = verbose

        self.obstacles = []
        self.paths = []

        self.vertices = set()
        self.obstacles = []
        self.open_list = OrderedDict()
        self.close_list = OrderedDict()

        self.parse()
        self.search()
        self.print()
    
    # member function parse() parses the txt file into member objects
    def parse(self):
        with open(self.fname, 'r') as f:
            lines = f.read().splitlines()
            start_state_line = [int(x) for x in lines[0].split(' ')]
            self.start_point = Point(start_state_line[0], start_state_line[1])
            goal_state_line = [int(x) for x in lines[1].split(' ')]
            self.goal_point = Point(goal_state_line[0], goal_state_line[1])
            self.num_obstacle = int(lines[2])

            for obstacle_line in lines[3:]:
                self.obstacles.append([])
                obstacle_line = [int(x) for x in obstacle_line.split(' ')]
                obstacle_points = zip(obstacle_line[0::2], obstacle_line[1::2])
                for x,y in obstacle_points:
                    self.vertices.add(Point(x,y))
                    self.obstacles[-1].append(Point(x,y))
        if self.verbose:
            print(self.vertices)

    # member function check() helps validate if the move is valid or not
    def check(self, p1, p2):
        for obstacle in self.obstacles:
            if intersect(p1, p2, obstacle[0], obstacle[2]):
                return False
            if intersect(p1, p2, obstacle[1], obstacle[3]):
                return False
        return True

    # member function search() deals with a-star search algorithm
    def search(self):
        self.open_list[self.start_point] = State(self.start_point, 0, dis(self.start_point, self.goal_point), [], self.start_point)

        while self.open_list:
            
            curr_point, curr_state = self.open_list.popitem(last=False)
            self.close_list[curr_point] = curr_state

            if curr_state.point == self.goal_point:
                break

            for next_point in self.vertices:
                if next_point == curr_point:
                    continue
                # if the line(curr_point, next_point) did not intersect any obstacles
                if self.check(curr_point, next_point):
                    curr_state.children.append(next_point)
                    next_g = curr_state.g + dis(curr_point, next_point)
                    next_h = dis(next_point, self.goal_point) # the same
                    # if the next_point in open list, we compare next_g and original_g
                    # to see if any update is required
                    if next_point in self.open_list:
                        if self.open_list[next_point].g > next_g:
                            self.open_list[next_point].g = next_g
                            self.open_list[next_point].h = next_h
                            self.open_list[next_point].parent = curr_state.point
                    # if the next_point in close list, we also compare next_g and original_g
                    # to see if any update is required, also need to put it back into open list
                    # if there is an update 
                    elif next_point in self.close_list:
                        if self.close_list[next_point].g > next_g:
                            self.close_list[next_point].g = next_g
                            self.close_list[next_point].h = next_h
                            self.close_list[next_point].parent = curr_state.point
                            self.open_list[next_point] = self.close_list[next_point]
                            del self.close_list[next_point] # remove from the close list
                    # if the next_point is neither in open list or close list, put it into open list
                    else:
                        self.open_list[next_point] = State(next_point, next_g, next_h, [], curr_point) 
            
            # sort the open list base on the f value (g value + h value) for each state
            self.open_list = OrderedDict(sorted(self.open_list.items(), key=lambda x: x[1].g+x[1].h))

            # debug messages
            if self.verbose:
                print('============================================================')
                print('Current State', curr_state)
                print('Open List:', self.open_list.keys())
                print('Close List:', self.close_list.keys())
                print('============================================================')
        
        curr_state = self.close_list[self.goal_point]
        while curr_state.point != self.start_point:
            self.paths.append(curr_state)
            curr_state = self.close_list[self.close_list[curr_state.point].parent]
        self.paths.append(curr_state)

    # member function print() prints the paths of optimal solution
    def print(self):
        self.paths.reverse()
        print('Point\t Cumulative Cost')
        for state in self.paths:
            print('{}\t {}'.format(state.point, state.g))
        

def run_simple():
    aStarSearch('data1.txt', verbose=False)

def run_difficult():
    aStarSearch('data2.txt', verbose=False)

def run_mine():
    aStarSearch('data3.txt', verbose=False)


if __name__ == '__main__':
    run_simple()
    run_difficult()
    run_mine()