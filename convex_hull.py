from typing import List

from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT6':
    from PyQt6.QtCore import QLineF, QPointF, QObject
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time

# Some global color constants that might be useful
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25


#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

    # Class constructor
    def __init__(self):
        super().__init__()
        self.pause = False

    # Some helper methods that make calls to the GUI, allowing us to send updates
    # to be displayed.

    def showTangent(self, line, color):
        self.view.addLines(line, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseTangent(self, line):
        self.view.clearLines(line)

    def blinkTangent(self, line, color):
        self.showTangent(line, color)
        self.eraseTangent(line)

    def showHull(self, polygon, color):
        self.view.addLines(polygon, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseHull(self, polygon):
        self.view.clearLines(polygon)

    def showText(self, text):
        self.view.displayStatusText(text)

    # This is the method that gets called by the GUI and actually executes
    # the finding of the hull
    def compute_hull(self, points, pause, view):
        self.pause = pause
        self.view = view
        assert (type(points) == list and type(points[0]) == QPointF)

        t1 = time.time()
        # sort the points by increasing x-value
        points.sort(key=lambda p: p.x())
        t2 = time.time()

        t3 = time.time()
        # call the divide-and-conquer convex hull solver
        pointsList = divide_and_conquer(points)
        t4 = time.time()

        # convert the list of points to a list of lines
        polygon = [QLineF(pointsList[i], pointsList[(i + 1) % len(pointsList)]) for i in range(len(pointsList))]
        # display the convex hull
        self.showHull(polygon, RED)
        # Generate the text to display the time elapsed for the sorting algorithm
        self.showText('Time Elapsed (Sorting): {:3.3f} sec'.format(t2 - t1))
        # Generate the text to display the time elapsed for the convex hull algorithm
        self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))


def divide_and_conquer(points):
    # if there are 3 or fewer points, return the points
    if len(points) <= 3:
        return points
    # divide the points into two halves
    left = points[:len(points) // 2]
    right = points[len(points) // 2:]
    # recursive call on each half of the points
    left_hull = divide_and_conquer(left)
    right_hull = divide_and_conquer(right)
    # merge the two hulls
    return merge(left_hull, right_hull)


def merge(left, right):
    # create a list of tuples, points, which are the x and y coordinates of the points in left and right
    points = [(point.x(), point.y()) for point in left + right]
    # find the point with the lowest y coordinate and assigns it as the starting point of the convex hull
    start_point = min(points, key=lambda x: (x[1], x[0]))
    current_point = start_point
    # create a list of tuples, hull_points, which will contain the points on the convex hull
    hull_points = []
    while True:
        # add the current point to the convex hull
        hull_points.append(current_point)
        next_point = points[0]
        # iterate through the points list and select the next point on the convex hull
        for i in range(1, len(points)):
            # find the point with the largest counterclockwise angle relative to the current point
            if (next_point == current_point) or (
                # the cross product of the vectors (current_point, next_point) and (current_point, points[i])
                # is positive if the angle between the vectors is counterclockwise
                # and negative if the angle between the vectors is clockwise
                    (points[i][1] - current_point[1]) * (next_point[0] - current_point[0])
                    > (next_point[1] - current_point[1]) * (points[i][0] - current_point[0])
            ):
                next_point = points[i]
        current_point = next_point
        # continues until the current_point is equal to the start_point, which means the convex hull has been found
        if current_point == start_point:
            break
    # convert the list of tuples to a list of QPointF objects
    hull_points = [QPointF(*point) for point in hull_points]
    return hull_points
