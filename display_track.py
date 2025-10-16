
import matplotlib.pyplot as plt
import numpy as np

from math.track import Track

tr = Track()
tr.create_track()
points = tr.get_track()

arr = np.array(points)  # shape will be (n, 2)
x = arr[:, 0]
y = arr[:, 1]

plt.plot(x, y)
plt.show()
