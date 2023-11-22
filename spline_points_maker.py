import numpy as np

def main():
    np.savetxt('spline_points.csv', np.array(exp()), delimiter=',')

def exp():
    points = []
    for i in range(0, 100, 30):
        points.append([i, 100 * np.exp(-i / 50)])
    return points

if __name__ == '__main__':
    main()