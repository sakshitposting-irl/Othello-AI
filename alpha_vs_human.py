import pygame
import sys
import random
import math

# Constants
WIDTH, HEIGHT = 400, 400
BOARD_SIZE = 8
CELL_SIZE = WIDTH // BOARD_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello Board")

# Function to initialize the board
def initialize_board():
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    board[3][3] = board[4][4] = 1  # 1 represents black
    board[3][4] = board[4][3] = 2  # 2 represents white
    return board

# Function to draw the Othello board with pieces
def draw_board(board):
    screen.fill(GREEN)

    # Draw black intersections
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT))
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))

    # Draw pieces based on the board
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 1:
                pygame.draw.circle(screen, BLACK, ((col + 0.5) * CELL_SIZE, (row + 0.5) * CELL_SIZE), CELL_SIZE // 2 - 5)
                pygame.draw.circle(screen, BLACK, ((col + 0.5) * CELL_SIZE, (row + 0.5) * CELL_SIZE), CELL_SIZE // 2 - 10)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, WHITE, ((col + 0.5) * CELL_SIZE, (row + 0.5) * CELL_SIZE), CELL_SIZE // 2 - 5)
                pygame.draw.circle(screen, WHITE, ((col + 0.5) * CELL_SIZE, (row + 0.5) * CELL_SIZE), CELL_SIZE // 2 - 10)

    pygame.display.flip()

# Function to check if a move is valid
def is_valid_move(board, row, col, player):
    if board[row][col] != 0:
        return False

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == 3 - player:
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == 3 - player:
                r, c = r + dr, c + dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                return True

    return False

# Function to make a move
def make_move(board, row, col, player):
    if is_valid_move(board, row, col, player):
        board[row][col] = player
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == 3 - player:
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == 3 - player:
                    r, c = r + dr, c + dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                    r, c = row + dr, col + dc
                    while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == 3 - player:
                        board[r][c] = player
                        r, c = r + dr, c + dc
        return True
    else:
        return False

# Function to check if the game is over
def is_game_over(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 0:
                return False
            for player in [1, 2]:
                if is_valid_move(board, row, col, player):
                    return False
    return True

# Function to determine the winner
def determine_winner(board):
    count_black = sum(row.count(1) for row in board)
    count_white = sum(row.count(2) for row in board)
    
    if count_black > count_white:
        return "Black"
    elif count_white > count_black:
        return "White"
    else:
        return "Draw"

# AI Agent class
class AlphaBetaAI:
    def __init__(self, player):
        self.player = player

    def make_move(self, board):
        _, move = self.minimax(board, 3, -math.inf, math.inf, True)
        return move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        valid_moves = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if is_valid_move(board, r, c, self.player)]

        if depth == 0 or len(valid_moves) == 0:
            return self.evaluate(board), None

        if maximizing_player:
            max_eval = -math.inf
            best_move = None

            for move in valid_moves:
                new_board = [row.copy() for row in board]
                make_move(new_board, move[0], move[1], self.player)
                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, False)

                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break

            return max_eval, best_move

        else:
            min_eval = math.inf
            best_move = None

            for move in valid_moves:
                new_board = [row.copy() for row in board]
                make_move(new_board, move[0], move[1], 3 - self.player)
                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, True)

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, min_eval)
                if beta <= alpha:
                    break

            return min_eval, best_move

    def evaluate(self, board):
        # Simple evaluation function (count the difference in pieces)
        count_black = sum(row.count(1) for row in board)
        count_white = sum(row.count(2) for row in board)
        return count_black - count_white

# Main game loop
running = True
board = initialize_board()
current_player = 1

# Create AI agent
ai_agent = AlphaBetaAI(2)  # 2 represents white (opponent of the human player)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            col = event.pos[0] // CELL_SIZE
            row = event.pos[1] // CELL_SIZE
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and make_move(board, row, col, current_player):
                current_player = 3 - current_player  # Switch player

    # AI agent's move
    if current_player == 2:
        ai_move = ai_agent.make_move(board)
        if ai_move is not None:
            make_move(board, ai_move[0], ai_move[1], ai_agent.player)
            current_player = 3 - current_player  # Switch player
        else:
            current_player = 3 - current_player  # Switch player if no valid move

    draw_board(board)

    if is_game_over(board):
        winner = determine_winner(board)
        print("Game over! Winner: ", winner)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Winner: {winner}", True, WHITE)
        screen.blit(text, (50, HEIGHT // 2 - 18))
        pygame.display.flip()
        pygame.time.wait(3000)  # Display the winner for 3 seconds
        running = False
        
    elif not any(is_valid_move(board, row, col, current_player) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)):
        if not any(is_valid_move(board, row, col, 3 - current_player) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)):
            winner = determine_winner(board)
            print("No valid move for either player. Winner: ", winner)
            font = pygame.font.Font(None, 36)
            text = font.render(f"Winner: {winner}", True, WHITE)
            screen.blit(text, (50, HEIGHT // 2 - 18))
            pygame.display.flip()
            pygame.time.wait(3000)  # Display the winner for 3 seconds
            running = False
        else:
            current_player = 3 - current_player  # Switch player

# Quit Pygame before exiting
pygame.quit()