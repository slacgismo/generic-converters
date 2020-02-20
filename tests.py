import unittest
from unittest.mock import Mock
from unittest.mock import patch
import converters.json2glm
import converters.json2png


class TestJson2Glm(unittest.TestCase):

    def test_clock_glm(self):
        result = json2glm.clock_glm()
        self.assertTrue(result)

    def test_classes_glm(self):
        result = json2glm.classes_glm()
        self.assertTrue(result)

    def test_globals_glm(self):
        result = json2glm.globals_glm()
        self.assertTrue(result)

    def test_objects_glm(self):
        result = json2glm.objects_glm()
        self.assertTrue(result)

    def test_json2glm(self):
        result = json2glm.json2glm()


class TestJson2Png(unittest.TestCase):

    def test_json2png(self):
        result = json2glm.json2glm()



if __name__ == '__main__':
    unittest.main()
