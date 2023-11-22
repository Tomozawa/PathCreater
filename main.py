import numpy as np
from tkinter import messagebox
import datetime
from scipy import interpolate
from matplotlib import pyplot as plt

def main():
    spline_points = np.loadtxt('spline_points.csv', delimiter=',', dtype='float')
    domain = (int(np.ceil(spline_points[0][0])), int(np.floor(spline_points[-1][0])))

    points = []
    f = interpolate.interp1d(spline_points.T[0], spline_points.T[1], kind='quadratic')
    for i in range(domain[0], domain[1]):
        points.append(np.array([i, f(i)]))
    
    plots = plot_point(points, 10)

    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    timestamp = now.strftime('%Y%m%d%H%M%S')
    np.savetxt(f'path_plot{timestamp}.csv', plots, delimiter=',')

    messagebox.showinfo('Path Creater', 'ファイルを保存しました')

    plt.scatter(np.array(plots).T[0], np.array(plots).T[1])
    plt.show()

def plot_point(points: list[np.ndarray], distance: float) -> list:
    if len(points) <= 1:
        return None
    
    pair_vec_iter = []
    for i in range(1, len(points)):
        pair_vec_iter.append({
            'from': points[i - 1].copy(),
            'to': points[i].copy()
        })

    trip_distance = 0
    plots = []

    for pair_vec in pair_vec_iter:
        dif_vec = pair_vec['to'] - pair_vec['from']
        dif_norm = np.linalg.norm(dif_vec, ord=2)
        left_distance = distance - trip_distance
        if left_distance < dif_norm:
            left_dif_ratio = left_distance / dif_norm
            plots.append((1 - left_dif_ratio) * pair_vec['from'] + left_dif_ratio * pair_vec['to'])
            print(left_dif_ratio)
            trip_distance = dif_norm - left_distance
            continue
        trip_distance += dif_norm
    
    return plots

if __name__ == '__main__':
    main()