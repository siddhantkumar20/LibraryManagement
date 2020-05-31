import shutil
from unittest import TestCase

from FileHandling import *


class TestFileHandling(TestCase):
    def test_CreateFileIfNotExist(self):
        os.mkdir("tempPath")
        self.addCleanup(lambda: shutil.rmtree("tempPath"))
        fileName = "tempPath/a/b/c/d/e/file"
        createFilesIfNotExist(fileName)
        self.assertTrue(os.path.exists(fileName))
        self.assertTrue(os.path.isfile(fileName))

    def test_GetFolderPath(self):
        folderPath = "tempPath/a/b/c/d/e/"
        self.assertEqual(folderPath, getFolderPath("tempPath", "a", "b", "c", "d", "e"))
        self.assertEqual("users/", getFolderPath("users", ))

    def test_WriteAndReadFirstLine(self):
        os.mkdir("tempPath")
        self.addCleanup(lambda: shutil.rmtree("tempPath"))
        filename = "tempPath/fileName"
        string = "1====Name====123456====email@ex.com====h 43, Delhi"
        writeFirstLine(string, filename)
        self.assertEqual(string, readFirstLine(filename))

    def test_WriteAndReadLastLine(self):
        os.mkdir("tempPath")
        self.addCleanup(lambda: shutil.rmtree("tempPath"))
        filename = "tempPath/fileName"
        string = "1====Name====123456====email@ex.com====h 43, Delhi"
        writeFirstLine("SomeRandomText", filename)  # this is necessary else the test will break
        writeLastLine(string, filename)
        self.assertEqual(string, readLastLine(filename))

    def test_WriteThenReadThenWriteAtIdAndThenReadAtId(self):
        os.mkdir("tempPath")
        self.addCleanup(lambda: shutil.rmtree("tempPath"))
        filename = "tempPath/fileName"
        string1 = "1====Name====123456====email@ex.com====h 43, Delhi"
        string2 = "2====Name====123456====email@ex.com====h 43, Delhi"
        string3 = "3====Name====123456====email@ex.com====h 43, Delhi"
        string4 = "4====Name====123456====email@ex.com====h 43, Delhi"
        writeFirstLine(string1, filename)
        writeLastLine(string2, filename)
        writeLastLine(string3, filename)
        writeLastLine(string4, filename)
        self.assertEqual(string2, readLineBySpecifiedId(filename, "2"))
        testString = "3====Name====12345678910====email@ex.com====h 43, Delhi"
        writeLineBySpecifiedId(testString, filename, "3")
        self.assertEqual(testString, readLineBySpecifiedId(filename, "3"))

    def test_getFilesByString(self):
        os.mkdir("tempPath")
        self.addCleanup(lambda: shutil.rmtree("tempPath"))
        createFilesIfNotExist("tempPath/0-name0")  # I should not use this function to create files but
        createFilesIfNotExist("tempPath/1-name1")  # just leave it for this time
        createFilesIfNotExist("tempPath/2-name2")
        createFilesIfNotExist("tempPath/3-name3")
        files = getFilesByString("2", "tempPath/")
        self.assertEqual(1, len(files))
        self.assertEqual("2-name2", files[0])
        files = getFilesByString("name", "tempPath/")
        self.assertEqual(4, len(files))
