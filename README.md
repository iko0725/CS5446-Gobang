# Mastering the Game of Gobang from Scratch
<!-- ![Gobang game with White player wins](imgs/training_effect.png) -->
<div align="center">
<img src="imgs/training_effect.png" width = "300" height="300" alt="Gobang game with white player winning" align=center />
</div>

**Gobang**, also known as Five in a Row, is a popular board game played between two players, whose goal is to align five consecutive stones of the same color on a grid. In this work, we present a comprehensive comparison and analysis of different reinforcement learning algorithms in the game of Gobang. We consider various algorithms, including Minimax Algorithm with Alpha-beata pruning (Minimax), Monte Carlo Tree Search (MCTS), Genetic Algorithm, Deep Q-Network (DQN), and AlphaZero. 


## RUN CODE
We have implemented a text-based user interface and integrated all the algorithms to enable automatic gameplay among them. If you want to play with these algorithm, set player1_name or player2_name as human.

~~~~
python gobang_text_ui.py --board_size --player1_name --player2_name --iteration --save_dir
~~~~

**Example**: 


~~~~
python gobang_text_ui.py --board_size 9 --player1_name minimax --player2_name genetic --save_dir ./results
~~~~

* `--board_size`: We surpport board size 7 (4-in-a-row) and board size 9, 15 (five-in-a-row). If you input board size 7, the chess game automatically start with 4-in-a-row chess rules and models. 

* `--player1_name`: The algorithm who play first in the Gobang game. We surpport Genetic Algorithm (genetic), Marte Corlo Tree Search (mcts), Minimax Algorithm with Alpha-beta prunning (minmax), Deep Q-Network (dqn) and AlphaZero (alphazero).

* `--player2_name`: The algorithm who play second in the Gobang game. We surpport Genetic Algorithm (genetic), Marte Corlo Tree Search (mcts), Minimax Algorithm with Alpha-beta prunning (minmax), Deep Q-Network (dqn) and AlphaZero (alphazero).

* `--iteration`: The training epoch for alphazero algorithm, default is 3000. We support 500, 1000, 1500, 2000, 2500, 3000. If you dont use AlphaZero in the game, ignore this argument.

* `--save_dir`: This directory is used to save moves history and winnter informaiton for both player1 and player2. The example file is: p1_alphazero_p2_genetic_move_history.json.


## Results
Results on board size $9\times9$ (five-in-a-row).
<div align="center">
<img src="imgs/board_size_9.jpg" width = "500" height="400" alt="Results on board size 9x9" align=center />
</div>
<!-- ![Results on board size 9x9](imgs/board_size_9.jpg =100x) -->

Time cost per move
<div align="center">
<img src="imgs/time_cost_per_move.png" width = "500" height="400" alt="Time cost per move" align=center />
</div>
<!-- ![Time cost per move](imgs/time_cost_per_move.png) -->


## Reference Code
1. https://github.com/Explorerhpx/Final-Artificial-Intelligence-Project
2. https://github.com/kktsubota/gobang
3. https://github.com/zhiyiYo/Alpha-Gobang-Zero

## Reference Paper
1. Junru Wang and Lan Huang, "Evolving Gomoku solver by genetic algorithm," 2014 IEEE Workshop on Advanced Research and Technology in Industry Applications (WARTIA), Ottawa, ON, Canada, 2014, pp. 1064-1067, doi: 10.1109/WARTIA.2014.6976460.
2. hKang, Junhao, Hang Joon Kim and Ijcta. “Effective Monte-Carlo Tree Search Strategies for Gomoku AI.” 2016.

