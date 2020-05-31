from typing import List

import FileHandling


# todo add validateUser thing
class User:

    def __init__(self, userId=None, name="", phoneNo="", email="", address="", isBookIssued=False):
        # userId is none when we want to add new user And search
        # phone will be a string currently
        self.userId = None if userId is None else int(userId)
        self.name = name
        self.phoneNo = phoneNo
        self.address = address
        self.email = email
        self.isBookIssued = isBookIssued

    def addUser(self):
        if self.isBookIssued:
            raise Exception("New User cannot have issued Book before hand...")
        self.userId = self._getCount()
        self._writeFirstLine()

    @staticmethod
    def _getCount() -> int:
        count = 0
        try:
            count = int(FileHandling.readFirstLine("{}count".format(FileHandling.getFolderPath("users", ))))
            FileHandling.writeFirstLine(str(count + 1), "{}count".format(FileHandling.getFolderPath("users", )))
        except IOError:
            # file does not exist case
            FileHandling.writeFirstLine("0", "{}count".format(FileHandling.getFolderPath("users", )))
        finally:
            return count

    def updateUserData(self):
        self._writeFirstLine()

    def getUser(self) -> bool:
        # userId should be set before calling this function
        if self.userId is None:
            return False

        if not self.name:
            self.name = self._getUserNameFromId()

        self._readFirstLine()
        return True

    def searchUsers(self) -> 'List[User]':
        # Reason why '' around List[User] -> https://stackoverflow.com/questions/15741887
        files = FileHandling.getFilesByString(self.name, FileHandling.getFolderPath("users", ))
        users: List[User] = list()
        for file in files:
            data = file.split("-")
            users.append(User(data[0], data[1]))
        return users

    def _writeFirstLine(self):
        filename = "{}{}-{}".format(FileHandling.getFolderPath("users", ), self.userId,
                                    self.name)  # filename = users/userId-username
        # stringToWrite = "1====Name====123456====email@ex.com====h 43, Delhi====0"
        stringToWrite = "{}===={}===={}===={}===={}===={}".format(self.userId, self.name, self.phoneNo, self.email,
                                                                  self.address, int(self.isBookIssued))
        FileHandling.writeFirstLine(stringToWrite, filename)

    def _readFirstLine(self):
        filename = "{}{}-{}".format(FileHandling.getFolderPath("users", ), self.userId,
                                    self.name)
        # filename = users/userId-username
        firstLine = FileHandling.readFirstLine(filename)
        items = firstLine.split("====")
        if self.userId != int(items[0]):
            raise Exception("UserId Not Matched with FileName....")

        self.phoneNo = items[2]
        self.email = items[3]
        self.address = items[4]
        self.isBookIssued = bool(int(items[5]))

    def _getUserNameFromId(self) -> str:
        files = FileHandling.getFilesByString(str(self.userId), FileHandling.getFolderPath("users", ))
        if len(files) > 1:
            raise Exception("Error More than One files with Same UserId")
        return files[0].split("-")[1]

    def __eq__(self, other: object) -> bool:
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
