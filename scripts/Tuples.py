from collections import namedtuple

WindowLayout = namedtuple('WindowLayout',
                          ['mainTextPosition',
                           'inputTextPosition',
                           'progressIndicatorPosition',
                           'windowSize'],
                          verbose=True)