import numpy as np
from numpy.lib.function_base import append
import pandas as pd
from tkinter import *
import math
import time 
import os

from numpy.core.fromnumeric import size
from pandas.core.arrays.sparse import dtype

size_of_board = 600
"""
initialization of sudoku class based on Tic-Toc-Toe game from 

MIT License
Copyright (c) 2020 Aqeel Anwar
https://github.com/aqeelanwar/Tic-Tac-Toe

"""
class sudoku():
    def __init__(self):
        self.window = Tk()
        self.window.title('')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        # Input from user in form of clicks
        #self.window.bind('<Button-1>', self.click)
    
    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(9):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)

        for i in range(9):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)


def convert_df(row):
    #print(row)
    quiz = row[0]
    ans = row[1]
    board = np.zeros((9,9), dtype=int)
    solved_board = np.zeros((9,9), dtype=int)

    for i in range(0,9):
        for j in range (0,9):
            board[i][j] = quiz[9*i + j]

    for i in range(0,9):
        for j in range (0,9):
            solved_board[i][j] = ans[9*i + j]
    
    return board, solved_board

def init_solve(board, solved_board):
    init_board = np.copy(board)
    #print(board)
    has_changed = True
    while(has_changed):
        has_changed= False
        for col in range(0,9):
            for row in range(0,9):
                if( board[row][col] == 0):
                    #print("solving cell vale at",board[row][col],"at [",row,",",col,"]") 
                    if(solveCell(board, row,col)): has_changed=True
            
    #print(init_board)
    #print(board)
    if(np.array_equal(init_board, board)): 
        
        return False
    if(np.array_equal(board, solved_board)): 
        
        return True
    #print(board)
    #print(solved_board)

def checkCell(board, row, col):
    if(board[row][col] != 0):
        print("Already Solved!", board[row][col],"at [",row,",",col,"]")
        return True
    #print("Stack" ,checkStack(col))
    #print("Band ", checkBand(row))
    #print("Square" ,checkSquare(findSquare(row,col)))
    return False


def solveCell(board, row, col):
    #print("Row: ", row, " Col: ", col)
    #if(checkCell(row, col)): return False
    band = checkBand(board, row)
    if(size(band) == 1):
        #print("Solved!", band[0],"at [",row,",",col,"]")
        #print("solved band")
        board[row][col] = band[0]
        return True
    stack = checkStack(board, col)
    if(size(stack) == 1):
        #print("Solved!", stack[0], "at [",row,",",col,"]")
        #print("solved stack")
        board[row][col] = stack[0]
        return True
    square = checkSquare(findSquare(board, row,col))
    if(size(square) == 1):
        #print("Solved: ", square[0], "at [",row,",",col,"]")
        #print("solved square")
        board[row][col] = square[0]
        return True

    all_possible = []
    all_possible = [x for x in band if x in band and x in stack and x in square]
    #print(all_possible)
    if(size(all_possible) == 1):
        #print("Solved using reduction", all_possible[0], "at [",row,",",col,"]")
        board[row][col] = all_possible[0]
        return True
    elif(size(all_possible) == 0):
        print("ERROR: NO POSSIBLE: ", all_possible, "at [",row,",",col,"]")
        print(board)
    else:
        return False


def checkStack(board, col):
    column = board[:,col]
    possible = []
    #print("stack", col)
    for i in range(1,10):
        if(checkArrayVal(column, i)):
            #print("Appending  ",i)
            possible.append(i)
    return possible

def checkBand(board, row):
    ro = board[row]
    #print("Band:")
    #print(ro)
    possible = []
    for i in range(1,10):
        if(checkArrayVal(ro, i)):
            #print("Appending  ",i)
            possible.append(i)
    return possible

def checkArrayVal(arr, val):
    #print("array", arr)
    for i, x in np.ndenumerate(arr):
        #print("comparing ", str(x) , " ", val, " at ", i)
        if x == val:
            return False

    return True

def findSquare(board, row, col):
    row = math.floor((row)/3)
    col = math.floor((col)/3)
    if(row == 1): row = 3
    elif(row == 2): row = 6
    else: row = 0
    if(col == 1): col = 3
    elif(col == 2): col = 6
    else: col = 0
    square = board[row:row+3,col:col+3]
    return square


def checkSquare(square):
    #print(square)
    possible = []
    for i in range(1,10):
        if(checkSquareVal(square, i)):
            #print("Appending  ",i)
            possible.append(i)
    return possible

def checkSquareVal(square, val):
    #print(square)
    for i in range(0,3):
        for j in range(0,3):
            if(square[i][j] == val):
                return False
    return True
                
filepath = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(filepath,"sudoku.csv"))

init_time = time.perf_counter()
count_pass = 0
boards = 10000
for i in range(boards):
    board , solved_board = convert_df(df.iloc[i, :])
    if(init_solve(board, solved_board)) : count_pass+=1
    else: print("Got Wrong ", i)

done_time = time.perf_counter()
time_taken = done_time-init_time

print("\nAnd Alexander wept\n")
print("Solved: ",count_pass, "/", boards, " in ", time_taken, " seconds")
if count_pass == boards: print("\nFor there were no more worlds left to conquer\n")
else: print("\nd'oh\n")

