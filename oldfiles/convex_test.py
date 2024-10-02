from scipy.spatial import ConvexHull # M=make myself
import random as rn
from constants import *
import numpy as np
import math
from functools import cmp_to_key
from convex_hull import Convex_Hull

rn.seed(30)


def create_points():
        num_points = rn.randint(MIN_POINTS, MAX_POINTS)

        points = []
        for _ in range(num_points):
            x = rn.randint(MARGIN, W_WIDTH - MARGIN)
            y = rn.randint(MARGIN, W_HEIGHT - MARGIN)
            points.append((x,y))

        return np.array(points)


# finds the lowest point and if there are multiple the farthest left
def bottom_left_point(points): # works
    x = y = 7000
    point_index = -1
    for index, point in enumerate(points):
        if point[1] < y:
            x = point[0]
            y = point[1]
            point_index = index
            continue
        if point[1] == y:
            if point[0] < x:
                x = point[0]
                y = point[1]
                point_index = index
    return point_index, points[point_index]

"""
# def heap_sort(points, angles):
#     N = len(angles)

#     for i in range(N//2 - 1, -1, -1):
#         heapify(points, angles, N, i)

#     for i in range(N-1, 0, -1):
#         angles[i], angles[0] = angles[0], angles[i]
#         points[i], points[0] = points[0], points[i]
#         heapify(points, angles, i, 0)


# def heapify(points, angles, N, i):
#     largest = i
#     l = 2 * i + 1
#     r = 2 * i + 2

#     if l < N and angles[largest] < angles[l]:
#         largest = l

#     if r < N and angles[largest] < angles[r]:
#         largest = r

#     if largest != i:
#         angles[i], angles[largest] = angles[largest], angles[i]
#         points[i], points[largest] = points[largest], points[i]
#         heapify(points, angles, N, largest)


# def calculate_and_sort(points, point_p):
#     print(f'Length: {len(points)}\nBefore: \n{points}\n\n')
#     point_angles = [0] * len(points)
#     zeros = []
#     for index, point in enumerate(points):
#         delta_x = point_p[0] - point[0]
#         delta_y = point_p[1] - point[1]

#         if delta_y == 0:
#             zeros.append(point)
#             np.delete(points, index)
#             continue
        
#         angle = delta_x / delta_y
#         point_angles[index] = angle
#     heap_sort(points, point_angles)

#     if len(zeros) == 0:
#         return points
    
#     for point in zeros:
#         delta_x = point_p[0] - point[0]
#         if delta_x < 0:
#             np.insert(points, 0, point)    #    points.insert(0, point)
#         elif delta_x > 0:
#             np.append(points, point)       #    points.append(point)

#     print(len(points))
#     print(points)
#     return points


# def sort(points, point_p):
#     length = len(points)

#     for index in range(length//2 - 1, -1, -1):
#         heapify(points, point_p, length, index)

#     for index in range(length-1, 0, -1):
#         points[index], points[0] = points[0], points[index]
#         heapify(points, point_p, index, 0)


# def heapify(points, point_p, length, i):
#     largest = i
#     left = 2 * i + 1
#     right = 2 * i + 2

#     largest_angle = -1 * (point_p[0] - points[largest][0]) / (point_p[1] - points[largest][0])
#     left_angle = -1 * (point_p[0] - points[left][0]) / (point_p[1] - points[left][0])
#     right_angle = -1 * (point_p[0] - points[right][0]) / (point_p[1] - points[right][0])



#     # if point_p[1] - points[largest][1] != 0:
#     #     larg = -1 * (point_p[0] - points[largest][0]) / (point_p[1] - points[largest][0])
#     # else:
#     #     larg = 10000 if point_p[0] - points[largest][0] > 0 else -1000

#     # if point_p[1] - points[l][1] != 0:
#     #     lang = -1 * (point_p[0] - points[l][0]) / (point_p[1] - points[l][0])
#     # else:
#     #     lang = 10000 if point_p[0] - points[l][0] > 0 else -1000

#     # if point_p[1] - points[r][1] != 0:
#     #     rang = -1 * (point_p[0] - points[r][0]) / (point_p[1] - points[r][0])
#     # else:
#     #     rang = 10000 if point_p[0] - points[r][0] > 0 else -1000


#     if left < length and largest_angle < left_angle:
#         largest = left

#     if right < length and largest_angle < right_angle:
#         largest = right

#     if largest != i:
#         points[i], points[largest] = points[largest], points[i]
#         heapify(points, point_p, length, largest)

# def remove_dupes(points, angles, point_p):
#     new_points = []
#     new_angles = []
#     for index in range(len(angles)):
#         if angles[index] == angles[index+1]:
#             f = lambda x1, y1, x2, y2 : math.sqrt((x2-x1)**2 + (y2-y1)**2)
#             distance_1 = f(point_p[0], point_p[1], points[index][0], points[index][1])
#             distance_2 = f(point_p[0], point_p[1], points[index+1][0], points[index+1][1])
#             if distance_1 > distance_2:
#                 points[index]
#             else:
#                 points[index+1][0] = -1
#                 points[index+1][0] = -1
"""
def distance_squared(point_a, point_b):
    return math.pow(point_a[0] - point_b[0], 2) + math.pow(point_a[1] - point_b[1], 2)

def taxicab_distance(p1, point_p):
    return abs(point_p[0] - p1[0]) + abs(point_p[1] - p1[1])

def compare(point_a, point_b, point_p):
    dir = ccw(point_a, point_b, point_p)

    if dir < 0:
        return 1
    elif dir > 0:
        return -1
    else:
        if taxicab_distance(point_a, point_p) < taxicab_distance(point_b, point_p):
            return -1
        else:
            return 1

# def sort(points, point_p):
#     sorted_points = sorted(points[1:], cmp= lambda point_a, point_b : compare(point_a, point_b, point_p))
#     return sorted_points



def ccw(first, middle, last):
    return ((middle[0] - first[0]) * (last[1] - first[1])) - ((middle[1] - first[1]) * (last[0] - first[0]))

def find(list, elem):
    x = elem[0]
    y = elem[1]

    for index, point in enumerate(list):
        if x == point[0] and y == point[1]:
            return index
    return -1


def convex_hull(points):
    stack = []

    index_p, point_p = bottom_left_point(points)
    #np.delete(points, index_p)
    #points[0], points[index_p] = points[index_p], points[0]

    #points_sorted = sort(points, point_p)
    points_sorted = sorted(points,key=cmp_to_key(lambda point_a, point_b : compare(point_a, point_b, point_p)))

    #np.delete(points_sorted, np.where(points_sorted, point_p))
    #print(f'Sorted: {points_sorted}')
    #remove dupes
    remove = []
    new_list = []
    for index in range(len(points_sorted)-1):
        p1 = points_sorted[index]
        p2 = points_sorted[index+1]

        if ccw(p1, p2, point_p) != 0:
            continue

        distance1 = taxicab_distance(p1, point_p)
        distance2 = taxicab_distance(p2, point_p)

        if distance1 > distance2:
            remove.append(p2)
            #new_list = np.delete(points_sorted, p2, axis=0)
        else:
            remove.append(p1)
            #new_list = np.delete(points_sorted, p1, axis=0)
    print(f'Removed: {remove}')
    # Removes all points in the remove list from the sorted list
    # temp = []
    # for point in points_sorted:
    #     if np.any(remove, point):
    #         temp.append(point)
    # points_sorted = temp
    #for point in points_sorted: this is removing entire rows
    #    np.delete(points_sorted, point)
    #points_sorted = np.delete(points_sorted, remove, axis=0)
    #points_sorted = points_sorted[(points_sorted != remove).all(axis=1)]
    new_list = points_sorted
    for point in remove:
        for index, s_point in enumerate(points_sorted):
            if point[0] == s_point[0] and point[1] == s_point[1]:
                new_list.pop(index) #= np.delete(new_list, index, axis=0)
                continue
            

    print(f'Sorted: {new_list}')


    stack.append(point_p)
    stack.append(new_list[0])
    stack.append(new_list[1])
    for index in range(2, len(new_list)):
        
        while len(stack) > 1 and ccw(stack[-2], stack[-1], new_list[index]) <= 0:
            stack.pop()
        stack.append(new_list[index])

    #return stack
    indexes = []
    # for index, point in enumerate(points):
    #     if np.any(stack == point):
    #             indexes.append(index)
    # for point in stack:
    #     x = np.nonzero(points_sorted == point)
    #     indexes.append(x)
    #     print(x)
    #print(f'Ind: {indexes}')
    for point in stack:
        ind = find(points, point)
        indexes.append(ind)
    return indexes

"""
   sorting works

"""


if __name__ == '__main__':
    #rng_points = create_points()
    # rng_points = np.array([(24, 78), (54, 83), (79, 91), (66, 81), (64, 50), (35, 2),
    #                     (63, 66), (48, 67), (66, 63), (64, 83), (25, 87), (18, 100),
    #                     (12, 83), (47, 62), (60, 53), (63, 23), (4, 87), (90, 50),
    #                     (34, 36), (69, 2), (7, 51), (95, 82), (54, 77), (36, 76),
    #                     (83, 42), (80, 53), (45, 47), (97, 61), (51, 14), (78, 28)])
    rng_points = np.array([(0,0),(7,0),(3,1),(5,2),(9,6),(3,3),(5,5),(1,4)])
    np.random.shuffle(rng_points)
    print(f'Shuffled: {rng_points}')
    #print(f'Point: {bottom_left_point(rng_points)}\n\n')

    hull = ConvexHull(rng_points)
    print(f'\n\nHull\n{hull.vertices}')

    print(f'{hull.vertices[0]}')

    my_hull = Convex_Hull(rng_points)
    h = my_hull.convex_hull()
    #my_hull = convex_hull(rng_points)
    print(f'\n\nMy Hull\n{h}')

# Sorting
# (0, 0), (7, 0), (3, 1), (5, 2), (9, 6), (3, 3), (5, 5), (1, 4) base, sorted correctly
# [1, 4], [9, 6], [5, 2], [3, 1], [7, 0], [0, 0], [3, 3] first
# (0, 0), (1, 4), (5, 5), (3, 3), (9, 6), (5, 2), (3, 1), (7, 0) second
# (1, 4), (5, 5), (3, 3), (9, 6), (5, 2), (3, 1), (7, 0), (0, 0) third
# (1, 4), (5, 5), (3, 3), (9, 6), (5, 2), (3, 1), (7, 0), (0, 0) forth
# (7, 0), (3, 1), (5, 2), (9, 6), (5, 5), (3, 3), (1, 4), (0, 0) fifth
# (0, 0), (7, 0), (3, 1), (5, 2), (9, 6), (3, 3), (5, 5), (1, 4) sixth
# (0, 0), (7, 0), (3, 1), (5, 2), (9, 6), (3, 3), (5, 5), (1, 4) seventh

# Removing Collinear
# (0, 0), (7, 0), (3, 1), (5, 2), (9, 6), (5, 5), (1, 4) base, correctly removed (3, 3)
# (0, 0), (7, 0), (3, 1), (3, 3) - only (0, 0) and (3, 3) are in removed list
# (0, 0), (7, 0), (3, 1), (5, 2), (9, 6), (3, 3), (5, 5), (1, 4)
# (7, 0), (3, 1), (9, 6), (3, 3), (5, 5), (1, 4)
# (0, 0), (7, 0), (3, 1), (9, 6), (3, 3), (5, 5), (1, 4)
# (7, 0), (3, 1), (5, 2), (9, 6), (5, 5), (1, 4)