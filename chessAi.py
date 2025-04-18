'''
    Keep DEPTH <= 4 for AI to run smoothly.

    DEPTH means the fot will looks depth moves ahead and calculate the best possible move based on PIECE-CAPTURE-SCORE AND PIECE-POSITION SCORE :
    DEPTH = 4
'''


'''

WAYS TO IMPROVE AI AND MAKE AI FASTER

1) Create a database for initial ai moves/ book openings
2) AI find possible moves for all the piece after each move, if one piece is moved possible moves for other piece would be same no need to find again
    In this case new possible move would be :
        i) if any piece could move to the starting location of piece moved
        ii) if the piece moved to (x, y) position check if it blocked any piece to move to that location
3) no need to evaluate all the position again and again use zobrus hashing to save good position and depth
4) if [ black moved x, white move a, black moved y, white move b ] is sometime same as: 
      [ black moved y, white move a, black moved x, white move b ]
      [ black moved x, white move b, black moved y, white move a ]
      [ black moved y, white move b, black moved y, white move a ]
5) Teach theories to AI, like some time it is better to capture threat than to move a pawn or take back our piece to previous position rather than attacking


'''


import random
from queue import Queue

# Constants
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4  # AI search depth (can be lowered to improve performance)

# Piece material values
pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

# Positional scores
knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 2, 2, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 2, 1, 1, 2, 3, 4]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = list(reversed(whitePawnScores))

piecePositionScores = {
    "N": knightScores,
    "B": bishopScores,
    "Q": queenScores,
    "R": rookScores,
    "wp": whitePawnScores,
    "bp": blackPawnScores
}

# Global variables
nextMove = None
SET_WHITE_AS_BOT = -1


# Random move fallback
def findRandomMoves(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


# Best move finder (entry point)
def findBestMove(gs, validMoves, returnQueue: Queue):
    global nextMove, SET_WHITE_AS_BOT, whitePawnScores, blackPawnScores
    nextMove = None
    random.shuffle(validMoves)

    if gs.playerWantsToPlayAsBlack:
        whitePawnScores, blackPawnScores = blackPawnScores, whitePawnScores

    SET_WHITE_AS_BOT = 1 if gs.whiteToMove else -1

    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, SET_WHITE_AS_BOT)
    returnQueue.put(nextMove)


# Recursive AI logic with alpha-beta pruning
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove

    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        gs.undoMove()

        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(f"Best so far: {move} with score {score}")

        alpha = max(alpha, score)
        if alpha >= beta:
            break

    return maxScore


# Board evaluation function
def scoreBoard(gs):
    if gs.checkmate:
        gs.checkmate = False
        return -CHECKMATE if gs.whiteToMove else CHECKMATE
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(8):
        for col in range(8):
            square = gs.board[row][col]
            if square != "--":
                pieceType = square[1]
                color = square[0]
                positionScore = 0

                if pieceType != "K":
                    if pieceType == "p":
                        key = square  # "wp" or "bp"
                        positionScore = piecePositionScores[key][row][col]
                    else:
                        positionScore = piecePositionScores[pieceType][row][col]

                material = pieceScore[pieceType]
                totalScore = material + positionScore * 0.1

                if SET_WHITE_AS_BOT:
                    score += totalScore if color == 'w' else -totalScore
                else:
                    score -= totalScore if color == 'w' else -totalScore

    return score



'''def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE # for bot worst score
    bestMoveForPlayer = None # for black
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove) # bot (black) makes a move
        opponentsMoves = gs.getValidMoves() # player (white) get all valid moves 
        opponentMaxScore = -CHECKMATE # player(opponent/white) worst possibility
        for opponentsMove in opponentsMoves:
            # the more positive the score the better the score for player(opponent)
            # player (opponent/white) makes a move for bot (black)
            gs.makeMove(opponentsMove) # player makes a move
            if gs.checkmate:
                score = -turnMultiplier * CHECKMATE # if player (white) makes a move and it results in checkmate than its the max score for player but worst for bot
            elif gs.stalemate:
                score = STALEMATE
            else:
                score = -turnMultiplier * scoreMaterial(gs.board)
            if score > opponentMaxScore:
                opponentMaxScore = score
            gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore: # if player (opponent/white) moves does not result in checkmate(worst score for bot)
            ''''''
            opponentMaxScore = max score for the opponent if bot played playerMove

            it is calculating all possibles moves for player after bot makes move and store the minimum score of player after making player move in opponentMinMaxScore
            then again it check what if bot whould have played different move
            ''''''
            opponentMinMaxScore = opponentMaxScore
            bestMoveForPlayer = playerMove
        gs.undoMove()
    return bestMoveForPlayer '''

'''def findMoveMinMax(gs, validMoves, depth, whiteToMove): #depth represent how many moves ahead we want to look to find current best move
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore = -CHECKMATE # worst score for white
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore

    else:
        minScore = CHECKMATE # worst score for black
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore'''
# without alpha beta pruning
'''def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves() # opponent validmoves
        ''''''
        - sign because what ever opponents best score is, is worst score for us
        negative turnMultiplier because it changes turns after moves made 
        ''''''
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore'''

# calculate score of the board based on position
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]

    return score
'''