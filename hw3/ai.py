##################################################
## Author: Cheng-Yen Yang (1968990)
## Email: cycyang@uw.edu
## Course: EE 562 (Autumn 2020)
## Assignment: Assignment 3
##################################################

import time
import random 
import io

# import numpy as np

class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"

class ai:
    def __init__(self):
        self.depth = 10     # search depth of the minmaxSearch algorithm
        self.alpha = 0.8    # scaling factor of the advanced method

        self.time_record = [[] for _ in range(10)] # use to get average search time for record
        
    class state:
        def __init__(self, a, b, a_fin, b_fin):
            self.a = a
            self.b = b
            self.a_fin = a_fin
            self.b_fin = b_fin
            # use to memorize the move that can maximize the herustic value
            self.path = {}

        def __repr__(self):
                return '{}, {}, {}, {}\n'.format(
                    self.a, self.a_fin, self.b, self.b_fin
                )

        def __eq__(self, other):
            return self.a == other.a and self.b == other.b and \
                self.a_fin == other.a_fin and self.b_fin == other.b_fin

    # Kalah:
    #         b[5]  b[4]  b[3]  b[2]  b[1]  b[0]
    # b_fin                                         a_fin
    #         a[0]  a[1]  a[2]  a[3]  a[4]  a[5]
    # Main function call:
    # Input:
    # a: a[5] array storing the stones in your holes
    # b: b[5] array storing the stones in opponent's holes
    # a_fin: Your scoring hole (Kalah)
    # b_fin: Opponent's scoring hole (Kalah)
    # t: search time limit (ms)
    # a always moves first
    #
    # Return:
    # You should return a value 0-5 number indicating your move, with search time limitation given as parameter
    # If you are eligible for a second move, just neglect. The framework will call this function again
    # You need to design your heuristics.
    # You must use minimax search with alpha-beta pruning as the basic algorithm
    # use timer to limit search, for example:
    # start = time.time()
    # end = time.time()
    # elapsed_time = end - start
    # if elapsed_time * 1000 >= t:
    #    return result immediately 
    def move(self, a, b, a_fin, b_fin, t):
        #For test only: return a random move
        # r = []
        # for i in range(6):
        #     if a[i] != 0:
        #         r.append(i)
        # # To test the execution time, use time and file modules
        # # In your experiments, you can try different depth, for example:
        # f = open('time.txt', 'a') #append to time.txt so that you can see running time for all moves.
        # # Make sure to clean the file before each of your experiment
        # for d in [3, 5, 7]: #You should try more
        #     f.write('depth = '+str(d)+'\n')
        #     t_start = time.time()
        #     self.minimax(depth = d)
        #     f.write(str(time.time()-t_start)+'\n')
        # f.close()
        # return r[random.randint(0, len(r)-1)]
        # #But remember in your final version you should choose only one depth according to your CPU speed (TA's is 2.0GHz)
        # #and remove timing code. 
        
        #Comment all the code above and start your code here
        # f = open('time.txt', 'a')
        # for d in [1,2,3,4,5,6,7,8,9,10]:
        #     self.depth = d
        #     f.write('depth = '+str(d)+'\n')
        #     curr_state = self.state(a, b, a_fin, b_fin)
        #     t_start = time.time()
        #     val = self.minmaxSearch(curr_state, float('-inf'), float('inf'), 0)
        #     for key in curr_state.path:
        #         if curr_state.path[key] == val:
        #             action = key
        #     search_time = time.time()-t_start
        #     self.time_record[d-1].append(search_time)
        #     f.write(str(search_time)+'\n')
        
        # for d in [1,2,3,4,5,6,7,8,9,10]:
        #     f.write('depth= ' + str(d) + ': ' + str(sum(self.time_record[d-1])/len(self.time_record[d-1])) + '+/-' + str(np.std(self.time_record[d-1])) + '\n')

        curr_state = self.state(a, b, a_fin, b_fin)
        val = self.minmaxSearch(curr_state, float('-inf'), float('inf'), 0)
        for key in curr_state.path:
            if curr_state.path[key] == val:
                action = key

        return action

    def h(self, state, method='naive'):
        '''
        Calculates and returns the heuristic value for the current state.

        Keyword arguments:
            state (State) - the current state
            method (string) - 'naive' or 'advanced' method for different heuristic function

        Returns:
            value (float) - the heuristic value
        '''
        if method == 'naive':
            return state.a_fin - state.b_fin
        if method == 'advanced':
            return self.alpha * (state.a_fin - state) - (1-self.alpha) * (sum(state.a) - sum(state.b))

    def getNextState(self, state, move):
        '''
        Returns the next state with a given move on the holes. 
        Code were mainly reference from the updateLocalState() function in main.py.

        Keyword arguments:
            state (State) - the current state
            move (int) - the hole player select to move

        Returns:
            next_state (State) - the next state after the move
        '''

        # not a valid move if no stone in the selected hole (move)
        if state.a[move] == 0:
            return 
        
        # Rearrange the Kalah board from a, b, a_fin and b_fin from the state for easier 
        # implementation of the "action" of each turn.
        # Kalah Board:
        #             b[5]  b[4]  b[3]  b[2]  b[1]  b[0]
        #   b_fin                                         a_fin
        #             a[0]  a[1]  a[2]  a[3]  a[4]  a[5]
        # Kalah 1-D Board:
        #        a[move:] + a_fin + b + a[:move]
        ao = state.a[:]
        
        board = state.a[move:] + [state.a_fin] + state.b + state.a[:move]
        count = state.a[move]
        board[0] = 0
        p = 1

        while count > 0:
            board[p] += 1
            p = (p+1) % 13
            count -= 1
        
        a_fin = board[6-move]
        b_fin = state.b_fin
        a = board[13-move:] + board[:6-move]
        b = board[7-move:13-move]
        cagain = bool()
        ceat = False

        p = (p-1) % 13
        if p == 6 - move:
            cagain = True
        if p <= 5 - move and ao[move] < 14:
            id = p + move
            if (ao[id] == 0 or p % 13 == 0) and b[5 - id] > 0:
                ceat = True
        elif p >= 14 - move and ao[move] < 14:
            id = p + move - 13
            if (ao[id] == 0 or p % 13 == 0) and b[5 - id] > 0:
                ceat = True
        
        if ceat:
            a_fin += a[id] + b[5-id]
            b[5-id] = 0
            a[id] = 0

        if sum(a) == 0:
            b_fin += sum(b)
        if sum(b) == 0:
            a_fin += sum(a)

        return self.state(a,b,a_fin,b_fin)

    def getSuccessors(self, state):
        '''
        Returns a dictionary the record all the successors of the state.

        Keyword arguments:
            state (State) - the current state

        Returns:
            successors (dict) - dictionary of all the successors with key being moves
        '''
        successors = {}
        for move in range(6):
            if self.getNextState(state, move):
                successors[move] = self.getNextState(state, move)
        
        return successors


    # min-max search algorithm with alpha-beta pruning
    # it will return the maximum/minimum heuristic value from the current state
    def minmaxSearch(self, state, alpha, beta, depth, parent_move=None, maxx=True):
        '''
        Min-max search algorithm with alpha-beta pruning implementation.

        Keyword arguments:
            state (State) - the current state
            alpha (float) - alpha value for alpha-beta pruning
            beta (float) - beta value for alpha-beta pruning
            deoth (int) - the current search depth
            maxx (bool) - boolean value to determine min or max serach for the current search

        Returns:
            val (float) - the maximum/minimum heuristic value
        '''

        # return the herusitic value if reach maximum search depth or terminal states
        if depth == self.depth or state.a_fin > 36 or state.b_fin > 36 \
            or (state.a_fin == 36 and state.b_fin == 36):
            return self.h(state, method='naive')

        val = float('-inf') if maxx else float('inf')

        for move, next_state in self.getSuccessors(state).items():
            if not parent_move:
                parent_move = move
            if maxx:
                val = max(val, self.minmaxSearch(next_state, alpha, beta, depth+1, parent_move, False))
                state.path[move] = val
                # state.path[parent_move] = val
                if val >= beta:
                    return val
                alpha = max(alpha, val)
            else:
                val = min(val, self.minmaxSearch(next_state, alpha, beta, depth+1, parent_move, True))
                if val <= alpha:
                    return val
                beta = min(beta, val)

        return val
