import time


class Timer(object):

    t0 = None

    def start(self):
        self.t0 = time.time()

    def stop(self):
        if self.t0 is not None:
            elapsed = time.time() - self.t0
            self.t0 = None
            return elapsed
        return 0
