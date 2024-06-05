import re
import matplotlib.pyplot as plt

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
