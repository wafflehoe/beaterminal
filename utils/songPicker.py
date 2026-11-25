import curses
from main import centerText, returnKeybinds, print
from pathlib import Path

# song metadata
import tomllib


loadedSongs = []

def loadSong(folder: Path):
    with open(folder.resolve() / "songDetails.toml", "rb") as file:
        dictionary = tomllib.load(file)
    name = dictionary['songDetails']['name']
    mainFile = folder.resolve() / dictionary['map']['entryFile']
    song = folder.resolve() / dictionary['songDetails']['songFile']
    loadedSongs.append([folder, name, mainFile, song])
    return True

menu = "songSelect"
optionChosenBottom = 2
chosenSong = []

def renderSongSelection(stdscr:"curses.window", height, width, keybinds):
    global menu
    #top text
    menuText = "Loaded Songs"
    stdscr.addstr(0, centerText(menuText, width, 1/2), menuText)
    stdscr.addstr(1, centerText("-" * width, width, 1/2), "-" * width)
    #register keybinds
    def keyEnter():
        global menu
        global chosenSong

        global optionChosenBottom
        if (menu == "songSelect"):
            if (len(loadedSongs) > 0):
                menu = "options"
                chosenSong = loadedSongs[currentRow - 3] 
        elif (menu == "options"):
            if (optionChosenBottom == 2):
                return (True, "songLoader", chosenSong)

    def keyLeft():
        global menu
        global optionChosenBottom
        if (menu == "options"):
            print("left pressed", optionChosenBottom - 1)
            optionChosenBottom = max(0, optionChosenBottom - 1)
            print(optionChosenBottom)

    def keyRight():
        global menu
        nonlocal options
        global optionChosenBottom
        if (menu == "options"):
            print("right pressed", menu)
            optionChosenBottom = min(len(options) - 1, optionChosenBottom + 1)
            print(optionChosenBottom)


    keys = returnKeybinds(keybinds, enterFunc=keyEnter, leftFunc=keyLeft, rightFunc=keyRight)

    #load songs in ./maps
    currentRow = 3
    maxRows = 3
    mapFolder = Path(__file__).resolve().parent.parent / "maps"
    for item in mapFolder.rglob("*"):
        if item.is_dir():
            try:
                if loadSong(item):
                    songName = loadedSongs[len(loadedSongs) - 1][1]
                    stdscr.addstr(maxRows, centerText(songName, width, 1/2), songName)
                maxRows += 1
            except Exception as e:
                pass
    if (len(loadedSongs) <= 0):
        menu = "options"
    if (menu == "songSelect"):
        if (len(loadedSongs) > 0):
            stdscr.addch(currentRow, centerText(loadedSongs[currentRow - 3][1], width, 1/2) - 1, ">")

                
    #bottom options
    options = [
        "Modifiers",
        "Delete",
        "Open",
        "Refresh",
        "Back"
    ]
    if (menu == "options"):
        stdscr.addstr(height - 1, centerText(options[optionChosenBottom], width, (optionChosenBottom + 1)/(len(options) + 1)) - 1, ">")
        
    stdscr.addstr(height - 2, centerText("-" * width, width, 1/2), "-" * width)
    for i in range(len(options)):
        stdscr.addstr(height - 1, centerText(options[i], width, (i + 1)/(len(options) + 1)), options[i])

    key = stdscr.getch()
    handler = keys.get(key)
    global chosenSong
    if handler:
        test = handler()
        if test:
            chosenSong = test


def main(stdscr: "curses.window", height, width, keybinds):
    while True:
        stdscr.erase()
        renderSongSelection(stdscr, height, width, keybinds)
        global chosenSong
        if len(chosenSong) > 0:
            if (chosenSong[0] == True):
                print("lol")
                return (chosenSong[1], chosenSong[2])
        stdscr.refresh()
        pass