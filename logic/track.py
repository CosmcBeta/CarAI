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

    def _create_points(self) -> NDArray[np.int64]:
        number_of_points = self.rng.integers(constants.MIN_POINTS, constants.MAX_POINTS, endpoint=True)

        x = self.rng.integers(constants.MARGIN, constants.W_WIDTH - constants.MARGIN, number_of_points, endpoint=True)
        y = self.rng.integers(constants.MARGIN, constants.W_WIDTH - constants.MARGIN, number_of_points, endpoint=True)
        return np.column_stack((x, y))

    def _find_midpoints(self, points: NDArray[np.int64]):
        x, y = np.hsplit(points, (1,))

        x1 = x[1:]
        x2 = x[:-1]

        y1 = y[1:]
        y2 = y[:-1]

        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2

        mid_points = np.hstack((mid_x, mid_y))

        xf, xl = x[0], x[-1]
        yf, yl = y[0], y[-1]
        mx = (xf + xl) // 2
        my = (yf + yl) // 2

        mp = np.array([mx, my])
        mp = np.reshape(mp, (-1, 2))
        # print(mp.shape)
        mid_points = np.vstack((mid_points, mp))


        displacement = self.rng.integers(constants.MIN_DISPLACEMENT, constants.MAX_DISPLACEMENT, mid_points.size).reshape((-1, 2))

        mid_points += displacement

        new_points = np.empty(points.size + mid_points.size, dtype=points.dtype).reshape(points.shape[0] + mid_points.shape[0], 2)

        k = 0
        for i in range(len(points)):
            new_points[k] = points[i]
            k += 1
            new_points[k] = mid_points[i]
            k += 1

        return new_points


    def create_track(self) -> NDArray[np.int64]:
        rng_points = self._create_points()
        convex_hull = ConvexHull(rng_points)

        hull_points: NDArray[np.int64] = rng_points[convex_hull.vertices]

        center = np.mean(hull_points, 0)
        angles = np.arctan2(hull_points[:, 1] - center[1], hull_points[:, 0] - center[0])
        sorted_indices = np.argsort(angles)
        ordered_hull: NDArray[np.int64] = hull_points[sorted_indices]

        with_mid = self._find_midpoints(ordered_hull)

        return with_mid
        # points = self._find_midpoints(points)
        # points = self._push_points_apart(points)
        # points = self._fix_angles(points)
