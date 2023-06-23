import os, os.path
import numpy as np
import csv
import matplotlib.pyplot as plt
import random

data_directory = os.path.expanduser("~") + "/profiler/test_wall_1130_1"
data_directory = os.path.expanduser("~") + "/Desktop/PycharmProjects/profile_render/test_wall_1130_1"
os.chdir(data_directory)
total_layer_count = int(len(os.listdir(data_directory)) / 3)  # ie) pose_0, x_0 and y_0 makes up 1 layer
print('tot', total_layer_count)
layer_increment = 3500
# initialize
total_profile_x, total_profile_y = [], []
profile_x, profile_y = {}, {}


def read_csv():
    global profile_x, profile_y
    for files in os.listdir(data_directory):
        print('files:', files)
        if files.startswith('profiles_x_'):
            with open(files, "r") as f:
                reader = csv.reader(f, delimiter=",")
                next(reader)  # skip first row
                for i, data in enumerate(reader):
                    # profile_x.append(data)
                    profile_x[i] = [float(x) for x in data]
                total_profile_x.append([profile_x])
                profile_x = dict()
        elif files.startswith('profiles_y_'):
            with open(files, "r") as f:
                reader = csv.reader(f, delimiter=",")
                next(reader)  # skip first row
                for i, data in enumerate(reader):
                    # profile_y.append(data)
                    profile_y[i] = [-float(x) for x in data]
                total_profile_y.append([profile_y])
                profile_y = dict()
        else:  # poses_#.csv
            pass

    return total_profile_x, total_profile_y


def smoothing_profile(profile_x, profile_y, layer_number):
    for key, item in profile_y[layer_number][0].items():
        a = np.array(item)
        b = a[1:] - a[:-1]
        v = abs(b) > 100
        edges = v.nonzero()[0]
        edges += 2
        if list(edges):  # check if not empty
            for index in sorted(edges, reverse=True):
                del item[index]
                del profile_x[layer_number][0][key][index]

    return profile_x, profile_y


def random_rgb(rand_seed=10):
    random.seed(rand_seed)
    r = random.uniform(0, 1)
    g = random.uniform(0, 1)
    b = random.uniform(0, 1)
    return [(r, g, b)]


def plot(layer_number=0, color="blue", error=100):
    x, y = read_csv()
    x, y = smoothing_profile(x, y, layer_number=layer_number)
    # Structured as: x[layer number][0][nth profile]
    for i in range(0, total_layer_count):
        random_color = random_rgb(rand_seed=i+3)  # every layer with random color
        for j in range(len(x[i][0])):
            if 10 < j < 25:  # excludes profiles of the both ends of a bead
                x_profile_coordinates = x[i][0][j]
                y_profile_coordinates = [a + layer_increment * i for a in y[i][0][j]]
                plt.plot(x_profile_coordinates, y_profile_coordinates, alpha=0.2, color='none')
                plt.fill_between(x_profile_coordinates, np.array(y_profile_coordinates) - error,
                                 np.array(y_profile_coordinates) + error, alpha=0.2, color=random_color, edgecolor="none")
            else:
                pass
    plt.xlabel('x')
    plt.ylabel('z')
    plt.title('{} Profiles Overlap of {} layers'.format(25-10, total_layer_count))
    plt.show()


if __name__ == "__main__":
    plot()
    pass