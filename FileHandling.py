import os
from fileinput import FileInput
from typing import List


def createFilesIfNotExist(filePath: str):
    lastIndex = filePath.rfind('/')
    if lastIndex == (len(filePath) - 1):
        raise Exception("File cannot be a directory")

    if os.path.exists(filePath):
        return

    if os.path.exists(filePath[0: lastIndex]):
        # only file does not exist therefore returning early
        with open(filePath, 'w') as f:  # writing empty file
            pass
        return

    currentIndex = filePath.find('/', 0)
    # just some optimizations
    isParentFolderExist = True
    for i in range(0, len(filePath)):
        fileString = filePath[0: currentIndex]
        if (not isParentFolderExist) or (not os.path.exists(fileString)):
            # according docs python first evaluates first condition and only checks second if first is false
            os.mkdir(fileString)
            isParentFolderExist = False
        if currentIndex == lastIndex:
            break
        currentIndex = filePath.find('/', currentIndex + 1)

    with open(filePath, 'w') as f:  # writing empty file
        pass


def writeFirstLine(string: str, filePath: str):
    createFilesIfNotExist(filePath)
    if os.path.getsize(filePath) == 0:
        # fileIsEmpty
        with open(filePath, 'w') as f:  # writing empty file
            f.write(string + '\n')
    else:
        with FileInput(filePath, inplace=True) as f:
            for line in f:
                if f.isfirstline():
                    print(string, end='\n')
                else:
                    print(line, end='')


def writeLastLine(string: str, filePath: str):
    # simply appending the text
    # skipping file exist checks
    with open(filePath, 'a') as f:
        f.write(string + '\n')


def writeLineBySpecifiedId(string: str, filePath: str, Id: str):
    with FileInput(filePath, inplace=True) as f:
        for line in f:
            if line.startswith(Id):  # replace line with string passed, if line contains the specified Id
                print(string, end='\n')
            else:
                print(line, end='')


def readFirstLine(filePath: str) -> str:
    with open(filePath, 'r') as f:
        f.seek(0)
        string = f.readline()
    return string[:-1]  # removing last '\n' in the string


def readLastLine(filePath: str) -> str:
    with open(filePath, 'r') as f:
        f.seek(0, os.SEEK_END)
        backStep = 2
        f.seek(f.tell() - backStep, os.SEEK_SET)
        ch = f.read(1)
        readLine = ch
        while True:
            # if (f.tell() - backStep) < 0: break skipping this check as we will always use readFirstLine to read First
            f.seek(f.tell() - backStep, os.SEEK_SET)
            ch = f.read(1)
            if ch == '\n':
                break
            readLine = readLine + ch
    return readLine[::-1]  # reverse the string and return


def readLineBySpecifiedId(filePath: str, Id: str):
    # we can optimize this function but we will do that later
    with open(filePath, 'r') as f:
        for line in f:
            if line.startswith(Id):
                lineString = line
                break
    return lineString[:-1]  # remove the last '\n'


def readContinuousLines(filePath: str, count: int = 10, shouldSkipFirstLine: bool = False):
    # will create this function when needed
    pass


def getFilesByString(string: str, folderPath: str) -> List[str]:
    # have not added sorting to this.
    files: List[str] = list()
    for file in os.listdir(folderPath):
        if string in file:
            files.append(file)
    return files
