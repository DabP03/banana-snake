import board,busio
import displayio
import terminalio
from time import sleep
from adafruit_st7735r import ST7735R
from bitmaptools import fill_region
from adafruit_display_text import label


class Display:
    def __init__(self):
        self.WIDTH = 16
        self.HEIGHT = 16
        self.BACKGROUND = 0
        self.SNAKE = 1
        self.FRUIT = 2
        self.HEAD_UP = 3
        self.HEAD_DOWN = 4
        self.HEAD_LEFT = 5
        self.HEAD_RIGHT = 6

        # Init display
        mosi_pin = board.GP11
        clk_pin = board.GP10
        cs_pin = board.GP18
        dc_pin = board.GP16
        reset_pin = board.GP17
        displayio.release_displays()
        spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)
        display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin)
        display = ST7735R(display_bus, width=128, height=160, bgr = True)

        # Init screen
        screen = displayio.Group()
        display.root_group = screen

        # Bitmap
        bitmap = displayio.Bitmap(128, 128, 3)
        colors = displayio.Palette(3)
        colors[0] = 0x000000 #background
        colors[1] = 0x00FF00 #snake
        colors[2] = 0xFF0000 #fruit, eyes

        # Tiles
        def fill_tile(index, value):
            x = index * 8 + 1
            fill_region(bitmap, x, 1, x+7, 8, value)
        def fill_eye(index, down, right):
            x = (index*8+5) if right else (index*8+2)
            y = 5 if down else 2
            fill_region(bitmap, x, y, x+2, y+2, 2)

        for i in range(1, 7):
            fill_tile(i, 1)
        fill_tile(2, 2)
        # Eyes
        fill_eye(3, False, False)
        fill_eye(3, False, True)
        fill_eye(4, True, False)
        fill_eye(4, True, True)
        fill_eye(5, False, False)
        fill_eye(5, True, False)
        fill_eye(6, False, True)
        fill_eye(6, True, True)

        # Init board
        self.board = displayio.TileGrid(bitmap, pixel_shader=colors, width=16, height=16, tile_width=8, tile_height=8)
        screen.append(self.board)
        
        # Text area
        text_group = displayio.Group(x=0, y=128)
        screen.append(text_group)
        background = displayio.Palette(1)
        background[0] = 0x242424
        text_group.append(displayio.TileGrid(displayio.Bitmap(128, 32, 1), pixel_shader=background))
        
        score_text = label.Label(terminalio.FONT, text=("Score: " + str(0)), color=0x808080)
        score_text.anchored_position = (5, 2)
        score_text.anchor_point = (0, 0)
        text_group.append(score_text)
        self.__score_text = score_text
        
        gameover_text = label.Label(terminalio.FONT, text="GAME OVER", color=0x000000, background_color=0xFF0000)
        gameover_text.anchored_position = (64, 30)
        gameover_text.anchor_point = (0.5, 1)
        text_group.append(gameover_text)
        gameover_text.hidden = True
        self.__gameover_text = gameover_text
    
    def set_score(self, score):
        self.__score_text.text = "Score: " + str(score)
        
    def set_gameover(self, visible):
        self.__gameover_text.hidden = not visible
