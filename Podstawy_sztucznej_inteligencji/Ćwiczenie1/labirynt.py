from collections import deque
import os
import time

KIERUNKI = {
    '┼': ['G', 'D', 'L', 'P'], '┐': ['D', 'L'], '┤': ['G', 'D', 'L'], '╵': ['G'],
    '│': ['G', 'D'], '┘': ['G', 'L'], '┴': ['G', 'L', 'P'], '╷': ['D'],
    '─': ['L', 'P'], '└': ['G', 'P'], '├': ['G', 'D', 'P'], '╴': ['L'],
    ' ': [], '┌': ['D', 'P'], '┬': ['D', 'L', 'P'], '╶': ['P']
}


CZERWONY = "\033[1;31m"
ZIELONY = "\033[1;32m"
ZOLTY   = "\033[1;33m"
NIEBIESKI = "\033[1;34m"
RESET   = "\033[0m"

def wczytaj_mape(sciezka_do_pliku):
    with open(sciezka_do_pliku, encoding="utf-8") as plik:
        mapa = [list(wiersz.rstrip('\n')) for wiersz in plik]

    maksymalna_dlugosc = max(len(wiersz) for wiersz in mapa)
    for wiersz in mapa:
        while len(wiersz) < maksymalna_dlugosc:
            wiersz.append(' ')
    return mapa


def rysuj_mape(mapa, start, cel, odwiedzone, oczekujace):
    # os.system('clear')
    os.system('cls')
    for numer_wiersza, wiersz in enumerate(mapa):
        for numer_kolumny, znak in enumerate(wiersz):
            pozycja = (numer_wiersza, numer_kolumny)
            if pozycja == start:
                print(CZERWONY + znak + RESET, end='')
            elif pozycja == cel:
                print(NIEBIESKI + znak + RESET, end='')
            elif pozycja in oczekujace:
                print(ZOLTY + znak + RESET, end='')
            elif pozycja in odwiedzone:
                print(ZIELONY + znak + RESET, end='')
            else:
                print(znak, end='')
        print()
    time.sleep(0.1)


def znajdz_sasiadow(mapa, wiersz, kolumna):
    sasiedzi = []
    liczba_wierszy = len(mapa)
    liczba_kolumn = len(mapa[0])
    dozwolone = KIERUNKI.get(mapa[wiersz][kolumna], [])

    for kierunek in dozwolone:
        if kierunek == 'G' and wiersz > 0 and 'D' in KIERUNKI.get(mapa[wiersz-1][kolumna], []):
            sasiedzi.append((wiersz - 1, kolumna))
        elif kierunek == 'D' and wiersz < liczba_wierszy - 1 and 'G' in KIERUNKI.get(mapa[wiersz + 1][kolumna],[]):
            sasiedzi.append((wiersz + 1, kolumna))
        elif kierunek == 'L' and kolumna > 0 and 'P' in KIERUNKI.get(mapa[wiersz][kolumna - 1], []):
            sasiedzi.append((wiersz, kolumna - 1))
        elif kierunek == 'P' and kolumna < liczba_kolumn - 1 and 'L' in KIERUNKI.get(mapa[wiersz][kolumna + 1], []):
            sasiedzi.append((wiersz, kolumna + 1))

    return sasiedzi
    
def szukaj_bfs(mapa, start, cel):
    kolejka = deque([start])
    odwiedzone = set([start])
    licznik_krokow = 0

    while kolejka:
        oczekujace = list(kolejka)
        rysuj_mape(mapa,start,cel,odwiedzone,oczekujace)

        akutalny_wiersz, aktualna_kolumna = kolejka.popleft()

        if (akutalny_wiersz, aktualna_kolumna) == cel:
            return True, licznik_krokow
        
        for nowy_wiersz, nowa_kolumna in znajdz_sasiadow(mapa, akutalny_wiersz, aktualna_kolumna):
            if (nowy_wiersz, nowa_kolumna) not in odwiedzone:
                odwiedzone.add((nowy_wiersz, nowa_kolumna))
                kolejka.append((nowy_wiersz, nowa_kolumna))

        licznik_krokow += 1

    return False, licznik_krokow


def szukaj_dfs(mapa, start, cel):
    stos = [start]
    odwiedzone = set([start])
    licznik_krokow = 0

    while stos:
        oczekujace = list(stos)
        rysuj_mape(mapa,start,cel,odwiedzone,oczekujace)

        aktualny_wiersz, aktualna_kolumna = stos.pop()

        if (aktualny_wiersz, aktualna_kolumna) == cel:
            return True, licznik_krokow
        
        for nowy_wiersz, nowa_kolumna in znajdz_sasiadow(mapa, aktualny_wiersz, aktualna_kolumna):
            if (nowy_wiersz, nowa_kolumna) not in odwiedzone:
                odwiedzone.add((nowy_wiersz, nowa_kolumna))
                stos.append((nowy_wiersz, nowa_kolumna))
        
        licznik_krokow += 1

    return False, licznik_krokow


sciezka = input("Podaj nazwę pliku z mapą: ")
mapa = wczytaj_mape(sciezka)

start_y, start_x = map(int, input("Współrzędne startowe (wiersz, kolumna): ").split())
cel_y, cel_x = map(int, input("Współrzędne końcowe (wiersz kolumna): ").split())
algorytm = input("(BFS/DFS)? ").strip().upper()

if algorytm == "BFS":
    znaleziono, kroki = szukaj_bfs(mapa, (start_y, start_x), (cel_y, cel_x))
else:
    znaleziono, kroki = szukaj_dfs(mapa, (start_y, start_x), (cel_y, cel_x))

if znaleziono:
    print(f"Znaleziono scieżkę, liczba {kroki} kroków")
else :
    print(f"Nie znaleziono scieżki, liczba {kroki} kroków")




