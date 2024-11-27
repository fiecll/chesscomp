from Chessnut import Game
import random

# フェーズごとの駒の価値設定
PIECE_VALUES_EARLY = {
    'P': 142, 'N': 784, 'B': 828, 'R': 1286, 'Q': 2528, 'K': 0
}
PIECE_VALUES_LATE = {
    'P': 207, 'N': 868, 'B': 916, 'R': 1378, 'Q': 2698, 'K': 0
}

# 駒ごとの位置評価テーブル（中盤と終盤のテーブルを含む）
PIECE_SQUARE_TABLES = {
    "p_mid": [
         0,  0,  0,  0,  0,  0,  0,  0,
        -4, 20, -8, -4, -4, -8, 20, -4,
        -6, -8, -6, -2, -2, -6, -8, -6,
        -6,  5,  3, 21, 21,  3,  5, -6,
       -17, -9, 20, 35, 35, 20, -9, -17,
       -18, -2, 19, 24, 24, 19, -2, -18,
       -11,  6,  7,  3,  3,  7,  6, -11,
         0,  0,  0,  0,  0,  0,  0,  0
    ],
    "p_late": [
         0,  0,  0,  0,  0,  0,  0,  0,
         3, -9,  1, 18, 18,  1, -9,  3,
         8, -5,  2,  4,  4,  2, -5,  8,
         8,  9,  7, -6, -6,  7,  9,  8,
         3,  3, -8, -3, -3, -8,  3,  3,
        -4, -5,  5,  4,  4,  5, -5, -4,
         7, -4,  8, -2, -2,  8, -4,  7,
         0,  0,  0,  0,  0,  0,  0,  0
    ],
    "n_mid": [
       -195, -67, -42, -29, -29, -42, -67, -195,
        -63, -19,   5,  14,  14,   5, -19,  -63,
        -11,  37,  56,  65,  65,  56,  37,  -11,
        -26,  16,  38,  50,  50,  38,  16,  -26,
        -25,  18,  43,  47,  47,  43,  18,  -25,
        -71, -22,   0,   9,   9,   0, -22,  -71,
        -83, -43, -21, -10, -10, -21, -43,  -83,
       -161, -96, -80, -73, -73, -80, -96, -161
    ],
    "n_late": [
       -109, -89, -50, -13, -13, -50, -89, -109,
        -65, -50, -24,  13,  13, -24, -50,  -65,
        -54, -38,  -7,  27,  27,  -7, -38,  -54,
        -46, -25,   3,  40,  40,   3, -25,  -46,
        -41, -25,   6,  38,  38,   6, -25,  -41,
        -50, -39,  -7,  28,  28,  -7, -39,  -50,
        -69, -54, -17,   9,   9, -17, -54,  -69,
       -105, -82, -46, -14, -14, -46, -82, -105
    ],
    "b_mid": [
    -35, -11, -19, -29, -29, -19, -11, -35,
    -23,  17,   6,  -2,  -2,   6,  17, -23,
    -17,  16,  12,   2,   2,  12,  16, -17,
    -11,  27,  16,   9,   9,  16,  27, -11,
    -11,  28,  21,  10,  10,  21,  28, -11,
     -9,  27,  21,  11,  11,  21,  27,  -9,
    -20,  20,  12,   1,   1,  12,  20, -20,
    -44, -13, -25, -34, -34, -25, -13, -44
    ],
    "b_late": [
        -55, -32, -36, -17, -17, -36, -32, -55,
        -34, -10, -12,   6,   6, -12, -10, -34,
        -24,  -2,   0,  13,  13,   0,  -2, -24,
        -26,  -4,  -7,  14,  14,  -7,  -4, -26,
        -26,  -3,  -5,  16,  16,  -5,  -3, -26,
        -23,   0,  -3,  16,  16,  -3,   0, -23,
        -34,  -9, -14,   4,   4, -14,  -9, -34,
        -58, -31, -37, -19, -19, -37, -31, -58
    ],
    "r_mid": [
        -23, -15, -11,  -5,  -5, -11, -15, -23,
        -12,   4,   8,  12,  12,   8,   4, -12,
        -21,  -7,   0,   2,   2,   0,  -7, -21,
        -22,  -7,   0,   1,   1,   0,  -7, -22,
        -22,  -6,  -1,   2,   2,  -1,  -6, -22,
        -21,  -9,  -4,   2,   2,  -4,  -9, -21,
        -21,  -8,  -3,   0,   0,  -3,  -8, -21,
        -25, -16, -16,  -9,  -9, -16, -16, -25
    ],
    "r_late": [
        0,   0,   0,   0,   0,   0,   0,   0,
        0,   0,   0,   0,   0,   0,   0,   0,
        0,   0,   0,   0,   0,   0,   0,   0,
        0,   0,   0,   0,   0,   0,   0,   0,
        0,   0,   0,   0,   0,   0,   0,   0,
        0,   0,   0,   0,   0,   0,   0,   0,
        0,   0,   0,   0,   0,   0,   0,   0,
        0,   0,   0,   0,   0,   0,   0,   0
    ],
    "q_mid": [
        -1,  -4,  -1,   0,   0,  -1,  -4,  -1,
        -2,   7,   7,   6,   6,   7,   7,  -2,
        -2,   6,   8,  10,  10,   8,   6,  -2,
        -3,   9,   8,   7,   7,   8,   9,  -3,
        -1,   8,  10,   7,   7,  10,   8,  -1,
        -2,   6,   9,   9,   9,   9,   6,  -2,
        -4,   6,   9,   8,   8,   9,   6,  -4,
        0,  -4,  -3,  -1,  -1,  -3,  -4,   0
    ],
    "q_late": [
        -74, -55, -43, -30, -30, -43, -55, -74,
        -55, -30, -21,  -6,  -6, -21, -30, -55,
        -40, -16, -10,   3,   3, -10, -16, -40,
        -27,  -5,  10,  21,  21,  10,  -5, -27,
        -29,  -5,   9,  19,  19,   9,  -5, -29,
        -39, -17,  -8,   5,   5,  -8, -17, -39,
        -56, -30, -21,  -5,  -5, -21, -30, -56,
        -71, -56, -42, -29, -29, -42, -56, -71
    ],
    "k_mid": [
        64,  87,  49,   0,   0,  49,  87,  64,
        87, 120,  64,  25,  25,  64, 120,  87,
        122, 159,  85,  36,  36,  85, 159, 122,
        145, 176, 112,  69,  69, 112, 176, 145,
        169, 191, 136, 108, 108, 136, 191, 169,
        198, 253, 168, 120, 120, 168, 253, 198,
        277, 305, 241, 183, 183, 241, 305, 277,
        272, 325, 273, 190, 190, 273, 325, 272
    ],
    "k_late": [
        5,  60,  75,  75,  75,  75,  60,   5,
        40,  99, 128, 141, 141, 128,  99,  40,
        87, 164, 174, 189, 189, 174, 164,  87,
        98, 166, 197, 194, 194, 197, 166,  98,
        103, 152, 168, 169, 169, 168, 152, 103,
        86, 138, 165, 173, 173, 165, 138,  86,
        57,  98, 138, 131, 131, 138,  98,  57,
        0,  41,  80,  93,  93,  80,  41,   0
    ]
}

IMBALANCE_SELF = {
    'Bishop pair': [1438, 0, 0, 0, 0, 0],
    'pawn': [40, 38, 0, 0, 0, 0],
    'knight': [32, 255, -62, 0, 0, 0],
    'bishop': [0, 104, 4, 0, 0, 0],
    'rook': [-25, -2, 47, 105, -208, 0],
    'queen': [-189, 24, 117, 133, -134, -6]
}

IMBALANCE_OPPONENT = {
    'Bishop pair': [0, 0, 0, 0, 0, 0],
    'pawn': [36, 0, 0, 0, 0, 0],
    'knight': [9, 63, 0, 0, 0, 0],
    'bishop': [59, 65, 42, 0, 0, 0],
    'rook': [46, 39, 24, -24, 0, 0],
    'queen': [97, 100, -42, 137, 268, 0]
}




def get_piece_value(piece, phase="mid"):
    """駒の価値を返す。フェーズによって価値を切り替える"""
    piece = piece.upper()
    if phase == "late":
        return PIECE_VALUES_LATE.get(piece, 0)
    return PIECE_VALUES_EARLY.get(piece, 0)


def determine_phase(game):
    """ゲームのフェーズを判定する"""
    # FEN文字列を解析
    fen = str(game).split()[0]
    total_pieces = sum(1 for char in fen if char.upper() in "PNBRQ")
    return "mid" if total_pieces > 20 else "late"

def calculate_imbalance_score(piece_counts_self, piece_counts_opponent):
    """
    不均衡スコアを計算する

    Args:
        piece_counts_self: 自駒の数を保持する辞書 {'pawn': 3, 'knight': 2, ...}
        piece_counts_opponent: 相手駒の数を保持する辞書 {'pawn': 4, 'knight': 1, ...}

    Returns:
        int: 不均衡スコア
    """
    score = 0

    # 自駒内の不均衡スコアを計算
    for i, (piece_self, count_self) in enumerate(piece_counts_self.items()):
        for j, (piece_other, count_other) in enumerate(piece_counts_self.items()):
            if count_self > 0 and count_other > 0:
                value = IMBALANCE_SELF.get(piece_self, [0] * 6)[j]
                score += count_self * count_other * value

    # 自駒と相手駒間の不均衡スコアを計算
    for i, (piece_self, count_self) in enumerate(piece_counts_self.items()):
        for j, (piece_other, count_other) in enumerate(piece_counts_opponent.items()):
            if count_self > 0 and count_other > 0:
                value = IMBALANCE_OPPONENT.get(piece_self, [0] * 6)[j]
                score += count_self * count_other * value

    return score

def count_pieces(board):
    """
    駒の数をカウントする

    Args:
        board: FEN形式の盤面状態

    Returns:
        (dict, dict): 自駒と相手駒の数を保持する辞書
    """
    piece_counts_self = {'pawn': 0, 'knight': 0, 'bishop': 0, 'rook': 0, 'queen': 0, 'Bishop pair': 0}
    piece_counts_opponent = {'pawn': 0, 'knight': 0, 'bishop': 0, 'rook': 0, 'queen': 0, 'Bishop pair': 0}

    for char in board.replace('/', ''):
        if char.isdigit():
            continue
        elif char.isupper():  # 自駒
            piece = piece_name(char)
            if piece:  # None でなければカウント
                piece_counts_self[piece] += 1
        elif char.islower():  # 相手駒
            piece = piece_name(char.upper())
            if piece:  # None でなければカウント
                piece_counts_opponent[piece] += 1

    # ビショップペアの判定
    if piece_counts_self['bishop'] >= 2:
        piece_counts_self['Bishop pair'] = 1
    if piece_counts_opponent['bishop'] >= 2:
        piece_counts_opponent['Bishop pair'] = 1

    return piece_counts_self, piece_counts_opponent



def piece_name(char):
    """駒の文字を名前に変換"""
    mapping = {'P': 'pawn', 'N': 'knight', 'B': 'bishop', 'R': 'rook', 'Q': 'queen'}
    return mapping.get(char, None)  # 不明な駒は None を返す


def evaluate_board(game, phase="mid"):
    """
    盤面を評価する関数
    """
    fen = str(game).split()[0]
    score = 0

    # 基本スコア（駒の価値 + 位置スコア）
    for i, char in enumerate(fen.replace('/', '')):
        if char.isdigit():  # 空白（数字）をスキップ
            continue
        value = get_piece_value(char, phase)
        score += value if char.isupper() else -value

        # 位置評価
        table_key = char.lower() + ("_late" if phase == "late" else "_mid")
        if table_key in PIECE_SQUARE_TABLES:
            table = PIECE_SQUARE_TABLES[table_key]
            position_value = table[i] if char.isupper() else -table[63 - i]
            score += position_value

    # 不均衡スコアを加算
    piece_counts_self, piece_counts_opponent = count_pieces(fen)
    imbalance_score = calculate_imbalance_score(piece_counts_self, piece_counts_opponent)
    score += imbalance_score

    return score



def chess_bot(obs):

    game = Game(obs.board)
    moves = list(game.get_moves())

    if not moves:
        return None  # 合法手がない場合

    phase = determine_phase(game)
    best_move = None
    best_score = float('-inf')

    for move in moves:
        g = Game(obs.board)
        g.apply_move(move)  # 仮にこの手を適用
        score = evaluate_board(g, phase)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move
