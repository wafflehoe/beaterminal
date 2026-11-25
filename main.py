import curses
from pathlib import Path
import json

# main menu stuff
import time
import math
from datetime import datetime
import random

#other modules for menus
import utils.songPicker



#log feature
logPath = Path(__file__).resolve().parent / "log.txt"
location = "mainMenu"

#config (options)
optionsPath = Path(__file__).resolve().parent / "config" / "basicConfig.json"
optionsPath.resolve()


def getKeybinds():
    with open(optionsPath, "r") as file:
        jsonified = json.load(file)

    return jsonified["keybinds"]

def returnKeybinds(keybinds, upFunc = None, downFunc = None, leftFunc = None, rightFunc = None, enterFunc = None, anyFunc = None):
    trueKeybinds = {}
    actions = {
      "up": upFunc,
      "down": downFunc,
      "left": leftFunc,
      "right": rightFunc,
      "enter": enterFunc,
    }
    for key, action in keybinds.items():
        whichKeybind = actions.get(action)
        if whichKeybind:
            try:
                key = int(key)
            except:
                pass
            trueKeybinds[key] = actions[action] 
        elif anyFunc:
            trueKeybinds[key] = anyFunc
    return trueKeybinds
            

def print(*args):
    with open(logPath, "a") as file:
        for i in range(len(args)):
            file.write(str(args[i]) + " ")
        file.write("\n")

def centerText(text, width, percentage) -> int:
    return int(width * percentage) - math.floor(len(text)/2) 






def mainMenu(stdscr: "curses.window", height, width, keybinds):
    # minecraft like text for the menu uptop
    splashTextEndings = [
        "the worst rhythm game ever",
        "the only game to actively steal your soul",
        "why did i make this",
        "sorry my bedtime's " + str(datetime.now().hour % 12) + "PM zZZ",
        f"XxxausYhwher {"red sus"} JiwjnnnXCiXxxausIn"
    ]
    randomNumber = random.randint(0, len(splashTextEndings) - 1)
    splashText = f"beaterminal: {splashTextEndings[randomNumber]}"
    optionChosen = 1
    page = "mainMenu"
    options = {
        "mainMenu": [
            "Options",
            "Play",
            "Notes"
        ]
    }
    #key definitions, what should happen when I press up? left?
    def keyUp():
        if (page == "mainMenu"):
            print("up")

    def keyLeft():
        nonlocal optionChosen
        if (page == "mainMenu"):
            optionChosen = max(0, optionChosen - 1)

    def keyDown():
        if (page == "mainMenu"):
            print("up")
    
    def keyRight():
        nonlocal optionChosen
        if (page == "mainMenu"):
            optionChosen = min(2, optionChosen + 1)

    def keyEnter():
        nonlocal optionChosen
        global location
        if (page == "mainMenu"):
            if (optionChosen == 1):
                location = "songSelect"

    # keys = {
    #     curses.KEY_UP: keyUp,
    #     curses.KEY_LEFT: keyLeft,
    #     curses.KEY_RIGHT: keyRight,
    #     curses.KEY_DOWN: keyDown,
    #     curses.KEY_ENTER: keyEnter,
    #     10: keyEnter,
    #     13: keyEnter,
    # }

    keys = returnKeybinds(
        keybinds,
        keyUp,
        keyDown,
        keyLeft,
        keyRight,
        keyEnter
        )

    print(keys)
    backgroundElements: list[list[int]] = []
    timeSinceLastDrop = 0

    # render the main menu

    def renderMainMenu():
        # background
        nonlocal backgroundElements
        nonlocal timeSinceLastDrop    

        stdscr.erase()
        for i in range(len(backgroundElements)):
            if (timeSinceLastDrop == 0):
                if (random.randint(0,12) == 0):
                    if (backgroundElements[i][0] - 1 <= 0):
                        backgroundElements[i][0] += 1
                    elif (backgroundElements[i][0] + 1 >= width):
                        backgroundElements[i][0] -= 1
                    else:
                        if (random.randint(0,1) == 0):
                            backgroundElements[i][0] += 1
                        else:
                            backgroundElements[i][0] -= 1
                backgroundElements[i][1] += 1
            if (backgroundElements[i][1] < height - 1):
                stdscr.addch(backgroundElements[i][1], backgroundElements[i][0], "O")


        if (timeSinceLastDrop == 0):
            timeSinceLastDrop = random.randint(5000, 7000)
            for i in range(width):
                if (random.randint(0, 300) == 0):
                    backgroundElements.append([i, 1])
        else:
            timeSinceLastDrop -= 1
        
        #actual options
        stdscr.addstr(0, centerText(splashText, width, 1/2), splashText, curses.A_BOLD)
        stdscr.addstr(int(height/2), centerText(options[page][0], width, 1/4), options[page][0])
        stdscr.addstr(int(height/2), centerText(options[page][1], width, 2/4), options[page][1])
        stdscr.addstr(int(height/2), centerText(options[page][2], width, 3/4), options[page][2])    
        # cursor
        stdscr.addch(int(height/2), centerText(options[page][optionChosen], width, (optionChosen + 1)/4) - 1, ">")
    
    # main game loop
    while True:        
        global location
        key = stdscr.getch()        
        if (location != "mainMenu"):
            break
                
        if (page == "mainMenu"):
            renderMainMenu()        
            handler = keys.get(key)
            if handler:
                handler()


    pass

chosenSong = ([])
with open(logPath, "w") as file:
    file.write("")

def main(stdscr: 'curses.window'):   
    keybinds = getKeybinds()
    stdscr.clear() 
    while True:

        curses.initscr()
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.keypad(True)

        global location
        global chosenSong
        height, width = stdscr.getmaxyx()
        match location:
            case "mainMenu":
                mainMenu(stdscr, height, width, keybinds)
            case "songSelect":
                location, chosenSong = utils.songPicker.main(stdscr, height, width, keybinds)
                print(chosenSong)
            case "songLoader":
                
            

if __name__ == "__main__":
    curses.wrapper(main)