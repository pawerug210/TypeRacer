import PyGameWrapper
import Tuples
import Common

text = 'By using Keras as the high-level API for the upcoming TensorFlow 2.0 release, we will make it easier for ' \
       'developers new to machine learning to get started while providing advanced capabilities for researchers. '

class Game(object):

    def start(self):
        layout = Tuples.WindowLayout(inputTextPosition=[20, 100],
                                     mainTextPosition=[20, 50],
                                     progressIndicatorPosition=[20, 20],
                                     windowSize=(800, 600))
        instance = PyGameWrapper.PyGameWrapper(layout)
        instance.run(text)
        while instance.Running:
            instance.handleEvents()
