import pygame
import random

pygame.init()

# setup
WIDTH = 500
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Zeph's 2048")
time = pygame.time.Clock()
fps = 60
fontSize = pygame.font.Font('freesansbold.ttf', 22)

# 2048 color libary. Taken from Github and modified
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

# initialize game variables
boardValues = [[0 for _ in range(4)] for _ in range(4)]
gameOver = False
createNew = True
initCount = 0
direction = ''
# Storing High Score. Stored it in a notepad
score = 0
file = open('highScore', 'r')
initHigh = int(file.readline())
file.close()
highScore = initHigh


# draw game over and restart
def drawOver():
    pygame.draw.rect(screen, 'black', [50, 50, 340, 100], 0, 10)
    gameOverText1 = fontSize.render('Game Over Man!', True, 'white')
    gameOverText2 = fontSize.render('Press Space Bar to Restart!', True, 'white')
    screen.blit(gameOverText1, (130, 65))
    screen.blit(gameOverText2, (70, 105))


# turn based on direction
def takeTurn(dirc, board):  # check thru every row/col
    global score
    merge = [[False for _ in range(4)] for _ in range(4)]
    if dirc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:  # a row if not a top row
                    for q in range(i):  # How far down you are
                        if board[q][j] == 0:  # check peice right above other piece
                            shift += 1
                    if shift > 0:  # found 0s above piece
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0  # want next piece to move into space if it wants to
                    if board[i - shift - 1][j] == board[i - shift][j] and not merge[i - shift - 1][j] and not \
                            merge[i - shift][j]:  # if two pieces that come in are the same
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]  # add the value to score
                        board[i - shift][j] = 0
                        merge[i - shift - 1][j] = True

    elif dirc == 'DOWN':  # start by checking up then go down
        for i in range(3):  # not checking bottom row
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                    if shift > 0:
                        board[2 - i + shift][j] = board[2 - i][j]
                        board[2 - i][j] = 0
                    if 3 - i + shift <= 3:  # is piece below acutally a piece. Don't want errors
                        if board[2 - i + shift][j] == board[3 - i + shift][j] and not merge[3 - i + shift][j] and not \
                                merge[2 - i + shift][j]:
                            board[3 - i + shift][j] *= 2
                            score += board[3 - i + shift][j]
                            board[2 - i + shift][j] = 0
                            merge[3 - i + shift][j] = True


    elif dirc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                    if shift > 0:
                        board[i][3 - j + shift] = board[i][3 - j]
                        board[i][3 - j] = 0
                    if 4 - j + shift <= 3:
                        if board[i][4 - j + shift] == board[i][3 - j + shift] and not merge[i][4 - j + shift] and not \
                                merge[i][3 - j + shift]:
                            board[i][4 - j + shift] *= 2
                            score += board[i][4 - j + shift]
                            board[i][3 - j + shift] = 0
                            merge[i][4 - j + shift] = True

    elif dirc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                    if shift > 0:
                        board[i][j - shift] = board[i][j]
                        board[i][j] = 0
                    if board[i][j - shift] == board[i][j - shift - 1] and not merge[i][j - shift - 1] and not merge[i][
                        j - shift]:
                        board[i][j - shift - 1] *= 2
                        score += board[i][j - shift - 1]
                        board[i][j - shift] = 0
                        merge[i][j - shift - 1] = True
    return board


# Create random pieces at start
def newPieces(board):
    count = 0
    full = False  # var to check if board is full
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:  # 1 in 10 chance you get a 4
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# background for board
def drawBoard():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 500, 500], 0, 0)
    scoreText = fontSize.render(f'Score: {score}', True, 'black')
    highScoreText = fontSize.render(f'High Score: {highScore}', True, 'black')
    screen.blit(scoreText, (25, 510))
    screen.blit(highScoreText, (25, 550))
    pass


# tiles
def drawPieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                valueColor = colors['light text']
            else:
                valueColor = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            # Window is 500 wide | 4 rectnagles | 20 spacing gap beween each peice | 500 - (5-20) = 400 / 4 = 100 | 120 = 20 + 100
            pygame.draw.rect(screen, color, [j * 120 + 20, i * 120 + 20, 100, 100], 0,
                             5)  # Top left. Top corner. rounded rectangle.
            if value > 0:  # game dosen't tell you there is a zero
                valueLen = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 50 - (5 * valueLen))  # font gets smaller as vlaue goes up
                valueText = font.render(str(value), True, valueColor)
                textRect = valueText.get_rect(
                    center=(j * 120 + 70, i * 120 + 70))  # x and y cordinate for center of text in rect
                screen.blit(valueText, textRect)
                pygame.draw.rect(screen, 'black', [j * 120 + 20, i * 120 + 20, 100, 100], 2,
                                 5)  # black outline for each square


# loops for game
run = True
while run:
    time.tick(fps)
    screen.fill('tan')
    drawBoard()  # background, score, high score, etc..
    drawPieces(boardValues)
    # variable new square
    if createNew or initCount < 2:
        boardValues, gameOver = newPieces(boardValues)
        createNew = False
        initCount += 1
    if direction != '':
        boardValues = takeTurn(direction, boardValues)
        direction = ''
        createNew = True

    if gameOver:  # dont want to go back and forth into the file manually. Only save when game is over
        drawOver()
        if highScore > initHigh:
            file = open('highScore', 'w')
            file.write(f'{highScore}')
            file.close()
            initHigh = highScore

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'

            if gameOver:
                if event.key == pygame.K_SPACE:
                    boardValues = [[0 for _ in range(4)] for _ in range(4)]
                    createNew = True
                    initCount = 0
                    score = 0
                    direction = ''
                    gameOver = False

        if score > highScore:
            highScore = score

    pygame.display.flip()
pygame.quit()
