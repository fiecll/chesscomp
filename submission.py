from Chessnut import Game
import random

# フェーズごとの駒の価値設定
PIECE_VALUES_EARLY = {
    'P': 142,   # ポーン
    'N': 784,   # ナイト
    'B': 828,   # ビショップ
    'R': 1286,  # ルーク
    'Q': 2528,  # クイーン
    'K': 0      # キング
}

PIECE_VALUES_LATE = {
    'P': 207,   # ポーン
    'N': 868,   # ナイト
    'B': 916,   # ビショップ
    'R': 1378,  # ルーク
    'Q': 2698,  # クイーン
    'K': 0      # キング
}

def get_piece_value(piece, phase="mid"):
    """駒の価値を返す。フェーズによって価値を切り替える"""
    if piece.islower():  # 小文字は相手の駒
        piece = piece.upper()
    if phase == "late":
        return PIECE_VALUES_LATE.get(piece, 0)
    else:
        return PIECE_VALUES_EARLY.get(piece, 0)

def determine_phase(game):
    """ゲームのフェーズを判定する"""
    # 残りの駒の数でフェーズを判定
    total_pieces = sum(1 for square in game.board if square.upper() in "PNBRQ")
    if total_pieces > 20:  # 駒が多い → 序盤/中盤
        return "mid"
    else:  # 駒が少ない → 終盤
        return "late"

def chess_bot(obs):
    """
    フェーズに応じて駒の価値を変更するチェスボット

    Args:
        obs: 現在の盤面状態（FEN形式）を含むオブジェクト
    """
    # 現在の盤面を解析し、合法な手を生成
    game = Game(obs.board)
    moves = list(game.get_moves())

    # 動ける手がない場合は終了（Noneを返す）
    if not moves:
        return None

    # ゲームのフェーズを判定
    phase = determine_phase(game)

    for move in moves[:10]:
        g = Game(obs.board)
        g.apply_move(move)
        if g.status == Game.CHECKMATE:
            return move

    # 2. Check for captures
    for move in moves:
        if game.board.get_piece(Game.xy2i(move[2:4])) != ' ':
            return move

    # 3. Check for queen promotions
    for move in moves:
        if "q" in move.lower():
            return move

    # 4. Random move if no checkmates or captures
    return random.choice(moves)