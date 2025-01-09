import time
import random
import board
from digitalio import DigitalInOut, Direction, Pull

# Game settings
GRID_WIDTH = 16
GRID_HEIGHT = 16
SPEED = 0.75  # sleep timer, the higher the slower

# Directions
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

# Pins
PIN_UP = board.GP2
PIN_DOWN = board.GP3
PIN_LEFT = board.GP4
PIN_RIGHT = board.GP5



# Tiles
BACKGROUND = 0
SNAKE = 1
HEAD_UP = 2
HEAD_DOWN = 3
HEAD_LEFT = 4
HEAD_RIGHT = 5
FOOD = 6

def print_grid(grid):
    for row in grid:
        print("".join(row))
    print("\n" + "=" * GRID_WIDTH)

class SnakeGame:
    def __init__(self):
        self.grid = [[BACKGROUND] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.snake = [(GRID_HEIGHT // 2, GRID_WIDTH // 2)]  # Initial snake position
        self.food = self.place_food()
        self.direction = RIGHT
        self.running = True
        self.points = 0

        # Setup GPIO buttons with interrupt handlers
        self.up_button = self.setup_button(PIN_UP)
        self.down_button = self.setup_button(PIN_DOWN)
        self.left_button = self.setup_button(PIN_LEFT)
        self.right_button = self.setup_button(PIN_RIGHT)

        # Debouncing
        self.last_press_time = {
            'up': 0,
            'down': 0,
            'left': 0,
            'right': 0
        }
        self.debounce_time = 0.2  # 200ms debounce

    def setup_button(self, pin):
        button = DigitalInOut(pin)
        button.direction = Direction.INPUT
        button.pull = Pull.UP
        return button

    def handle_input(self):
        current_time = time.monotonic()

        if not self.up_button.value and current_time - self.last_press_time['up'] > self.debounce_time:
            self.change_direction(UP)
            self.last_press_time['up'] = current_time
        elif not self.down_button.value and current_time - self.last_press_time['down'] > self.debounce_time:
            self.change_direction(DOWN)
            self.last_press_time['down'] = current_time
        elif not self.left_button.value and current_time - self.last_press_time['left'] > self.debounce_time:
            self.change_direction(LEFT)
            self.last_press_time['left'] = current_time
        elif not self.right_button.value and current_time - self.last_press_time['right'] > self.debounce_time:
            self.change_direction(RIGHT)
            self.last_press_time['right'] = current_time

    def place_food(self):
        while True:
            position = (random.randint(0, GRID_HEIGHT - 1), random.randint(0, GRID_WIDTH - 1))
            if position not in self.snake:
                return position

    def update_grid(self):
        # Clear the grid
        self.grid = [[BACKGROUND] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

        # Place food
        food_y, food_x = self.food
        self.grid[food_y][food_x] = FOOD

        # Place snake
        for y, x in self.snake:
            self.grid[y][x] = SNAKE

        # Place head
        head_y, head_x = self.snake[0]
        if self.direction == UP:
            self.grid[head_y][head_x] = HEAD_UP
        elif self.direction == DOWN:
            self.grid[head_y][head_x] = HEAD_DOWN
        elif self.direction == LEFT:
            self.grid[head_y][head_x] = HEAD_LEFT
        else:
            self.grid[head_y][head_x] = HEAD_RIGHT


    def move_snake(self):
        head_y, head_x = self.snake[0]
        delta_y, delta_x = self.direction
        new_head = (head_y + delta_y, head_x + delta_x)

        # Check for collisions
        if (new_head[0] < 0 or new_head[0] >= GRID_HEIGHT or
            new_head[1] < 0 or new_head[1] >= GRID_WIDTH or
            new_head in self.snake):
            self.running = False
            return

        # Add new head
        self.snake.insert(0, new_head)

        # Check if food is eaten
        if new_head == self.food:
            self.food = self.place_food()
            self.points += 1
        else:
            # Remove tail
            self.snake.pop()

    def change_direction(self, new_direction):
        # Prevent the snake from reversing
        opposite_direction = (-self.direction[0], -self.direction[1])
        if new_direction != opposite_direction:
            self.direction = new_direction

    def step(self):
        self.handle_input()
        self.move_snake()
        self.update_grid()

    def play(self):
        while self.running:
            self.step()
            print_grid(self.grid)
            time.sleep(SPEED)

    def game_over(self):
        print("===============Game Over!===============")
        print()
        print("Points: ", self.points)
        print()
        print("========================================")

if __name__ == "__main__":
    game = SnakeGame()
    game.play()
    game.game_over()
