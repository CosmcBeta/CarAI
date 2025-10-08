import math
import random as rn
import sys

import numpy as np
import pygame
from numpy._typing import NDArray
from scipy import interpolate

import util.constants as constants
from core.convex_hull import ConvexHull


class Track(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.randomize_seed()
        self.final_points = []
        self.key_points: list[tuple[int, int]] = []
        self.image: pygame.Surface = pygame.Surface([constants.D_WIDTH, constants.D_HEIGHT])
        self.image.set_colorkey("black")
        self.rect: pygame.Rect = self.image.get_rect()

    # Sets the seed
    def set_seed(self, seed: int):
        self.seed: int = seed
        rn.seed(self.seed)

    # Returns the seed
    def get_seed(self):
        return self.seed

    # Randomizes the seed
    def randomize_seed(self) -> None:
        self.seed = rn.randrange(sys.maxsize)
        rn.seed(self.seed)

    # Returns randomly generated points of a random amount between the min and max
    def _create_random_points(self) -> list[tuple[int, int]]:
        num_points = rn.randint(constants.MIN_POINTS, constants.MAX_POINTS)

        points: list[tuple[int ,int]] = []
        for _ in range(num_points):
            x = rn.randint(constants.MARGIN, constants.W_WIDTH - constants.MARGIN)
            y = rn.randint(constants.MARGIN, constants.W_HEIGHT - constants.MARGIN)
            points.append((x,y))

        return points

    # Finds the midpoints and addes them to the points list and then returns the list
    def _find_midpoints(self, points: list[tuple[int, int]]) -> list[tuple[int, int]]:
        new_points = points
        k = 0
        for i in range(len(self.hull) - 1):
            x1, y1 = new_points[self.hull[i]]
            x2, y2 = new_points[self.hull[i+1]]
            mp = (x1 + x2) // 2, (y1 + y2) // 2

            new_points.insert(i+1 + k, mp)
            k += 1

            for j in range(i+1, len(self.hull)):
                self.hull[j] += 1

        x1, y1 = points[self.hull[0]]
        x2, y2 = points[self.hull[-1]]
        mp = (x1 + x2) // 2, (y1 + y2) // 2
        new_points.append(mp)

        # displacement
        for i in range(1, len(points), 2):
            x_dis = rn.randint(constants.MIN_DISPLACEMENT, constants.MAX_DISPLACEMENT)
            y_dis = rn.randint(constants.MIN_DISPLACEMENT, constants.MAX_DISPLACEMENT)
            x, y = points[i]
            points[i] = (x + x_dis, y + y_dis)

        return new_points

    # Returns spline curve
    def _spline_curve(self) -> list[tuple[int, int]]:
        x: NDArray[np.int_] = np.array([p[0] for p in self.final_points])
        y: NDArray[np.int_] = np.array([p[1] for p in self.final_points])

        # First input is the array of x values
        # Second input is the first value in the array of x values
        # In this line of code, it makes the array of values peridoic
        # It adds the first value of the array to the last position
        # so that the first and last value in the array are the same
        # This ensures the spline is closed, so the curve loops back to the start.
        # Without this, the curve could leave a gap between the first and last points.
        x = np.r_[x, x[0]]
        y = np.r_[y, y[0]]


        tck, _ = interpolate.splprep([x, y], s=0, per=True)

        xi, yi = interpolate.splev(np.linspace(0, 1, constants.TRACK_POINTS), tck)
        return [(int(xi[i]), int(yi[i])) for i in range(len(xi))]

    # Returns the points after fixing the angles of the points so that they aren't too sharp
    def _fix_angles(self, points: list[tuple[int, int]]) -> list[tuple[int, int]]:
        for i in range(len(points)):
            prev_point = i - 1 if i > 0 else len(points) - 1
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
            if (abs(math.degrees(angle)) > constants.MAX_ANGLE):
                diff = math.radians(constants.MAX_ANGLE * math.copysign(1,angle)) - angle
                cos = math.cos(diff)
                sin = math.sin(diff)
                new_x = (next_x * cos - next_y * sin) * next_length
                new_y = (next_x * sin + next_y * cos) * next_length
                tx = int(points[i][0] + new_x)
                ty = int(points[i][1] + new_y)
                points[next_point] = (tx, ty)
        return points

    # Pushes the points apart so they are greater than the minumum distance between points
    def _push_points_apart(self, points: list[tuple[int, int]]) -> list[tuple[int, int]]:
        for index, point in enumerate(points):
            next_point_index = 0 if index == len(points) - 1 else index + 1
            next_point = points[next_point_index]

            dx = next_point[0] - point[0]
            dy = next_point[1] - point[1]
            distance = math.sqrt(dx**2 + dy**2)

            if distance < constants.DISTANCE_BETWEEN_POINTS:
                diff = constants.DISTANCE_BETWEEN_POINTS - distance
                dx /= distance
                dx *= diff
                dy /= distance
                dy *= diff
                x, y = points[next_point_index]
                x += dx
                y += dy
                points[next_point_index] = (int(x), int(y))

        return points


    # def _draw_points(self, points, color="white"):
    #     for point in points:
    #         pygame.draw.circle(self.image, color, point, 3)

    # def _draw_hull(self, color="blue"):
    #     for i in range(len(self.hull) - 1):
    #         pygame.draw.line(self.image, color, self.final_points[self.hull[i]], self.final_points[self.hull[i+1]])
    #     pygame.draw.line(self.image, color, self.final_points[self.hull[0]], self.final_points[self.hull[-1]])

    # def _draw_line_between_points(self, color="blue"):
    #     for i in range(len(self.final_points) - 1):
    #         pygame.draw.line(self.image, color, self.final_points[i], self.final_points[i+1], 2)
    #     pygame.draw.line(self.image, color, self.final_points[0], self.final_points[-1])

    # Draws circle at each point to make the track
    def _draw_track(self, color: str = 'gray') -> None:
        radius = constants.TRACK_WIDTH // 2
        for point in self.key_points:
            _ = pygame.draw.circle(self.image, color, point, radius)

    # Goes through the process of making the track
    def create_track(self) -> None:
        rng_points = self._create_random_points()
        c_hull: ConvexHull = ConvexHull(rng_points)
        self.hull: list[int] = c_hull.convex_hull() # Index of each point in the hull

        points: list[tuple[int, int]] = []
        for i in range(len(self.hull)):
            points.append(rng_points[self.hull[i]])
        c_hull.set_new_points_list(points)
        self.hull = c_hull.convex_hull()

        points = self._find_midpoints(points)
        points = self._push_points_apart(points)
        points = self._fix_angles(points)

        self.final_points: list[tuple[int, int]] = []
        for x, y in points:
            x = min(max(x, constants.MARGIN), constants.W_WIDTH - constants.MARGIN)
            y = min(max(y, constants.MARGIN), constants.W_HEIGHT - constants.MARGIN)

            self.final_points.append((x + 500, y + 500)) # Fix magic number

        self.key_points = self._spline_curve()

    # Clears the track
    def clear_track(self) -> None:
        _ = self.image.fill((0,0,0,0))

    # Draws the track
    def draw(self, surface: pygame.Surface, camera: pygame.Rect) -> None:
        self._draw_track()
        _ = surface.blit(self.image, (self.rect.x - camera.x, self.rect.y - camera.y))
