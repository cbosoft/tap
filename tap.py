from matplotlib import pyplot as plt
import time
import subprocess as sp
import os
import sys

class ProgressBar:

    def __init__(self, length):
        self.length = length
        self.pos = -1

    def update(self, i=None):
        rows, columns = os.popen('stty size', 'r').read().split()

        if i is None:
            i = self.pos + 1

        frac = f'▌{i+1}/{self.length}▐'
        columns = int(columns) - len(frac)
        col_per_i = columns / self.length
        prog = int(col_per_i * (i+1))
        prog = frac.rjust(prog-1, '█') + '█'
        end = '' if i < self.length-1 else '\n'
        print(f'█{prog}\r', end=end)

        self.pos = i

    def clear(self):
        print('\u001b[2K')


def run(command, count=100):
    lengths = list()
    times = list()
    routes = list()

    pb = ProgressBar(count)
    for i in range(count):
        pb.update()
        start = time.time()
        pr = sp.Popen(command, shell=True, stderr=sp.PIPE, stdout=sp.PIPE)
        pr.wait()
        end = time.time()
        length = float(pr.stderr.read().decode())
        times.append(end - start)
        lengths.append(length)

        route = pr.stdout.read().decode()[:-1]
        route = [[float(c) for c in r.split()] for r in route.split('\n')]
        route = list(zip(*route))
        routes.append(route)
    return lengths, times, routes


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tap.py <travelling-salesman-command> [<name>]")
        exit(1)

    lengths, times, routes = run(sys.argv[1])

    plt.subplots_adjust(hspace=0.1, wspace=0.25)
    fig, ((timeax, lengthax), (routeax, __)) = plt.subplots(nrows=2, ncols=2)

    timeax.hist(times, bins=int(len(times)**0.5))
    timeax.set_title("Time Distribution")

    lengthax.hist(lengths, bins=int(len(lengths)**0.5))
    lengthax.set_title("Distance Distribution")

    for (rx, ry) in routes:
        routeax.plot(rx, ry)
    routeax.set_xlabel("X")
    routeax.set_ylabel("Y")
    routeax.set_title("Route")
    name = "unnamed" if len(sys.argv) < 3 else sys.argv[2]
    plt.savefig(f'result_{name}.pdf', bbox_inches='tight')

