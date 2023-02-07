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

        # when passing lines to the display, pass a list of QLineF objects.  Each QLineF
        # object can be created with two QPointF objects corresponding to the endpoints
        polygon = [QLineF(pointsList[i], pointsList[(i + 1) % len(pointsList)]) for i in range(len(pointsList))]
        self.showHull(polygon, RED)
        self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))


def divide_and_conquer(points):
    # if there are 3 or fewer points, return the convex hull
    if len(points) <= 3:
        return points
    left = points[:len(points) // 2]
    right = points[len(points) // 2:]
    # recursive call on each half
    left_hull = divide_and_conquer(left)
    right_hull = divide_and_conquer(right)
    # merge the two hulls
    return merge(left_hull, right_hull)


def merge(left, right):
    points = [(point.x(), point.y()) for point in left + right]
    start_point = min(points, key=lambda x: (x[1], x[0]))
    current_point = start_point
    hull_points = []

    while True:
        hull_points.append(current_point)
        next_point = points[0]
        for i in range(1, len(points)):
            if (next_point == current_point) or (
                    (points[i][1] - current_point[1]) * (next_point[0] - current_point[0])
                    > (next_point[1] - current_point[1]) * (points[i][0] - current_point[0])
            ):
                next_point = points[i]
        current_point = next_point
        if current_point == start_point:
            break

    hull_points = [QPointF(*point) for point in hull_points]
    return hull_points
