import matplotlib.pyplot as plt
import math
import numpy as np

if __name__ == "__main__":
    convex_hull = [0, 0.0012, 0.009, 0.0832, 0.8024, 4.4934, 9.0436]
    ch = [i * 1.5 for i in convex_hull]
    n_2 = [i ** 2 for i in range(1, 8)]
    log = [i * math.log(i) for i in range(1, 8)]
    fig, ax = plt.subplots()
    x = np.linspace(0, 1000000, 7)

    plt.plot(x, ch, label='convex hull')  # blue
    plt.plot(x, n_2, label='n^2')  # orange
    plt.plot(x, log, label='log')  # green

    plt.xlabel("n")
    plt.ylabel("t")
    plt.title("Convex Hull Analysis")
    ax.set_xscale('log')
    plt.show()
