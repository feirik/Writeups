### Task description
This is a writeup for guessing_game_4 of the norwegian CTF Cybertalent 2021 Winter. The background for the task is [Ulam's game](https://en.wikipedia.org/wiki/Ulam%27s_game), where an observer attempts to guess a number the responder has chosen while the responder is allowed to lie K times.

The CTF task was divided into four sub-tasks:
  * N=64, M=6, K=0
  * N=128, M=13, K=1
  * N=2048, M=15, K=1
  * N=4096, M=23, K=3

Where N=Numbers to choose from, M=Number of questions to ask, K=Number of allowed lies for the responder.

## N=64, M=6, K=0
For the first sub-task the responder was not allowed to lie. The observer can utilize binary search and reduce the potential range the number can reside in by half for each guess. To me this was mainly a test to get to know the API and test the responder logic. The logic turned out to be strict and not bypassable by direct bruteforcing, as in guessing the same number every game and expecting it eventually to be true.

## N=128, M=13, K=1
I started to make progress on this subtask when I set up the framework for a solved end state. I created a 'false count list' to keep track of which numbers the responder had confirmed were not the chosen number. The problem would be solved if the list only contained one candidate lied about less than two times after the 13 guesses.

Initially I tried to create test lists based on mathematical relations such as odd/even, modulo and binary search. I tracked the performance of my 13 guess lists based on the number of remaining candidates. The results were poor and I turned to creating random lists of half the numbers between 0 to 127. The results improved and I eventually bruteforced a solution by combining random lists.

## N=2048, M=15, K=1
This subtask included plenty of trail and error. Eventually I realized that this subtask required a precise solution. After some googling I found [http://www.desjardins.org/david/thesis/thesis.pdf](http://www.desjardins.org/david/thesis/thesis.pdf) which had two interesting entries in the appendix:

  * E=1 N=15 M=2048: OK, 14 tree nodes, 2 leaf nodes (0 safe).
  * E=3 N=23 M=4096: OK, 43 tree nodes, 6 leaf nodes (0 safe).

The thesis also included the source code for a C-program creating the above output. Based on the thesis and the output I concluded that the solutions would need to be **very** precise. On the positive side, if I managed to find the solution to this third subtask, I would likely solve the fourth one aswell.

By now I had started processing the 'false count list' into sub-lists based on the false count in each guessing step. In academia this was often referred to as pennies and non-pennies, I named my sub-lists 'zero false list' and 'one false list' to make them scalable for the last subtask.

The major question regarding the C-program was whether it included the 'pennies and non-pennies' steps I needed for my solution. I thought it was likely that the program was proving tree nodes solutions based on theorems rather than step by step instruction. The program was also difficult to interpret from ambigious variable names. [The Berlekamp thesis ](https://dspace.mit.edu/handle/1721.1/14783) referenced by desJardins turned out to be useful in understanding the program:

*"After each question we record the number of words which have 0 negative votes, the number which have 1 negative vote,... the number which have c negative votes. We write these numbers as components of a column vector, and call this vector the state of the game. If there are n questions remaining, this vector is called an n-state. The topmost components of this vector are often zeros. For this reason, we index the components from the bottom up and omit any zeros above the highest nonzero component." (Page 120)*

This turned my focus to the state variables in the C-program. I ended up printing the state vector for each step in the addtree function seen in [thesis.c](thesis.c). The output from my modified program can be seen in [2048_15_1_thesis_output](2048_15_1_thesis_output.txt) and [4096_23_3_thesis_output](4096_23_3_thesis_output.txt).

From reading the output bottom up I subtracted the difference in each guess step to reach the next state. From the 2048 output it is seen that we remove half of the contents in both the 'zero false list' and 'one false list' in every step until we reach 1 'zero false' and 11 'one false' in the 11th guess. This was a solved state according to [https://web.mat.bham.ac.uk/D.Osthus/simpleliar2.pdf](https://web.mat.bham.ac.uk/D.Osthus/simpleliar2.pdf) and trivial to solve in the remaining steps.

## N=4096, M=23, K=3
With the [thesis output](4096_23_3_thesis_output.txt) at hand I expanded my program with a 'two false list' and 'three false list' to account for the additional lies. A different challenge for this subtask is that the thesis output branches into different paths at an earlier stage:
  * [step:10] [tree:00] state[0]: 146 state[1]: 34 state[2]: 9 state[3]: 0
  * [step:10] [tree:01..22] state[0]: 140 state[1]: 44 state[2]: 4 state[3]: 1

From above we see that all solution trees except one share the same state after the 13th guess. Later on there are additional splits. I tried to choose the tree paths the majority of the solutions were using. To overcome the splitting I bruteforced attempts and added debug messages printing if I occationally ended up in the implemented tree solution. After 21 guesses the responder gave up and I had my final flag! This final solver can be seen in [solve.py](solve.py).


