import pygame as p

import ChessEngine

width = height = 512
dimensions = 8
squareSize = height // dimensions
maxFPS = 15
images = {}


def LoadImages():
    pieces = ["wP", "wR", "wB", "wN", "wQ", "wK", "bP", "bR", "bB", "bN", "bQ", "bK"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("pieces/" + piece + ".png"), (squareSize, squareSize))


def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.GetValidMoves()
    moveMade = False
    LoadImages()
    running = True
    squareSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // squareSize
                row = location[1] // squareSize
                if squareSelected == (row, col):
                    squareSelected = ()
                    playerClicks = []
                else:
                    squareSelected = (row, col)
                    playerClicks.append(squareSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.GetChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            if move in validMoves:
                                gs.MakeMove(validMoves[i])
                                moveMade = True
                                squareSelected = ()
                                playerClicks = []
                    if not moveMade:
                        playerClicks = [squareSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_u:
                    gs.UndoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.GetValidMoves()
            moveMade = False
        DrawGameState(screen, gs)
        clock.tick(maxFPS)
        p.display.flip()


def DrawGameState(screen, gs):
    DrawBoard(screen)
    DrawPieces(screen, gs.board)


def DrawBoard(screen):
    colors = [p.Color("white"), (52, 204, 235)]
    for r in range(dimensions):
        for c in range(dimensions):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * squareSize, r * squareSize, squareSize, squareSize))


def DrawPieces(screen, board):
    for r in range(dimensions):
        for c in range(dimensions):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c * squareSize, r * squareSize, squareSize, squareSize))


if __name__ == "__main__":
    main()
