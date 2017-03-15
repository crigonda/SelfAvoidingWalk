"""Tests on processes."""

from multiprocessing import Process, Queue
from time import sleep

class DispProcess(Process):
    """A process putting values in its queue."""

    def __init__(self, queue):
        super(DispProcess, self).__init__()
        self.queue = queue

    def getQueue(self):
        """Queue getter."""
        return self.queue

    def run(self):
        count = 0
        while True:
            # Puts the current value in the queue
            self.queue.put(count)
            count += 1
            sleep(1)

class PrintObject(object):
    """An object displaying the values in its queue."""

    def __init__(self, proc):
        self.proc = proc

    def run(self):
        """Main."""
        val = 0
        while val < 10:
            # Gets the oldest value in the queue
            val = self.proc.getQueue().get()
            print(val)
        self.proc.terminate()


if __name__ == '__main__':
    QUEUE = Queue()
    PROC = DispProcess(QUEUE)
    PRINTER = PrintObject(PROC)
    PROC.start()
    PRINTER.run()
