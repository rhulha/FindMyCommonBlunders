import re
import chess.engine
import chess.pgn

pattern = r'\[%eval ([-+]?\d+(\.\d+)?)\]'

pgn_file = open("lichess_paranoidray_2023-07-10.pgn")
#pgn_file = open("test.pgn")

blunders = {}

engine = chess.engine.SimpleEngine.popen_uci("stockfish-windows-x86-64-avx2.exe")

while True:
    last_score = 0
    game = chess.pgn.read_game(pgn_file)
    if game is None:
        break

    i_am_white = game.headers["White"] == "paranoidray"
    i_am_black = game.headers["Black"] == "paranoidray"

    my_color = i_am_white

    if i_am_white:
        print("I am white")
    else:
        print("I am black")

    board = game.board()

    for node in game.mainline():
        move = node.move
        board.push(move)
        comment = node.comment
        myturn = my_color != node.turn() # turn is the next move, so we need to reverse it

        # print(move)

        match = re.match(pattern, comment)
        if match:
            found_score=True
            number_part = match.group(1)
            score = float(number_part)

        if not found_score:
            info = engine.analyse(board, chess.engine.Limit(time=0.2), root_moves=[move])
            # print(info["score"].relative.score())
            score = info["score"].relative.score() / 1000
        
        score_diff = score - last_score
        # print(score_diff)

        last_score = score

        score_diff = abs(score_diff)

        if not myturn:
            continue

        # pgn = game.accept(chess.pgn.StringExporter())
        # 
        #print(pgn)

        fen_move = board.fen() + " " + move.uci()
        if score_diff > 3:
            if fen_move not in blunders:
                blunders[fen_move] = 1
            else:
                blunders[fen_move] += 1
            break # only look at the first blunder in a game

pgn_file.close()
engine.quit()

most_common_blunders = sorted(blunders, key=blunders.get, reverse=True)[:10]
print("Your most common blunders are:")
for move in most_common_blunders:
    print(move)

