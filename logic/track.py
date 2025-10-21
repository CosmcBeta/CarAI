import numpy as np
import sys

from numpy.typing import NDArray
from scipy.spatial import ConvexHull

from util import constants
class Track:
    def __init__(self) -> None:
        self.randomize_seed()
        self.set_seed(1)

    def randomize_seed(self) -> None:
        self.seed: int = np.random.randint(sys.maxsize)
        self.rng: np.random.Generator = np.random.default_rng(self.seed)

    def set_seed(self, seed: int) -> None:
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def get_seed(self) -> int:
        return self.seed

    def _create_points(self) -> NDArray[np.float64]:
        number_of_points = self.rng.integers(constants.MIN_POINTS, constants.MAX_POINTS, endpoint=True)

        margin = constants.MARGIN
        high = constants.W_WIDTH - constants.MARGIN

        x = self.rng.random(number_of_points) * (high - margin) + margin
        y = self.rng.random(number_of_points) * (high - margin) + margin

        # x = self.rng.(constants.MARGIN, constants.W_WIDTH - constants.MARGIN, number_of_points, endpoint=True)
        # y = self.rng.(constants.MARGIN, constants.W_WIDTH - constants.MARGIN, number_of_points, endpoint=True)
        return np.column_stack((x, y))

    # Finds the midpoints between each point, then adds a random displacement to them and adds them to the array
    def _find_midpoints(self, points: NDArray[np.float64]) -> NDArray[np.float64]:
        x, y = np.hsplit(points, (1,))
        x1, x2 = x[1:], x[:-1]
        y1, y2 = y[1:], y[:-1]
        mid_points = np.hstack(((x1 + x2) / 2, (y1 + y2) / 2))

        x_first, x_last = x[0], x[-1]
        y_first, y_last = y[0], y[-1]
        mp = np.array([(x_first + x_last) / 2, (y_first + y_last) / 2]).reshape((-1, 2))
        mid_points = np.vstack((mid_points, mp))

        displacement = self.rng.integers(constants.MIN_DISPLACEMENT, constants.MAX_DISPLACEMENT, mid_points.size).reshape((-1, 2))
        mid_points += displacement

        new_points = np.empty((2 * len(points), 2), dtype=points.dtype)
        new_points[0::2] = points
        new_points[1::2] = mid_points

        return new_points

    def _push_points_apart(self, points: NDArray[np.float64]):
        x, y = np.hsplit(points, (1,))
        x1, x2 = x[1:], x[:-1]
        y1, y2 = y[1:], y[:-1]

        x_first, x_last = x[0], x[-1]
        y_first, y_last = y[0], y[-1]
        x1 = np.vstack((x1, x_first))
        x2 = np.vstack((x_last, x2))
        y1 = np.vstack((y1, y_first))
        y2 = np.vstack((y_last, y2))

        dx = x2 - x1
        dy = y2 - y1
        distance = np.sqrt(dx**2 + dy**2)

        mask = distance < constants.DISTANCE_BETWEEN_POINTS
        diff = constants.DISTANCE_BETWEEN_POINTS - distance
        diff = diff[:, np.newaxis]

        direction = np.stack((dx, dy), axis=1)
        direction /= distance[:, np.newaxis]
        move = direction * diff
        points[1:][mask] += move[mask]

        return points




    def create_track(self) -> NDArray[np.float64]:
        rng_points = self._create_points()
        convex_hull = ConvexHull(rng_points)

        hull_points: NDArray[np.float64] = rng_points[convex_hull.vertices]

        center = np.mean(hull_points, 0)
        angles = np.arctan2(hull_points[:, 1] - center[1], hull_points[:, 0] - center[0])
        sorted_indices = np.argsort(angles)
        ordered_hull: NDArray[np.float64] = hull_points[sorted_indices]

        with_mid = self._find_midpoints(ordered_hull)
        # with_push = self._push_points_apart(with_mid)

        return with_mid
        # points = self._find_midpoints(points)
        # points = self._fix_angles(points)
