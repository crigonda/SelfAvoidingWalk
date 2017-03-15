"""Verification of the article results."""

from math import floor
from Walk import randomWalk, nonReversingWalk, selfAvoidingWalk, distance

def averageDistance(nbSteps, nbWalks, func):
    """Computes the average distance of a walk."""
    totalDistance = 0
    startPoint = (0, 0)
    for _ in range(nbWalks):
        arrival = None
        while arrival is None:
            arrival = func(startPoint, nbSteps)
        totalDistance += distance(startPoint, arrival)
    return pow(totalDistance/nbWalks, 2)

def buildAbs(maxVal):
    """Build the abscissa values."""
    return [5*i for i in range(floor(maxVal/5)+1)]

def buildOrd(abscissaTab, nbWalks):
    """Computes all the ordinates values."""
    random = []
    nonReversing = []
    selfAvoiding = []
    for ab in abscissaTab:
        print("# Computing for ab = ", ab)
        print(" -> Random...")
        random.append(averageDistance(ab, nbWalks, randomWalk))
        print(" -> Non reversing...")
        nonReversing.append(averageDistance(ab, nbWalks, nonReversingWalk))
        print(" -> Self-avoiding...")
        selfAvoiding.append(averageDistance(ab, nbWalks, selfAvoidingWalk))
    return random, nonReversing, selfAvoiding

# ********************************** MODIFY ONLY THESE PARAMETERS **********************************
# The maximum number of steps for a walk
MAXSTEP = 100
# The number of walks used to get an average
NBWALKS = 500
# **************************************************************************************************
RANDOM, NONREVERSING, SELFAVOIDING = buildOrd(buildAbs(MAXSTEP), NBWALKS)
print(RANDOM)
print(NONREVERSING)
print(SELFAVOIDING)
