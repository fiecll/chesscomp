from Chessnut import Game
import random

# 駒価値
PIECE_VALUES = {
    "p": 1,   # ポーン
    "n": 3,   # ナイト
    "b": 3,   # ビショップ
    "r": 5,   # ルーク
    "q": 9,   # クイーン
    "k": 100  # キング
}

# 駒ごとの位置評価テーブル
PIECE_SQUARE_TABLES = {
    "p": [  # ポーン
         0,  0,  0,  0,  0,  0,  0,  0,
         5, 10, 10, -5, -5, 10, 10,  5,
         5, -5, -10,  0,  0, -10, -5,  5,
         0,  0,  0, 20, 20,  0,  0,  0,
         5,  5, 10, 25, 25, 10,  5,  5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
         0,  0,  0,  0,  0,  0,  0,  0
    ],
    "n": [  # ナイト
        -5, -4, -3, -3, -3, -3, -4, -5,
        -4, -2,  0,  0,  0,  0, -2, -4,
        -3,  0,  1,  1,  1,  1,  0, -3,
        -3,  0,  1,  2,  2,  1,  0, -3,
        -3,  0,  1,  2,  2,  1,  0, -3,
        -3,  0,  1,  1,  1,  1,  0, -3,
        -4, -2,  0,  0,  0,  0, -2, -4,
        -5, -4, -3, -3, -3, -3, -4, -5
    ],
    "b": [  # ビショップ
        -2, -1, -1, -1, -1, -1, -1, -2,
        -1,  0,  0,  0,  0,  0,  0, -1,
        -1,  0,  1,  1,  1,  1,  0, -1,
        -1,  1,  1,  1,  1,  1,  1, -1,
        -1,  0,  1,  1,  1,  1,  0, -1,
        -1,  1,  1,  1,  1,  1,  1, -1,
        -1,  0,  0,  0,  0,  0,  0, -1,
        -2, -1, -1, -1, -1, -1, -1, -2
    ],
    "r": [  # ルーク
         0,  0,  0,  0,  0,  0,  0,  0,
         1,  2,  2,  2,  2,  2,  2,  1,
        -1,  0,  0,  0,  0,  0,  0, -1,
        -1,  0,  0,  0,  0,  0,  0, -1,
        -1,  0,  0,  0,  0,  0,  0, -1,
        -1,  0,  0,  0,  0,  0,  0, -1,
        -1,  0,  0,  0,  0,  0,  0, -1,
         0,  0,  0,  1,  1,  0,  0,  0
    ],
    "q": [  # クイーン
        -2, -1, -1, -0, -0, -1, -1, -2,
        -1,  0,  0,  0,  0,  0,  0, -1,
        -1,  0,  1,  1,  1,  1,  0, -1,
         0,  0,  1,  1,  1,  1,  0, -1,
        -1,  0,  1,  1,  1,  1,  0, -1,
        -1,  1,  1,  1,  1,  1,  1, -1,
        -1,  0,  1,  0,  0,  0,  0, -1,
        -2, -1, -1, -0, -0, -1, -1, -2
    ],
    "k": [  # キング
        -3, -4, -4, -5, -5, -4, -4, -3,
        -3, -4, -4, -5, -5, -4, -4, -3,
        -3, -4, -4, -5, -5, -4, -4, -3,
        -3, -4, -4, -5, -5, -4, -4, -3,
        -2, -3, -3, -4, -4, -3, -3, -2,
        -1, -2, -2, -2, -2, -2, -2, -1,
         2,  2,  0,  0,  0,  0,  2,  2,
         2,  3,  1,  0,  0,  1,  3,  2
    ]
}

def evaluate_board(game):
    """
    評価関数：指定された要素を含む
    """
    board = game.board
    score = 0

    # マテリアルの不均衡（駒価値と位置評価）
    for square in range(64):
        piece = board.get_piece(square)
        if piece != " ":
            value = PIECE_VALUES.get(piece.lower(), 0)
            position_bonus = PIECE_SQUARE_TABLES.get(piece.lower(), [0] * 64)[square]
            if piece.isupper():  # 自分の駒
                score += value + position_bonus
            else:  # 相手の駒
                score -= value + position_bonus

    # モビリティ（駒の動きやすさ）
    own_moves = len(list(game.get_moves()))
    game.turn = 'black' if game.turn == 'white' else 'white'
    opponent_moves = len(list(game.get_moves()))
    game.turn = 'black' if game.turn == 'white' else 'white'  # 元に戻す
    mobility = own_moves - opponent_moves
    score += 0.1 * mobility  # 重み付けは調整可能

    # キングの安全性
    own_king_safety = evaluate_king_safety(board, 'white')
    opponent_king_safety = evaluate_king_safety(board, 'black')
    score += opponent_king_safety - own_king_safety

    # パスポーンの強さ
    own_passed_pawns = evaluate_passed_pawns(board, 'white')
    opponent_passed_pawns = evaluate_passed_pawns(board, 'black')
    score += own_passed_pawns - opponent_passed_pawns

    # 空間（スペース）
    own_space = evaluate_space(board, 'white')
    opponent_space = evaluate_space(board, 'black')
    score += 0.1 * (own_space - opponent_space)

    # 脅威（スレット）
    own_threats = evaluate_threats(board, 'white')
    opponent_threats = evaluate_threats(board, 'black')
    score += own_threats - opponent_threats

    # 主導権（イニシアチブ）
    if game.turn == 'white':
        score += 0.05 * (own_threats - opponent_threats)
    else:
        score -= 0.05 * (opponent_threats - own_threats)

    # コンテンプト（引き分けを避ける意欲）
    if abs(score) < 0.5:
        if game.turn == 'white':
            score += 0.1
        else:
            score -= 0.1

    return score

def chess_bot(obs):
    """
    強化された評価関数を使用したチェスボット。
    """
    game = Game(obs.board)
    moves = list(game.get_moves())

    best_score = float("-inf")
    best_move = None

    for move in moves:
        simulated_game = Game(obs.board)
        simulated_game.apply_move(move)
        score = evaluate_board(simulated_game)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move if best_move else random.choice(moves)

# 補助関数の実装

def evaluate_king_safety(board, color):
    """
    キングの安全性を評価する。
    """
    king_pos = board.find('K' if color == 'white' else 'k')
    safety_score = 0

    # キング周辺のマスを取得
    adjacent_squares = get_adjacent_squares(king_pos)
    for sq in adjacent_squares:
        piece = board.get_piece(sq)
        if piece.islower() if color == 'white' else piece.isupper():
            safety_score -= 0.5  # 敵の駒が近くにある場合ペナルティ

    return safety_score

def get_adjacent_squares(square):
    """
    指定されたマスの周囲8マスを取得する。
    """
    adjacent_squares = []
    rank = square // 8
    file = square % 8
    for dr in [-1, 0, 1]:
        for df in [-1, 0, 1]:
            if dr == 0 and df == 0:
                continue
            r = rank + dr
            f = file + df
            if 0 <= r < 8 and 0 <= f < 8:
                adjacent_squares.append(r * 8 + f)
    return adjacent_squares

def evaluate_passed_pawns(board, color):
    """
    パスポーンの強さを評価する。
    """
    score = 0
    pawn = 'P' if color == 'white' else 'p'
    direction = 1 if color == 'white' else -1

    for square in range(64):
        piece = board.get_piece(square)
        if piece == pawn:
            if is_passed_pawn(board, square, color):
                rank = square // 8 if color == 'white' else 7 - (square // 8)
                score += (rank + 1) * 0.1  # 前進しているほど高評価

    return score

def is_passed_pawn(board, square, color):
    """
    パスポーンかどうかを判定する。
    """
    rank = square // 8
    file = square % 8
    opponent_pawn = 'p' if color == 'white' else 'P'
    direction = 1 if color == 'white' else -1

    for df in [-1, 0, 1]:
        f = file + df
        r = rank + direction
        while 0 <= r < 8:
            if 0 <= f < 8:
                sq = r * 8 + f
                if board.get_piece(sq) == opponent_pawn:
                    return False
            r += direction
    return True

def evaluate_space(board, color):
    """
    空間の広さを評価する。
    """
    space = 0
    pieces = ['P', 'N', 'B', 'R', 'Q', 'K'] if color == 'white' else ['p', 'n', 'b', 'r', 'q', 'k']
    for square in range(64):
        piece = board.get_piece(square)
        if piece in pieces:
            # 駒ごとに前方のマス数をカウント
            space += count_forward_squares(square, color)
    return space

def count_forward_squares(square, color):
    """
    指定された駒の前方のマス数をカウントする。
    """
    rank = square // 8
    direction = 1 if color == 'white' else -1
    forward_squares = 0

    r = rank + direction
    while 0 <= r < 8:
        forward_squares += 1
        r += direction

    return forward_squares

def evaluate_threats(board, color):
    """
    脅威の数を評価する。
    """
    threats = 0
    own_pieces = ['P', 'N', 'B', 'R', 'Q', 'K'] if color == 'white' else ['p', 'n', 'b', 'r', 'q', 'k']
    opponent_pieces = ['p', 'n', 'b', 'r', 'q', 'k'] if color == 'white' else ['P', 'N', 'B', 'R', 'Q', 'K']

    for square in range(64):
        piece = board.get_piece(square)
        if piece in own_pieces:
            moves = get_pseudo_legal_moves(board, square, piece)
            for target_square in moves:
                target_piece = board.get_piece(target_square)
                if target_piece in opponent_pieces:
                    threats += 1

    return threats

def get_pseudo_legal_moves(board, square, piece):
    """
    指定された駒の擬似合法手を取得する（簡略化）。
    """
    # この関数は実際のルールに基づくべきですが、ここでは簡略化しています。
    moves = []
    # 実装は省略
    return moves
