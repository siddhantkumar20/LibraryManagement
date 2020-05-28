import shutil
from unittest import TestCase

from FileHandling import *


class Test(TestCase):
    def test_CreateFileIfNotExist(self):
        os.mkdir("tempPath")
        self.addCleanup(lambda: shutil.rmtree("tempPath"))
        fileName = "tempPath/a/b/c/d/e/file"
        createFilesIfNotExist(fileName)
        self.assertTrue(os.path.exists(fileName))
        self.assertTrue(os.path.isfile(fileName))

    def test_WriteAndReadFirstLine(self):
        os.mkdir("tempPath")
        self.addCleanup(lambda: shutil.rmtree("tempPath"))
        filename = "tempPath/fileName"
        string = "1====Name====123456====email@ex.com====h 43, Delhi"
        writeStringAtFirstLine(string, filename)
        self.assertEqual(string + '\n', readFirstLine(filename))
