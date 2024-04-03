import os

PATH = os.path.join(os.path.dirname(__file__), "Assets")

class Highscores:
    class Entry:
        def __init__(self, name: str, score):
            # force 3 long
            if (len(name) < 3):
                name += ' ' * (3 - len(name))

            elif (len(name) > 3):
                name = name[:3]
            
            self.name = name
            self.score = score

        def fromStr(string: str):
            # an entry should look like "BOB,1234"

            if (len(string) <= 4):
                # a broken name that shouldn't exist
                raise ValueError("Highscore string too small")

            # hackey slicing
            name = string[:3]
            score = float(string[4:])

            return Highscores.Entry(name, score)

    def loadFromList(self, scores: list[str]):
        # an entry should look like "BOB,1234"

        # add all entries then sort
        for score in scores:
            try:
                self.scores.append(Highscores.Entry.fromStr(score))
            except ValueError:
                continue

        self.scores.sort(key = lambda entry: entry.score, reverse=True)

    def insertScore(self, name : str, score):
        self.scores.append(Highscores.Entry(name, score))

        # I know this is slow.
        # Python doesn't have a builtin Binary Search (why???)
        # Python is actually really bad a sorting things well
        self.scores.sort(key = lambda entry: entry.score, reverse=True)

    def loadScores(self):
        self.scores : list[Highscores.Entry] = []

        file_path = os.path.join(PATH, "highscores.txt")

        # open file and load (if the file exists)
        try:
            with open(file_path, "r") as file:
                self.loadFromList(file.readlines())
        
        except FileNotFoundError:
            with open(file_path, "w") as file:
                pass

    def saveScores(self):
        file_path = os.path.join(PATH, "highscores.txt")

        with open(file_path, "w") as file:
            for score in self.scores:
                file.write(score.name + ',' + str(score.score) + '\n')

    def __init__(self):
        self.loadScores()
 