import re, chess.pgn

pattern = r'\[%eval ([-+]?\d+(\.\d+)?)\]'

pgn_file = open("test.pgn")

game = chess.pgn.read_game(pgn_file)

board = game.board()

last_score = 0

for node in game.mainline():
    move = node.move
    comment = node.comment

    match = re.match(pattern, comment)
    if match:
        found_score=True
        number_part = match.group(1)
        score = float(number_part)

    score_diff = score - last_score
    # print(score_diff)

    print(move, score, round(score_diff,2), "BLACK" if node.turn() else "WHITE") # reversed, because turn gives the next one to move.

    last_score = score

    if score_diff > 1:
        print("Blunder by Black!")
    if score_diff < -1:
        print("Blunder by White!")
     
    board.push(move)

pgn_file.close()
