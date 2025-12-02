import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sympy as sp
import random
import math

WZOR_FUNKCJI = "x**2 - 10*cos(2*pi*x) + x/5"

X_START = -5.0
X_END = 5.0
CEL = 'max'
ALGORYTM = 'sa' # 'hc' lub 'sa'


TEMP_POCZATKOWA = 10.0
TEMP_KONCOWA = 0.01
STRATEGIA_CHLODZENIA = 'geometryczna' # 'liniowa' lub 'geometryczna'
WSPOLCZYNNIK_CHLODZENIA = 0.90  #geometrycznej (np. 0.95), liniowej (np. 0.1)


KROK_MAX = 0.5 
LICZBA_KROKOW = 200


def przygotuj_funkcje(wzor):
    x = sp.symbols('x')
    wyrazenie = sp.sympify(wzor)
    f = sp.lambdify(x, wyrazenie, modules=['numpy'])
    return f

func = przygotuj_funkcje(WZOR_FUNKCJI)


def czy_lepszy(nowy_y, stary_y, cel):
    if cel == 'min':
        return nowy_y < stary_y
    else: # max
        return nowy_y > stary_y

def uruchom_symulacje():
    historia_x = []
    historia_y = []
    historia_temp = []

    # punkt startowy
    obecne_x = random.uniform(X_START, X_END)
    obecne_y = func(obecne_x)
    
    temperatura = TEMP_POCZATKOWA
    
    historia_x.append(obecne_x)
    historia_y.append(obecne_y)
    historia_temp.append(temperatura)

    best_x = obecne_x
    best_y = obecne_y

    for i in range(LICZBA_KROKOW):
        przesuniecie_krok = random.uniform(-KROK_MAX, KROK_MAX)
        nowe_x = obecne_x + przesuniecie_krok

        nowe_x = max(X_START, min(nowe_x, X_END))
        nowe_y = func(nowe_x)

        delta = nowe_y - obecne_y
        if CEL == 'max':
            delta = -delta
        

        akceptacja = False
        
        if ALGORYTM == 'hc':
            if czy_lepszy(nowe_y, obecne_y, CEL):
                akceptacja = True


        elif ALGORYTM == 'sa':
            if delta < 0:
                akceptacja = True
            else:
                prawdopodobienstwo = math.exp(-delta / temperatura) if temperatura > 0 else 0
                
                if random.random() < prawdopodobienstwo:
                    akceptacja = True

            if STRATEGIA_CHLODZENIA == 'liniowa':
                temperatura -= WSPOLCZYNNIK_CHLODZENIA
            else: # geometryczna
                temperatura *= WSPOLCZYNNIK_CHLODZENIA
            
            temperatura = max(temperatura, 0.00001)

        if akceptacja:
            obecne_x = nowe_x
            obecne_y = nowe_y
            
            if czy_lepszy(obecne_y, best_y, CEL):
                best_x = obecne_x
                best_y = obecne_y

        historia_x.append(obecne_x)
        historia_y.append(obecne_y)
        historia_temp.append(temperatura)

    return historia_x, historia_y, best_x, best_y

hist_x, hist_y, wynik_x, wynik_y = uruchom_symulacje()

print(f"Znalezione ekstremum ({CEL}):")
print(f"x = {wynik_x:.4f}")
print(f"y = {wynik_y:.4f}")



#animacja
x_tlo = np.linspace(X_START, X_END, 1000)
y_tlo = func(x_tlo)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x_tlo, y_tlo, 'b-', label='Funkcja', alpha=0.5)
ax.set_title(f"Algorytm: {ALGORYTM.upper()} | Cel: {CEL.upper()}")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid(True)


punkt, = ax.plot([], [], 'ro', markersize=10, label='Aktualna pozycja')
sciezka, = ax.plot([], [], 'r:', alpha=0.5) # Ślad
tekst = ax.text(0.02, 0.15, '', transform=ax.transAxes)

def init():
    punkt.set_data([], [])
    sciezka.set_data([], [])
    tekst.set_text('')
    return punkt, sciezka, tekst

def update(frame):
    x = hist_x[frame]
    y = hist_y[frame]
    
    punkt.set_data([x], [y])
    

    start_trace = max(0, frame - 20)
    sciezka.set_data(hist_x[start_trace:frame+1], hist_y[start_trace:frame+1])
    

    info = f"Krok: {frame}\nx: {x:.2f}\ny: {y:.2f}"
    if ALGORYTM == 'sa':
        temp = 0 if frame >= len(hist_x) else hist_x[frame] 
    tekst.set_text(info)
    return punkt, sciezka, tekst

ani = animation.FuncAnimation(fig, update, frames=len(hist_x), 
                              init_func=init, blit=True, interval=50)

plt.show()