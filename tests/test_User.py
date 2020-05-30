from unittest import TestCase, mock

from User import User


class TestUser(TestCase):

    def test__AddingUser(self):
        user = User(None, "Name", "123456", "email@ex.com", "h 43, Delhi", False)
        with mock.patch("FileHandling.readFirstLine", side_effect=IOError) as mockRead, \
                mock.patch("FileHandling.writeFirstLine") as mockWrite:
            user.userId = user._getCount()
            self.assertEqual(0, user.userId)
            mockRead.assert_called_once_with("users/count")
            mockWrite.assert_called_once_with("0", "users/count")

        with mock.patch("FileHandling.writeFirstLine") as mockWrite:
            user._writeFirstLine()
            string = "0====Name====123456====email@ex.com====h 43, Delhi====0"
            mockWrite.assert_called_once_with(string, "users/0-Name")

    def test__GetUser(self):
        user = User(0)
        with mock.patch("FileHandling.getFilesByString", return_value=["0-Name", ]) as mockFiles:
            name = user._getUserNameFromId()
            self.assertEqual("Name", name)
            user.name = name
            mockFiles.assert_called_once_with("0", "users/")

        with mock.patch("FileHandling.readFirstLine",
                        return_value="0====Name====123456====email@ex.com====h 43, Delhi====0") as mockRead:
            user._readFirstLine()
            self.assertEqual(0, user.userId)
            self.assertEqual("Name", user.name)
            self.assertEqual("123456", user.phoneNo)
            self.assertEqual("email@ex.com", user.email)
            self.assertEqual("h 43, Delhi", user.address)
            self.assertEqual(False, user.isBookIssued)
            mockRead.assert_called_once_with("users/0-Name")

    def test_GetCount(self):
        # checked IOError exception already so not checking that
        user = User(None, "Name", "123456", "email@ex.com", "h 43, Delhi", False)
        count = 0
        with mock.patch("FileHandling.readFirstLine") as mockRead, \
                mock.patch("FileHandling.writeFirstLine") as mockWrite:
            mockRead.return_value = count
            self.assertEqual(0, user._getCount())
            mockRead.assert_called_with("users/count")
            mockWrite.assert_called_with("1", "users/count")
            count = count + 1
            mockRead.return_value = count
            self.assertEqual(1, user._getCount())
            mockRead.assert_called_with("users/count")
            mockWrite.assert_called_with("2", "users/count")

    def test_SearchUsers(self):
        user0 = User(0, "Name0")
        user1 = User(1, "Name1")
        user2 = User(2, "Name2")
        user3 = User(3, "Nam2")
        with mock.patch("FileHandling.getFilesByString") as mockSearch:
            user = User(None, name="Name")
            mockSearch.return_value = ["0-Name0", "1-Name1", "2-Name2"]
            users = user.searchUsers()
            self.assertEqual(len(users), 3)
            self.assertEqual(user0, users[0])
            self.assertEqual(user1, users[1])
            self.assertEqual(user2, users[2])
            mockSearch.assert_called_with("Name", "users/")

            user = User(None, name="Nam")
            mockSearch.return_value = ["3-Nam2", ]
            users = user.searchUsers()
            self.assertEqual(len(users), 1)
            self.assertEqual(user3, users[0])
            mockSearch.assert_called_with("Nam", "users/")
