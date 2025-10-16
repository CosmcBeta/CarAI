from functools import cmp_to_key

from util.constants import DISPLAY_SIZE


class ConvexHull():
    # p_min is the reference point for the Graham method of calculating the convex hull
    def __init__(self, points: list[tuple[int, int]]) -> None:
        self.points: list[tuple[int, int]] = points
        self.p_min: tuple[int, int] = points[self._bottom_left_point()]

    # Sets the points to a new list of points
    def set_new_points_list(self, new_points: list[tuple[int, int]]):
        self.points = new_points

    # Finds the Taxicab distance between the point and the reference point
    def _taxicab_distance(self, point: tuple[int ,int]):
        return abs(self.p_min[0] - point[0]) + abs(self.p_min[1] - point[1])

    # Compares the polar angle between two points
    def _compare(self, p1: tuple[int, int], p2: tuple[int, int]):
        orientation = self._ccw(p1, p2, self.p_min)

        if orientation == 0:
            return -1 if self._taxicab_distance(p1) < self._taxicab_distance(p2) else 1

        return 1 if orientation < 0 else -1

    # Returns the index of a point in the points list
    def _get_index(self, p: tuple[int, int]) -> int:
        for index, point in enumerate(self.points):
            if point[0] == p[0] and point[1] == p[1]:
                return index
        return -1

    # Determines if the point is a left turn or a right turn
    # Negative if ccw(left turn), positive if cw(right turn), 0 if collinear
    # This is the cross product of vectors 2-1 and 3-1
    def _ccw(self, p1: tuple[int, int], p2: tuple[int, int], p3: tuple[int, int]) -> int:
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3

        return (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

    # Returns index of the bottom left point
    def _bottom_left_point(self) -> int:
        x, y = DISPLAY_SIZE
        point_index = -1
        for index, point in enumerate(self.points):
            # Finds the lowest y valued point
            if point[1] < y:
                x, y = point
                point_index = index
                continue

            # If points are on the same y-level,
            # return the lowest x valued point
            if point[1] == y and point[0] < x:
                x, y = point
                point_index: int = index

        return point_index

    # Calculate and return the convex hull
    def convex_hull(self):
        # Sorts all the points by the polar angle with reference point
        sorted_points = sorted(self.points, key=cmp_to_key(lambda point_a, point_b : self._compare(point_a, point_b)))
        final_points: list[tuple[int, int]] = []

        i = 0
        while i < len(sorted_points) - 1:
            p1 = sorted_points[i]
            p2 = sorted_points[i + 1]

            # If collinear with p_min
            if self._ccw(p1, p2, self.p_min) == 0:
                d1 = self._taxicab_distance(p1)
                d2 = self._taxicab_distance(p2)
                # Keep only the closer one
                final_points.append(p1 if d1 < d2 else p2)
                i += 2  # Skip the next one since it's already handled
            else:
                final_points.append(p1)
                i += 1

        # Add the last point if not handled
        if sorted_points:
            final_points.append(sorted_points[-1])


        # Finds the convex hull
        stack = [self.p_min, final_points[0], final_points[1]]
        for index in range(2, len(final_points)):
            while len(stack) > 1 and self._ccw(stack[-2], stack[-1], final_points[index]) <= 0:
                _ = stack.pop()
            stack.append(final_points[index])

        # Returns the indexes of all points in the convex hull
        indexes: list[int] = []
        for point in stack:
            ind = self._get_index(point)
            indexes.append(ind)
        return indexes
