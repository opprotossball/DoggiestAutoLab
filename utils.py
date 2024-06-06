import re
import matplotlib.pyplot as plt
import os
import json
import numpy as np

def parse(file_path):
    best_list = []
    worst_list = []
    mean_list = []
    with open(file_path, 'r', encoding='cp1252') as file:
        for line in file:
            vals = re.findall(r'dl=([\d\.]+)', line)
            if len(vals) < 3:
                continue
            best_list.append(float(vals[0]))
            worst_list.append(float(vals[1]))
            mean_list.append(float(vals[2]))
    return best_list, worst_list, mean_list

def plot(best, worst, mean, title='Koszt', x_label='Numer pokolenia'):
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(best)), best, label='Najlepszy')
    plt.plot(range(len(worst)), worst, label='Najgorszy')
    plt.plot(range(len(mean)), mean, label='Średnia')
    plt.xlabel(x_label)
    plt.ylabel('Koszt')
    plt.title(title)
    plt.legend()
    plt.show()

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]

def plot_optimization(path):
    files = os.listdir(path)
    files.sort(key=natural_sort_key)
    bests = []
    avgs = []
    worsts = []
    for file_name in files:
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            print(f"Processing file: {file_name}")
            b, w, a = parse(file_path)
            bests.append(b[-1])
            avgs.append(a[-1])
            worsts.append(w[-1])
    plot(bests, worsts, avgs, x_label='Optymalizacja')

def print_results(path):
    bests, worsts, avgs = parse(path)
    print(f'Najlepszy: {bests[-1]:.2f}')
    print(f'Średni: {avgs[-1]:.2f}')
    print(f'Najgorszy: {worsts[-1]:.2f}')

def get_parameters(path):
    json_lines = []
    reading_json = False
    with open(path, 'r', ) as file:
        for line in file:
            if line.strip().startswith('{'):
                reading_json = True
            if reading_json:
                json_lines.append(line.strip())
            if line.strip().endswith('}'):
                break
    json_string = ' '.join(json_lines)
    try:
        json_data = json.loads(json_string)
    except json.JSONDecodeError:
        raise Exception("The JSON data is not valid.")
    return json_data

def print_parameters(path):
        for key, value in get_parameters(path).items():
            if key == 'pokolenia' or key == 'osobniki':
                print(f"{key}: {int(value)}")
            else:
                print(f"{key}: {value:.2f}")

def best_params_and_costs(path):
    files = os.listdir(path)
    files.sort(key=natural_sort_key)
    best_avg = 999999
    best = 999999
    worst = 999999
    best_params = None
    for file_name in files:
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            b, w, a = parse(file_path)
            if a[-1] < best_avg:
                print(f"Best file so far: {file_name}")
                best_avg = a[-1]
                best = b[-1]
                worst = w[-1]
                best_params = get_parameters(file_path)
    print(f'Najlepszy: {best:.2f}')
    print(f'Średni: {best_avg:.2f}')
    print(f'Najgorszy: {worst:.2f}')
    for key, value in best_params.items():
        if key == 'pokolenia' or key == 'osobniki':
            print(f"{key}: {int(value)}")
        else:
            print(f"{key}: {value:.2f}")

def param_impact(path):
    all_params = ["pokolenia", "osobniki", "aco_ro", "aco_alfa", "aco_beta", "aco_wsp_ob"]
    vals = {p: [] for p in all_params}
    files = os.listdir(path)
    for file_name in files:
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            b, w, a = parse(file_path)
            params = get_parameters(file_path)
            for p in all_params:
                vals[p].append((params[p], a[-1]))
    for p in all_params:
        plot_param_impact(vals, p)

def plot_param_impact(impact_dir, param):
    vals = impact_dir[param]
    x, y = zip(*vals)
    x = np.array(x)
    y = np.array(y)
    # coefficients = np.polyfit(x, y, 1)
    # polynomial = np.poly1d(coefficients)
    # y_fit = polynomial(x)
    plt.scatter(x, y)
    # plt.plot(x, y_fit, color='red')
    plt.xlabel(f'{param}')
    plt.ylabel('Średni koszt')
    plt.title(f"Wpływ parametru '{param}' na koszt")
    plt.show()

def apb_param_impact(path):
    all_params = ["pokolenia", "osobniki", "aco_ro", "aco_alfa", "aco_beta", "aco_wsp_ob"]
    vals = {p: [] for p in all_params}
    files = os.listdir(path)
    for file_name in files:
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            _, _, a = parse(file_path)
            params = get_parameters(file_path)
            for p in all_params:
                vals[p].append((params[p], a[-1]))
    x = [a[0] / b[0] for a, b in zip(vals['aco_alfa'], vals['aco_beta'])]
    y = [v[1] for v in vals['aco_alfa']]
    x = np.array(x)
    y = np.array(y)
    plt.scatter(x, y)
    plt.xlabel(r'$\alpha$ / $\beta$')
    plt.ylabel('Średni koszt')
    plt.title(r"Wpływ stosunku $\alpha$ i $\beta$ na koszt")
    plt.show()
