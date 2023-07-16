import chess.pgn

pgn_file = open("lichess_paranoidray_2023-07-10.pgn")

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
        print(move)

        board.push(move)


pgn_file.close()