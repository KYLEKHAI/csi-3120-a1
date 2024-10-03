# csi-3120-a1

### Student numbers

- Kyle Khai Tran: 300302165
  <br>
- Dipak Chinnasamy Selvam: 300313402

### Information on whether the program works or has known defects

The program has several defects:

- The parse tree for the valid expressions are incorrectly printed
  - The individual lexemes (nodes) were correctly printed out but the entire expression validation is not checked one by one
  - The indentation issue for each level is not properly printed
- The invalid expression of "\x" is not being validated properly as it is tokenized as if the expression is valid (given by the output: **The tokenized string for input string \x is \\\_x**)
- Although the rules have changed from Karim and the error messages for the invalid expressions do not need to be the same as Sample_Output.txt, there are a few differences in catching the specific error:
  - Expression <strong>\\\x\\\\</strong>:
    - SampleOutput.txt: Invalid lambda expression at 0.
    - My output: Backslashes not followed by a variable name at 0.
  - Expression <strong>((x</strong>:
    - Sample_Output.txt: Missing complete lambda expression starting at index 4. - My output: Backslashes not followed by a variable name at 0.
  - Expression <strong>()</strong>:
    - Sample_Output.txt: Bracket ( at index: 1 is not matched with a closing bracket ')'.
    - My output: Bracket ( at index: 0 is not matched with a closing bracket ')'.

### Any deviations from the assignment requirements, if applicable

- N/A the assignment rules were followed (ex: no external libraries, # TODO functions were created)

### Reference all the websites and external sources you used for help, so you don’t fall into plagiarism

- https://www.geeksforgeeks.org/
- https://docs.python.org/3/reference/lexical_analysis.html
- https://medium.com/@pythonmembers.club/building-a-lexer-in-python-a-tutorial-3b6de161fe84
- https://dev.to/ndesmic/writing-a-tokenizer-1j85
- ChatGPT: Shown in the screenshots zip folder called **Use_of_LLM.zip**
- Reviewing class lectures/notes/tutorials/labs
