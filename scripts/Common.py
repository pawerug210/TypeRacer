

def addNonePadding(array, desiredLength):
    return array + ([None] * (desiredLength - len(array)))


def applyMask(data, mask, value):
    return (d for d, s in zip(data, mask) if s == value)