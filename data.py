#cython: language_level=3

import os
import sys
import glob
import json

DATABASE_FILENAME = 'database.json'


def popTextFile(filename: str) -> str:
    with open(getFileName(filename), 'r') as f:
        lines = f.readlines()

    # If we have no lines, then return none
    if len(lines) == 0:
        return None
    popped = lines[0]

    # Save the new file without the first one
    with open(getFileName(filename), 'w') as f:
        # If we have more than one line, then write the rest of them to the file
        if len(lines) > 1:
            for i in lines[1:]:
                f.write(i)

    return popped


def updateJson(path: str, data: dict):
    try:
        d = loadJSON(path)
    except FileNotFoundError:
        d = {}
    d.update(data)
    saveJSON(path, d)


def getLineFromTextFile(filename: str) -> str:
    with open(getFileName(filename), 'r') as f:
        return f.readline().strip()


def deleteLineFromTextFile(line: str, filename: str):
    with open(getFileName(filename), 'r') as f:
        lines = f.readlines()

    with open(getFileName(filename), 'w') as f:
        for i in lines:
            if line in i:
                continue
            f.write(i)


def saveToTextFile(data: str, path: str):
    data = data.strip()
    with open(getFileName(path), 'a') as f:
        if isFileEmpty(path):
            f.write(data)
        else:
            f.write('\n' + data)


def getFileName(path: str):
    directory = ''
    if getattr(sys, 'frozen', False):
        if os.name == 'nt':
            directory = sys.executable[:sys.executable.rfind('\\')]
        else:
            directory = sys.executable[:sys.executable.rfind('/')]
    return os.path.join(directory, path)


def saveListToTextFile(data: list, path: str):
    with open(getFileName(path), 'a') as f:
        fileEmpty = isFileEmpty(path)

        for i in data:
            if fileEmpty:
                f.write(i.strip())
                fileEmpty = False
            else:
                f.write('\n' + i.strip())


def isFileEmpty(fileName: str) -> bool:
    return os.stat(fileName).st_size == 0


def loadJSON(fileName: str) -> dict:
    with open(getFileName(fileName), 'r') as f:
        return json.load(f)


def saveJSON(path: str, data: dict):
    path = getFileName(path)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    return True
