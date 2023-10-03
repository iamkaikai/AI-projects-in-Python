# Minimax - depth 3
After implementing Minimax with a depth of 3, the AI's behavior improved significantly, showing a clear strategy for targeting the opponent's high-value pieces like Queen or Rook. However, when the depth is shallow, the AI tends to rely heavily on a single knight and three pawns throughout the game. Additionally, I observed that the Minimax AI struggles to deliver a checkmate when the opponent is left with only a king, a situation that should be relatively straightforward to resolve.



# visited node comparision
random.seed(1)
depth = 3

making move, white turn True
Alpha-Beta Pruning AI recommending move g1h3
(minimax) visited nodes = 206603
(alpha-beta) visited nodes = 9774
-------------------------------
making move, white turn False
Random AI recommending move h7h6
---------------
making move, white turn True
Alpha-Beta Pruning AI recommending move h3g5
(minimax) visited nodes = 398038
(alpha-beta) visited nodes = 19090
-------------------------------
making move, white turn False
Random AI recommending move a7a5
---------------
making move, white turn True
Alpha-Beta Pruning AI recommending move g5f7
(minimax) visited nodes = 697510
(alpha-beta) visited nodes = 32209
-------------------------------
making move, white turn False
Random AI recommending move e8f7
---------------
making move, white turn True
Alpha-Beta Pruning AI recommending move h1g1
(minimax) visited nodes = 936145
(alpha-beta) visited nodes = 44094
-------------------------------
making move, white turn False
Random AI recommending move f7g6
---------------
making move, white turn True
Alpha-Beta Pruning AI recommending move g1h1
(minimax) visited nodes = 1160113
(alpha-beta) visited nodes = 55607
-------------------------------
making move, white turn False
Random AI recommending move b8c6
---------------
making move, white turn True
Alpha-Beta Pruning AI recommending move h1g1
(minimax) visited nodes = 1417635
(alpha-beta) visited nodes = 68841
-------------------------------
making move, white turn False
Random AI recommending move c6d4
---------------
making move, white turn True
Alpha-Beta Pruning AI recommending move g1h1
(minimax) visited nodes = 1715452
(alpha-beta) visited nodes = 85251
-------------------------------




