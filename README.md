# Tiny Chess Engine

A compact chess engine in a single Python file, built for the make.fun
tiny-chess-01 bounty: the whole engine is `main.py`, at most 4,096 bytes.

It parses each FEN the env serves, generates its own legal moves
(castling, en passant and promotion included), and searches with
iterative-deepening negamax, alpha-beta pruning, capture quiescence and
MVV-LVA ordering under a fixed node budget — never a clock, so replays
play the same moves. Evaluation is material plus piece-square terms
computed from file/rank geometry: pawn advance and centre, knight and
bishop centrality, rook seventh-rank, and king shelter.

Run it with the competition env:

    MAKEFUN_ENV_URL=<env url> python3 main.py
