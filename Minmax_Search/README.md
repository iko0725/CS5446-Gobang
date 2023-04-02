## Minimax Tree Search

This is a Python implementation of Minimax Tree Search Algorithm.

- Quick start: `python3 gomoku.py`
- you can easily change the board size by `python3 gomoku.py --board-size n`
- `--first ai` means the first player is AI (Here is Minmax algo), `--first me` means the first player is human (Here is another algo)
- If you want to play against another algorithm, you can use:
   `python3 gomoku.py --first me --player1_name genetic --player2_name Minmax`
   It means that `genetic` is the first player and `Minmax` is the second player and `me` plays first. The process is that `genetic` plays first. And its AI opponent `Minmax` plays next. And so on.

   Another example is that `python3 gomoku.py --first ai --player1_name genetic --player2_name Minmax`
    It means that `genetic` is the first player and `Minmax` is the second player and `ai` plays first. The process is that `Minmax` plays first. And another algorithm like `genetic` plays next. And so on.

- more config details please refer to `config.py`

*This AI is firstly inspired by that of [Xuanxuan](https://github.com/lihongxun945/gobang), which is written in JavaScript.*