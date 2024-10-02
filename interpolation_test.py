from constants import *
import numpy as np
from scipy import interpolate
import track

#tck, u = interpolate.splprep([x, y], s=0, per=True)

# If periodic motion, aka last element and first element are the same, set per to true.
# in the source, this sets last value equal to first value

# S is the smoothness of the curve, keep this 0

#xi, yi = interpolate.splev(np.linspace(0, 1, TRACK_POINTS), tck)