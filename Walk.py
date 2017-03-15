"""Different types of walk."""

from random import randint
from math import sqrt
from enum import Enum

# Walk type
class WalkType(Enum):
    """RANDOM - NON_REVERSING - SELF_AVOIDING"""
    RANDOM = 1 ; NON_REVERSING = 2 ; SELF_AVOIDING = 3

# Direction of a step
class Direction(Enum):
    """NORTH - EAST - SOUTH - WEST"""
    NORTH = 1 ; EAST = 2 ; SOUTH = 3 ; WEST = 4

# ============================================== WALKS =============================================
def randomWalk(startPoint, nbSteps, model=None, generator=None):
    """Generates a random walk."""
    point = startPoint
    for _ in range(nbSteps):
        nextDirection = pickDirection(initDir(), generator)
        point = move(point, nextDirection, 1)
        if model is not None:
            notifyModel(model, nextDirection)
    # Returns the arrival point
    return point

def nonReversingWalk(startPoint, nbSteps, model=None, generator=None):
    """Generates a non reversing walk."""
    point = startPoint
    nextDirection = None
    for _ in range(nbSteps):
        nextDirection = pickDirection(initDir(opposite(nextDirection)), generator)
        point = move(point, nextDirection, 1)
        if model is not None:
            notifyModel(model, nextDirection)
    # Returns the arrival point
    return point

def selfAvoidingWalk(startPoint, nbSteps, backTrack=False, model=None, generator=None):
    """Generates a self avoiding walk."""
    point = startPoint
    nextDirection = None
    previousPts = [startPoint]
    count = 0
    while count < nbSteps:
        nextDirection = pickDirection(initDir(opposite(nextDirection)), generator)
        point = move(point, nextDirection, 1)
        # If the walk is folds up on itself
        if previousPts.count(point):
            if backTrack:
                # Backtracks until there is no more conflict possible
                nextDirection, stepsBack = backtrack(previousPts, nbSteps, model)
                point = previousPts[-1]
                count -= stepsBack
            else:
                # If the next point have already been passed on, cancels the current walk.
                # Cancelling the walk instead of continuing with restricted choices avoids
                # miscalculating the average length of a self avoiding walk
                return None
        else:
            previousPts.append(point)
            count += 1
            if model is not None:
                notifyModel(model, nextDirection)
    # Returns the arrival point
    return point

def backtrack(points, nbSteps, model=None):
    """Goes back until there is no more conflict possible."""
    finished = False
    stepsBack = 0
    sight = 2
    while not finished:
        comingFrom = towards(points[-1], points[-2])
        if conflict(points, points[-1], sight, comingFrom):
            points.pop()
            stepsBack += 1
            if model is not None:
                notifyModel(model, comingFrom, 'b')
        else:
            finished = True
    return opposite(comingFrom), stepsBack

# ======================================= AUXILIARY FUNCTIONS ======================================
def pickDirection(directions, generator=None):
    """Picks a direction among a list."""
    # The list should not be empty
    if directions:
        if generator is not None:
            nextInt = int(generator.generate() * (len(directions)))
        else:
            nextInt = randint(0, len(directions) - 1)
        direction = directions[nextInt]
        return direction
    else:
        return None

def opposite(direction):
    """Returns the opposite of a direction."""
    if direction == Direction.NORTH:
        return Direction.SOUTH
    elif direction == Direction.EAST:
        return Direction.WEST
    elif direction == Direction.SOUTH:
        return Direction.NORTH
    elif direction == Direction.WEST:
        return Direction.EAST
    else:
        return None

def initDir(forbidden=None):
    """Creates a list with available directions."""
    directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
    if forbidden is not None:
        directions.remove(forbidden)
    return directions

def move(p, direction, stepSize):
    """Moves in a given direction."""
    x, y = p
    if direction == Direction.NORTH:
        return (x, y+stepSize)
    elif direction == Direction.EAST:
        return (x+stepSize, y)
    elif direction == Direction.SOUTH:
        return (x, y-stepSize)
    elif direction == Direction.WEST:
        return (x-stepSize, y)
    else:
        return None

def towards(p1, p2):
    """Returns the 'p1 to p2' direction."""
    subOp = lambda x, y: x - y
    p1SubP2 = list(map(subOp, p2, p1))
    if p1SubP2[0] > 0:
        return Direction.EAST
    elif p1SubP2[0] < 0:
        return Direction.WEST
    elif p1SubP2[1] > 0:
        return Direction.NORTH
    elif p1SubP2[1] < 0:
        return Direction.SOUTH
    # If the points are the same
    else:
        return None

def conflict(walk, point, sight, comingFrom=None):
    """Detects if the given point can collide with the walk."""
    # TODO : change conflict...
    directions = initDir(comingFrom)
    conf = False
    if sight > 0:
        for di in directions:
            newPoint = move(point, di, 1)
            if walk.count(newPoint):
                return True
            else:
                conf = conf and conflict(walk, newPoint, sight-1, Direction(opposite(di)))
    return conf

def notifyModel(model, direction, mode='f'):
    """Updates the model."""
    model.put((direction, mode))

def distance(p1, p2):
    """Computes the Euclidian distance between two points."""
    subOp = lambda x, y: pow(x - y, 2)
    return sqrt(sum(list(map(subOp, p1, p2))))
# ==================================================================================================
