import numpy as np
import matplotlib.pyplot as plt

class Summary:
    def __init__(self, side):
        self.side = side
        self.r_history = []
        self.durations = []

    def visualize(self):
        r_cumsum = np.cumsum(np.array(self.r_history))

        xpoints = np.arange(1, r_cumsum.size + 1, 1, dtype=int)
        ypoints = np.array(r_cumsum)

        plt.plot(xpoints, ypoints)
        plt.show()

    def __str__(self):
        r = sum(self.r_history)
        num_stops = sum([value == -1 for value in self.r_history])
        num_take_profits = sum([value > 0 for value in self.r_history])
        num_positions = len(self.r_history)
        max_duration = 0
        min_duration = 0
        duration_in_h = 0

        if len(self.durations) > 0:
            max_duration = max(self.durations) / 3600
            min_duration = min(self.durations) / 3600
            duration_in_h = (sum(self.durations) / len(self.durations)) / 3600

        print(f'Max: {max_duration}, Min: {min_duration}, Average: {duration_in_h}')

        header = "{:.7}\t {:.2}\t\t {:.3}\t\t {:<10}\t {:<10}\t {:<10}".format('Side','R','Win Rate','Num Stops', 'Num Profits', 'Num Positions', 'Duration in H')
        entry = "{:.7}\t {:.2f}\t\t {:.3f}\t\t {:<10}\t {:<10}\t {:<10}".format(self.side, r, num_take_profits / num_positions if num_positions else 0, num_stops, num_take_profits, num_positions)
        return "\n".join([header, entry])