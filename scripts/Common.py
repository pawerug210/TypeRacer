

def addNonePadding(array, desiredLength):
    return array + ([None] * (desiredLength - len(array)))


def applyMask(data, mask, value):
    return (d for d, s in zip(data, mask) if s == value)

def readFile(filename):
    f = open(filename, "r", encoding='utf-8')
    return f.read()