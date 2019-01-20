

class TypeRacerHelper(object):

    def __init__(self, text=[]):
        self.Text = text
        self.UserText = []
        self._correctness = []

    def setText(self, text):
        self.Text = text
        self.UserText = []
        self._correctness = []

    def addChar(self, char):
        self.UserText.append(char)
        self._correctness.append(self._isCharCorrect(char, len(self._correctness)))

    def removeChar(self):
        del self.UserText[-1]
        del self._correctness[-1]

    def isNewWord(self):
        return self.UserText[-1] == ' ' and all(self._correctness)

    def getCorrectnessList(self):
        return self._correctness

    def _isCharCorrect(self, char, index):
        return self.Text[index] == char and self._correctness[-1]
