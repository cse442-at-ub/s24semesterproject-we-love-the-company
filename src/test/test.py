import unittest
import pygame

class TestTests(unittest.TestCase):

    # a test to test if testing works,
    # should always pass
    def test_test(self):
        self.assertTrue(True)


if __name__ == "__main__":
    pygame.init()

    unittest.main(verbosity=2, exit=False)

    unittest.main(module="menus", verbosity=2, exit=False)

    unittest.main(module="grids", verbosity=2, exit=False)

    unittest.main(module="cache", verbosity=2, exit=False)
    
    pygame.quit()