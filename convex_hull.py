import math
import numpy as np

from functools import cmp_to_key


class ConvexHull():
    
    def __init__(self, points):
        self.points = points
        self.point_p_index = self._bottom_left_point()
        self.point_p = points[self.point_p_index]


    def new_points_list(self, new_points):
        self.points = new_points 

    # Distance between two points squared
    def distance_squared(self, p1, p2):
        return math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2)
    
    # Finds the Taxicab distance between the point and point P
    def _taxicab_distance(self, p1):
        return abs(self.point_p[0] - p1[0]) + abs(self.point_p[1] - p1[1])


    # Compares the polar angle between two points
    def _compare(self, p1, p2):
        dir = self._ccw(p1, p2, self.point_p)

        if dir < 0:
            return 1
        elif dir > 0:
            return -1
        else:
            if self._taxicab_distance(p1) < self._taxicab_distance(p2):
                return -1
            else:
                return 1
        
    
    # Returns the index of a point in the points list
    def _get_index(self, point):
        x = point[0]
        y = point[1]

        for index, point in enumerate(self.points):
            if x == point[0] and y == point[1]:
                return index
        return -1
            

    # Determines if the point is a left turn or a right turn
    # Negative if ccw(left turn), positive if cw(right turn), 0 if collinear
    def _ccw(self, p1, p2, p3):
        return ((p2[0] - p1[0]) * (p3[1] - p1[1])) - ((p2[1] - p1[1]) * (p3[0] - p1[0]))
    

    # Returns index of the bottom left point
    def _bottom_left_point(self):
        x = y = 7000
        point_index = -1
        for index, point in enumerate(self.points):
            # Finds the lowest y valued point
            if point[1] < y:
                x = point[0]
                y = point[1]
                point_index = index
                continue

            # If points are on the same y-level,
            # return the lowest x valued point
            if point[1] == y and point[0] < x:
                x = point[0]
                y = point[1]
                point_index = index
        
        return point_index
    

    # Calculate and return the convex hull
    def convex_hull(self):
        # Sorts all the points by the polar angle with point_p
        sorted_points = sorted(self.points,key=cmp_to_key(lambda point_a, point_b : self._compare(point_a, point_b)))

        # Finds all points that need to be removed from the list
        removing = []
        for index in range(len(sorted_points)-1):
            p1 = sorted_points[index]
            p2 = sorted_points[index+1]

            if self._ccw(p1, p2, self.point_p) != 0:
                continue

            d1 = self._taxicab_distance(p1)
            d2 = self._taxicab_distance(p2)

            if d1 > d2:
                removing.append(p2)
            else:
                removing.append(p1)
    
        # Removes the points from the sorted list
        final_list = sorted_points
        for point in removing:
            for index, s_point in enumerate(sorted_points):
                if point[0] == s_point[0] and point[1] == s_point[1]:
                    final_list.pop(index)
                    continue

        # Finds the convex hull
        stack = [self.point_p, final_list[0], final_list[1]]
        for index in range(2, len(final_list)):
            while len(stack) > 1 and self._ccw(stack[-2], stack[-1], final_list[index]) <= 0:
                stack.pop()
            stack.append(final_list[index])

        # Returns the indexes of all points in the convex hull
        indexes = []
        for point in stack:
            ind = self._get_index(point)
            indexes.append(ind)
        return indexes
    