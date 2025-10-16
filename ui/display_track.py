from logic.track import Track

import matplotlib.pyplot as plt
import numpy as np

def display():
    track: Track = Track()
    track.create_track()
    points = track.get_track()

    arr = np.array(points)
    x = arr[:, 0]
    y = arr[:, 1]

    plt.plot(x, y)
    plt.show()
