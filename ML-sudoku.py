import numpy as np
from tkinter import *
import math

from numpy.core.fromnumeric import size

size_of_board = 600
start_board = np.array( [ [5, 3, 0, 6, 7, 0, 0, 1, 0,],
                    [6, 0, 0, 1, 9, 5, 0, 0, 0,],
                    [0, 9, 8, 0, 0, 0, 0, 6, 0,],
                    [8, 0, 9, 0, 6, 0, 4, 0, 3,],
                    [4, 0, 0, 8, 0, 3, 0, 0, 1,],
                    [7, 0, 3, 0, 2, 0, 0, 0, 6,],
                    [0, 6, 1, 0, 0, 7, 2, 8, 0,],
                    [0, 0, 0, 4, 1, 9, 0, 0, 5,],
                    [0, 0, 0, 0, 8, 0, 0, 7, 9,],
                    ] )
init_board = start_board

solved_board = np.array( [ 
                    [5, 3, 4, 6, 7, 8, 9, 1, 2,],
                    [6, 7, 2, 1, 9, 5, 3, 4, 8,],
                    [1, 9, 8, 3, 4, 2, 5, 6, 7,],
                    [8, 5, 9, 7, 6, 1, 4, 2, 3,],
                    [4, 2, 6, 8, 5, 3, 7, 9, 1,],
                    [7, 1, 3, 9, 2, 4, 8, 5, 6,],
                    [9, 6, 1, 5, 3, 7, 2, 8, 4,],
                    [2, 8, 7, 4, 1, 9, 6, 3, 5,],
                    [3, 4, 5, 2, 8, 6, 1, 7, 9,],
                    ] )
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

def init_solve(board):
    #print(board)
    has_changed = True
    while(has_changed):
        has_changed= False
        for col in range(0,9):
            for row in range(0,9):
                if( board[row][col] == 0):
                    #print("solving cell vale at",board[row][col],"at [",row,",",col,"]") 
                    if(solveCell(board, row,col)): has_changed=True
        
        if not has_changed: print("and Alexander wept")
        
    print(init_board)
    print(board)
    if(np.array_equal(init_board, board)): print("fuck")
    if(np.array_equal(board, solved_board)): print("for there were no more worlds left to conquer")
    print(solved_board)

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
                

#print(board)
#print("\n")
#array_board = np.zeros((9,3,3))
#print(array_board)
#array_board[0] = board[:3, :3]
#print(array_board)
#column = board[:,3]
#print("column 1" ,column[0])

#poss_band = checkBand(2)
#print(poss_band)

#poss_stack = checkStack(1)
#print(poss_stack)

#poss_square=checkSquare(array_board[0], 1)

#square = findSquare(2, 1)
#print(square)
#poss_square = checkSquare(square)
#print(poss_square)

#checkCell(1,5)
#solveCell(1,5)
#print(board[:,1])
board = np.array( [ [5, 3, 0, 6, 7, 0, 0, 1, 0,],
                    [6, 0, 0, 1, 9, 5, 0, 0, 0,],
                    [0, 9, 8, 0, 0, 0, 0, 6, 0,],
                    [8, 0, 9, 0, 6, 0, 4, 0, 3,],
                    [4, 0, 0, 8, 0, 3, 0, 0, 1,],
                    [7, 0, 3, 0, 2, 0, 0, 0, 6,],
                    [0, 6, 1, 0, 0, 7, 2, 8, 0,],
                    [0, 0, 0, 4, 1, 9, 0, 0, 5,],
                    [0, 0, 0, 0, 8, 0, 0, 7, 9,],
                    ] )
init_solve(board)
#for i in range(0,9):
#    print(i)
