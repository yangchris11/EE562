##################################################
## Author: Cheng-Yen Yang (1968990)
## Email: cycyang@uw.edu
## Course: EE 562 (Autumn 2020)
## Assignment: Assignment 1
##################################################


# State is a object that can represent a state of the numbers of missionaries, cannibals,
# and the location or side of the boat. 
# The idea was developed from the reference:
#       - https://en.wikipedia.org/wiki/Missionaries_and_cannibals_problem
class State(object):
    def __init__(self, n_mis, n_can, dirc):
        self.n_mis = n_mis
        self.n_can = n_can
        self.dirc = dirc

    # __str__ method return string representing the summary of the states
    # e.g., (3,3,L), (3,1,R), (3,2,L), ..., (0,0,R)
    def __str__(self):
        if self.dirc:
            return '({},{},L)'.format(self.n_mis, self.n_can)
        else:
            return '({},{},R)'.format(self.n_mis, self.n_can)    

    # __eq__ method help compares whether two states are identical
    def __eq__(self, other):
        if self.n_mis == other.n_mis and self.n_can == other.n_can and self.dirc == other.dirc:
            return True
        else:
            return False

    # __hash__ method turns the state into hashable object (tuple)
    def __hash__(self):
        return hash((self.n_mis, self.n_can, self.dirc))

    # valid method helps filter out the illegal state such as:
    #       - n_mis or n_can < 0
    #       - n_mis or n_can > 3
    #       - n_can > n_mis while n_mis != 0 on either side of the river 
    def valid(self):
        if self.n_mis < 0 or self.n_can < 0 or self.n_mis > 3 or self.n_can > 3:
            return False
        elif self.n_mis and self.n_mis < self.n_can:
            return False
        elif 3 - self.n_mis and (3 - self.n_mis) < (3 - self.n_can):
            return False
        return True

    # transit method helps generate the next state base on the pass-in argument action
    # and the current dirc (location of the boat) then return it
    def transit(self, action):
        if self.dirc:
            return State(self.n_mis-action[0], self.n_can-action[1], self.dirc-action[2])
        else:
            return State(self.n_mis+action[0], self.n_can+action[1], self.dirc+action[2])


# The five possible actions (⟨1,0,1⟩, ⟨2,0,1⟩, ⟨0,1,1⟩, ⟨0,2,1⟩, and ⟨1,1,1⟩) are then 
# subtracted from the previous state, with the resulted state become 
actions = [
    (0, 1, 1),
    (1, 0, 1),
    (2, 0, 1),
    (1, 1 ,1),
    (0, 2, 1)
]

# The two states: initial_state and terminate state, are use to start our seach and
# determine when to stop.
initial_state = State(3,3,1)            # (3,3,L)
terminate_state = State(0,0,0)          # (0,0,R)

# The three different global counters: illegal_cnt, repeated_cnt and total_cnt 
# keep tracks of the different states searched to find each solution.
# The three kinds of states are described as:
#       - illegal states in which the cannibals eat the missionaries,
#       - repeated states that are the same as an ancestor state on the same path,
#       - total states searched (ie. all states except the illegal and repeated ones).
illegal_cnt = 0
repeated_cnt = 0
total_cnt = 0

# Recursive depth-first search that takes the current state and all previous states 
# as arguments then traversal down the states search tree.
def dfs(current_state, prev_states):

    global illegal_cnt, repeated_cnt, total_cnt
    
    if current_state == terminate_state:
        total_cnt += 1
        print('Solution:')
        for state in prev_states:
            print(state)
        print(current_state)
        return
    
    elif current_state in prev_states:
        repeated_cnt += 1
        return

    elif not current_state.valid():
        illegal_cnt += 1
        return

    else:
        total_cnt += 1
        for action in actions:
            dfs(current_state.transit(action), prev_states+[current_state])

    
def run():
    dfs(initial_state, [])
    print('totals {} illegals {} repeats {}'.format(total_cnt, illegal_cnt, repeated_cnt))


if __name__ == '__main__':
    run()