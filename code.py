from snake_display import Display
        

dis = Display()
dis.board[7,7] = dis.FRUIT
# Heads display
for x in range(4,1,-1):
    dis.board[x,7] = dis.SNAKE
for x in range(10,13):
    dis.board[x,7] = dis.SNAKE
for y in range(4,1,-1):
    dis.board[7,y] = dis.SNAKE
for y in range(10,13):
    dis.board[7,y] = dis.SNAKE
dis.board[7,9] = dis.HEAD_UP
dis.board[7,5] = dis.HEAD_DOWN
dis.board[9,7] = dis.HEAD_LEFT
dis.board[5,7] = dis.HEAD_RIGHT
dis.set_score(255)
dis.set_gameover(True)


# Main loop
while(True):
    pass
