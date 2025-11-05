import random
import time

N = 12                
POP_SIZE = 200   
MUTATION_CHANCE = 0.25
CROSSOVER_CHANCE = 0.75
MAX_ITER = 10000
ELITISM = 2      


def losowy_uklad(n):
    return [random.randint(0, n - 1) for _ in range(n)]

def inicjalizuj_populacje(n, rozmiar):
    return [losowy_uklad(n) for _ in range(rozmiar)]

def ocena(osobnik):
    blad = 0
    n = len(osobnik)
    for i in range(n):
        for j in range(i + 1, n):
            if osobnik[i] == osobnik[j] or abs(osobnik[i] - osobnik[j]) == abs(i - j):
                blad += 1
    return blad

def krzyzowanie(rodzic1, rodzic2):
    if random.random() > CROSSOVER_CHANCE:
        return rodzic1[:], rodzic2[:]
    punkt = random.randint(1, len(rodzic1) - 2)
    return rodzic1[:punkt] + rodzic2[punkt:], rodzic2[:punkt] + rodzic1[punkt:]

def mutacja(osobnik, n):
    if random.random() < MUTATION_CHANCE:
        i = random.randint(0, n - 1)
        osobnik[i] = random.randint(0, n - 1)
    return osobnik

def najlepszy_osobnik(populacja):
    najlepszy = min(populacja, key=ocena)
    return najlepszy, ocena(najlepszy)

def pokaz_plansze(uklad):
    n = len(uklad)
    naglowek = "   " + " ".join(chr(65 + x) for x in range(n))
    print(naglowek)
    for wiersz in range(n):
        linia = ["Q" if uklad[wiersz] == kol else "." for kol in range(n)]
        print(f"{wiersz + 1:2}  " + " ".join(linia))


def algorytm_genetyczny():
    if N in (2, 3):
        print("Dla N=2 i N=3 nie istnieją rozwiązania.")
        return

    populacja = inicjalizuj_populacje(N, POP_SIZE)
    najlepszy, najlepszy_fit = najlepszy_osobnik(populacja)
    generacja = 0
    print(f"Początkowy fitness: {najlepszy_fit}")

    start = time.time()
    while generacja < MAX_ITER:
        generacja += 1


        if najlepszy_fit == 0:
            print(f"Rozwiązanie w generacji {generacja - 1}")
            break


        populacja = sorted(populacja, key=ocena)
        nowa_populacja = populacja[:ELITISM]  

        while len(nowa_populacja) < POP_SIZE:
            rodzic1 = random.choice(populacja[:POP_SIZE // 2])
            rodzic2 = random.choice(populacja[:POP_SIZE // 2])

            dziecko1, dziecko2 = krzyzowanie(rodzic1, rodzic2)
            mutacja(dziecko1, N)
            mutacja(dziecko2, N)

            nowa_populacja.append(dziecko1)
            if len(nowa_populacja) < POP_SIZE:
                nowa_populacja.append(dziecko2)

        populacja = nowa_populacja
        najlepszy, najlepszy_fit = najlepszy_osobnik(populacja)

        if generacja % 2 == 0:
            print(f"Generacja {generacja:5d}  Fitness: {najlepszy_fit}")

    czas = time.time() - start
    print(f"\nCzas: {czas:.2f}s  Generacje: {generacja}  Najlepszy fitness: {najlepszy_fit}")
    print("\nNajlepszy osobnik:", najlepszy)
    print("\nPlansza:")
    pokaz_plansze(najlepszy)

if __name__ == "__main__":
    algorytm_genetyczny()