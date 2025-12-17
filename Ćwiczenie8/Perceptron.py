import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.lines import Line2D

data = [
    (np.array([1, -3, -4]), -1),
    (np.array([1, -2,  1]), -1),
    (np.array([1,  0,  1]), -1),
    (np.array([1,  2,  2]), -1),
    (np.array([1, -2, -4]),  1),
    (np.array([1,  0, -2]),  1),
    (np.array([1,  2,  1]),  1),
    (np.array([1,  3, -4]),  1)
]

wagi_startowe = np.random.rand(3) 
learning_rate = 0.1  # lr            
max_iter = 1000                   


def funkcja_aktywacji(x):
    return 1 if x >= 0 else -1

def rysuj_wykres(dane, wagi, epoka, tytul=""):
    plt.figure(figsize=(8, 6))
    
    # Rysowanie punktów
    for x, t in dane:
        color = 'red' if t == -1 else 'green'
        marker = 'o' if t == -1 else '^'
        plt.scatter(x[1], x[2], c=color, marker=marker, s=100)
    
    x_axis = np.linspace(-5, 5, 100)
    if wagi[2] != 0:
        y_axis = -(wagi[1] * x_axis + wagi[0]) / wagi[2]
        plt.plot(x_axis, y_axis, '-b')
    else:
        plt.axvline(x=-wagi[0]/wagi[1], color='b')

    legend_elements = [
        Line2D([0], [0], color='b', label='Linia decyzyjna'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Klasa -1'),
        Line2D([0], [0], marker='^', color='w', markerfacecolor='green', markersize=10, label='Klasa 1')
    ]
    plt.legend(handles=legend_elements, loc='upper left')

    plt.title(f"Perceptron - Epoka {epoka} {tytul}")
    plt.grid(True)
    plt.xlim(-5, 5)
    plt.ylim(-6, 4)
    plt.show()

def trenuj_perceptron(dane, wagi, lr, limit):
    obecne_wagi = wagi.copy()
    epoka = 0
    bledy = True 
    
    while bledy and epoka < limit:
        bledy = False 
        random.shuffle(dane)
        
        epoka += 1
        licznik_bledow = 0
        
        for x, t in dane:
            net = np.dot(obecne_wagi, x) # net = (1 * w0) + (x1 * w1) + (x2 * w2)
                                         # Suma = (Bias * WagaBiasu) + (Cecha1 * Waga1) + (Cecha2 * Waga2)
            y = funkcja_aktywacji(net)
            
            if y != t:
                obecne_wagi = obecne_wagi + lr * (t - y) * x
                bledy = True
                licznik_bledow += 1
                
        print(f"Epoka {epoka}: błędów = {licznik_bledow}, wagi = {np.round(obecne_wagi, 3)}")
        rysuj_wykres(dane, obecne_wagi, epoka, f"(Błędów: {licznik_bledow})")
        
    return obecne_wagi, epoka

if __name__ == "__main__":
    rysuj_wykres(data, wagi_startowe, 0, "(Start)")

    wagi_koncowe, liczba_epok = trenuj_perceptron(data, wagi_startowe, learning_rate, max_iter)


    print(f"Ostateczne wagi: {wagi_koncowe}")
    print(f"Liczba epok: {liczba_epok}")
    rysuj_wykres(data, wagi_koncowe, liczba_epok, "(KONIEC)")