import curses

import pywinctl as pw
import sys
import subprocess

from utils.generalFunctions import print

currentWindows = []

def main(stdscr: "curses.window", height, width, keybinds, currentSong):
    print("currentSong")
    while True:
        stdscr.erase()
        stdscr.refresh()
        pass

def createTerminalWindow(code):
    if sys.platform == "win32":
        currentWindows.append(
            subprocess.Popen(
                [sys.executable, str(code)],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        )

