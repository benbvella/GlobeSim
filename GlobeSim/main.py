# to do:
# simulateTimeStep function:
#   correct subduction system
# undo and redo functionality
# save and load files
# introduce threading during time step simulation?

# current bugs:
# left-click mouse automatically activates after closing tkinter windows

import tkwindow
import pygame, sys, random
import tkinter as tk
from tkinter import ttk
import numpy as np
from math import *

sys.setrecursionlimit(3000)
pygame.init()

mainClock = pygame.time.Clock()

icon = pygame.image.load('images/icon.png')
move1 = pygame.image.load('images/moveOFF.png')
move2 = pygame.image.load('images/moveON.png')
drawPlate1 = pygame.image.load('images/drawPlateOFF.png')
drawPlate2 = pygame.image.load('images/drawPlateON.png')
drawTerrain1 = pygame.image.load('images/drawTerrainOFF.png')
drawTerrain2 = pygame.image.load('images/drawTerrainON.png')
movePlate1 = pygame.image.load('images/movePlateOFF.png')
movePlate2 = pygame.image.load('images/movePlateON.png')
color1 = pygame.image.load('images/colorOFF.png')
color2 = pygame.image.load('images/colorON.png')
add1 = pygame.image.load('images/add.png')
pick1 = pygame.image.load('images/pickOFF.png')
pick2 = pygame.image.load('images/pickON.png')
play1 = pygame.image.load('images/playOFF.png')
play2 = pygame.image.load('images/playON.png')
step1 = pygame.image.load('images/stepLEFT.png')
step2 = pygame.image.load('images/stepRIGHT.png')
skip1 = pygame.image.load('images/skipLEFT.png')
skip2 = pygame.image.load('images/skipRIGHT.png')
print1 = pygame.image.load('images/print.png')

arial = pygame.font.SysFont("Arial", 12)
arialBold = pygame.font.SysFont("Arial Bold", 18)
letterWidths = {" ": 4.4453125, "!": 4.4453125, '"': 5.6796875, "#": 8.8984375, "$": 8.8984375, "%": 14.2265625, "&": 10.671875, "'": 3.0546875, "(": 5.328125, ")": 5.328125, "*": 6.2265625,
"+": 9.34375, ",": 4.4453125, "-": 5.328125, ".": 4.4453125, "/": 4.4453125, "0": 8.8984375, "1": 7.7228125, "2": 8.8984375, "3": 8.8984375, "4": 8.8984375,
"5": 8.8984375, "6": 8.8984375, "7": 8.8984375, "8": 8.8984375, "9": 8.8984375, ":": 4.4453125, ";": 4.4453125, "<": 9.34375, "=": 9.34375, ">": 9.34375,
"?": 8.8984375, "@": 16.2421875, "A": 10.671875, "B": 10.671875, "C": 11.5546875, "D": 11.5546875, "E": 10.671875, "F": 9.7734375, "G": 12.4453125,
"H": 11.5546875, "I": 4.4453125, "J": 8, "K": 10.671875, "L": 8.8984375, "M": 13.328125, "N": 11.5546875, "O": 12.4453125, "P": 10.671875, "Q": 12.4453125,
"R": 11.5546875, "S": 10.671875, "T": 9.7734375, "U": 11.5546875, "V": 10.671875, "W": 15.1015625, "X": 10.671875, "Y": 10.671875, "Z": 9.7734375, "[": 4.4453125,
"]": 4.4453125, "^": 7.5078125, "_": 8.8984375, "`": 5.328125, "a": 8.8984375, "b": 8.8984375, "c": 8, "d": 8.8984375, "e": 8.8984375, "f": 4.15921875, "g": 8.8984375,
"h": 8.8984375, "i": 3.5546875, "j": 3.5546875, "k": 8, "l": 3.5546875, "m": 13.328125, "n": 8.8984375, "o": 8.8984375, "p": 8.8984375, "q": 8.8984375,
"r": 5.328125, "s": 8, "t": 4.4453125, "u": 8.8984375, "v": 8, "w": 11.5546875, "x": 8, "y": 8, "z": 8, "{": 5.34375, "|": 4.15625, "}": 5.34375, "~": 9.34375}

run = True
mode = 0
fps = 20
gfps = 20
disableKeys = False

resolution = 3
dataRes = 1000  # multiple of twos recommended. processing time increases expentially.
res1 = dataRes / pi  # constant used for radians-to-cells conversion

screenWidth = 800
screenHeight = 500
leftWidth = 100
rightWidth = 100

time = 0
maxTime = 0

see = 0
seeDict = [-1, 0, 1, 0]
terrainColors = [25855, 25600, 6579300]
# ocean blue, land green, mountain grey.

minZoom = 64
zoom = minZoom
position = [0,0]
mouseTransform = [0,0]
scrollSpeed = 100

clicking = False
picking = False
panning = False
mouseOnGlobe = False

mouse = [0,0]
displayMouse = [0,0]
mouseVector = [0,0]
mouseSpherical = [0,0]
mouseCell = None

brushColor = 0
brushSize = 50
brushN = cos(brushSize / res1)
plateColor = 0
terrainColor = 0

selectedPlate = []

modeButtons = []
playButtons = [] #different types!
plateButtons = []
terrainButtons = []

coordinates = []
data = [[]]
plateData = [[255, 65280, 16711680],[[[0], [(0, 0, 1)], [0]],[[0], [(0, 0, 1)], [0]],[[0], [(0, 0, 1)], [0]]], [[],[],[]]]
# [colors], [movement data: [[startTimes], [poles], [speeds]]], [density coefficient tables]

class TapButton():
    def __init__(self, img, name=None):
        self.img = img
        self.label = name
        self.labellength = 5
        self.x = 0
        self.y = 0
        self.width = img.get_width()
        self.height = img.get_height()

        if self.label:
            for letter in list(self.label):
                self.labellength += letterWidths[letter]
    
    def draw(self):
        win.blit(pygame.transform.scale(self.img, (self.width, self.height)), (self.x, self.y))
        pygame.draw.rect(win, 0, (self.x, self.y, self.width, self.height), 1)

        if self.hover() and self.label:
            pygame.draw.rect(win, (200,200,200), (mouse[0] + 8, mouse[1] + 9, self.labellength, 15))
            pygame.draw.rect(win, 0, (mouse[0] + 8, mouse[1] + 9, self.labellength, 15), 1)
            drawText(self.label, arial, 0, mouse[0] + 10, mouse[1] + 10)
    
    def hover(self):
        return pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(mouse)

class ToggleButton():
    def __init__(self, img1, img2, value, name=None, clicked=False, ismode=False):
        self.img1 = img1
        self.img2 = img2
        self.value = value
        self.label = name
        self.labellength = 5
        self.clicked = clicked
        self.ismode = ismode
        self.x = 0
        self.y = 0
        self.width = img1.get_width()
        self.height = img1.get_height()
        
        if self.label:
            for letter in list(self.label):
                self.labellength += letterWidths[letter] * 0.8

    def draw(self):
        if self.clicked:
            img = self.img2
        else:
            img = self.img1
        
        win.blit(pygame.transform.scale(img, (self.width, self.height)), (self.x, self.y))
        pygame.draw.rect(win, 0, (self.x, self.y, self.width, self.height), 1)

        if self.ismode and self.clicked:
            pygame.draw.rect(win, (255,255,255), (self.x + self.width-1, self.y, 1, self.height))

        if self.hover() and self.label:
            pygame.draw.rect(win, (200,200,200), (mouse[0] + 8, mouse[1] + 9, self.labellength, 15))
            pygame.draw.rect(win, 0, (mouse[0] + 8, mouse[1] + 9, self.labellength, 15), 1)
            drawText(self.label, arial, 0, mouse[0] + 10, mouse[1] + 10)
    
    def hover(self):
        return pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(mouse)

class Slider():
    def __init__(self, low=0, high=100, x=0, y=0, width=150, height=20, position=0.5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.low = low
        self.high = high
        self.pos = position
    
    def draw(self):
        pygame.draw.line(win, 0, (self.x, self.y + self.height / 2), (self.x + self.width, self.y + self.height / 2))
        pygame.draw.rect(win, (200,200,200), (self.x + self.width * self.pos - 5, self.y, 10, self.height))
        pygame.draw.rect(win, (100,100,100), (self.x + self.width * self.pos - 5, self.y, 10, self.height), 1)
    
    def read(self):
        return self.low + self.pos * (self.high - self.low)
    
    def hover(self):
        return pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(mouse)

def start():
    global win
    win = pygame.display.set_mode((screenWidth,screenHeight), pygame.RESIZABLE)
    pygame.display.set_icon(icon)
    pygame.display.set_caption("GlobeSim v0.1")
    makeButtons()
    newGlobe(dataRes)
    sizeDisplay()
    main()

def main():
    global fps
    global screenWidth, screenHeight
    global brushSize, brushN
    global mouseTransform

    while run:
        fps = mainClock.get_fps()
        if not fps: 
            fps = gfps

        manageMouse()
        manageAllKeys()

        # resize if necessary
        if win.get_width() != screenWidth or win.get_height() != screenHeight:
            screenWidth = win.get_width()
            screenHeight = win.get_height()
            sizeDisplay()

        # advance the time
        if playButtons[2].clicked:
            if time < 2000:
                setTime(time + 1)
            else:
                playButtons[2].clicked = False

        sizeSliders()

        # clicking actions
        if clicking:
            # if clicking slider
            if checkSlider(brushSlider):
                brushSize = checkSlider(brushSlider)
                brushN = cos(brushSize / res1)

            if checkSlider(timeSlider):
                setTime(checkSlider(timeSlider))
            
            #if clicking globe
            if mouseOnGlobe:
                try:
                    if (mode == 0 or panning):
                        mouseLoc = mouseSpherical
                        mouseTransform = [(clickLoc[1] - mouseLoc[1]), (mouseLoc[0] - clickLoc[0]) * ((abs(pi - abs(fixPos(clickLoc[1] - pi/2) - position[0])) > pi/2) * 2 - 1)]
                        # Imperfect fix for upside-down latitudinal rotation. May be removed for simplicity
                    elif mode == 1:
                        brush(0, displayMouse)
                    elif mode == 2:
                        brush(1, displayMouse)
                except (TypeError, IndexError): pass 

        drawWindow()
        mainClock.tick(gfps)

def manageMouse():
    global mouse, displayMouse, mouseVector, mouseSpherical, mouseCell, mouseOnGlobe

    mouse = pygame.mouse.get_pos()
    displayMouse = ((mouse[0] - leftWidth) // resolution, (mouse[1] - 60) // resolution)
    
    if displayMouse[0] > 0 and mouse[0] < screenWidth - rightWidth and displayMouse[1] > 0 and mouse[1] < screenHeight - 20 and sqrt(((displayMouse[0] - displayCenter[0])**2) + ((displayMouse[1] - displayCenter[1])**2)) < zoom:
        mouseOnGlobe = True
        mouseVector = pixel3d(displayMouse)
        mouseSpherical = vtoSpherical(mouseVector)
        mouseCell = data[time][trunc(mouseSpherical[0] * res1)][trunc(mouseSpherical[1] * res1 * sin(mouseSpherical[0]))].copy()
    else:
        mouseOnGlobe = False

def manageAllKeys():
    global disableKeys

    manageKeyEvents()
    manageContinuousKeys()

    if disableKeys:
        disableKeys -= 1

def manageKeyEvents():
    global run
    global clicking, picking, panning
    global selectedPlate, clickLoc
    global zoom, position, mouseTransform
    global brushColor, plateColor

    for event in pygame.event.get():
        if disableKeys:
            break
        
        if event.type == pygame.QUIT: # closing window
            run = False
        
        elif event.type == pygame.KEYDOWN: # one-time key presses
            if event.key == pygame.K_ESCAPE: # esc
                run = False
            elif event.key > 48 and event.key < 53: # mode numbers - 1 to 4
                changeMode(event.key - 49)
            elif event.key == pygame.K_LCTRL: # ctrl
                panning = True
            elif event.key == pygame.K_p: #admin command for testing time seperation
                print(data)
            elif event.key == pygame.K_x: # exit plate mover
                if mode == 3 and selectedPlate:
                    plateData[0][selectedPlate[1]] += selectedPlate[2]
                    selectedPlate = []
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                panning = False
                position = [position[0] + mouseTransform[0], position[1] + mouseTransform[1]]
                mouseTransform = [0,0]
            
        elif event.type == pygame.MOUSEBUTTONDOWN: # mouse stuff
            if event.button == 1: #left click
                clicking = True
                checkAllButtons() # if clicking button
                if mouseOnGlobe:
                    if mode == 0 or panning:
                        clickLoc = mouseSpherical
                    elif mode == 3:
                        if selectedPlate:
                            try:
                                try:
                                    indx = plateData[1][selectedPlate[1]][0].index(time) # check if time already exists
                                    plateData[1][selectedPlate[1]][1][indx] = normalize(CROSS(selectedPlate[0],mouseVector)) # if so, replace motion
                                    plateData[1][selectedPlate[1]][2][indx] = -acos(DOT3(selectedPlate[0],mouseVector))
                                except ValueError:
                                    indx = getMovementIndex(selectedPlate[1], time) + 1 # get insertion index of new motion
                                    plateData[1][selectedPlate[1]][0].insert(indx, time) # insert start time in correct location
                                    plateData[1][selectedPlate[1]][1].insert(indx, normalize(CROSS(selectedPlate[0],mouseVector))) # insert pole in correct loc
                                    plateData[1][selectedPlate[1]][2].insert(indx, -acos(DOT3(selectedPlate[0],mouseVector))) # insert speed in correct loc
                            except (ZeroDivisionError, TypeError): pass
                            else:
                                simulateFutureTimesteps(time)
                        else:
                            selectedPlate = [mouseVector, mouseCell[0], colorFraction(plateData[0][mouseCell[0]], 5)]
                            plateData[0][selectedPlate[1]] -= selectedPlate[2]
                    elif picking:
                        clicking = picking = pickButton.clicked = False
                        brushColor = mouseCell[0]
                        offButtons(plateButtons)
                        plateButtons[brushColor].clicked = True
                
            elif event.button == 2: # middle click
                if mouseOnGlobe:
                    clicking = panning = True
                    clickLoc = mouseSpherical
                
            elif event.button == 3: # right click
                if mode == 1 and checkButtons(plateButtons) and len(plateButtons) > 1:
                    button = checkButtons(plateButtons) - 1
                    del plateButtons[button]
                    del plateData[0][button]
                    del plateData[1][button]
                    del plateData[2][button]
                    if brushColor >= button:
                        brushColor = plateColor = max(plateColor - 1, 0)
                    plateButtons[plateColor].clicked = True
                    sizeButtons()
                
            elif event.button == 4: #scrolling up
                zoom *= 1 + scrollSpeed / 100 / fps
                
            elif event.button == 5: #scrolling down
                if zoom >= minZoom:
                    zoom /= 1 + scrollSpeed / 100 / fps
            
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: #left click
                clicking = False
                if (mode == 0 or panning):
                    position = [fixPos(position[0] + mouseTransform[0]), fixPos(position[1] + mouseTransform[1])]
                    mouseTransform = [0,0]
            elif event.button == 2: # middle click
                clicking = panning = False
                position = [position[0] + mouseTransform[0], position[1] + mouseTransform[1]]
                mouseTransform = [0,0]

def manageContinuousKeys():
    global zoom
    global brushSize, brushN

    moveSpeed = scrollSpeed / zoom / fps
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_RIGHTBRACKET]:
        zoom *= 1 + scrollSpeed / 100 / fps
    if keys[pygame.K_LEFTBRACKET]:
        if zoom >= 64:
            zoom /= 1 + scrollSpeed / 100 / fps
    
    if keys[pygame.K_RIGHT]:
        position[0] = fixPos(position[0] - moveSpeed)
    if keys[pygame.K_LEFT]:
        position[0] = fixPos(position[0] + moveSpeed)
    if keys[pygame.K_UP]:
        position[1] = fixPos(position[1] - moveSpeed)
    if keys[pygame.K_DOWN]:
        position[1] = fixPos(position[1] + moveSpeed)
    
    if keys[pygame.K_MINUS]:
        brushSize = max(int(brushSize / 1.1), 1)
        brushN = cos(brushSize / res1)
    if keys[pygame.K_EQUALS]:
        brushSize = min(max(int(brushSize * 1.1), brushSize + 1), dataRes / 2 - 1)
        brushN = cos(brushSize / res1)

def changeMode(to):
    global mode, see, picking, brushColor, selectedPlate
    mode = to

    picking = pickButton.clicked = False

    if selectedPlate:
        plateData[0][selectedPlate[1]] += selectedPlate[2]
        selectedPlate = []

    if seeDict[mode] + 1: #change visual to appropriate one, unless moving
        see = seeDict[mode]
    
    for n in range(len(modeButtons)): #update mode buttons
        modeButtons[n].clicked = n == mode

    if mode == 1:
        brushColor = plateColor
    elif mode == 2:
        brushColor = terrainColor

def setTime(n):
    global time, maxTime
    time = n
    if time > maxTime:
        try:
            data[n-1]
        except IndexError:
            setTime(n-1)
        maxTime = time
        simulateTimeStep(n)

def newGlobe(res): # generate new globe
    for lat in range(res): #latitudes
        data[0].append([]) # new data latitude
        coordinates.append([]) #new coordinate latitude
        latr = (lat+0.5)*pi/res   # in radians, bottom is zero
        z1, z2 = sin(latr), cos(latr) # speeds up processing
        cells = round(2*res*z1) # cells for that location
        for lon in range(cells): #longitude
            data[0][lat].append([0,0,0,0]) # adds new cell to data. format: [plate id, plate material, underlying plate id, age]
            lonr = 2 * lon * pi / cells # in radians
            coordinates[lat].append((z1*cos(lonr),z1*sin(lonr),z2, lon)) # cartesian coords of point

def simulateFutureTimesteps(startTime:int):
    if startTime < maxTime:
        root = tk.Tk()
        base = ttk.Frame(root)
        base.pack(pady=10)
        bar = ttk.Progressbar(base, length=150)
        bar.grid(column=0, row=1, padx=10)
        progress_label = tk.Label(base, text=f"Simulating Time Steps... {bar['value']}%")
        progress_label.grid(column=0, row=0)
        root.update()

        for n in range(startTime + 1, maxTime + 1): # simulate from startTime to maxTime
            del data[n]
            simulateTimeStep(n)
            bar['value'] = trunc((n - startTime) / (maxTime - startTime) * 100)
            progress_label['text'] = f"Simulating Time Steps... {bar['value']}%"
            root.update()

        root.destroy()

def simulateTimeStep(n:int):
    data.insert(n, [])

    for table in plateData[2]: # update the density coeeficient table for each plate
        if table == []:
            table.append(random.random()*2-1)
        for i in range(len(table), maxTime+1):
            table.append(table[-1] * 0.9 + random.random() * 0.2 - 0.1) # randomized increase or decrease, centered toward 0

    plateIndices = []
    for plateID in range(len(plateData[0])):
        plateIndices.append(getMovementIndex(plateID, n-1))

    for lat in range(len(data[n-1])): # create empty base
        data[n].append([])
        for lon in range(len(data[n-1][lat])):
            data[n][lat].append([-1,0,0,0]) # add empty cell to data. format: [plate id, plate material, underlying plate id, age]
    
    for lat in range(len(data[n])): # move each cell according to plate id
        for lon in range(len(data[n][lat])):
            cell = data[n-1][lat][lon].copy()
            plateInfo = plateData[1][cell[0]]
            moveIndex = plateIndices[cell[0]]
            try:
                if plateInfo[2][moveIndex]:
                    cellCoords = vtoSpherical(rotate(coordinates[lat][lon][:-1], plateInfo[1][moveIndex], plateInfo[2][moveIndex] / 10))
                    cellLat = trunc(cellCoords[0] * res1)
                    cellLon = trunc(cellCoords[1] * res1 * sin(cellCoords[0]))
                else:
                    cellLat = lat
                    cellLon = lon
            except ValueError: pass
            else:
                newcell = data[n][cellLat][cellLon]
                if newcell[0] + 1:  # if already filled
                    if cell[1] > newcell[1]: # if pasted cell is less dense crust type
                        cell[3] += 1
                        data[n][cellLat][cellLon] = cell
                    elif cell[1] == newcell[1]: # cells are same crust type
                        if cell[3] + plateData[2][cell[0]][n] < newcell[3] + plateData[2][newcell[0]][n]: # age + density coefficient must be lower
                            data[n][cellLat][cellLon] = [cell[0], min(2, cell[1] + 1), 0, cell[3] + 1] # replace current cell
                        else: 
                            data[n][cellLat][cellLon][1] = min(2, cell[1] + 1) # current cell stays
                else: # not filled
                    cell[3] += 1
                    data[n][cellLat][cellLon] = cell
    
    missing = []
    for lat in range(len(data[n])): # log any missing cells
        for lon in range(len(data[n][lat])):
            if data[n][lat][lon][0] == -1:
                missing.append([lat, lon])
                try: 
                    missing[-1].append(trunc(lon / sin(lat / res1) * sin((lat + 1) / res1)))
                    missing[-1].append(trunc(lon / sin(lat / res1) * sin((lat - 1) / res1)))
                except: pass
    
    while missing: # fill in each missing cell one at a time
        missingCell = random.choice(missing)

        nearCells = []
        try: nearCells.append(data[n][missingCell[0]][missingCell[1]-1]) #left cell
        except: pass
        try: nearCells.append(data[n][missingCell[0]][missingCell[1]+1]) #right cell
        except: pass
        try: nearCells.append(data[n][missingCell[0] + 1][missingCell[2]]) #up cell
        except: pass
        try: nearCells.append(data[n][missingCell[0] - 1][missingCell[3]]) #down cell
        except: pass
        
        remainingNearCells = []
        setNew = False
        for i in nearCells:
            if i[0] + 1:
                remainingNearCells.append(i)
                if i[0] != remainingNearCells[0][0]: # if multiple plates are nearby, then the cell will assume that it's new crust
                    setNew = True

        if remainingNearCells: # if cells remain around it
            data[n][missingCell[0]][missingCell[1]] = random.choice(remainingNearCells).copy() # fill it! (with random nearby cell)
            if setNew:
                data[n][missingCell[0]][missingCell[1]][1] = 0 # set land type to ocean
                data[n][missingCell[0]][missingCell[1]][3] = 0 # set cell age to 0
            elif len(remainingNearCells) < 4:
                data[n][missingCell[0]][missingCell[1]][1] = 0 # set land type to ocean
            missing.remove(missingCell)

def sizeDisplay():
    global display, displayCenter, displayArrayW, displayArrayH, leftWidth, rightWidth

    leftWidth = max(int(screenWidth / 12), int((screenHeight - 20) / 4 - 10), 75)
    rightWidth = max(int(screenWidth / 6), 150)

    display = pygame.Surface(((screenWidth - leftWidth - rightWidth) / resolution, (screenHeight - 80) / resolution))
    displayCenter = (display.get_width()/2, display.get_height()/2)
    displayArrayW, displayArrayH = range(display.get_width()), range(display.get_height()) #improve rendering

    sizeButtons()

def sizeButtons():
    global pickButton, addButton

    for n in range(len(modeButtons)):
        modeButtons[n].x = 5
        modeButtons[n].y = n * leftWidth + 25
        modeButtons[n].width = modeButtons[n].height = leftWidth - 10

    buttonwidth = int(rightWidth / 5 - 10)
    for n in range(len(plateButtons)):
        plateButtons[n].width = plateButtons[n].height = buttonwidth
        plateButtons[n].x = screenWidth - rightWidth + (n%5) * (buttonwidth + 10) + 5
        plateButtons[n].y = rightWidth + (n//5) * (buttonwidth + 10) + 80
    
    for n in range(len(terrainButtons)):
        terrainButtons[n].width = terrainButtons[n].height = buttonwidth
        terrainButtons[n].x = screenWidth - rightWidth + n * (buttonwidth + 10) + 5
        terrainButtons[n].y = rightWidth + 80

    for n in range(len(playButtons)):
        playButtons[n].x = leftWidth + n * 37 + 5
        playButtons[n].y = 24

    pickButton.width = pickButton.height = addButton.width = addButton.height = buttonwidth
    pickButton.x = screenWidth - rightWidth + (len(plateButtons)%5) * (buttonwidth + 10) + 5
    addButton.x = screenWidth - rightWidth + ((len(plateButtons)+1)%5) * (buttonwidth + 10) + 5
    pickButton.y = rightWidth + (len(plateButtons)//5) * (buttonwidth + 10) + 80
    addButton.y = rightWidth + ((len(plateButtons)+1)//5) * (buttonwidth + 10) + 80
    printButton.x = screenWidth - printButton.width - 8
    printButton.y = 27

def sizeSliders():
    global brushSlider, timeSlider
    brushSlider = Slider(1, dataRes / 2 - 1, screenWidth - rightWidth + 5, 50 + rightWidth, rightWidth - 30)
    brushSlider.pos = (brushSize - brushSlider.low) / (brushSlider.high - brushSlider.low)
    timeSlider = Slider(0, max(maxTime,1), leftWidth + 200, 25, screenWidth - leftWidth - rightWidth - 245, 30)
    timeSlider.pos = time / max(maxTime,1)

def drawWindow():
    win.fill((255,255,255))
    drawDisplay()
    drawMenu()
    pygame.display.update()

def drawMenu():
    pygame.draw.rect(win, 0, (0, 0, screenWidth, 20))

    pygame.draw.rect(win, (200,200,200), (0, 20, leftWidth - 5, screenHeight - 20))
    pygame.draw.line(win, 0, (leftWidth-6, 20), (leftWidth-6, screenHeight))
    for button in modeButtons:
        button.draw()
    
    for button in playButtons:
        button.draw()
    timeSlider.draw()
    drawText(str(time) + " My", arial, 0, screenWidth - rightWidth - 32, 35)

    if mode == 1 or mode == 2:
        drawText("Brush Settings:", arial, 0, screenWidth - rightWidth + 5, 25)
        pygame.draw.rect(win, 0, (screenWidth - rightWidth + 5, 45, rightWidth - 10, rightWidth - 10), 1)
        brushSlider.draw()
        drawText(str(brushSize), arial, 0, screenWidth - 20, rightWidth + 53)
    
    if mode == 0:
        if mouseOnGlobe:
            drawText("Current Cell: " + str(mouseCell), arial, 0, screenWidth - rightWidth + 5, 65)
        else:
            drawText("Current Cell: None", arial, 0, screenWidth - rightWidth + 5, 65)
    
    elif mode == 1:
        pygame.draw.circle(win, plateData[0][brushColor], (screenWidth - rightWidth / 2, rightWidth / 2 + 40), brushSize / dataRes * (rightWidth - 10))
        pygame.draw.circle(win, 0, (screenWidth - rightWidth / 2, rightWidth / 2 + 40), brushSize / dataRes * (rightWidth - 10), 1)
        for n in range(len(plateButtons)):
            button = plateButtons[n]
            button.draw()
            pygame.draw.rect(win, plateData[0][n], (button.x + 2, button.y + 2, button.width - 4, button.height - 4))
        pickButton.draw()
        addButton.draw()
    
    elif mode == 2:
        pygame.draw.circle(win, terrainColors[brushColor], (screenWidth - rightWidth / 2, rightWidth / 2 + 40), brushSize / dataRes * (rightWidth - 10))
        pygame.draw.circle(win, 0, (screenWidth - rightWidth / 2, rightWidth / 2 + 40), brushSize / dataRes * (rightWidth - 10), 1)
        for button in terrainButtons:
            button.draw()
            pygame.draw.rect(win, terrainColors[button.value], (button.x + 2, button.y + 2, button.width - 4, button.height - 4))
    
    elif mode == 3:
        midRight = screenWidth - (rightWidth / 2)
        pygame.draw.line(win, (100,100,100), (midRight, 55), (midRight, 230))
        drawText("Plate ID", arial, 0, screenWidth - rightWidth + 10, 55)
        drawText("Plate Color", arial, 0, screenWidth - rightWidth + 10, 75)
        drawText("Start Time", arial, 0, screenWidth - rightWidth + 10, 95)
        drawText("End Time", arial, 0, screenWidth - rightWidth + 10, 115)
        drawText("Current Pole", arial, 0, screenWidth - rightWidth + 10, 145)
        drawText("Current Speed", arial, 0, screenWidth - rightWidth + 10, 165)
        drawText("New Pole", arial, 0, screenWidth - rightWidth + 10, 195)
        drawText("New Speed", arial, 0, screenWidth - rightWidth + 10, 215)
        if selectedPlate:
            movementID = getMovementIndex(selectedPlate[1], time)
            drawText(str(selectedPlate[1]), arial, 0, midRight + 10, 55)
            drawText(str(plateData[0][selectedPlate[1]]), arial, 0, midRight + 10, 75)
            drawText(str(plateData[1][selectedPlate[1]][0][0]), arial, 0, midRight + 10, 95)
            drawText(str(plateData[1][selectedPlate[1]][0][-1]), arial, 0, midRight + 10, 115)
            currentpole = plateData[1][selectedPlate[1]][1][movementID]
            drawText(str((round(currentpole[0],2), round(currentpole[1],2), round(currentpole[2],2))), arial, 0, midRight + 10, 145)
            drawText(str(round(plateData[1][selectedPlate[1]][2][movementID], 2)), arial, 0, midRight + 10, 165)
            try:
                newpole = normalize(CROSS(selectedPlate[0],mouseVector))
                drawText(str((round(newpole[0],2), round(newpole[1],2), round(newpole[2],2))), arial, 0, midRight + 10, 195)
                drawText(str(round(acos(DOT3(selectedPlate[0],mouseVector)), 2)), arial, 0, midRight + 10, 215)
            except:
                s = pygame.Surface((rightWidth, 40)) # grey cover to indicate not in use
                s.set_alpha(128)
                s.fill((255,255,255))
                win.blit(s, (screenWidth - rightWidth + 10, 195))
            printButton.draw()
            drawText("(x to cancel)", arialBold, 0, midRight - 35, screenHeight - 30)
        else:
            s = pygame.Surface((rightWidth, screenHeight)) # grey cover to indicate not in use
            s.set_alpha(128)
            s.fill((255,255,255))
            win.blit(s, (screenWidth - rightWidth, 20))
        drawText("Plate Info:", arialBold, 0, screenWidth - rightWidth + 5, 30)
    
    if mouseOnGlobe:
        drawText("Mouse: (lat: "+str(round((mouseSpherical[0]-mouseTransform[1])/pi*180-90,2))+", lon: "+str(round(-fixPos(mouseSpherical[1]+mouseTransform[0]-pi/2)/pi*180,2))+")", arial, 0, leftWidth + 10, screenHeight - 17)
    else: 
        drawText("Mouse: Not on Globe", arial, 0, leftWidth + 10, screenHeight - 17)
    drawText("Location: (lat: "+str(round(-(position[1]+mouseTransform[1])/pi*180,2))+", lon: "+str(round(-(position[0]+mouseTransform[0])/pi*180,2))+")", arial, 0, screenWidth // 2 - 90, screenHeight - 17)
    drawText("Zoom: "+str(round(zoom/minZoom*100))+"%", arial, 0, screenWidth - rightWidth - 75, screenHeight - 17)

def drawDisplay():
    display.fill(0)
    pygame.draw.circle(display, 1, displayCenter, zoom) #sphere base
    
    r1, r2, r3, r4 = sin(position[0] + mouseTransform[0]), cos(position[0] + mouseTransform[0]), sin(position[1] + mouseTransform[1]), cos(position[1] + mouseTransform[1])
    
    tmp = pygame.PixelArray(display)
    
    plateColors = plateData[0]
    currentData = data[time]
    
    if see == 0:
        for xcoord in displayArrayW:
            x = (xcoord - displayCenter[0]) / zoom    #x coordinate, from -1 to 1
            x2, xr1, xr2 = 1-x**2, x*r1, x*r2
            for ycoord in displayArrayH:
                if tmp[xcoord,ycoord]: # check if in circle
                    z = (ycoord - displayCenter[1]) / zoom    #z coordinate, from -1 to 1

                    try:
                        y = sqrt(x2 - z ** 2) #y coordinate, from -1 to 1

                        y2 = y*r4 - z*r3 # perform rotations about x and z axes
                        z3 = y*r3 + z*r4
                        x3 = xr2 - y2*r1
                        y3 = xr1 + y2*r2
                    
                        latr = acos(z3)
                        rad = sin(latr)
                        tmp[xcoord,ycoord] = plateColors[currentData[trunc(latr * res1)][trunc(acos(x3 / rad) * sign(y3) * res1 * rad)][0]] #truncation optimization
                    except: pass
    else:
        for xcoord in displayArrayW:
            x = (xcoord - displayCenter[0]) / zoom    #x coordinate, from -1 to 1
            x2, xr1, xr2 = 1-x**2, x*r1, x*r2
            for ycoord in displayArrayH:
                if tmp[xcoord,ycoord]: # check if in circle
                    z = (ycoord - displayCenter[1]) / zoom    #z coordinate, from -1 to 1

                    try:
                        y = sqrt(x2 - z ** 2) #y coordinate, from -1 to 1

                        y2 = y*r4 - z*r3 # perform rotations about x and z axes
                        z3 = y*r3 + z*r4
                        x3 = xr2 - y2*r1
                        y3 = xr1 + y2*r2
                        
                        latr = acos(z3)
                        rad = sin(latr)
                        cell = currentData[trunc(latr * res1)][trunc(acos(x3 / rad) * sign(y3) * res1 * rad)]
                        if cell[1]:
                            tmp[xcoord,ycoord] = terrainColors[cell[1]]
                        else:
                            col1 = display.unmap_rgb(plateColors[cell[0]])
                            tmp[xcoord,ycoord] = (col1.r // 2.5, interpolate(100, col1.g, 0.4), interpolate(255, col1.b, 0.4))
                        
                        # tempcolor = pygame.Color(0,0,0)
                        # tempcolor.hsva = (currentData[trunc(latr * res1)][trunc(acos(x3 / rad) * sign(y3) * res1 * rad)][3] * 8, 100, 100)
                        # tmp[xcoord,ycoord] = tempcolor
                    except: pass

    drawLine(tmp, normalize((1,0.001,0)), normalize((-1,0.001,0)), 1000, (255,255,255,3))
    drawLine(tmp, normalize((1,-0.001,0)), normalize((-1,-0.001,0)), 1000, (255,255,255,3))
    drawLine(tmp, normalize((0,0.001,1)), normalize((0,0.001,-1)), 1000, (255,255,255,3))
    drawLine(tmp, normalize((0,-0.001,1)), normalize((0,-0.001,-1)), 1000, (255,255,255,3))
    drawLine(tmp, normalize((0.001,0,1)), normalize((0.001,0,-1)), 1000, (255,255,255,3))
    drawLine(tmp, normalize((-0.001,0,1)), normalize((-0.001,0,-1)), 1000, (255,255,255,3))

    if selectedPlate:
        try:
            movementID = getMovementIndex(selectedPlate[1], time) #index of plate's current movement
            drawLine(tmp, None, selectedPlate[0], 1000, (150,0,0,1), plateData[1][selectedPlate[1]][1][movementID], plateData[1][selectedPlate[1]][2][movementID]) # draw current movement
            drawLine(tmp, mouseVector, selectedPlate[0], 1000, (220,200,0,1)) # draw new movement
        except: pass

    tmp.close()

    win.blit(pygame.transform.scale(display, (screenWidth - leftWidth - rightWidth, screenHeight - 80)), (leftWidth,60)) #scale display to window

def makeButtons():
    global addButton, pickButton, printButton

    addButton = TapButton(add1, "New Plate")
    printButton = TapButton(print1, "Print Movements as Table")
    pickButton = ToggleButton(pick1, pick2, 0, name="Pick Plate")

    playButtons.append(TapButton(skip1, "Skip to Beginning"))
    playButtons.append(TapButton(step1, "Back"))
    playButtons.append(ToggleButton(play1, play2, True, name="Play"))
    playButtons.append(TapButton(step2, "Forward"))
    playButtons.append(TapButton(skip2, "Skip to End"))

    modeButtons.append(ToggleButton(move1, move2, 0, name="Move (1)", clicked=True, ismode=True))
    modeButtons.append(ToggleButton(drawPlate1, drawPlate2, 1, name="Draw Plates (2)", ismode=True))
    modeButtons.append(ToggleButton(drawTerrain1, drawTerrain2, 2, name="Draw Terrain (3)", ismode=True))
    modeButtons.append(ToggleButton(movePlate1, movePlate2, 3, name="Move Plates (4)", ismode=True))

    plateButtons.append(ToggleButton(color1, color2, 0, name="Blue", clicked=True))
    plateButtons.append(ToggleButton(color1, color2, 1, name="Green"))
    plateButtons.append(ToggleButton(color1, color2, 2, name="Red"))

    terrainButtons.append(ToggleButton(color1, color2, 0, name="Ocean", clicked=True))
    terrainButtons.append(ToggleButton(color1, color2, 1, name="Land"))
    terrainButtons.append(ToggleButton(color1, color2, 2, name="Mountain"))

def checkAllButtons():
    global brushColor, plateColor, terrainColor, picking

    if checkButtons(modeButtons):
        changeMode(readButtons(modeButtons))

    if playButtons[0].hover():
        setTime(0)
    if playButtons[1].hover():
        if time > 0:
            setTime(time-1)
    if playButtons[2].hover():
        playButtons[2].clicked = not playButtons[2].clicked
    if playButtons[3].hover():
        if time < 2000:
            setTime(time+1)
    if playButtons[4].hover():
        setTime(maxTime)

    if mode == 1:
        if pickButton.hover():
            picking = pickButton.clicked = not picking
        elif addButton.hover():
            newColor = entryWindow("Plate Id", 0, 36000)
            if newColor != -1:
                tempcolor = pygame.Color(0,0,0)
                tempcolor.hsva = (newColor // 100, 100, newColor % 100, 100)
                plateColor = brushColor = len(plateData[0]) # set to newest plate

                plateData[0].append(display.map_rgb(tempcolor)) # create new plate color
                plateData[1].append([[0], [(0, 0, 1)], [0]]) # create new plate movement
                plateData[2].append([]) # create new density coefficient table

                plateButtons.append(ToggleButton(color1, color2, brushColor)) # new plate button
                offButtons(plateButtons)
                plateButtons[brushColor].clicked = True
                sizeButtons()
        elif checkButtons(plateButtons):
            plateColor = brushColor = checkButtons(plateButtons) - 1
    elif mode == 2:
        if checkButtons(terrainButtons):
            terrainColor = brushColor = readButtons(terrainButtons)
    elif mode == 3:
        if selectedPlate:
            if printButton.hover():
                movementTable(selectedPlate[1])

def checkButtons(group):
    "Clicks toggle button in a group, and returns the index of that button in the list + 1."
    for n in range(len(group)):
        if group[n].hover():
            offButtons(group)
            group[n].clicked = True
            return n + 1

def checkSlider(slider:Slider):
    if slider.hover():
        slider.pos = (mouse[0] - slider.x) / slider.width
        return int(slider.low + slider.pos * (slider.high - slider.low))

def readButtons(group):
    for button in group:
        if button.clicked:
            return button.value

def offButtons(group):
    for button in group:
        button.clicked = False

def brush(layer:int, location:tuple):
    center = pixel3d(location)
    centerLat = int(vtoSpherical(center)[0] * res1)
    
    for lat in range(centerLat - brushSize, centerLat + brushSize):
        latData = data[time][lat]
        for cell in coordinates[lat]:
            if latData[cell[3]][layer] != brushColor:
                if DOT3(center, cell) > brushN:
                    latData[cell[3]][layer] = brushColor

def getMovementIndex(plateID, t):
    times = plateData[1][plateID][0]
    for n in times:
        if n > t: #after target time
            return times.index(n) - 1 # return the index before it
    return len(times) - 1 # if none larger, must be the last one

def fixPos(n):
    return (n + pi) % (2*pi) - pi

def drawLine(tmp, vector1, vector2, detail, color, pole = None, dist = None):
    if not pole:
        pole = normalize(CROSS(vector1, vector2))
        unit = acos(DOT3(vector1, vector2)) / detail
    else:
        unit = dist / detail
    changed = []
    r1, r2, r3, r4 = sin(-position[0]-mouseTransform[0]), cos(-position[0]-mouseTransform[0]), sin(-position[1]-mouseTransform[1]), cos(-position[1]-mouseTransform[1])
    for n in range(detail):
        pix = vectortoPixel(rotate(vector2, pole, unit * n), r1, r2, r3, r4)
        x = int(pix[0])
        y = int(pix[1])
        if pix[2] and x > 0 and y > 0 and not ([x,y] in changed):
            try:
                if tmp[x,y]:
                    col = display.unmap_rgb(tmp[x,y])
                    col.r += (color[0] - col.r) // color[3]
                    col.g += (color[1] - col.g) // color[3]
                    col.b += (color[2] - col.b) // color[3]
                    tmp[x,y] = col
                    changed.append([x,y])
            except: pass

def drawText(text:str, font, color, x, y):
    img = font.render(text, True, color)
    win.blit(img, (x,y))

def entryWindow(item:str, min:int, max:int):
    "Create a tkinter window that returns a user input in the range of [min, max]."
    global disableKeys
    disableKeys = 2

    root = tk.Tk()
    window = tkwindow.EntryWindow(root, item, min, max)
    root.mainloop()

    return window.out

def movementTable(plateID:int):
    "Create a tkinter ui window for direct editing of a plate's movement data."

    global disableKeys
    disableKeys = 2

    root = tk.Tk()
    window = tkwindow.MovementTableWindow(root, plateID, plateData[1][plateID])
    root.mainloop()
    
    if plateData[1][plateID] != window.data: # update plate's movement data
        plateData[1][plateID] = window.data
        if not 0 in plateData[1][plateID][0]: # if index 0 is missing (required for processing)
            plateData[1][plateID][0].insert(0,0)
            plateData[1][plateID][1].insert(0,[0,0,0])
            plateData[1][plateID][2].insert(0,0)
        simulateFutureTimesteps(0)

def rotate(v:tuple, pole:tuple, theta):
    "Returns a vector rotated around a pole by theta radians using Rodrigues' Rotation Formula."
    return np.array(v)*cos(theta) + np.array(CROSS(v,pole))*sin(theta) + np.array(pole)*DOT3(v,pole)*(1-cos(theta))

def DOT3(v1:tuple, v2:tuple):
    "Return the dot product of two 3-dimensional vectors."
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def CROSS(v1:tuple, v2:tuple):
    "Return the cross product vector of two 3-dimensional vectors."
    return (v1[1]*v2[2] - v1[2]*v2[1], v1[2]*v2[0] - v1[0]*v2[2], v1[0]*v2[1] - v1[1]*v2[0])

def normalize(v:tuple):
    "Normalize a 3d vector."
    l = sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
    return (v[0]/l, v[1]/l, v[2]/l)

def interpolate(a, b, n):
    return a + n*(b-a)

def pixeltoSpherical(pixel:tuple):
    """ Returns the spherical coordinates of a point on a sphere based on the point's location on the display.
        
        Output: (latitude, longitude) in radians"""
    return vtoSpherical(pixel3d(pixel))

def pixel3d(pixel:tuple):
    """ Returns the 3d cartesian coordinates of a point on a sphere based on the point's location on the display.
        
        Output: (x, y, z)"""
    x = (pixel[0] - displayCenter[0]) / zoom
    z = (pixel[1] - displayCenter[1]) / zoom
    try:
        y = sqrt(1 - x**2 - z**2)
        r1, r2, r3, r4 = sin(position[0]), cos(position[0]), sin(position[1]), cos(position[1])

        y2 = y*r4 - z*r3
        z3 = y*r3 + z*r4
        x3 = x*r2 - y2*r1
        y3 = x*r1 + y2*r2

        return (x3, y3, z3)
    except: pass

def vectortoPixel(v:tuple, r1=sin(-position[0]), r2=cos(-position[0]), r3=sin(-position[1]), r4=cos(-position[1])):
    """ Returns the pixel coordinates of a 3d vector on a sphere, and whether the pixel is visible or hidden.
        Only accepts normalized 3d vectors.
        
        Output: (x coordinate, y coordinate, visible?)"""

    x3 = v[0]*r2 - v[1]*r1
    y2 = v[0]*r1 + v[1]*r2
    y3 = y2*r4 - v[2]*r3
    z3 = y2*r3 + v[2]*r4

    xcoord = x3 * zoom + displayCenter[0]
    ycoord = z3 * zoom + displayCenter[1]
    return (xcoord, ycoord, y3 > 0)

def vtoSpherical(v:tuple):
    """ Returns the spherical coordinates of a 3d vector on a sphere.
        Only accepts normalized 3d vectors.
        
        Output: (latitude, longitude) in radians"""
    lat = acos(v[2])
    return (lat, acos(v[0] / sin(lat)) * sign(v[1]))

def colorFraction(color:int, fract:int):
    return color // 65536 // fract * 65536 + color // 256 % 256 // fract * 256 + color % 256 // fract

def sign(n):
    "Return the sign of a number."
    if n < 0: 
        return -1
    else:
        return n > 0

start()

pygame.quit()
sys.exit()
