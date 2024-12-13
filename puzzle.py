# Author: Silla Ibrahim

import customtkinter
import numpy as np
import math
import heapq
import time
import ast


customtkinter.set_appearance_mode("dark")
app = customtkinter.CTk()
app.title("Slidding Puzzle | by Silla Ibrahim")
app.geometry("900x650+300+5")
app.resizable(width=False, height=False)
app.grid_rowconfigure(0, weight=0) 
app.grid_columnconfigure(0, weight=0)

Font = font=customtkinter.CTkFont(family="geogia", size=15, weight="bold");
TileFont = font=customtkinter.CTkFont(family="geogia", size=25, weight="bold");


## main board section
main_frame = customtkinter.CTkFrame(app, width=500, height=650)
main_frame.grid(row=0, column=1, padx=20, pady=5)

## board of tiles
board_frame = customtkinter.CTkFrame(main_frame, width=500, height=500, fg_color="grey")
board_frame.grid(row=0, column=0, padx=20, pady=10)

## constants 
tiles_number = 3
board_width = 500 - 10 - 2*(tiles_number-1)
board_height = 500 - 10 - 2*(tiles_number-1)


## gloabl variables
tiles =[]
initialState = []
final =[]
heuristic = True
running = False
visited = 0
explored_label = None
move_label = None
planning_label = None
planning = False
counter = 0
depth = 0
cancelId = None
Weighted_bool = customtkinter.BooleanVar()
man_bool = customtkinter.BooleanVar(None,True)
misplaced_bool = customtkinter.BooleanVar()

## board initialization and control functions
def board_init():

    global initialState
    global final
    global counter
    global tiles
    global cancelId
    global board_width
    global board_height
    global visited
    global running
    global planning
    global TileFont
    initialState = [2, 8, 7, 5, 3, -1, 4, 1, 6] # start with unsolvable init state
    
    if cancelId!= None: # in case of resetting in middle of solving
        cancel()
        counter =0
    final = []
    visited = 0
    running = False
    planning = False
    update_info()
    while not checkSolvability(initialState):
        count = 1
        tiles = []
        initialState = [None] * tiles_number*tiles_number
        array = np.arange(0, tiles_number*tiles_number)
        np.random.shuffle(array)
        for row in range(tiles_number):
            for column in range(tiles_number):
                flag = row*column == (tiles_number - 1)*(tiles_number - 1)
                popped = array[-1]
                array = np.delete(array, -1)
                if flag:
                    tile = customtkinter.CTkLabel(board_frame, width=board_width/tiles_number, height=board_height/tiles_number, text="", corner_radius= 10)
                    tile.grid(row=int(popped)//tiles_number, column=int(popped)%tiles_number, padx=5, pady=5)
                    initialState[int(popped)]=-1
                else:
                    tile = customtkinter.CTkLabel(board_frame, width=board_width/tiles_number, height=board_height/tiles_number, fg_color="#DADADA", text=count, text_color="#20283E", font=TileFont, corner_radius= 10)
                    tile.grid(row=int(popped)//tiles_number, column=int(popped)%tiles_number, padx=5, pady=5)
                    initialState[int(popped)]=count
                    
                    
                count+=1
                tiles.append(tile)
        
    
   
    return None

def checkSolvability(state):
    inverse_count =0
    if tiles_number%2 != 0:
        for i in range(len(state)-1):
            for j in range(i + 1, len(state)):
                if (state[i]!=-1 and state[j]!=-1) and (state[i]>state[j]):
                    inverse_count+=1
        return inverse_count%2 == 0
    else:
        for i in range(len(state)-1):
            for j in range(i + 1, len(state)):
                if (state[i]!=-1 and state[j]!=-1) and (state[i]>state[j]):
                    inverse_count+=1
        return (inverse_count + (4 - state.index(-1)//tiles_number))%2 != 0


def increaseSize():
    global tiles_number
    global board_width
    global board_height
    global tiles
    global board_frame
    global main_frame
    if tiles_number<5:
        tiles_number = tiles_number + 1
    board_width = 500 - 10 - 2*(tiles_number-1)
    board_height = 500 - 10 - 2*(tiles_number-1)
    board_frame = customtkinter.CTkFrame(main_frame, width=500, height=500, fg_color="grey")
    board_frame.grid(row=0, column=0, padx=20, pady=5)
    board_init()




def decreaseSize():
    global tiles_number
    global board_width
    global board_height
    global board_frame
    global  main_frame
    if tiles_number> 3:
        tiles_number = tiles_number - 1
    board_width = 500 - 10 - 2*(tiles_number-1)
    board_height = 500 - 10 - 2*(tiles_number-1)
    board_frame = customtkinter.CTkFrame(main_frame, width=500, height=500, fg_color="grey")
    board_frame.grid(row=0, column=0, padx=20, pady=5)
    board_init()
    


def start():
    global counter
    global cancelId
    global final
    global running
    
    
    if len(final)>0:
        if counter < len(final):
            update_board(final[counter])
            counter +=1
            cancelId = app.after(1000, start)
        else:
            running = False
            update_info()
            cancel()

def run():
    global running
    if not running and len(final)>0:
        start()
        running = True
    update_info()

def cancel():
    global counter
    global cancelId

    counter = 0
    app.after_cancel(cancelId)
        
        

def update_board(state):
    global tiles_number
    global tiles
    global TileFont

    
    count = 0
    for tile in state:
        label = tiles[count]
        if tile == -1:
            label.configure(text="", fg_color="grey")
        else:
            label.configure(text=tile, fg_color="#DADADA", text_color="black", font=TileFont)

        label.grid_forget()
        label.grid(row=(count//tiles_number), column=(count%tiles_number), padx=5, pady=5)
        count += 1
       
def update_info():
    global explored_label
    global move_label
    global visited
    global planning_label
    global planning
    global running


    explored_label.configure(text="Explored State(s): "+str(visited), fg_color="#DADADA", text_color="black", font=Font)
    explored_label.grid_forget()
    explored_label.grid(row=0, column=0, padx=20, pady=5)

    move_label.configure(text="Number of Move(s): "+str(len(final)), fg_color="#DADADA", text_color="black", font=Font)
    move_label.grid_forget()
    move_label.grid(row=0, column=1, padx=20, pady=5)

    planning_label.configure(text="Status: Running" if running  else ("Status: Planning" if planning else ("Status: Done" if len(final)>0 else "Status: Idle")), corner_radius=10, text_color="#B3C100", font=Font, fg_color="grey", )
    planning_label.grid_forget()
    planning_label.grid(row=0, column=2, padx=20, pady=5)

    


  

def uncheckMan():

    if misplaced_bool.get():
        man_bool.set(False)
    else:
        man_bool.set(True)

def uncheckMisplaced():
    if man_bool.get():
        misplaced_bool.set(False)
    else:
        misplaced_bool.set(True)
    
def resolve():
    global final
    global counter
    global cancelId
    global planning

    if cancelId!= None: # in case of re-resolving in middle of srunning
        cancel()

    planning = True
    update_info()
    app.update()
    agent = AI_Agent(initialState)
    final = agent.astar_search()
    counter = 0
    planning = False
    update_info()

def reset():
    global initialState
    global counter
    global cancelId
    global visited
    global final
    global running
    global planning

    if cancelId!= None: # in case of re-resolving in middle of srunning
        cancel()

    update_board(initialState)
    counter = 0
    visited = 0
    running = False
    planning = False
    final = []
    update_info()


## sections container
section_frame = customtkinter.CTkFrame(app, width=120, height=200)
section_frame.grid(row=0, column=0, padx=20, pady=15)


section_info = customtkinter.CTkFrame(main_frame, width=100, height=50, fg_color="#DADADA")
section_info.grid(row=1, column=0, padx=20, pady=10)


## sub sections

""" board parameters"""
sub_frame1 = customtkinter.CTkFrame(section_frame, width=150, height=200, fg_color="#DADADA")
sub_frame1.grid(row=0, column=0, padx=20, pady=20)

boardSize_label = customtkinter.CTkLabel(sub_frame1, text="Tiles Number Parameters", font=Font, text_color="black")
boardSize_label.grid(row=0, column=0, padx=20, pady=5)

board_size_button1 = customtkinter.CTkButton(sub_frame1, text="Increase ", font=Font, command=increaseSize)
board_size_button1.grid(row=1, column=0, padx=20, pady=15)

board_size_button2 = customtkinter.CTkButton(sub_frame1, text="Decrease ", font=Font, command=decreaseSize)
board_size_button2.grid(row=2, column=0, padx=20, pady=15)


""" Heuristics parameters"""
sub_frame2 = customtkinter.CTkFrame(section_frame, width=150, height=200, fg_color="#DADADA")
sub_frame2.grid(row=1, column=0, padx=20, pady=10)

heuristic_label = customtkinter.CTkLabel(sub_frame2, text="Heuristics Parameters", font=Font, text_color="black")
heuristic_label.grid(row=0, column=0, padx=20, pady=5)

manhattan_checkbox = customtkinter.CTkCheckBox(sub_frame2, text="Manhattan Distance", font=Font, text_color="black", variable=man_bool, command=uncheckMisplaced)
manhattan_checkbox.grid(row=1, column=0, padx=15, pady=10)

misplaced_checkbox = customtkinter.CTkCheckBox(sub_frame2, text="Misplaced Tiles Num", font=Font, text_color="black", variable=misplaced_bool, command=uncheckMan)
misplaced_checkbox.grid(row=2, column=0, padx=20, pady=10)


""" Technique parameters"""
sub_frame3 = customtkinter.CTkFrame(section_frame, width=150, height=200, fg_color="#DADADA")
sub_frame3.grid(row=2, column=0, padx=20, pady=10)

technique_label = customtkinter.CTkLabel(sub_frame3, text="Technique Parameters", font=Font, text_color="black")
technique_label.grid(row=0, column=0, padx=20, pady=5)

Weighted_checkbox = customtkinter.CTkCheckBox(sub_frame3, text="Weighted A star", font=Font, text_color="black", variable=Weighted_bool)
Weighted_checkbox.grid(row=1, column=0, padx=20, pady=10)

## puzle parameters

shuffle_button = customtkinter.CTkButton(section_frame, text="Shuffle", font=Font, command=board_init)
shuffle_button.grid(row=3, column=0, padx=20, pady=5)

reset_button = customtkinter.CTkButton(section_frame, text="Reset", font=Font, command=reset)
reset_button.grid(row=4, column=0, padx=20, pady=5)

resolve_button = customtkinter.CTkButton(section_frame, text="Plan", font=Font, command=resolve)
resolve_button.grid(row=5, column=0, padx=20, pady=5)


start_button = customtkinter.CTkButton(section_frame, text="Start Agent", font=Font, command=run)
start_button.grid(row=6, column=0, padx=20, pady=10)



## info section

explored_label = customtkinter.CTkLabel(section_info, text="Explored State(s): "+str(visited), font=Font, text_color="black")
explored_label.grid(row=0, column=0, padx=20, pady=5)


move_label = customtkinter.CTkLabel(section_info, text="Move(s): "+str(len(final)), font=Font, text_color="black")
move_label.grid(row=0, column=1, padx=20, pady=5)


planning_label = customtkinter.CTkLabel(section_info, text="Status: Idle", font=Font, text_color="black")
planning_label.grid(row=0, column=2, padx=20, pady=5)



#______________________________________________________________________________________________________________________________________
    
class PriorityQueue:
    

    
    def __init__(self, order='min'):
        self.heap = []
        if order != 'min':
            raise ValueError("Order must be either 'min'.")

    def append(self, item, value):
        """Insert item at its correct position."""
        heapq.heappush(self.heap, (value, item))

    def pop(self):
        """Pop and return the item (with min or max f(x) value)
        depending on the order."""
        if self.heap:
            both = heapq.heappop(self.heap)
            return both[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __len__(self):
        """Return current capacity of PriorityQueue."""
        return len(self.heap)

    def __contains__(self, key):
        """Return True if the key is in PriorityQueue."""
        return any([item == key for _, item in self.heap])

    def __getitem__(self, key):
        """Returns the first value associated with key in PriorityQueue.
        Raises KeyError if key is not present."""
        for value, item in self.heap:
            if item == key:
                return value
        raise KeyError(str(key) + " is not in the priority queue")

    def __delitem__(self, key):
        """Delete the first occurrence of key."""
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)




#________________________________________________________________________________________________________________

class AI_Agent:
    def __init__(self, initialState):
        self.initialState = initialState
        self.parentState = {str(initialState): -1}
        self.weight = 10
        self.cost = {str(initialState): 0}



    def expand(self, state):
        lis = list()
        for neighborLoc in self.getNeighborsLoc(state):
            lis.append(self.swap(state.copy(), neighborLoc, state.index(-1)))
        
        return lis
    

    def fun(self, state): 
        global man_bool
        global misplaced_bool
        global Weighted_bool
        if man_bool.get():

            if Weighted_bool.get():
                
                return (self.cost[str(state)] + self.weight*self.getManhattanHeuristic(state))
            else:
               
                return (self.cost[str(state)] + self.getManhattanHeuristic(state))
        else:
            
            if Weighted_bool.get():

                return (self.cost[str(state)] + self.weight*self.getMisplacedTileHeuristic(state))
            else:

                return (self.cost[str(state)] + self.getMisplacedTileHeuristic(state))
        



    def getManhattanHeuristic(self, state):
        global tiles_number
        manDist = 0
        rowLen = tiles_number
        for tile in state:
            if tile != -1:
                row1 = (state.index(tile))//rowLen
                colu1 = (state.index(tile))%rowLen
                row2 = (tile-1)//rowLen
                colu2 = (tile-1)%rowLen
                manDist += (abs(row1-row2) + abs(colu1-colu2))
        return manDist

    

    def getMisplacedTileHeuristic(self, state):
        misplace = 0
        count = 1

        for i in state:
            if i != count and i!= -1: 
                misplace += 1
            count += 1
        return misplace
    


    def swap(self, state, index1, index2):
        temp = state[index1]
        state[index1] = state[index2]
        state[index2] = temp
        return state


    
    
    def isGoal(self, state):
        count = 1
        for i in state:
            if i != count and i != -1: 
                return False
            count +=1
        return True
    
    def relaxed_cost(self, parent, child):
        self.cost[str(child)] = self.cost[str(parent)] + 1
        self.parentState[str(child)]= parent
        return None
    
    
    def getNeighborsLoc(self, state):
        global tiles_number
        emptyIndex = state.index(-1)
        neighborsLoc = []
        rowLength = tiles_number 

        if (emptyIndex - rowLength) >= 0:
            neighborsLoc.append(emptyIndex - rowLength)

        if (emptyIndex + rowLength) <= (len(state)-1):
            neighborsLoc.append(emptyIndex + rowLength)

        if (emptyIndex%rowLength) != 0:
            neighborsLoc.append(emptyIndex - 1)
        
        if ((emptyIndex + 1) <= (len(state)-1)) and (((emptyIndex + 1)%rowLength) != 0):
            neighborsLoc.append(emptyIndex + 1)
       
        return neighborsLoc
    
    
    def astar_search(self):
    
        global visited
        visited = 0
        start = self.initialState
        frontier = PriorityQueue('min')
        frontier.append(str(start), self.fun(start))
        explored = set()
        sequence = list()
        while frontier:
            state = ast.literal_eval(frontier.pop())
            if self.isGoal(state):
                print("goal state found!")
                node = state
                while self.parentState[str(node)] != -1:
                    sequence.append(node)
                    node =self.parentState[str(node)]
                return sequence[::-1]
            explored.add(str(state))
            visited +=1
            for child in self.expand(state):
                if str(child) not in explored and str(child) not in frontier:
                    self.relaxed_cost(state, child)
                    frontier.append(str(child), self.fun(child))
                elif str(child) in frontier:
                    prevCost = self.cost[str(child)]
                    prevParent = self.parentState[str(child)]
                    self.relaxed_cost(state, child)
                    if self.fun(child) < frontier[str(child)]:
                        del frontier[str(child)]
                        frontier.append(str(child), self.fun(child))
                    else:
                        self.cost[str(child)]= prevCost
                        self.parentState[str(child)]= prevParent
                        
                        
                        
                        
        return None





# main___________________________________________________________________________________

board_init() # environment contain the AI agent


app.mainloop()


