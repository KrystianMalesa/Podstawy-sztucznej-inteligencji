import math
import string
import random

N = 3
HUMAN = 'X'
AI = 'O'
 

def make_board(N):
    rows = string.ascii_uppercase[:N]   
    cols = []
    for i in range(N):
        liczba = i + 1 
        tekst = str(liczba) 
        cols.append(tekst)
    
    board = {}
    for r in rows:
        for c in cols:
            board[r + c] = ' '
    return board, rows, cols


def print_board(board, rows, cols):
    header = "  " + " | ".join(cols)
    print(header)
    print(" " + "---" * N)
    for r in rows:
        line = []
        for c in cols:
            line.append(board[r + c])
            
        print(f"{r} " + " | ".join(line))
        print(" " + "---" * N)


def generate_lines(rows, cols):
    lines = []

    for r in rows:
        line = []
        for c in cols:
            line.append(r + c)
        lines.append(line)

    for c in cols:
        line = []
        for r in rows:
            line.append(r + c)
        lines.append(line)

    diag1 = []
    diag2 = []
    
    for i in range(N):
        diag1.append(rows[i] + cols[i])
        diag2.append(rows[i] + cols[N - 1 - i])
        
    lines.append(diag1)
    lines.append(diag2)

    return lines


def moves(board):
    empty = []
    for key, value in board.items():
        if value == ' ':
            empty.append(key)
    return empty


def make_move(board, move, player):
    board[move] = player

def undo_move(board, move):
    board[move] = ' '


def check_winner(board, lines):
    for line in lines:
        human_points = 0
        ai_points = 0
        for line_position in line:
            if board[line_position] == HUMAN:
                human_points += 1
            elif board[line_position] == AI:
                ai_points += 1
        if human_points == N:
            return HUMAN
        if ai_points == N:
            return AI
    return None

def evaluate(board, lines, depth):
    winner = check_winner(board, lines)
    if winner == AI:
        return 1
    elif winner == HUMAN:
        return -1
    elif not moves(board):
        return 0
    else: 
        return None 

def minimax(board, depth, maximizing, lines, alpha, beta):
    eval_score = evaluate(board, lines, depth)
    if eval_score is not None: 
        return eval_score
    if depth == 0:
        return 0

    possible_moves = moves(board)
    if maximizing:
        best = -math.inf
        for m in possible_moves:
            make_move(board, m, AI)
            val = minimax(board, depth-1, False, lines, alpha, beta)
            undo_move(board, m)
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:  
                break
        return best
    else:
        best = math.inf
        for m in possible_moves:
            make_move(board, m, HUMAN)
            val = minimax(board, depth-1, True, lines, alpha, beta)
            undo_move(board, m)
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:  
                break
        return best

def is_valid_move(board, move):
    return move in board and board[move] == ' '

def get_valid_human_move(board, rows, cols):
    while True:
        input_r = input().upper()
        if input_r not in rows:
            print(f"Nieprawidłowy wiersz")
            continue
            
        input_c = input()
        if input_c not in cols:
            print(f"Nieprawidłowa kolumna")
            continue
            
        move = input_r + input_c
        if not is_valid_move(board, move):
            print("To pole jest już zajęte. Wybierz inne.")
            continue
            
        return move



def gra_minimax():
    board, rows, cols = make_board(N)
    print_board(board, rows, cols)
    wining_lines = generate_lines(rows, cols)
    player_plays = input("Czy chcesz zacząć jako pierwszy? (T/N): ")
    MAX_DEPTH_LIMIT = 9
    
    while True:
        if player_plays.upper() == 'T':
            move = get_valid_human_move(board, rows, cols)  
            make_move(board, move, HUMAN)
            print_board(board, rows, cols)
        
        winner = check_winner(board, wining_lines)
        if winner == HUMAN:
            print("Wygrał gracz!")
            return
        if winner == AI:
            print("Wygrał komputer!")
            return

        if not moves(board):
            print("Remis!")
            return


        empty_spots = moves(board)
        depth = min(MAX_DEPTH_LIMIT, len(empty_spots))   # Depth limit
        scores = {}
        alpha = -math.inf
        beta = math.inf  
        
        print("\nAI myśli...")
        for m in empty_spots:
            make_move(board, m, AI)
            score = minimax(board, depth - 1, False, wining_lines, alpha, beta)
            scores[m] = score
            undo_move(board, m)
            print(f"Ruch {m}: ocena {score}")
            
        max_score = max(scores.values())
        best_moves = []
        for k, v in scores.items():
            if v == max_score:
                best_moves.append(k)
                
        best_move = random.choice(best_moves)
        
        make_move(board, best_move, AI)
        print(f"Komputer zagrał: {best_move}")
        print_board(board, rows, cols)

        winner = check_winner(board, wining_lines)
        if winner == AI:
            print("Wygrał komputer!")
            return
        if not moves(board):
            print("Remis!")
            return
        
        player_plays = 'T'


if __name__ == "__main__":
    gra_minimax()