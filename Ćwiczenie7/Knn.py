import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from fpdf import FPDF
from collections import Counter

WIELKOSC_ZBIORU_TESTOWEGO = 0.40
LISTA_K = [1, 3, 5, 7, 10, 15]
LISTA_METRYK = ['euclidean', 'manhattan']
NORMALIZACJA_DANYCH = True
ZIARNO_LOSOWOSCI = 43

def generuj_pdf(dataframe, nazwa_pliku="Raport_kNN.pdf"):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Raport z kNN", 0, 1, 'C')
    pdf.ln(5)
    
    pdf.set_font("Arial", '', 10)
    info = f"Test size: {WIELKOSC_ZBIORU_TESTOWEGO*100}%, Normalization: {NORMALIZACJA_DANYCH}"
    pdf.cell(0, 10, info, 0, 1, 'C')
    pdf.ln(5)
    
    col_widths = [25, 30, 15, 60, 60] 
    headers = dataframe.columns
    
    pdf.set_font("Arial", 'B', 10)
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, str(header), 1, 0, 'C')
    pdf.ln()
    
    pdf.set_font("Arial", '', 10)
    for index, row in dataframe.iterrows():
        for i, item in enumerate(row):
            pdf.cell(col_widths[i], 10, str(item), 1, 0, 'C')
        pdf.ln()

    pdf.output(nazwa_pliku)
    print(f"Wygenerowano plik PDF: {nazwa_pliku}")


def oblicz_odleglosc(punkt_a, punkt_b, metryka):
    if metryka == 'euclidean':
        return np.sqrt(np.sum((punkt_a - punkt_b)**2))
    elif metryka == 'manhattan':
        return np.sum(np.abs(punkt_a - punkt_b))
    return 0

def klasyfikuj_knn(X_train, y_train, test_point, k, metryka):
    odleglosci = []
    
    for i in range(len(X_train)):
        dist = oblicz_odleglosc(test_point, X_train[i], metryka)
        odleglosci.append((dist, y_train[i])) 
    
    odleglosci.sort(key=lambda x: x[0])
    najblizsi_sasiedzi = odleglosci[:k]
    klasy_sasiadow = [n[1] for n in najblizsi_sasiedzi]
    
    najczestsza_klasa = Counter(klasy_sasiadow).most_common(1)[0][0]
    return najczestsza_klasa

def przewiduj_dla_calego_zbioru(X_train, y_train, X_test, k, metryka):
    predictions = []
    for test_row in X_test:
        wynik = klasyfikuj_knn(X_train, y_train, test_row, k, metryka)
        predictions.append(wynik)
    return np.array(predictions)

def moje_accuracy(y_true, y_pred):
    poprawne = np.sum(y_true == y_pred)
    return poprawne / len(y_true)

def pobierz_dane_offline(nazwa):
    if nazwa.lower() == 'iris':
        data = datasets.load_iris()
    elif nazwa.lower() == 'wine':
        data = datasets.load_wine()
    return data.data, data.target
                 #X           y  
def main():
    wszystkie_wyniki = []
    zbiory_do_przetworzenia = ['Iris', 'Wine']

    for nazwa_zbioru in zbiory_do_przetworzenia:
        #X: Tabela z danymi (wymiary, chemia).
        #y: Klucz odpowiedzi (gatunki).
        X, y = pobierz_dane_offline(nazwa_zbioru)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=WIELKOSC_ZBIORU_TESTOWEGO, 
            random_state=ZIARNO_LOSOWOSCI, 
            stratify=y
        )

        if NORMALIZACJA_DANYCH:
            scaler = MinMaxScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)

        for metryka in LISTA_METRYK:
            for k in LISTA_K:
                y_pred_train = przewiduj_dla_calego_zbioru(X_train, y_train, X_train, k, metryka)
                y_pred_test = przewiduj_dla_calego_zbioru(X_train, y_train, X_test, k, metryka)
                
                acc_test = moje_accuracy(y_test, y_pred_test)
                acc_train = moje_accuracy(y_train, y_pred_train)
                
                wszystkie_wyniki.append({
                    'Dataset': nazwa_zbioru,
                    'Metric': metryka,
                    'k': k,
                    'Test Acc [%]': round(acc_test * 100, 2),
                    'Train Acc [%]': round(acc_train * 100, 2)
                })
                print(f"Obliczono: {nazwa_zbioru}, {metryka}, k={k}")

    if wszystkie_wyniki:
        df_results = pd.DataFrame(wszystkie_wyniki)
        print(f" ")
        print(df_results.to_string(index=False))
        generuj_pdf(df_results, "Raport_kNN.pdf")

if __name__ == "__main__":
    main()