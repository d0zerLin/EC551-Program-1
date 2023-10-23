EC551-Program-1
Introduction
Welcome to the EC551 Program 1 repository. This project is focused on processing and simplifying Boolean algebra expressions. Our program supports two input formats: EQN and PLA.

Team Members
Zhaohan Song
Email: jimmy95@bu.edu
Geye Lin
Email: gylin@bu.edu
Input and Output Formats
Input: EQN and PLA (from files)
Output: .txt files
EQN Format
For EQN, we've structured the input as:

css
Copy code
~a&~b&~c&~d | ~a&~b&~c&d | ~a&b&~c&d | a&~b&~c&d | a&b&~c&d | a&b&c&~d | a&b&c&d
This format can be found in input.eqn.

The processing for this EQN input is performed by the script boolean_EQN.py. Within this script, we initially determine the minterms of the Boolean algebra. Following this, the sympy library combined with the Quine-McCluskey method is employed to simplify and generate the result.

The output can be viewed in output_EQN.txt. Below is a snapshot of the expected output:
EQN Output

PLA Format
The input for the PLA format resembles:
PLA Input

The core logic for handling PLA formatted input is contained in the script boolean_PLA.py. Similar to the EQN format, we first identify the minterms of the Boolean algebra and subsequently leverage the capabilities of the sympy library in conjunction with the Quine-McCluskey method to generate the desired output.

The output of the PLA process can be accessed in output_EQN.txt. Notably, given the inputs specified previously, both EQN and PLA will produce identical outputs.

Conclusion
This project serves as a demonstration of processing and minimizing Boolean algebra expressions using modern programming techniques and mathematical methods. Feedback and contributions are always welcome!
