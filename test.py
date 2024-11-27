from submit import chess_bot
from kaggle_environments import make

env = make("chess")
env.reset()
result = env.run([chess_bot, "random"])
print(result)  # 実行結果を確認
