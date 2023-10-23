# EC551-Program-1

## Introduction

Welcome to the EC551 Program 1 repository. This project focuses on processing and simplifying Boolean algebra expressions. Our program supports two input formats: EQN and PLA.

## Team Members

- **Zhaohan Song**
  - Email: [jimmy95@bu.edu](mailto:jimmy95@bu.edu)
- **Geye Lin**
  - Email: [gylin@bu.edu](mailto:gylin@bu.edu)

## Input and Output Formats

- **Input**: EQN and PLA (from files)
- **Output**: .txt files

### EQN Format

For EQN, we've structured the input as:
\```
~a&~b&~c&~d | ~a&~b&~c&d | ~a&b&~c&d | a&~b&~c&d | a&b&~c&d | a&b&c&~d | a&b&c&d
\```
(注意：为了在这里显示效果，我在\````之间加入了反斜杠，实际粘贴到GitHub时，请去掉反斜杠)

This format can be found in [`input.eqn`](https://github.com/d0zerLin/EC551-Program-1/blob/main/input.eqn).

The processing logic is in [`boolean_EQN.py`](https://github.com/d0zerLin/EC551-Program-1/blob/main/boolean_EQN.py).

Output snapshot:
![EQN Output](https://github.com/d0zerLin/EC551-Program-1/blob/main/f79bb46fa3054243d0edf70a989d7e5.png?raw=true)

### PLA Format

PLA input format:
![PLA Input](https://github.com/d0zerLin/EC551-Program-1/blob/main/fc0478c6ae0eac58509de8fb7856a67.png)

Logic for this is in [`boolean_PLA.py`](https://github.com/d0zerLin/EC551-Program-1/blob/main/boolean_PLA.py).

Outputs can be found in `output_EQN.txt`.

## Conclusion

Feedback and contributions are welcomed!
