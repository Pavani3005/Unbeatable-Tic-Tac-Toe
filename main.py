import sys
import pygame, numpy as np

pygame.init()
white = (255,255,255)
gray = (180,180,180)
red = (255,0,0)
green = (0,255,0)
black = (0,0,0)

width = 600
height = 600
rows = 3
cols = 3
square_width = width // cols
circle_radius = square_width // 3
circle_width = 20
line_width = 6
cross_width = 25

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Unbeatable Tic Tac Toe")
screen.fill(black)
board = np.zeros((rows,cols))


def draw_lines(color = white):
    for i in range(1, rows):
        pygame.draw.line(screen, color, (0, square_width * i), (width, square_width * i), line_width)
        pygame.draw.line(screen, color, (square_width * i, 0), (square_width * i, height), line_width)

def draw_letters(color = white):
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, (int(col*square_width + square_width//2),int(row*square_width + square_width//2)), circle_radius, circle_width)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color, (col*square_width + square_width//4, row*square_width + square_width//4 ),(col*square_width + square_width*0.75, row* square_width + square_width*0.75), cross_width)
                pygame.draw.line(screen, color, (col*square_width + square_width//4, row*square_width + square_width*0.75 ),(col*square_width + square_width*0.75, row* square_width + square_width//4), cross_width)

def mark_players(row, col, player):
    board[row][col] = player

def is_available(row, col):
    return board[row][col] == 0

def is_board_full(check_board = board):
    for row in range(rows):
        for col in range(cols):
            if check_board[row][col] == 0:
                return False
    return True

def check_winner(player, board = board):
    for col in range(cols):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    for row in range(rows):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

def get_possible_moves(check_board = board):
    moves = []
    for row in range(rows):
        for col in range(cols):
            if check_board[row][col] == 0:
                moves.append((row,col))
    return moves

def minimax(minimaxboard, depth, is_maximizing):
    if check_winner(2, minimaxboard):
        return float('inf')
    elif check_winner(1, minimaxboard):
        return float('-inf')
    elif is_board_full(minimaxboard):
        return 0
    
    if is_maximizing:
        best_score = -1000
        for row in range(rows):
            for col in range(cols):
                if minimaxboard[row][col] == 0:
                    minimaxboard[row][col] = 2
                    score = minimax(minimaxboard, depth + 1, False)
                    minimaxboard[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for row in range(rows):
            for col in range(cols):
                if minimaxboard[row][col] == 0:
                    minimaxboard[row][col] = 1
                    score = minimax(minimaxboard, depth + 1, True)
                    minimaxboard[row][col] = 0
                    best_score = min(score, best_score)
        return best_score
    
def best_move():
    best_score = -1000
    move = (-1, -1)
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    score = best_score
                    move = (row, col)
    
    if move != (-1,-1):
        mark_players(move[0], move[1], 2)
        return True
    return False

def restart_game():
    screen.fill(black)
    draw_lines()
    for row in range(rows):
        for col in range(cols):
            board[row][col] = 0

draw_lines(white)
player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // square_width
            mouseY = event.pos[1] // square_width
            if is_available(mouseY, mouseX):
                mark_players(mouseY, mouseX, player)
                if check_winner(player):
                    game_over= True
                player = player%2 + 1

                if not game_over:
                    if best_move():
                        if check_winner(2):
                            game_over = True
                        player = player%2 + 1

                if not game_over:
                    if is_board_full():
                        game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1
        
    if not game_over:
        draw_letters()
    else:
        if check_winner(1):
            draw_letters(green)
            draw_lines(green)
        elif check_winner(2):
            draw_letters(red)
            draw_lines(red)
        else: 
            draw_letters(gray)
            draw_lines(gray)

    pygame.display.update()