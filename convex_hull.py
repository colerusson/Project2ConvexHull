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


def merge(left_hull, right_hull):
    n, m = len(left_hull), len(right_hull)
    i, j = 0, 0
    upper_hull, lower_hull = [], []

    while i < n and j < m:
        if left_hull[i].p1().y() < right_hull[j].p1().y():
            upper_hull.append(left_hull[i])
            i += 1
        else:
            upper_hull.append(right_hull[j])
            j += 1

    while i < n:
        upper_hull.append(left_hull[i])
        i += 1

    while j < m:
        upper_hull.append(right_hull[j])
        j += 1

    i, j = n - 1, m - 1
    while i >= 0 and j >= 0:
        if left_hull[i].p1().y() > right_hull[j].p1().y():
            lower_hull.append(left_hull[i])
            i -= 1
        else:
            lower_hull.append(right_hull[j])
            j -= 1

    while i >= 0:
        lower_hull.append(left_hull[i])
        i -= 1

    while j >= 0:
        lower_hull.append(right_hull[j])
        j -= 1

    final_hull = upper_hull + lower_hull[::-1]

    return [QLineF(final_hull[i], final_hull[(i + 1) % len(final_hull)]) for i in range(len(final_hull))]

#
# This is the class you have to complete.
#


def convex_hull_solver(points):
    hulls = []
    for point in points:
        hulls.append(point)

    convex_hulls = []
    while len(hulls) > 1:
        for i in range(0, len(hulls) - 1, 2):
            convex_hulls.append(merge(hulls[i], hulls[i + 1]))
        if len(hulls) % 2 == 1:
            convex_hulls.append(hulls[-1])
        hulls = convex_hulls
        convex_hulls = []

    convex_hulls = hulls[0]

    return convex_hulls


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
        polygon = self.divide_and_conquer(points)
        t4 = time.time()

        # when passing lines to the display, pass a list of QLineF objects.  Each QLineF
        # object can be created with two QPointF objects corresponding to the endpoints
        self.showHull(polygon, RED)
        self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))

    # the divide-and-conquer convex hull solver
    def divide_and_conquer(self, points):
        # if there are 3 or fewer points, return the convex hull
        if len(points) <= 3:
            return [QLineF(points[i], points[(i + 1) % len(points)]) for i in range(len(points))]
        # divide the points into two halves
        left = points[:len(points) // 2]
        right = points[len(points) // 2:]
        # recursive call on each half
        left_hull = self.divide_and_conquer(left)
        right_hull = self.divide_and_conquer(right)
        # merge the two hulls)
        return merge(left_hull, right_hull)

    # different approach - break down to make each point into a hull, then pass that into merge function
