## base.py の自分なりの理解を置いておく

### base.py の理解

- `chess_bot` 関数は、チェスの現在の盤面状態を受け取り、次の一手を選択して返します。
- `obs` は、`board` という属性を持つオブジェクトで、FEN（Forsyth–Edwards Notation）形式の文字列として盤面の状態を表します。
- 関数は、UCI（Universal Chess Interface）形式の文字列として次の手を返します。例："e2e4"

game = Game(obs.board)：obs.board に含まれるFEN文字列を使用して、新しいゲームオブジェクトを作成します。
moves = list(game.get_moves())：現在の盤面から合法な手（可能な手）のリストを取得します。
- `best_move = random.choice(moves)`：合法な手のリストからランダムに次の手を選びます。
- `return best_move.uci()`：選択した手をUCI形式の文字列として返します。


-現時点では、手の選択はほとんどランダムなので、これを改善したい
