from pathlib import Path
import math

#log feature
logPath = Path(__file__).resolve().parent / "log.txt"

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

def init():
    with open(logPath, "w") as file:
        file.write("")