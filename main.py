import time
import random
from machine import Pin

# Game settings
GRID_WIDTH = 16
GRID_HEIGHT = 16
SPEED = 0.75 # sleep timer, the higher the slower

# Directions
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

def print_grid(grid):
    for row in grid:
        print("".join(row))
    print("\n" + "=" * GRID_WIDTH)

class SnakeGame:
    def __init__(self):
        self.grid = [["."] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.snake = [(GRID_HEIGHT // 2, GRID_WIDTH // 2)]  # Initial snake position
        self.food = self.place_food()
        self.direction = RIGHT
        self.running = True
        self.points = 0

        # Setup GPIO buttons with interrupt handlers
        self.up_button = Pin(10, Pin.IN, None)
        self.down_button = Pin(11, Pin.IN, None)
        self.left_button = Pin(12, Pin.IN, None)
        self.right_button = Pin(13, Pin.IN, None)

        # Debouncing state
        self.last_interrupt_time = 0

        # Attach interrupt handlers
        self.up_button.irq(trigger=Pin.IRQ_FALLING, handler=self.handle_up)
        self.down_button.irq(trigger=Pin.IRQ_FALLING, handler=self.handle_down)
        self.left_button.irq(trigger=Pin.IRQ_FALLING, handler=self.handle_left)
        self.right_button.irq(trigger=Pin.IRQ_FALLING, handler=self.handle_right)

    def debounce(self):
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, self.last_interrupt_time) > 200:  # 200ms debounce
            self.last_interrupt_time = current_time
            return True
        return False

    def handle_up(self, pin):
        if self.debounce():
            self.change_direction(UP)

    def handle_down(self, pin):
        if self.debounce():
            self.change_direction(DOWN)

    def handle_left(self, pin):
        if self.debounce():
            self.change_direction(LEFT)

    def handle_right(self, pin):
        if self.debounce():
            self.change_direction(RIGHT)

    def place_food(self):
        while True:
            position = (random.randint(0, GRID_HEIGHT - 1), random.randint(0, GRID_WIDTH - 1))
            if position not in self.snake:
                return position

    def update_grid(self):
        # Clear the grid
        self.grid = [["."] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

        # Place food
        food_y, food_x = self.food
        self.grid[food_y][food_x] = "F"

        # Place snake
        for y, x in self.snake:
            self.grid[y][x] = "S"
    
        # Place head
        head_y, head_x = self.snake[0]
        self.grid[head_y][head_x] = "H"

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

