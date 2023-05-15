#This imports us a SenseHat object 
from sense_emu import SenseHat
import time
import threading

################################################
    #lets Define some vars
row = 8
speed = 2

#RGB colors
white = (255, 255, 255)
blue  = (0, 0, 255)
red  = (255, 0, 0)
reset = (0, 0, 0)

#This is our SenseHat object
sense = SenseHat()

#x and y of our block
xBlock = 0
yBlock = 0

#a mutex
lock = threading.Lock()
#this is our 2 d array 64 lights
ourArr = [[0 for x in range(row)] for y in range(row)]

#######################################################
    #this section is for moving pixles (DOES NOT WORK CUS STUPID)
#move mothod - this does not work yet
def move(event):
    print("move method")
    #get our list
    ourPixles = sense.get_pixels()
    printList(ourPixles)
    for x in ourPixles:
        if x == white:
            #move right
            if event.direction == "right":
                print("moving right")
                ourPixles[x] = reset
                ourPixles[x + 1] = white
            else:
                print("moving left")
                ourPixles[x] = reset
                ourPixles[x - 1] = white
                
#moves the pixle down
def moveDown():
    global xBlock
    global yBlock
    
    print(str(xBlock), str(yBlock))
    
    #waits to get a lock
    with lock:
        #checks if we would go out of bounds and does nothing if we would
        if xBlock != row-1:
            ourArr[xBlock][yBlock] = reset
            ourArr[xBlock + 1][yBlock] = white
            xBlock = xBlock +1
    setPixles(ourArr)
    
#moves the pixle left
def moveLeft():
    global xBlock
    global yBlock
    
    #waits to get a lock
    with lock:
        #checks if we would go out of bounds and does nothing if we would
        if yBlock != 0:
            ourArr[xBlock][yBlock] = reset
            ourArr[xBlock][yBlock-1] = white
            yBlock = yBlock-1
            
#moves the pixle right
def moveRight():
    global xBlock
    global yBlock
    
    #waits to get a lock
    with lock:
        #checks if we would go out of bounds and does nothing if we would
        if yBlock != row-1:
            ourArr[xBlock][yBlock] = reset
            ourArr[xBlock][yBlock+1] = white
            yBlock = yBlock+1
            
################################################
        #the following methods are for converting between 2d arr and list and setting a 2d Arr to the pixles

#converts a 2D Array to a list
def convertToList(ourArr):
    temList = []
    for x in range(row):
        for y in range(row):
            temList.append(ourArr[x][y])
    return temList

#converts a list into a 2d array
def convertTo2D(ourList):
    #vars
    x, y = 0, 0
    temArr = [[0 for x in range(row)] for y in range(row)]
    
    #loop thru our list
    for i in ourList:
        #copy each index from our list into temArr
        temArr[x][y] = i
        y += 1
        
        #one we reach the end of our row, set x back to zero and increase y by 1
        if y == row:
            y = 0
            x += 1
            
    #return our array
    return temArr

# gets a list from the sense hat and converts to a 2darray
def getArr():
    ourArr = convertTo2D(sense.get_pixels())
    return ourArr

#sets a 2D array into the sense hat
def setPixles(our2D):
    #covert our 2D to a list
    pixleList = convertToList(our2D)
    #set the list to pixles
    sense.set_pixels(pixleList)
    
##############################################
    
#function to do some things on startup
def start():
    #Clear out the sense hat
    sense.clear()

    #define what happens when the user presses left or right
    sense.stick.direction_left = moveLeft
    sense.stick.direction_right = moveRight


    #Has tetris scroll across the screen
    sense.show_message("Tetris", 0.1 , blue)
    sense.clear()
    
def spawnBlock():
    #assign a starting pixle
    ourArr[0][3] = white
    global xBlock
    global yBlock
    xBlock = 0
    yBlock = 3
    print(str(xBlock), str(yBlock))
#prints out our list of pixles
def printList(pixleList):
    for i in pixleList:
        print(i)
        
##############################################################
    # the 'main'

start()

#Now get a list of pixles (Should be all blank)
ourArr = convertTo2D(sense.get_pixels())

spawnBlock()
setPixles(ourArr)

time.sleep(speed)

is_bottom = False
        
#keep repeting untill we reach the bottom
while is_bottom == False:
    print("main " + str(xBlock) + str(yBlock))
    if xBlock >= row-1:
        is_bottom = True
    else:
        #remove the top pixle and move it one below
        moveDown()
        setPixles(ourArr)
        #this gives us a pause after each move
        time.sleep(speed)

print("Done")

