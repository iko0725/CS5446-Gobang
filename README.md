# Mastering the Game of Gobang from Scratch

In this work, we present a comprehensive comparison and analysis of different reinforcement learning algorithms in the game of Gobang. We consider various algorithms, including Minimax Algorithm with Alpha-beata pruning (Minimax), Monte Carlo Tree Search (MCTS), Genetic Algorithm, Deep Q-Network (DQN), and AlphaZero. We implement each algorithm and evaluate their performance on different board sizes, considering factors like winning rate, time cost per move. We find that on a smaller board, the performance of the algorithms varies, with Minimax and AlphaZero trained for 3000 epochs perform best. We also find Genetic Algorithm has the lowest time cost for per move despite its poor performance. In conclusion, we offer valuable insights into the behaviour of different algorithms in the context of Gobang.


## RUN CODE
We have implemented a text-based user interface and integrated all the algorithms to enable automatic gameplay among them.

python gobang_text_ui.py --board_size --player1_name --player2_name --iteration --save_dir

**Example**: python gobang_text_ui.py --board_size 9 --player1_name minimax --player2_name genetic --save_dir ./results

*board_size*: We surpport board size 7 (4-in-a-row) and board size 9, 15 (five-in-a-row). If you input board size 7, the chess game automatically start with 4-in-a-row chess rules and models. 

*player1_name*: The algorithm who play first in the Gobang game. We surpport Genetic Algorithm (genetic), Marte Corlo Tree Search (mcts), Minimax Algorithm with Alpha-beta prunning (minmax), Deep Q-Network (dqn) and AlphaZero (alphazero).

*player2_name*: The algorithm who play second in the Gobang game. We surpport Genetic Algorithm (genetic), Marte Corlo Tree Search (mcts), Minimax Algorithm with Alpha-beta prunning (minmax), Deep Q-Network (dqn) and AlphaZero (alphazero).

*iteration*: The training epoch for alphazero algorithm, default is 3000. We support 500, 1000, 1500, 2000, 2500, 3000. If you dont use AlphaZero in the game, ignore the augument.

*save_dir*: This directory is used to save moves history and winnter informaiton for both player1 and player2. The example file is: p1_alphazero_p2_genetic_move_history.json.


## Reference Code
1. https://github.com/Explorerhpx/Final-Artificial-Intelligence-Project
2. https://github.com/kktsubota/gobang
3. xxxxx alphazero link

## Reference Paper
1. Junru Wang and Lan Huang, "Evolving Gomoku solver by genetic algorithm," 2014 IEEE Workshop on Advanced Research and Technology in Industry Applications (WARTIA), Ottawa, ON, Canada, 2014, pp. 1064-1067, doi: 10.1109/WARTIA.2014.6976460.
2. hKang, Junhao, Hang Joon Kim and Ijcta. “Effective Monte-Carlo Tree Search Strategies for Gomoku AI.” 2016.

