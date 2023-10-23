# EC551-Program-1
This is the introduction of EC551 Program 1
Our team include 2 members: Zhaohan Song(jimmy95@bu.edu) & Geye Lin(gylin@bu.edu)
We choose the two input formats: EQN and PLA.
We choose a file as input for both EQN and PLA, and .txt for output.
For EQN, we set the input like ~a&~b&~c&~d | ~a&~b&~c&d | ~a&b&~c&d | a&~b&~c&d | a&b&~c&d | a&b&c&~d | a&b&c&d, which can be found in input.eqn.
The EQN function could be found in boolean_EQN.py, which we first find the minterm of the boolean algebra, and using sympy library and Quine-McCluskey method to finish the rest function.
The output of EQN is shown in output_EQN.txt, which looks like:
![alt text](https://github.com/d0zerLin/EC551-Program-1/blob/main/f79bb46fa3054243d0edf70a989d7e5.png?raw=true)
