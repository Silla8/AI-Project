import customtkinter
import numpy as np
import math
import heapq
import time
import ast

customtkinter.set_appearance_mode("dark")
app = customtkinter.CTk()
app.title("AI Agent | Numbered Slidding Puzzle")
app.geometry("800x650+300+5")
app.resizable(width=False, height=False)
app.grid_rowconfigure(0, weight=0) 
app.grid_columnconfigure(0, weight=0)

Font = font=customtkinter.CTkFont(family="geogia", size=12, weight="bold");

## board of tiles
board_frame = customtkinter.CTkFrame(app, width=450, height=400, fg_color="grey")
board_frame.grid(row=0, column=1, padx=20, pady=5)

## constants 
tiles_number = 3
board_width = 450 - 10 - 2*(tiles_number-1)
board_height = 400 - 10 - 2*(tiles_number-1)
counter = 0
depth = 0
cancelId = None

## gloabl variables
tiles =[]
initialState = []
final =[]
agent = None
heuristic = True
stop = True

## board initialization and control functions
def board_init():

    count = 1
    global initialState
    global final
    global agent
    global counter
    initialState = [None] * tiles_number*tiles_number
    array = np.arange(0, tiles_number*tiles_number)
    np.random.shuffle(array)
    for row in range(tiles_number):
        row_tiles =[]
        for column in range(tiles_number):
            flag = row*column == (tiles_number - 1)*(tiles_number - 1)
            popped = array[-1]
            array = np.delete(array, -1)
            if flag:
                tile = customtkinter.CTkLabel(board_frame, width=board_width/tiles_number, height=board_height/tiles_number, text="")
                tile.grid(row=int(popped/(tiles_number)), column=popped%(tiles_number), padx=5, pady=5)
                initialState[int(popped)]=-1
            else:
                tile = customtkinter.CTkLabel(board_frame, width=board_width/tiles_number, height=board_height/tiles_number, fg_color="#DADADA", text=count, text_color="black", font=Font)
                tile.grid(row=int(popped/(tiles_number)), column=popped%(tiles_number), padx=5, pady=5)
                initialState[int(popped)]=count
                
            count+=1
            tiles.append(tile)
    
    agent = AI_Agent(initialState)
    final = agent.astar_search()
    return None



def increaseSize():
    global tiles_number
    global board_width
    global board_height
    global tiles
    global board_frame
    if tiles_number<5:
        tiles_number = tiles_number + 1
    board_width = 450 -10 - 2*(tiles_number-1)
    board_height = 400 -10 - 2*(tiles_number-1)
    board_frame = customtkinter.CTkFrame(app, width=450, height=400, fg_color="grey")
    board_frame.grid(row=0, column=1, padx=20, pady=5)
    board_init()




def decreaseSize():
    global tiles_number
    global board_width
    global board_height
    global board_frame
    global final
    if tiles_number> 3:
        tiles_number = tiles_number - 1
    board_width = 450 -10 - 2*(tiles_number-1)
    board_height = 400 -10 - 2*(tiles_number-1)
    board_frame = customtkinter.CTkFrame(app, width=450, height=400, fg_color="grey")
    board_frame.grid(row=0, column=1, padx=20, pady=5)
    board_init()
    


def start():
    global counter
    global cancelId
    global stop
    
   
    if counter < len(final):
        update_board(final[counter])
        counter +=1
        cancelId = app.after(1000, start)
    else:
        cancel()


def cancel():
    global counter
    global cancelId

    counter =0
    app.after_cancel(cancelId)
        
        

def heuristicChoice():
    global heuristic
    heuristic = not heuristic

def update_board(state):
    global tiles_number
    global board_width
    global board_height
    global tiles
    global board_frame
    global Font
    
    count = 0
    for tile in state:
        label = tiles[count]
        if tile == -1:
            label.configure(text="", fg_color="grey")
        else:
            label.configure(text=tile, fg_color="#DADADA", text_color="black", font=Font)

        label.grid_forget()
        label.grid(row=(count//tiles_number), column=(count%tiles_number), padx=5, pady=5)
        count += 1
       
    
        


## sections container
section_frame = customtkinter.CTkFrame(app, width=150, height=400)
section_frame.grid(row=0, column=0, padx=20, pady=15)


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

manhattan_checkbox = customtkinter.CTkCheckBox(sub_frame2, text="Manhattan Distance", font=Font, text_color="black", command=heuristicChoice)
manhattan_checkbox.grid(row=1, column=0, padx=15, pady=10)

misplaced_checkbox = customtkinter.CTkCheckBox(sub_frame2, text="Misplaced Tiles Num", font=Font, text_color="black", command=heuristicChoice)
misplaced_checkbox.grid(row=2, column=0, padx=20, pady=10)


""" Technique parameters"""
sub_frame3 = customtkinter.CTkFrame(section_frame, width=150, height=200, fg_color="#DADADA")
sub_frame3.grid(row=2, column=0, padx=20, pady=10)

technique_label = customtkinter.CTkLabel(sub_frame3, text="Technique Parameters", font=Font, text_color="black")
technique_label.grid(row=0, column=0, padx=20, pady=5)

Weighted_checkbox = customtkinter.CTkCheckBox(sub_frame3, text="Weighted A star", font=Font, text_color="black")
Weighted_checkbox.grid(row=1, column=0, padx=20, pady=10)

## puzle parameters

shuffle_button = customtkinter.CTkButton(section_frame, text="Reset Puzzle", font=Font, command=board_init)
shuffle_button.grid(row=3, column=0, padx=20, pady=15)

start_button = customtkinter.CTkButton(section_frame, text="Start AI Agent", font=Font, command=start)
start_button.grid(row=4, column=0, padx=20, pady=15)


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
        self.weight = 1
        self.cost = {str(initialState): 0}



    def expand(self, state):
        lis = list()
        for neighborLoc in self.getNeighborsLoc(state):
            lis.append(self.swap(state.copy(), neighborLoc, state.index(-1)))
        #for child in lis:
            #self.relaxed_cost(state, child)
        return lis
    

    def fun(self, state): 
        global heuristic
        return (self.cost[str(state)] + self.weight*self.getManhattanHeuristic(state))



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
    
    def getCostFromInitialState(self, state):
        global tiles_number
        cost = 0
        rowLen = tiles_number
        for tile in state:
            if tile != -1:
                row1 = (state.index(tile))%rowLen
                colu1 = (state.index(tile))//rowLen
                row2 = (tile-1)%rowLen
                colu2 = (tile-1)//rowLen
                cost += (abs(row1-row2) + abs(colu1-colu2))
        return cost



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
    
    def afficher(self, state):
        count = 1
        global tiles_number
        for i in state:
            if count%tiles_number != 1:
                with open("output.txt", "a") as file:
                    if i == -1:
                        file.write(f"  |")
                    else: 
                        file.write(f"{i} |")
            else:
                with open("output.txt", "a") as file:
                    file.write("\n")
             
                for j in range(tiles_number):
                    with open("output.txt", "a") as file:
                        file.write("___")

                with open("output.txt", "a") as file:
                    if i == -1:
                        file.write(f"\n  |")
                    else:
                        file.write(f"\n{i} |")
            count += 1
        
    def astar_search(self):
    
        global depth
        start = self.initialState
        frontier = PriorityQueue('min')
        frontier.append(str(start), self.fun(start))
        explored = set()
        sequence = list()
        iteration = 0  # Debugging iteration count
        while frontier:
            state = ast.literal_eval(frontier.pop())
            iteration+=1
            if self.isGoal(state):
                print("goal state found!")
                depth = 0
                node = state
                while self.parentState[str(node)] != -1:
                    sequence.append(node)
                    node =self.parentState[str(node)]
                    depth +=1
                return sequence[::-1]
            explored.add(str(state))
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

board_init()


app.mainloop()


