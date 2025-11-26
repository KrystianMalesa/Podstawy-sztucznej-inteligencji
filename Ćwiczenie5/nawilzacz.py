import numpy as np
import matplotlib.pyplot as matplot

WAGA_WILGOTNOSCI = 1.0  
WAGA_CENY = 0.5  
WAGA_TEMP = 0.2  

def funkcja_przynaleznosci_wyklad(x, a, b):
    return np.exp( - (np.abs(x - a)**2) / (b**2) )

def sterownik_rozmyty(wilg, temp, cena):
    #Fuzyfikacja
    wil_niska  = funkcja_przynaleznosci_wyklad(wilg, a=20, b=20) * WAGA_WILGOTNOSCI
    wil_wysoka = funkcja_przynaleznosci_wyklad(wilg, a=80, b=20) * WAGA_WILGOTNOSCI

    c_tanio = funkcja_przynaleznosci_wyklad(cena, a=0.5, b=0.5) * WAGA_CENY
    c_drogo = funkcja_przynaleznosci_wyklad(cena, a=1.5, b=0.5) * WAGA_CENY

    t_zimno = funkcja_przynaleznosci_wyklad(temp, a=15, b=7) * WAGA_TEMP

    #wnioskowanie
    aktywacja_off = wil_wysoka

    aktywacja_high = np.minimum(wil_niska, c_tanio)

    aktywacja_med_ekonomiczna = np.minimum(wil_niska, c_drogo)
    
    aktywacja_med = np.maximum(aktywacja_med_ekonomiczna, t_zimno)

    #Defuzyfikacja
    x_out = np.linspace(0, 100, 100)
    
    ksztalt_off  = funkcja_przynaleznosci_wyklad(x_out, a=0, b=20)
    ksztalt_med  = funkcja_przynaleznosci_wyklad(x_out, a=50, b=20)
    ksztalt_high = funkcja_przynaleznosci_wyklad(x_out, a=100, b=20)

    wynik_off  = np.minimum(ksztalt_off, aktywacja_off)
    wynik_med  = np.minimum(ksztalt_med, aktywacja_med)
    wynik_high = np.minimum(ksztalt_high, aktywacja_high)

    finalny_ksztalt = np.maximum(wynik_off, np.maximum(wynik_med, wynik_high))

    licznik = np.sum(x_out * finalny_ksztalt)
    mianownik = np.sum(finalny_ksztalt)

    if mianownik == 0: return 0
    return licznik / mianownik

def rysuj_charakterystyki():
    wilg_zakres = np.linspace(0, 100, 40)
    temp_zakres = np.linspace(15, 30, 40)
    X, Y = np.meshgrid(wilg_zakres, temp_zakres)
    
    ceny = [0.5, 1.0, 1.5]
    labels = ["Tani Prąd (0.5)", "Średnia Cena (1.0)", "Drogi Prąd (1.5)"]

    figura = matplot.figure(figsize=(19, 10))

    for i, cena in enumerate(ceny):
        Z = np.zeros_like(X)
        for r in range(X.shape[0]):
            for c in range(Y.shape[1]):
                Z[r,c] = sterownik_rozmyty(X[r,c], Y[r,c], cena)

        ax = figura.add_subplot(1, 3, i+1, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis')
        ax.set_title(f'{labels[i]}')
        ax.set_xlabel('Wilgotność [%]')
        ax.set_ylabel('Temp [C]')
        ax.set_zlabel('Moc [%]')
        ax.set_zlim(0, 100)

    matplot.tight_layout()
    matplot.show()

if __name__ == "__main__":
    rysuj_charakterystyki()