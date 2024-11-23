import pygame
import sys
from queue import Queue
import time

# Screen setup
WIDTH = 600
ROWS = 30  # Number of rows/columns in the grid
CELL_SIZE = WIDTH // ROWS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GREY = (200, 200, 200)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Visualizer")
font = pygame.font.SysFont("Arial", 20)

# Create the grid
def create_grid(rows):
    return [[WHITE for _ in range(rows)] for _ in range(rows)]

# Draw the gridlines
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GREY, (x, 0), (x, WIDTH))
        pygame.draw.line(screen, GREY, (0, x), (WIDTH, x))

# Draw the grid with colors
def draw(grid):
    for row in range(ROWS):
        for col in range(ROWS):
            color = grid[row][col]
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    draw_grid()
    pygame.display.update()

# Get the grid cell clicked
def get_clicked_pos(pos):
    x, y = pos
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col

# Display step counter
def display_steps(steps):
    text = font.render(f"Steps: {steps}", True, (0, 0, 0))
    screen.blit(text, (10, 10))
    pygame.display.update()

# Breadth-First Search (BFS) with shortest path calculation
def bfs(grid, start, end, speed):
    queue = Queue()
    queue.put((start, []))  # (current node, path so far)
    visited = set()
    steps = 0

    while not queue.empty():
        current, path = queue.get()
        if current in visited:
            continue
        visited.add(current)

        row, col = current
        grid[row][col] = YELLOW  # Mark as visited
        draw(grid)
        steps += 1
        display_steps(steps)
        time.sleep(speed)

        if current == end:
            path.append(current)
            path_length = len(path) - 1  # Exclude the start node
            for r, c in path:
                grid[r][c] = PURPLE  # Draw the shortest path
            grid[end[0]][end[1]] = GREEN

            # Display shortest path length
            text = font.render(f"Shortest Path: {path_length} cells", True, (0, 0, 0))
            screen.blit(text, (10, 40))  # Below step counter
            pygame.display.update()
            return True

        # Explore neighbors
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            neighbor = (row + dr, col + dc)
            nr, nc = neighbor
            if 0 <= nr < ROWS and 0 <= nc < ROWS and grid[nr][nc] != BLACK and neighbor not in visited:
                queue.put((neighbor, path + [current]))

    return False

# Depth-First Search (DFS)
def dfs(grid, current, end, path, visited, speed, steps):
    if current in visited:
        return False
    visited.add(current)

    row, col = current
    grid[row][col] = YELLOW  # Mark as visited
    draw(grid)
    steps[0] += 1
    display_steps(steps[0])
    time.sleep(speed)

    if current == end:
        for r, c in path:
            grid[r][c] = PURPLE  # Draw final path
        grid[end[0]][end[1]] = GREEN
        return True

    # Explore neighbors
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        neighbor = (row + dr, col + dc)
        nr, nc = neighbor
        if 0 <= nr < ROWS and 0 <= nc < ROWS and grid[nr][nc] != BLACK:
            if dfs(grid, neighbor, end, path + [current], visited, speed, steps):
                return True

    return False

# Main loop
def main():
    grid = create_grid(ROWS)
    start = None
    end = None
    speed = 0.05  # Speed of visualization

    while True:
        screen.fill(WHITE)  # Clear previous text
        draw(grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)

                if not start:  # Set start node
                    start = (row, col)
                    grid[row][col] = BLUE
                elif not end:  # Set end node
                    end = (row, col)
                    grid[row][col] = GREEN
                else:  # Set obstacle
                    grid[row][col] = BLACK

            elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                grid[row][col] = WHITE
                if (row, col) == start:
                    start = None
                elif (row, col) == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and start and end:  # Press 'B' for BFS
                    bfs(grid, start, end, speed)
                if event.key == pygame.K_d and start and end:  # Press 'D' for DFS
                    dfs(grid, start, end, [], set(), speed, [0])
                if event.key == pygame.K_r:  # Press 'R' to reset the grid
                    grid = create_grid(ROWS)
                    start = None
                    end = None

if __name__ == "__main__":
    main()
