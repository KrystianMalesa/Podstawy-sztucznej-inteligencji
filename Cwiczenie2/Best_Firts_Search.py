import sys
import math
import heapq
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, QComboBox, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer

def wczytaj_graf(sciezka):
    with open(sciezka, "r") as plik:
        linie = plik.read().splitlines()
    n = int(linie[0])
    wspolrzedne = [tuple(map(int, linie[i + 1].split())) for i in range(n)]
    sasiedzi = []
    for i in range(n):
        dane = list(map(int, linie[n + 1 + i].split()))
        sasiedzi.append([x - 1 for x in dane[1:]])  # numeracja od 0
    return n, wspolrzedne, sasiedzi

def dystans(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


def best_first_search(n, wspolrzedne, sasiedzi, start, cel):
    kolejka = []
    heapq.heappush(kolejka, (dystans(wspolrzedne[start], wspolrzedne[cel]), start, [start]))
    visited = set()
    while kolejka:
        priorytet, obecny, sciezka = heapq.heappop(kolejka)

        if obecny in visited:
            continue

        visited.add(obecny)
        yield sciezka, visited

        if obecny == cel:
            return

        for s in sasiedzi[obecny]:
            if s not in visited:
                nowy_priorytet = dystans(wspolrzedne[s], wspolrzedne[cel])
                heapq.heappush(kolejka, (nowy_priorytet, s, sciezka + [s]))

def a_star(n, wspolrzedne, sasiedzi, start, cel): # f(n) = g(n) + h(n)
    g_score = {i: math.inf for i in range(n)}
    g_score[start] = 0
    kolejka = []
    heapq.heappush(kolejka, (dystans(wspolrzedne[start], wspolrzedne[cel]), start, [start]))
    visited = set()

    while kolejka:
        priorytet, obecny, sciezka = heapq.heappop(kolejka)

        if obecny in visited:
            continue

        visited.add(obecny)
        yield sciezka, visited

        if obecny == cel:
            return
        
        for s in sasiedzi[obecny]:
            temp_g = g_score[obecny] + dystans(wspolrzedne[obecny], wspolrzedne[s])
            if temp_g < g_score[s]:
                g_score[s] = temp_g
                f = temp_g + dystans(wspolrzedne[s], wspolrzedne[cel])
                heapq.heappush(kolejka, (f, s, sciezka + [s]))

#GUI 
app = QApplication(sys.argv)
okno = QWidget()
okno.setWindowTitle("A* / Best-First Search – Wizualizacja")
okno.setGeometry(100, 100, 900, 700)

canvas = okno

wspolrzedne, sasiedzi, n = [], [], 0
sciezka, odwiedzone, generator = [], set(), None
start, cel = 0, 0

timer = QTimer()

def rysuj():
    painter = QPainter(canvas)
    painter.setRenderHint(QPainter.Antialiasing)
    promien = 10
    if not wspolrzedne:
        painter.end()
        return

    #parametry rysowania
    offset_x = 60
    offset_y = 100    #żeby nie zasłaniało 
    scale = 40

    #krawędzie
    painter.setPen(QPen(Qt.gray, 2))
    for i, sas in enumerate(sasiedzi):
        x1, y1 = wspolrzedne[i]
        for s in sas:
            x2, y2 = wspolrzedne[s]
            painter.drawLine(x1 * scale + offset_x, y1 * scale + offset_y,
                             x2 * scale + offset_x, y2 * scale + offset_y)

    #wierzchołki
    for i, (x, y) in enumerate(wspolrzedne):
        kolor = QColor("white")
        if i in odwiedzone:
            kolor = QColor("lightgreen")
        if i in sciezka:
            kolor = QColor("green")
        if i == start:
            kolor = QColor("red")
        if i == cel:
            kolor = QColor("blue")
        painter.setBrush(kolor)
        painter.setPen(Qt.black)
        painter.drawEllipse(x * scale + offset_x - promien, y * scale + offset_y - promien, 2 * promien, 2 * promien)
        painter.drawText(x * scale + offset_x - 5, y * scale + offset_y + 5, str(i + 1))
    painter.end()


def wczytaj():
    global wspolrzedne, sasiedzi, n
    sciezka = QFileDialog.getOpenFileName(okno, "Wybierz plik z grafem", "", "Tekst (*.txt)")[0]
    if not sciezka:
        return
    n, wspolrzedne, sasiedzi = wczytaj_graf(sciezka)
    canvas.update()

def start_alg():
    global start, cel, generator, odwiedzone, sciezka
    if not wspolrzedne:
        return
    try:
        start = int(start_input.text()) - 1
        cel = int(cel_input.text()) - 1
    except:
        return
    odwiedzone.clear()
    sciezka.clear()
    alg = alg_combo.currentText()
    if alg == "Best-First":
        generator = best_first_search(n, wspolrzedne, sasiedzi, start, cel)
    else:
        generator = a_star(n, wspolrzedne, sasiedzi, start, cel)
    timer.start(700)

def krok():
    global sciezka, odwiedzone
    try:
        sciezka, odwiedzone = next(generator)
        canvas.update()
    except StopIteration:
        timer.stop()
        if sciezka:
            dlugosc = sum(dystans(wspolrzedne[sciezka[i]], wspolrzedne[sciezka[i+1]]) for i in range(len(sciezka)-1))
            QMessageBox.information(okno, "Zakończono", f"Znaleziono ścieżkę.\nDługość: {dlugosc:.2f}")
        else:
            QMessageBox.warning(okno, "Brak ścieżki", "Nie znaleziono połączenia!")

timer.timeout.connect(krok)
okno.paintEvent = lambda e: rysuj()

#GUI elementy
btn_wczytaj = QPushButton("Wczytaj graf", okno)
btn_wczytaj.move(20, 20)
btn_wczytaj.clicked.connect(wczytaj)

QLabel("Start: ", okno).move(150, 25)
start_input = QLineEdit(okno)
start_input.setFixedWidth(40)
start_input.move(200, 20)

QLabel("Cel: ", okno).move(250, 25)
cel_input = QLineEdit(okno)
cel_input.setFixedWidth(40)
cel_input.move(290, 20)

alg_combo = QComboBox(okno)
alg_combo.addItems(["Best-First", "A*"])
alg_combo.move(350, 20)

btn_start = QPushButton("Start", okno)
btn_start.move(450, 20)
btn_start.clicked.connect(start_alg)

okno.show()
sys.exit(app.exec_())
