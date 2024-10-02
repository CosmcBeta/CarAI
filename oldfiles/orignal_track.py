from constants import *
from convex_hull import ConvexHull

import math
import pygame
import random as rn
import numpy as np
#from scipy.spatial import ConvexHull # M=make myself
from scipy import interpolate # make myself

"""
    takes in an array of points
    returns the index of the points on the convex hull
    in the array given
    use this as a list of the verticies

    **********************************  
    # Pseudocode
    let points be the list of points
    let stack = empty_stack()

    find the lowest y-coordinate and leftmost point, called P0
    sort points by polar angle with P0, if several points have the same polar angle then only keep the farthest

    for point in points:
        # pop the last point from the stack if we turn clockwise to reach this point
        while count stack > 1 and ccw(next_to_top(stack), top(stack), point) <= 0:
            pop stack
        push point to stack
    end
    **********************************


"""
def bottom_left_point(points):
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
    return point_index

    
class Track(pygame.sprite.Sprite):

    def __init__(self, useSeed=False):
        super().__init__()
        if useSeed: 
            rn.seed(SEED)
        self.hull = None
        self.final_points = []
        self.key_points = []
        self.image = pygame.Surface([D_WIDTH, D_HEIGHT]) 
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()

    
    def _create_points(self):
        num_points = rn.randint(MIN_POINTS, MAX_POINTS)

        points = []
        for _ in range(num_points):
            x = rn.randint(MARGIN, W_WIDTH - MARGIN)
            y = rn.randint(MARGIN, W_HEIGHT - MARGIN)
            points.append((x,y))

        return np.array(points)


    def _find_midpoint(self, points):
        new_points = points
        k = 0
        for i in range(len(self.hull.vertices) - 1):
            x1, y1 = new_points[self.hull.vertices[i]]
            x2, y2 = new_points[self.hull.vertices[i+1]]
            mp = (x1 + x2) / 2, (y1 + y2) / 2

            new_points.insert(i+1 + k, mp)
            k += 1

            for j in range(i+1, len(self.hull.vertices)):
                self.hull.vertices[j] += 1
            
        x1, y1 = points[self.hull.vertices[0]]
        x2, y2 = points[self.hull.vertices[-1]]
        mp = (x1 + x2) / 2, (y1 + y2) / 2
        new_points.append(mp)


        # displacement
        for i in range(1, len(points), 2):
            x_dis = rn.randint(MIN_DISPLACEMENT, MAX_DISPLACEMENT) #* rn.choice([-1, 1])
            y_dis = rn.randint(MIN_DISPLACEMENT, MAX_DISPLACEMENT) #* rn.choice([-1, 1])
            points[i] = tuple(map(sum, zip(points[i], (x_dis, y_dis)))) # see bottom

        return new_points


    def _spline_curve(self):
        x = np.array([p[0] for p in self.final_points])
        y = np.array([p[1] for p in self.final_points])

        x = np.r_[x, x[0]]
        y = np.r_[y, y[0]]

        tck, u = interpolate.splprep([x, y], s=0, per=True)

        xi, yi = interpolate.splev(np.linspace(0, 1, TRACK_POINTS), tck)
        return [(int(xi[i]), int(yi[i])) for i in range(len(xi))]
    
    """
    # def _fix_angles(self, points):
    #     for index in range(len(points)):
    #         point = points[index]
    #         previous_point = points[-1] if index == 0 else points[index - 1]
    #         if index == len(points) - 1:
    #             next_point = points[0]
    #             next_point_index = 0
    #         else:
    #             next_point = points[index + 1]
    #             next_point_index = index + 1
            
    #         f = lambda a, b : math.sqrt(math.pow(b[0] - a[0], 2) + math.pow(b[1] - a[1], 2))
    #         previous_length = f(previous_point, point)
    #         next_length = f(point, next_point)
    #         hypotenuse = f(previous_point, next_point)

    #         angle_rad = math.acos((previous_length**2 + next_length**2 - hypotenuse**2)/(2 * previous_length * next_length))
    #         angle = math.degrees(angle_rad)

    #         if angle >= MAX_ANGLE:
    #             difference = math.radians(angle - MAX_ANGLE)
    #             displacement = math.sqrt((2 * (next_length ** 2)) - (2 * (next_length ** 2) * math.cos(difference)))
    #             x = displacement * math.cos(math.radians(45))
    #             y = displacement * math.sin(math.radians(45))
    #             new_x = points[next_point_index][0] + x
    #             new_y = points[next_point_index][1] + y
    #             points[next_point_index] = (new_x, new_y)

    #     return points
    """
    def _fix_angles(self, points):
        for i in range(len(points)):
            if i > 0:
                prev_point = i - 1
            else:
                prev_point = len(points)-1
            next_point = (i+1) % len(points)

            previous_x = points[i][0] - points[prev_point][0]
            previous_y = points[i][1] - points[prev_point][1]
            previous_length = math.sqrt(previous_x**2 + previous_y**2)
            previous_x /= previous_length
            previous_y /= previous_length
            next_x = -(points[i][0] - points[next_point][0])
            next_y = -(points[i][1] - points[next_point][1])
            next_length = math.sqrt(next_x**2 + next_y**2)
            next_x /= next_length
            next_y /= next_length

            angle = math.atan2(previous_x * next_y - previous_y * next_x, previous_x * next_x + previous_y * next_y)
            if (abs(math.degrees(angle)) > MAX_ANGLE):
                diff = math.radians(MAX_ANGLE * math.copysign(1,angle)) - angle
                cos = math.cos(diff)
                sin = math.sin(diff)
                new_x = (next_x * cos - next_y * sin) * next_length
                new_y = (next_x * sin + next_y * cos) * next_length
                points[next_point][0] = int(points[i][0] + new_x)
                points[next_point][1] = int(points[i][1] + new_y)
        return points
    

    def _push_points_apart(self, points):
        for index in range(len(points)):
            point = points[index]
            next_point_index = 0 if index == len(points)-1 else index+1
            next_point = points[next_point_index]

            dx = next_point[0] - point[0]
            dy = next_point[1] - point[1]
            distance = math.sqrt(dx**2 + dy**2)

            if distance < DISTANCE_BETWEEN_POINTS:
                diff = DISTANCE_BETWEEN_POINTS - distance
                dx /= distance
                dx *= diff
                dy /= distance
                dy *= diff
                x, y = points[next_point_index]
                x += dx
                y += dy
                points[next_point_index] = (x, y)

        return points

    

    def _draw_points(self, points, color="white"):
        for point in points:
            pygame.draw.circle(self.image, color, point, 3)


    def _draw_hull(self, color="blue"):
        for i in range(len(self.hull.vertices) - 1):
            pygame.draw.line(self.image, color, self.final_points[self.hull.vertices[i]], self.final_points[self.hull.vertices[i+1]])
        pygame.draw.line(self.image, color, self.final_points[self.hull.vertices[0]], self.final_points[self.hull.vertices[-1]])


    def _draw_line_between_points(self, color="blue"):
        for i in range(len(self.final_points) - 1):
            pygame.draw.line(self.image, color, self.final_points[i], self.final_points[i+1], 2)
        pygame.draw.line(self.image, color, self.final_points[0], self.final_points[-1])


    def _draw_track(self, color="gray"):
        radius = TRACK_WIDTH // 2
        for point in self.key_points:
            pygame.draw.circle(self.image, color, point, radius)


    def create_track(self):
        rng_points = self._create_points()
        h = ConvexHull(rng_points)
        self.hull = ConvexHull(rng_points)

        points = []
        for i in range(len(self.hull.vertices)):
            points.append(tuple(rng_points[self.hull.vertices[i]]))
        self.hull = ConvexHull(points)

        points = self._find_midpoint(points)
        points = self._push_points_apart(points)
        points = self._fix_angles(points)

        self.final_points = []
        for point in points:
            temp = list(point)

            if temp[0] < MARGIN:
                temp[0] = MARGIN
            elif temp[0] > W_WIDTH - MARGIN:
                temp[0] = W_WIDTH - MARGIN
            if temp[1] < MARGIN:
                temp[1] = MARGIN
            elif temp[1] > W_HEIGHT - MARGIN:
                temp[1] = W_HEIGHT - MARGIN

            self.final_points.append((temp[0] + 500, temp[1] + 500))

        self.key_points = self._spline_curve()

    
    def draw(self, surface, camera):
        #pygame.draw.rect(self.image, "brown", (MARGIN + 500, MARGIN + 500, W_WIDTH - MARGIN*2 + 500, W_HEIGHT - MARGIN*2 + 500))# makes margin box
        self._draw_track()
        #self._draw_line_between_points()
        #self._draw_points(self.final_points, "purple")
        surface.blit(self.image, (self.rect.x - camera.x, self.rect.y - camera.y)) 
        # if debug:
        #     self._draw_hull(screen)
        #     self._draw_line_between_points(screen)
        #     self._draw_points(screen, self.final_points, "purple")



"""

points[i] = tuple(map(sum, zip(points[i], (x_dis, y_dis))))

==

x, y = points[i]
x += x_dis
y += y_dis
points[i] = (x, y)

"""