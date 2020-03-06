import unittest
from unittest.mock import Mock
from unittest.mock import patch
import json
from converters.json2glm import *
from converters.json2png import *


class TestJson2Glm(unittest.TestCase):

    def test_clock_glm(self):
        with open("./test_files/test.json", 'r') as fr:
            data = json.load(fr)
        result = clock_glm(data, "test.glm")
        self.assertTrue(result)

    def test_classes_glm(self):
        with open("./test_files/test.json", 'r') as fr:
            data = json.load(fr)
        result = classes_glm(data, "test.glm")
        self.assertTrue(result)

    def test_globals_glm(self):
        with open("./test_files/test.json", 'r') as fr:
            data = json.load(fr)
        result = globals_glm(data, "test.glm")
        self.assertTrue(result)

    def test_objects_glm(self):
        with open("./test_files/test.json", 'r') as fr:
            data = json.load(fr)
        result = objects_glm(data, "test.glm")
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
