import unittest

import os
import sys

import highscore

# python is such a well designed language
sys.path.append(os.getcwd() + "/src/game")

class HighscoreTests(unittest.TestCase):
    def setUp(self):
        self.scores = highscore.Highscores()
        self.scores.clearScores()
        self.scores.insertScore(' A ', 5)
        self.scores.insertScore('JOE', 199)
        self.scores.insertScore('EVE', 190)
        self.scores.insertScore('BOB', 200)

    def test_save_load(self):
        self.scores.saveScores()
        tmp = self.scores.get()
        self.scores.clearScores()

        self.assertEqual(self.scores.loadScores(), len(tmp))
        self.assertListEqual(tmp, self.scores.get())

    def test_highest(self):
        entry = highscore.Highscores.Entry('WIN', 9999)
        self.scores.insertScore(entry.name, entry.score)
        self.assertEqual(self.scores.get()[0], entry)

        self.test_save_load()

    def test_lowest(self):
        entry = highscore.Highscores.Entry(':( ', -100)
        self.scores.insertScore(entry.name, entry.score)
        self.assertEqual(self.scores.get()[-1], entry)

        self.test_save_load()

    def test_middle(self):
        entry = highscore.Highscores.Entry(':| ', 195)
        self.scores.insertScore(entry.name, entry.score)
        self.assertEqual(self.scores.get()[2], entry)

        self.test_save_load()

    def test_blank_name(self):
        entry = highscore.Highscores.Entry('   ', 123)
        self.scores.insertScore(entry.name, entry.score)

        for score in self.scores.get():
            self.assertNotEqual(score.name, '   ')

        self.test_save_load()

    def test_truncation(self):
        entry = highscore.Highscores.Entry('Jackson', 321)
        self.scores.insertScore(entry.name, entry.score)

        entry.name = 'Jac'
        self.assertEqual(self.scores.get()[0], entry)
        self.test_save_load()

    def test_expanding(self):
        entry = highscore.Highscores.Entry('me', 99999)
        self.scores.insertScore(entry.name, entry.score)

        entry.name = 'me '
        self.assertEqual(self.scores.get()[0], entry)
        self.test_save_load()