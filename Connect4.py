import random
import copy
import math

BOARD_WIDTH = 7
BOARD_HEIGHT = 6
CONNECT = 4
OPTIONS = ("human","strong","weak","random")
#options are
#           human
#           strong
#           weak
#           random
player1 = "human"   #red
player2 = "strong"   #yellow
MAX_GAMES = 100
DEFAULT_MAX_GAMES = 3
WEAK_DEPTH = 2
STRONG_DEPTH = 6
PRINTING = True

def new_board(old_board=None, move=None, player=None):
    if old_board==None:
        board = []

        for x in range(0, BOARD_WIDTH):
            col = []
            for y in range(0, BOARD_HEIGHT):
                col.append(None)
            board.append(col)
    else:
        boad = copy.deepcopy(old_board)

    if move!=None and player!=None:
        make_move(board, move, player)


    return board

def print_board(board):
    #error checking length of board
    if len(board) == 0:
        print("Error printing board: board is size 0")
        return

    #print column labels - useful for human players
    column_labels = "  "
    for i in range(0, len(board)):
        column_labels += str(i)+" "
    print(column_labels)

    #print board one row at a time
    for y in range(0, len(board[0])):
        line = "| "
        for x in range(0, len(board)):
            if board[x][y] == None:
                line+= "  "
            else:
                line += str(board[x][y]) + " "
        line += "|"
        print(line)

    #print bottom line
    line = "--"
    for i in range(0, len(board)):
        line+="--"
    line+="-"
    print(line)

def get_symbol(player):
    if player=="Red":
        return "R"
    elif player=="Yellow":
        return "Y"
    else:
        return "?"

def get_name(symbol):
    if symbol=="R":
        return "Red"
    elif symbol=="Y":
        return "Yellow"
    else:
        return "????"

def make_move(board, move, player):
    global BOARD_HEIGHT
    column = board[move]

    for y in range(BOARD_HEIGHT-1, -1, -1):
        if column[y] == None:
            column[y] = get_symbol(player)
            return True
    return False

def check_end(board):
    global CONNECT
    #check if a player won
    for x in range(0, BOARD_WIDTH):
        for y in range(0, BOARD_HEIGHT):
            piece = board[x][y]
            if piece != None:
                #check down
                if y<=BOARD_HEIGHT-CONNECT:
                    #print("here: "+str(y))
                    if board[x][y+1] == piece and board[x][y+2] == piece and board[x][y+3] == piece:
                        return True, piece
                #check right
                if x<=BOARD_WIDTH-CONNECT:
                    if board[x+1][y] == piece and board[x+2][y] == piece and board[x+3][y] == piece:
                        return True, piece
                #check down right diagonal
                if x<=BOARD_WIDTH-CONNECT and y<=BOARD_HEIGHT-CONNECT:
                    if board[x+1][y+1] == piece and board[x+2][y+2] == piece and board[x+3][y+3] == piece:
                        return True, piece
                #check down left diagonal
                if x>=CONNECT-1 and y<=BOARD_HEIGHT-CONNECT:
                    if board[x-1][y+1] == piece and board[x-2][y+2] == piece and board[x-3][y+3] == piece:
                        return True, piece

    #check if full
    full = True
    for x in range(0, BOARD_WIDTH):
        if board[x][0] == None:
            full = False
            break

    #if couldn't find winner
    if full:
        return True, None
    else:
        return False, None

def get_move_human(player):
    global BOARD_WIDTH
    str = input(player+"'s turn. Enter a column to place your piece: ")
    list = str.split()

    if len(list)>0:
        try:
            i = int(list[0])
        except Exception:
            return None
        if 0 <= i < BOARD_WIDTH:
            return i
        else:
            return None
    else:
        return None

def get_move_random():
    global BOARD_WIDTH
    return random.randrange(0, BOARD_WIDTH)

def get_legal(board):
    possible = []
    for x in range(0, BOARD_WIDTH):
        if board[x][0] == None:
            possible.append(x)

    return possible

def get_turn(board):
    pieces_placed = 0
    global BOARD_HEIGHT, BOARD_WIDTH
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            if board[x][y]!=None:
                pieces_placed += 1

    return pieces_placed+1

def get_move_minimax(board, player, max_depth):
    global BOARD_WIDTH, BOARD_HEIGHT
    #print("Mini is maxing at depth "+str(max_depth)+"...")
    best_move = None
    best_score = None

    turn = get_turn(board)
    if turn == 1:
        if max_depth >= 5: 
            return int(BOARD_WIDTH/2)
        else:
            return random.randrange(0, BOARD_WIDTH)

    legal_moves = get_legal(board)

    for move in legal_moves:
        _board = copy.deepcopy(board)
        make_move(_board, move, player)

        opp = get_opponent(player)
        score = _minimax_score(_board, opp, player, max_depth)
        #print(score)
        if best_score == None or best_score < score:
            best_score = score
            best_move = move

    return best_move


def _minimax_score(board, player_to_move, player_to_optimize, depth, alpha=-math.inf, beta=math.inf):
    #if player won return max(or min) score
    end, winning_piece = check_end(board)
    if winning_piece == get_symbol(player_to_optimize):
        return math.inf
    elif winning_piece == get_symbol(get_opponent(player_to_optimize)):
        return -math.inf
    elif end and winning_piece == None:
        return 0

    #if at max depth, return static score
    if depth <= 0:
        return static_score(board, player_to_optimize)


    legal_moves = get_legal(board)

    if len(legal_moves) == 0:
        print("legal moves is empty")
        raise ValueError

    scores = []
    for move in legal_moves:
        _board = copy.deepcopy(board)
        make_move(_board, move, player_to_move)

        opp = get_opponent(player_to_move)
        opp_best_response_score = _minimax_score(_board, opp, player_to_optimize, depth-1, alpha, beta)
        scores.append(opp_best_response_score)
        if player_to_optimize == player_to_move:#maximizing player
            alpha = max(alpha, opp_best_response_score)
            if alpha >= beta:
                break
        else:#minimizing player
            beta = min(beta, opp_best_response_score)
            if alpha >= beta:
                break

    if player_to_move == player_to_optimize:
        return max(scores)
    else:
        return min(scores)

#assumes possition given has not already been won or tied
#I'm not good at connect 4 so...from https://github.com/KeithGalli/Connect4-Python/blob/master/connect4_with_ai.py
def static_score(board, player_to_optimize):
    global BOARD_HEIGHT, BOARD_WIDTH, CONNECT
    opponent = get_opponent(player_to_optimize)
    score = 0

    #create list of center pieces
    center_array = [p for p in list(board[BOARD_WIDTH//2])]
    center_count = center_array.count(player_to_optimize)
    score += center_count * 3

    #score vertical
    for x in range(0, BOARD_WIDTH):
        column_array = [p for p in board[x]]
        for y in range(0, BOARD_HEIGHT-3):
            window = column_array[y:y+CONNECT]
            score += score_window(window, player_to_optimize)

    #score horizontal
    for y in range(0, BOARD_HEIGHT):
        row_array = [c[y] for c in board]
        for x in range(0, BOARD_WIDTH-3):
            window = row_array[x:x+CONNECT]
            score+= score_window(window, player_to_optimize)

    #score negative diagonal
    for x in range(0, BOARD_WIDTH-3):
        for y in range(0, BOARD_HEIGHT-3):
            window = [board[x+i][y+i] for i in range(0, CONNECT)]
            score += score_window(window, player_to_optimize)

    #score positive diagonal
    for x in range(BOARD_WIDTH-3):
        for y in range(BOARD_HEIGHT-3):
            window = [board[x+i][y+3-i] for i in range(CONNECT)]
            score += score_window(window, player_to_optimize)


    return score
        
def score_window(window, player_to_optimize):
    global CONNECT
    score = 0
    opp = get_opponent(player_to_optimize)
    opp_piece = get_symbol(opp)
    piece = get_symbol(player_to_optimize)

    if window.count(piece)==CONNECT:
        return math.inf
    elif window.count(piece) == CONNECT-1 and window.count(None) == 1:
        return 5
    elif window.count(piece) == CONNECT-2 and window.count(None) == 2:
        return 3
    elif window.count(opp_piece) == CONNECT-1 and window.count(None) == 1:
        return -4
    else:
        return 0





def get_opponent(player):
    if player=="Red":
        return "Yellow"
    elif player == "Yellow":
        return "Red"
    elif player == "R":
        return "Y"
    elif player == "Y":
        return "R"


#Testing--------------------------------------------------------------
#board = new_board()


#for i in range(10):
    #make_move(board, random.randrange(0, BOARD_WIDTH-1), "Red" if random.randrange(0, 2)==1 else "Yellow")

#print_board(board)


#raise ValueError #to stop program
#Testing--------------------------------------------------------------

#get players
if not player1 in OPTIONS:
    player1 = OPTIONS[0]
    print("Invalid Player 1. Using "+player1)
else:
    print("Red is "+player1)
if not player2 in OPTIONS:
    player2 = OPTIONS[0]
    print("Invalid Player 2. Using "+player2)
else:
    print("Yellow is "+player2)
#get max games
if not isinstance(MAX_GAMES, int) or MAX_GAMES <= 0:
    MAX_GAMES = DEFAULT_MAX_GAMES
    print("Invalid max games. Using a max games of "+str(MAX_GAMES))
else:
    print("With a max games of "+str(MAX_GAMES))


scores = {"Red":0,"Yellow":0, "Ties":0}  #player1,player2
games_played = 0
first_player = "Red"
while games_played < MAX_GAMES:
    board = new_board()
    if PRINTING:
        print_board(board)
    end, winner = check_end(board)
    first_player = get_opponent(first_player)
    player = get_opponent(first_player)
    while not end:
        #get correct move
        if player=="Red":
            if player1=="human":
                move = get_move_human(player)
            elif player1=="random":
                move = get_move_random()
            elif player1 == "weak":
                move = get_move_minimax(board, player, WEAK_DEPTH)
            elif player1 == "strong":
                move = get_move_minimax(board, player, STRONG_DEPTH)
        else:
            if player2=="human":
                move = get_move_human(player)
            elif player2=="random":
                move = get_move_random()
            elif player2 == "weak":
                move = get_move_minimax(board, player, WEAK_DEPTH)
            elif player2 == "strong":
                move = get_move_minimax(board, player, STRONG_DEPTH)
        #error checking the move
        if move == None:
                    print("Unknown column. Has to be in [0,6]")
                    continue

        make_move(board, move, player)
        if PRINTING:
            print_board(board)
            print(player+" played in column "+str(move))
        end, winner = check_end(board)
        player = get_opponent(player)

    if winner!=None:
        if PRINTING:
            print(get_name(winner)+" Wins!")
        scores[get_name(winner)]+=1
    else:
        if PRINTING:
            print("It's a Tie!")
        scores["Ties"]+=1
    games_played += 1
print(player1+"'s: "+ str(scores["Red"]) + " to "+player2+"'s: " + str(scores["Yellow"]) + ". With "+str(scores["Ties"])+ " ties.")


