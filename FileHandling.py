import os
from fileinput import FileInput


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


def writeStringAtFirstLine(string: str, filePath: str):
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


def writeStringAtLastLine(string: str, filePath: str):
    pass


def writeStringAtLineSpecifiedById(string: str, filePath: str, id: str):
    pass


def readFirstLine(filePath: str) -> str:
    with open(filePath, 'r') as f:
        f.seek(0)
        string = f.readline()
    return string


def readLastLine(filePath: str):
    pass


def readLineBySpecifiedId(filePath: str, id: str):
    pass


def readContinuousLines(filePath: str, count: int = 10, shouldSkipFirstLine: bool = False):
    pass
