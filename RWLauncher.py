"""Random walk simulation."""

from multiprocessing import Process, Queue

from Walk import WalkType, randomWalk, nonReversingWalk, selfAvoidingWalk
from OneTermGenerator import OneTermGenerator
from TwoTermGenerator import TwoTermGenerator
from WalkGUI import WalkGUI

class RWLauncher(Process):
    """Random walk launcher."""

    def __init__(self, startPoint, nbSteps, walkType, backtrack, guiQueue=None, generator=None):
        super(RWLauncher, self).__init__()
        self.startPoint = startPoint
        self.nbSteps = nbSteps
        self.walkType = walkType
        self.backtrack = backtrack
        self.queue = guiQueue
        self.generator = generator

    def run(self):
        """Runs the simulation."""
        if self.walkType == WalkType.RANDOM:
            randomWalk(self.startPoint, self.nbSteps, self.queue, self.generator)
        elif self.walkType == WalkType.NON_REVERSING:
            nonReversingWalk(self.startPoint, self.nbSteps, self.queue, self.generator)
        elif self.walkType == WalkType.SELF_AVOIDING:
            selfAvoidingWalk(self.startPoint, self.nbSteps, self.backtrack,\
            self.queue, self.generator)

    def getNbSteps(self):
        """Returns the simulation's number of steps."""
        return self.nbSteps

    def getWalkType(self):
        """Returns the walk type."""
        return self.walkType

    def getQueue(self):
        """Returns the queue."""
        return self.queue

    def getStartPoint(self):
        """Returns the starting point."""
        return self.startPoint

# ========================================== LAUNCHER PART =========================================
if __name__ == '__main__':
    # ******************************** MODIFY ONLY THESE PARAMETERS ********************************
    # The number of steps of the walk.
    NBSTEPS = 100
    # The random generator used for the generation. Set to 'None' to use the native generator, else
    # to 'OneTermGenerator()', or 'TwoTermGenerator()'.
    GENERATOR = None
    # Set to True to use backtrack during a self-avoiding walk.
    # If set to False, the simulation will stop at the first collision.
    BACKTRACK = True
    # The walk type : 'RANDOM', 'NON_REVERSING', or 'SELF_AVOIDING'.
    WALKTYPE = WalkType.RANDOM
    # **********************************************************************************************
    STARTPOINT = (NBSTEPS/2, NBSTEPS/2)
    # Creates the random walk simulator
    QUEUE = Queue()
    PROC = RWLauncher(STARTPOINT, NBSTEPS, WALKTYPE, BACKTRACK, QUEUE, GENERATOR)
    # Creates the GUI
    GUI = WalkGUI(PROC)
    # Starts the random walk
    PROC.start()
    # Displays the GUI
    GUI.display()
