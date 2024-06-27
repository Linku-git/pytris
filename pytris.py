import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
BLOCK_SIZE = 20
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
GAME_AREA_WIDTH = GRID_WIDTH * BLOCK_SIZE
GAME_AREA_HEIGHT = GRID_HEIGHT * BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Tetromino shapes and colors
SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 1], [1, 1]], # O
    [[1, 1, 1], [0, 1, 0]], # T
    [[1, 1, 1], [1, 0, 0]], # L
    [[1, 1, 1], [0, 0, 1]], # J
    [[1, 1, 0], [0, 1, 1]], # S
    [[0, 1, 1], [1, 1, 0]]  # Z
]

COLORS = [CYAN, YELLOW, PURPLE, ORANGE, BLUE, GREEN, RED]

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Game variables
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
current_piece = None
current_pos = [0, 0]
current_color = None
next_piece = None
next_color = None
score = 0
level = 1
game_over = False
clock = pygame.time.Clock()

def new_piece():
    global current_piece, current_pos, current_color, next_piece, next_color
    if next_piece is None:
        shape_index = random.randint(0, len(SHAPES) - 1)
        next_piece = SHAPES[shape_index]
        next_color = COLORS[shape_index]
    
    current_piece = next_piece
    current_color = next_color
    current_pos = [GRID_WIDTH // 2 - len(current_piece[0]) // 2, 0]
    
    shape_index = random.randint(0, len(SHAPES) - 1)
    next_piece = SHAPES[shape_index]
    next_color = COLORS[shape_index]

def rotate_piece():
    global current_piece
    current_piece = list(zip(*current_piece[::-1]))

def check_collision(offset_x=0, offset_y=0):
    for y, row in enumerate(current_piece):
        for x, cell in enumerate(row):
            if cell:
                pos_x = current_pos[0] + x + offset_x
                pos_y = current_pos[1] + y + offset_y
                if pos_x < 0 or pos_x >= GRID_WIDTH or pos_y >= GRID_HEIGHT or (pos_y >= 0 and grid[pos_y][pos_x]):
                    return True
    return False

def merge_piece():
    for y, row in enumerate(current_piece):
        for x, cell in enumerate(row):
            if cell:
                grid[current_pos[1] + y][current_pos[0] + x] = current_color

def clear_lines():
    global grid, score, level
    lines_cleared = 0
    for y in range(GRID_HEIGHT - 1, -1, -1):
        if all(grid[y]):
            del grid[y]
            grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            lines_cleared += 1
    score += lines_cleared ** 2 * 100
    level = min(10, score // 1000 + 1)

def draw_grid():
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * BLOCK_SIZE + (SCREEN_WIDTH - GAME_AREA_WIDTH) // 2, 
                               y * BLOCK_SIZE + (SCREEN_HEIGHT - GAME_AREA_HEIGHT) // 2, 
                               BLOCK_SIZE, BLOCK_SIZE)
            if cell:
                pygame.draw.rect(screen, cell, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

def draw_current_piece():
    for y, row in enumerate(current_piece):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, current_color, 
                                 ((current_pos[0] + x) * BLOCK_SIZE + (SCREEN_WIDTH - GAME_AREA_WIDTH) // 2, 
                                  (current_pos[1] + y) * BLOCK_SIZE + (SCREEN_HEIGHT - GAME_AREA_HEIGHT) // 2, 
                                  BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, 
                                 ((current_pos[0] + x) * BLOCK_SIZE + (SCREEN_WIDTH - GAME_AREA_WIDTH) // 2, 
                                  (current_pos[1] + y) * BLOCK_SIZE + (SCREEN_HEIGHT - GAME_AREA_HEIGHT) // 2, 
                                  BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_next_piece():
    for y, row in enumerate(next_piece):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, next_color, 
                                 (SCREEN_WIDTH - 100 + x * BLOCK_SIZE, 
                                  150 + y * BLOCK_SIZE, 
                                  BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, 
                                 (SCREEN_WIDTH - 100 + x * BLOCK_SIZE, 
                                  150 + y * BLOCK_SIZE, 
                                  BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_interface():
    # Draw game area border
    pygame.draw.rect(screen, WHITE, ((SCREEN_WIDTH - GAME_AREA_WIDTH) // 2 - 2, 
                                     (SCREEN_HEIGHT - GAME_AREA_HEIGHT) // 2 - 2, 
                                     GAME_AREA_WIDTH + 4, GAME_AREA_HEIGHT + 4), 2)
    
    font = pygame.font.Font(None, 36)
    
    # Score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))
    
    # Level
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (20, 60))
    
    # Next piece
    next_text = font.render("Next:", True, WHITE)
    screen.blit(next_text, (SCREEN_WIDTH - 120, 100))

new_piece()

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not check_collision(-1):
                current_pos[0] -= 1
            if event.key == pygame.K_RIGHT and not check_collision(1):
                current_pos[0] += 1
            if event.key == pygame.K_DOWN and not check_collision(0, 1):
                current_pos[1] += 1
            if event.key == pygame.K_UP:
                rotated = list(zip(*current_piece[::-1]))
                if not check_collision():
                    current_piece = rotated

    # Move piece down
    if not check_collision(0, 1):
        current_pos[1] += 1
    else:
        merge_piece()
        clear_lines()
        new_piece()
        if check_collision():
            game_over = True

    # Draw everything
    screen.fill(BLACK)
    draw_grid()
    draw_current_piece()
    draw_next_piece()
    draw_interface()
    pygame.display.flip()

    clock.tick(1 + level)  # Speed increases with level

# Game over screen
font = pygame.font.Font(None, 48)
game_over_text = font.render("Game Over", True, WHITE)
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                             SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
pygame.display.flip()

# Wait for a moment before quitting
pygame.time.wait(2000)
pygame.quit()