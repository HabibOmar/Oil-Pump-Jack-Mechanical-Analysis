import math
import matplotlib.pyplot as plt

# Defining constants
a1 = 350.0
a2 = 150.0
a3 = 450.0
a4 = 300.0
a5 = 700.0
b1 = 350.0
b4 = 220.0
c1 = 170.0
B4 = 165.0
B4_rad = math.radians(B4)


# Joint Variables Functions
def k1(theta2):
    return a2 * math.cos(theta2) + a1


def k2(theta2):
    return a2 * math.sin(theta2) - b1


def k3(x1, x2):
    return (a4 ** 2 - a3 ** 2 - x1 ** 2 - x2 ** 2) / (2 * a3)


def t13_plus(x1, x2, x3):
    return (x2 + math.sqrt(x1 ** 2 + x2 ** 2 - x3 ** 2)) / (x1 + x3)


def t13_minus(x1, x2, x3):
    return (x2 - math.sqrt(x1 ** 2 + x2 ** 2 - x3 ** 2)) / (x1 + x3)


def theta_13(x):
    return 2 * math.atan(x)


def theta_14(theta, x):
    return math.asin((a3 * math.sin(theta) + x) / a4)


def k4(theta4):
    angle = float(theta4 - B4_rad)
    return b4 * math.cos(angle) + c1


def k5(theta4):
    angle = float(theta4 - B4_rad)
    return b4 * math.sin(angle) + b1


def theta_15_plus(x4):
    return math.acos(x4 / a5)


def theta_15_minus(x4):
    return math.acos(x4 / a5)


def s16(theta5, x5):
    return a5 * math.sin(theta5) - x5


# A function to change back from radians to degrees and to make sure angle is between 0 and 360
def angle_fixer(array):
    for i in range(len(array)):
        array[i] = math.degrees(array[i])
        if array[i] < 0:
            array[i] += 360
        elif array[i] > 360:
            array[i] -= 360
    return array


def plotter(array1, array2, y_axis):
    plt.plot(array1, array2)
    plt.xlabel("Theta_12 (\u00B0)")
    plt.ylabel("%s (\u00B0)" % y_axis)
    plt.title("Theta_12 against %s" % y_axis)
    plt.show()


# Full cycle position analysis
with open("Results.txt", "w+") as results_file:
    results_file.write("\t\t\t\tClosure 1\t\t\t\t\t\t\tClosure 2\n")
    results_file.write(
        "{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}\n".format('theta12', 'theta13', 'theta14',
                                                                                  'theta15', 's16', 'theta13',
                                                                                  'theta14', 'theta15', 's16'))
    results_file.write(
        "_______________________________________________________________________________________"
        "___________________________________________________\n")

    # initializing arrays to use in matplotlib
    theta_12_arr = [i for i in range(0, 360)]
    theta_13_arr = []
    theta_14_arr = []
    theta_15_arr = []
    s16_arr = []

    for theta_12 in range(0, 360):
        theta_12_rad = math.radians(theta_12)
        theta13_1 = theta_13(t13_plus(k1(theta_12_rad), k2(theta_12_rad), k3(k1(theta_12_rad), k2(theta_12_rad))))
        theta13_2 = theta_13(t13_minus(k1(theta_12_rad), k2(theta_12_rad), k3(k1(theta_12_rad), k2(theta_12_rad))))
        theta_13_arr.append(theta13_1)
        # print(theta13_1, theta13_2)

        theta14_1 = theta_14(theta13_1, k2(theta_12_rad))
        theta14_2 = theta_14(theta13_2, k2(theta_12_rad))
        theta_14_arr.append(theta14_1)
        # print(theta14_1, theta14_2)

        theta_15_1 = theta_15_plus(k4(theta14_1))
        theta_15_2 = theta_15_minus(k4(theta14_2))
        theta_15_arr.append(theta_15_1)
        # print(theta_15_1, theta_15_2)

        s16_1 = s16(theta_15_1, k5(theta14_1))
        s16_2 = s16(theta_15_2, k5(theta14_2))
        s16_arr.append(s16_1)
        # print(s16_1, s16_2)

        results_file.write("%.3f\t\t%.4f\t\t%.4f\t\t%.4f\t\t%.4f\t%.4f\t\t%.4f\t\t%.4f\t\t%.4f\n" % (
            theta_12, theta13_1, theta14_1, theta_15_1, s16_1, theta13_2, theta14_2, theta_15_2, s16_2))
# Making sure angles are between 0 and 360
angle_fixer(theta_13_arr)
angle_fixer(theta_14_arr)
angle_fixer(theta_15_arr)

# Plotting graphs for first closure
plotter(theta_12_arr, theta_13_arr, "Theta_13")
plotter(theta_12_arr, theta_14_arr, "Theta_14")
plotter(theta_12_arr, theta_15_arr, "Theta_15")
plotter(theta_12_arr, s16_arr, "s16")
