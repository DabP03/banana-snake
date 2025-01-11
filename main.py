import time
import random
import board
from digitalio import DigitalInOut, Direction, Pull
from snake_display import Display


# Game settings
GAME_GRID_WIDTH = 16
GAME_GRID_HEIGHT = 16
GAME_SPEED = 0.75  # sleep timer, the higher the slower

# Directions
DIRECTION_NONE = (0, 0)
DIRECTION_UP = (-1, 0)
DIRECTION_DOWN = (1, 0)
DIRECTION_LEFT = (0, -1)
DIRECTION_RIGHT = (0, 1)

# Pins
PIN_UP = board.GP2
PIN_DOWN = board.GP3
PIN_LEFT = board.GP4
PIN_RIGHT = board.GP5

# Tiles
TILE_BACKGROUND = 0
TILE_SNAKE = 1
TILE_FOOD = 2
TILE_HEAD_UP = 3
TILE_HEAD_DOWN = 4
TILE_HEAD_LEFT = 5
TILE_HEAD_RIGHT = 6

class SnakeGame:
    def __init__(self,):
        self.snake = [(GAME_GRID_HEIGHT // 2, GAME_GRID_WIDTH // 2)]  # Initial snake position
        self.food = self.place_food()
        self.direction = DIRECTION_NONE
        self.running = True
        self.points = 0
        self.display = Display()
        self.time = None

        # Setup GPIO buttons with interrupt handlers
        self.up_button = self.setup_button(PIN_UP)
        self.down_button = self.setup_button(PIN_DOWN)
        self.left_button = self.setup_button(PIN_LEFT)
        self.right_button = self.setup_button(PIN_RIGHT)

    def setup_button(self, pin):
        button = DigitalInOut(pin)
        button.direction = Direction.INPUT
        button.pull = Pull.UP
        return button

    def handle_input(self):
        if not self.up_button.value:
            self.change_direction(DIRECTION_UP)
        elif not self.down_button.value:
            self.change_direction(DIRECTION_DOWN)
        elif not self.left_button.value:
            self.change_direction(DIRECTION_LEFT)
        elif not self.right_button.value:
            self.change_direction(DIRECTION_RIGHT)

    def place_food(self):
        while True:
            position = (random.randint(0, GAME_GRID_HEIGHT - 1), random.randint(0, GAME_GRID_WIDTH - 1))
            if position not in self.snake:
                return position

    def update_grid(self):
        # Clear the grid
        for x in range(GAME_GRID_WIDTH):
            for y in range(GAME_GRID_HEIGHT):
                self.display.board[x, y] = TILE_BACKGROUND 

        # Place food
        food_y, food_x = self.food
        self.display.board[food_x, food_y] = TILE_FOOD

        # Place snake
        for y, x in self.snake:
            self.display.board[x, y] = TILE_SNAKE

        # Place head
        head_y, head_x = self.snake[0]
        if self.direction == DIRECTION_UP:
            self.display.board[head_x, head_y] = TILE_HEAD_UP
        elif self.direction == DIRECTION_DOWN:
            self.display.board[head_x, head_y] = TILE_HEAD_DOWN
        elif self.direction == DIRECTION_LEFT:
            self.display.board[head_x, head_y] = TILE_HEAD_LEFT
        else:
            self.display.board[head_x, head_y] = TILE_HEAD_RIGHT

    def move_snake(self):
        head_y, head_x = self.snake[0]
        delta_y, delta_x = self.direction
        new_head = (head_y + delta_y, head_x + delta_x)

        # Check for collisions
        if (new_head[0] < 0 or new_head[0] >= GAME_GRID_HEIGHT or
            new_head[1] < 0 or new_head[1] >= GAME_GRID_WIDTH or
            new_head in self.snake):
            self.running = False
            return

        # Add new head
        self.snake.insert(0, new_head)

        # Check if food is eaten
        if new_head == self.food:
            self.food = self.place_food()
            self.points += 1
            self.display.set_score(self.points)
        else:
            # Remove tail
            self.snake.pop()

    def change_direction(self, new_direction):
        # Prevent the snake from reversing
        opposite_direction = (-self.direction[0], -self.direction[1])
        if new_direction != opposite_direction:
            self.direction = new_direction

    def step(self):
        # self.handle_input()
        self.move_snake()
        self.update_grid()

    def play(self):
        while self.running:
            self.time = time.monotonic() + GAME_SPEED
            while self.time > time.monotonic():
                self.handle_input()
            self.step()

    def reset(self):
        self.snake = [(GAME_GRID_HEIGHT // 2, GAME_GRID_WIDTH // 2)]  # Initial snake position
        self.food = self.place_food()
        self.direction = DIRECTION_NONE
        self.running = True
        self.points = 0
        self.time = None
        self.display.set_score(self.points)
        for x in range(GAME_GRID_WIDTH):
            for y in range(GAME_GRID_HEIGHT):
                self.display.board[x, y] = TILE_BACKGROUND 


    def game_over(self, is_over):
        self.display.set_gameover(is_over)

    def end_screen(self):
        self.game_over(True)
        self.direction = DIRECTION_NONE
        while self.direction == DIRECTION_NONE:
            self.handle_input()

    def start_screen(self):
        self.game_over(True)
        while self.direction == DIRECTION_NONE:
            self.handle_input()
        
        tail = DIRECTION_NONE
        if self.direction == DIRECTION_UP:
            tail = (GAME_GRID_HEIGHT // 2 + 1, GAME_GRID_WIDTH // 2)
        elif self.direction == DIRECTION_DOWN:
            tail = (GAME_GRID_HEIGHT // 2 - 1, GAME_GRID_WIDTH // 2)
        elif self.direction == DIRECTION_LEFT:
            tail = (GAME_GRID_HEIGHT // 2, GAME_GRID_WIDTH // 2 + 1)
        else:
            tail = (GAME_GRID_HEIGHT // 2, GAME_GRID_WIDTH // 2 - 1)
        self.snake.insert(1, tail)
        self.game_over(False)

if __name__ == "__main__":
    game = SnakeGame()
    while True:
        game.start_screen()
        game.play()
        game.end_screen()
        game.reset()

