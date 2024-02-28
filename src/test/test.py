import unittest
import pygame
import os

class TestTests(unittest.TestCase):

    # a test to test if testing works,
    # should always pass
    def test_test(self):
        self.assertTrue(True)


if __name__ == "__main__":
    pygame.init()

    for file in os.scandir("./src/test/"):
        if (file.is_file()):
            if (file.name.endswith(".py")):
                print("Running tests from " + file.name + ':')
                unittest.main(module=file.name[:-3], verbosity=2, exit=False)

    pygame.quit()