# This code contains a `PointCloud` class that lets you
# store a number of points and retrieve the nearest neighbor
# point of the point cloud for any given point.
#
# Then, we have the function `plot_over_line` to plot a discrete
# function - defined by values on the points of the point cloud -
# along a given line with a specified number of samples along the line.
# To this end, the nearest neighbor in the point cloud for each point
# on the line is determined, and that closest discrete function value
# is chosen for plotting.
#
# There are several "issues" with this implementation. First of all, there
# is a poorly named argument in the `plot_over_line` function. But there is
# much more that can be improved. Try to clean this code up and look into
# `plot_over_line_hints.py` for hints on where to start.



from __future__ import annotations
from typing import List
from dataclasses import dataclass
from math import pi, sqrt, sin, cos
from matplotlib.pyplot import plot, show, close


@dataclass
class Point:
    x: float
    y: float

    def distance_to(self, other: Point) -> float:
        dx = other.x - self.x
        dy = other.y - self.y
        return sqrt(dx*dx + dy*dy)

class DiscreteFunction:
    def __init__(self, point_cloud: PointCloud, point_values: List[float]) -> None:
        self.point_cloud = point_cloud
        self.point_values = point_values

    def __call__(self, point: Point) -> float:
        index = self.point_cloud.get_nearest_point_index(point)
        return self.point_values[index]

class PointCloud:
    def __init__(self, points: List[Point]) -> None:
        self._points = points

    @property
    def size(self) -> int:
        return len(self._points)

    # This is to make a `PointCloud` iterable, that is, to
    # allow looping over its points like this:
    #
    # for p in point_cloud:
    #     ...
    def __iter__(self):
        return iter(self._points)

    def __getitem__(self, index: int) -> Point:
        return self._points[index]

    def get_nearest(self, p: Point) -> Point:
        # Note: this is very inefficient, but does it for us...
        return min(self._points, key=lambda point: point.distance_to(p))

    def get_nearest_point_index(self, p: Point) -> int:
        # Note: this is very inefficient, but does it for us...
        return self._points.index(self.get_nearest(p))

def discretize_line(line: Line, n: int) -> List[Point]:
    dx = (line.target.x - line.source.x)/(n - 1)
    dy = (line.target.y - line.source.y)/(n - 1)
    return [Point(line.source.x + dx*float(i), line.source.y + dy*float(i)) for i in range(n)]

def get_values_on_line(point_cloud: PointCloud,
                        point_values: List[float],
                        line: Line,
                        n: int) -> List[float]:
    points_on_line = discretize_line(line, n)
    x = []
    y = []
    for i in range(n):
        current = points_on_line[i]
        x.append(line.source.distance_to(current))
        y.append(point_values[point_cloud.get_nearest_point_index(current)])
    return x, y

def plot_line_values(x: List[float], y: List[float]) -> None:

    plot(x, y)
    show()
    close()

def plot_over_line(discrete_function: DiscreteFunction,
                   line: Line,
                   n: int = 1000) -> None:
    assert point_cloud.size == len(point_values)

    x, y = get_values_on_line(point_cloud, point_values, line, n)
    plot_line_values(x, y)


def _test_function(position: Point) -> float:
    return sin(2.0*pi*position.x)*cos(2.0*pi*position.y)

class Line:
    def __init__(self, source: Point, target: Point) -> None:
        self.source = source
        self.target = target

if __name__ == "__main__":
    print("Plotting along a line though a point cloud...")
    print(
        "Note that this may take some time since we are "
        "doing a brute force nearest neighbor evaluation"
    )

    domain_size = (1.0, 1.0)
    number_of_points = (50, 50)
    dx = (
        domain_size[0]/float(number_of_points[0]),
        domain_size[1]/float(number_of_points[1])
    )

    point_cloud = PointCloud([
        Point(float(i)*dx[0], float(j)*dx[1])
        for i in range(number_of_points[0])
        for j in range(number_of_points[1])
    ])

    point_values = [_test_function(p) for p in point_cloud]
    discrete_function = DiscreteFunction(point_cloud, point_values)
    plot_over_line(
        discrete_function,
        Line(Point(0.0, 0.0), Point(1.0, 1.0)),
        n=2000
    )



