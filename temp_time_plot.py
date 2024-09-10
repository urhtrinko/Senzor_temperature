import numpy as np
import matplotlib.pyplot as plt

def graph_T_od_t(data):
    fig, ax = plt.subplots(1, 1, figsize=(6, 4))

    time = data[:, 0]
    temperature = data[:, 1]
    ax.plot(time, temperature, '-', color='C0')

    ax.set_xlabel('Čas [s]', fontsize=18)
    ax.set_ylabel('Temperatura [°C]', fontsize=18)
    ax.tick_params(axis='both', which='major', labelsize=14)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    data = np.loadtxt('Meritve/test_prst_zjutraj.txt')
    graph_T_od_t(data)