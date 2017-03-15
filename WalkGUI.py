"""Rendering of a random walk."""

from tkinter import Tk, PanedWindow, Canvas, LabelFrame, Scale, DoubleVar, Label
from tkinter import TOP, Y, BOTH, ALL, VERTICAL, HORIZONTAL
from math import floor, sqrt
from time import sleep
import queue

from Walk import WalkType, move, distance

# Default parameters
DEFAULT_REFRESH_RATE = 1
CANVAS_SIZE = 600
START_POS = (CANVAS_SIZE/2, CANVAS_SIZE/2)
BG_COLOR = '#f0f8ff'

class WalkGUI(object):
    """Rendering of a random walk."""

    def __init__(self, modelProc):
        self.modelProc = modelProc
        self.queue = modelProc.getQueue()
        # ----------------- Model parameters -----------------
        # Starting point
        self.curPoint = START_POS
        # Size of a step
        self.step = self.computeSize()
        # Waiting time between two events
        self.refreshRate = DEFAULT_REFRESH_RATE
        # Current simulation step
        self.count = 0
        # Canvas lines
        self.lines = []
        # ------------------------ GUI -----------------------
        # Main window
        self.window = Tk()
        self.window.title("Walk Rendering")
        self.window.configure(bg=BG_COLOR)
        self.window.protocol("WM_DELETE_WINDOW", self.onClosing)
        # Main pane
        mainPane = PanedWindow(self.window, orient=HORIZONTAL, bg=BG_COLOR)
        mainPane.pack(side=TOP, expand=Y, fill=BOTH, pady=5, padx=5)
        # Canvas frame
        canvasFrame = LabelFrame(mainPane, text="Rendering", padx=10, pady=10, bg=BG_COLOR)
        mainPane.add(canvasFrame)
        self.canvas = Canvas(canvasFrame, width=CANVAS_SIZE, height=CANVAS_SIZE, background="white")
        self.canvas.pack()
        # Parameters frame
        paramFrame = LabelFrame(mainPane, text="Simulation parameters",\
        padx=20, pady=20, bg=BG_COLOR)
        mainPane.add(paramFrame)
        # ===> Refresh rate slider
        self.stepVar = DoubleVar(paramFrame, value=DEFAULT_REFRESH_RATE)
        slider = Scale(paramFrame, from_=0, to_=10, resolution=0.1, length=350, orient=VERTICAL,\
        variable=self.stepVar, label="# Refresh rate", bg=BG_COLOR, bd=1)
        slider.bind("<ButtonRelease-1>", self.updateRate)
        slider.grid(row=1, column=1)
        # ===> Current step label
        self.stepLabel = Label(paramFrame, text="# Current step :\n" + str(self.count), bg=BG_COLOR)
        self.stepLabel.grid(row=3, column=1)
        # ===> Traveled distance label
        self.distanceLabel = Label(paramFrame, text="# Traveled distance :\n0", bg=BG_COLOR)
        self.distanceLabel.grid(row=5, column=1)
        # Rows and columns configuration
        paramFrame.grid_columnconfigure(0, weight=1)
        paramFrame.grid_columnconfigure(1, weight=2)
        paramFrame.grid_columnconfigure(2, weight=1)
        paramFrame.grid_rowconfigure(0, weight=1)
        paramFrame.grid_rowconfigure(2, weight=2)
        paramFrame.grid_rowconfigure(4, weight=2)
        paramFrame.grid_rowconfigure(6, weight=2)

    def computeSize(self):
        """Defines the size of a step, according to the walk type."""
        walkType = self.modelProc.getWalkType()
        nbSteps = self.modelProc.getNbSteps()
        if walkType == WalkType.RANDOM:
            return floor((CANVAS_SIZE/2)/(1.6*sqrt(nbSteps)))
        elif walkType == WalkType.NON_REVERSING:
            return floor((CANVAS_SIZE/2)/(2.5*sqrt(nbSteps)))
        else:
            return floor((CANVAS_SIZE/2)/(pow(nbSteps, 3/4)))

    def onClosing(self):
        """Called when exiting the window."""
        self.modelProc.terminate()
        self.window.destroy()

    def display(self):
        """Display the GUI."""
        # Sleep some time to be sure queue is not empty
        sleep(0.5)
        self.window.after(int(self.refreshRate*1000), self.getDirection)
        self.window.mainloop()

    def getDirection(self):
        """Gets a direction from the queue, if possible."""
        try:
            direction = self.queue.get(False)
            self.update(direction)
            self.window.after(int(self.refreshRate*1000), self.getDirection)
        except queue.Empty:
            self.updateDistance()

    def update(self, command):
        """Updates the rendering."""
        # If the model is backtracking
        direction = command[0]
        if command[1] == 'b':
            self.curPoint = move(self.curPoint, direction, self.step)
            self.canvas.delete(self.lines.pop())
            self.count -= 1
        else:
            nextPoint = move(self.curPoint, direction, self.step)
            newLine = self.canvas.create_line(self.curPoint[0], self.curPoint[1],\
            nextPoint[0], nextPoint[1])
            # Keeps a handle on the line to delete it if necessary (backtrack)
            self.lines.append(newLine)
            self.curPoint = nextPoint
            self.count += 1
            self.updateStep()
        return self.refreshRate

    def updateStep(self):
        """Updates the stepLabel value."""
        self.stepLabel['text'] = "# Current step :\n" + str(self.count)

    def updateDistance(self):
        """Updates the distanceLabel value."""
        # Computes the distance between the start point and the arrival one
        dist = distance(START_POS, self.curPoint)/self.step
        self.distanceLabel['text'] = "# Traveled distance :\n" + str(dist)

    def updateRate(self, event):
        """Updates the refresh rate when the slider is moved."""
        self.refreshRate = self.stepVar.get()

    def cleanCanvas(self):
        """Cleans the canvas."""
        self.canvas.delete(ALL)
