from typing import List

import FileHandling


class User:

    def __init__(self, userId=None, name="", phoneNo="", address="", email="", isBookIssued=False):
        # userId is none when we want to add new user
        # phone will be a string currently
        self.userId = userId
        self.name = name
        self.phoneNo = phoneNo
        self.address = address
        self.email = email
        self.isBookIssued = isBookIssued

    def addUser(self):
        if self.isBookIssued:
            raise Exception("New User cannot have issued Book before hand...")
        self._writeFirstLine()

    def updateUserData(self):
        self._writeFirstLine()

    def getUser(self) -> bool:
        # userId should be set before calling this function
        if self.userId is None:
            return False

        if not self.name:
            self._setUserNameFromId()

        self._readFirstLine()
        return True

    def searchUsers(self) -> List[User]:
        files = FileHandling.getFilesByString(self.name, "users/")
        users: List[User] = list()
        for file in files:
            data = file.split("-")
            users.append(User(data[0], data[1]))
        return users

    def _writeFirstLine(self):
        filename = "users/{}-{}".format(self.userId, self.name)  # filename = users/userId-username
        # stringToWrite = "1====Name====123456====email@ex.com====h 43, Delhi====0"
        stringToWrite = "{}===={}===={}===={}===={}===={}".format(self.userId, self.name, self.phoneNo, self.email,
                                                                  self.address, int(self.isBookIssued))
        FileHandling.writeFirstLine(stringToWrite, filename)

    def _readFirstLine(self):
        filename = "users/{}-{}".format(self.userId, self.name)  # filename = users/userId-username
        firstLine = FileHandling.readFirstLine(filename)
        items = firstLine.split("====")
        if self.userId != items[0]:
            raise Exception("UserId Not Matched with FileName....")

        self.phoneNo = items[2]
        self.email = items[3]
        self.address = items[4]
        self.isBookIssued = bool(items[5])

    def _setUserNameFromId(self):
        files = FileHandling.getFilesByString(self.userId, "users/")
        if len(files) > 1:
            raise Exception("Error More than One files with Same UserId")
        self.name = files[0].split("-")[1]
