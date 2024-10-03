import os
from typing import Union, List, Optional

alphabet_chars = list("abcdefghijklmnopqrstuvwxyz") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
numeric_chars = list("0123456789")
var_chars = alphabet_chars + numeric_chars
all_valid_chars = var_chars + ["(", ")", ".", "\\"]
valid_examples_fp = "./valid_examples.txt"
invalid_examples_fp = "./invalid_examples.txt"

def read_lines_from_txt(fp: [str, os.PathLike]) -> List[str]:
    """
    :param fp: File path of the .txt file.
    :return: The lines of the file path removing trailing whitespaces
    and newline characters.
    """
    # TODO

    # Initialize empty list to store lines
    linesList = []

    # Check for valid file path
    if os.path.exists(fp):

        # Open file in read mode
        with open(fp, 'r') as file:

            # Read lines from file
            linesList = file.readlines()

            # Removing trailing whitespaces and newline characters
            linesList = [line.strip() for line in linesList]
    
    else:
        # Error message for invalid file path
        print("File path is invalid")

    return linesList


def is_valid_var_name(s: str) -> bool:
    """
    :param s: Candidate input variable name
    :return: True if the variable name starts with a character,
    and contains only characters and digits. Returns False otherwise.
    """
    # TODO

    #Check if the variable name is valid according to the rules ofd lambda calculus
   
    # Check if the variable name is empty
    if len(s) == 0:
        return False
    
    # Check if the variable name starts with a valid letter
    firstChar = s[0]
    if not ("A" <= firstChar <= "Z" or "a" <= firstChar <= "z"):
        return False
    
    # Check if other characters in the variable name are valid letters or digits
    for char in s[1:]:
        if not ("A" <= char <= "Z" or "a" <= char <= "z" or "0" <= char <= "9"):
            return False
        
    return True


class Node:
    """
    Nodes in a parse tree
    Attributes:
        elem: a list of strings
        children: a list of child nodes
    """
    def __init__(self, elem: List[str] = None):
        self.elem = elem
        self.children = []


    def add_child_node(self, node: 'Node') -> None:
        self.children.append(node)


class ParseTree:
    """
    A full parse tree, with nodes
    Attributes:
        root: the root of the tree
    """
    def __init__(self, root):
        self.root = root

    def print_tree(self, node: Optional[Node] = None, level: int = 0) -> None:
        # TODO

        # Check if a node is not specified from the root node
        if node is None:
            node = self.root

        # Print the current node
        print("-" * level + "_".join(node.elem))
        
        # Recursive call to print every child node (show levels)
        for child in node.children:
            self.print_tree(child, level + 1)



def parse_tokens(s_: str) -> Union[List[str], bool]:
    """
    Gets the final tokens for valid strings as a list of strings, only for valid syntax,
    where tokens are (no whitespace included)
    \\ values for lambdas
    valid variable names
    opening and closing parenthesis
    Note that dots are replaced with corresponding parenthesis
    :param s_: the input string
    :return: A List of tokens (strings) if a valid input, otherwise False
    """

    s = s_[:]  #  Don't modify the original input string
    # TODO
    
    # Initialize an empty list to store tokens
    token_list = []

    # Index for traversing the input string
    i = 0  
    
    # Length of input
    length = len(s)

    # Track the open parantheses count
    openParenthesesCount = 0 

    while i < length:
        current_char = s[i]

        # Skip whitespaces
        if current_char.isspace():
            i += 1
            continue

        # Lambda expressions (start with backslash)
        if current_char == "\\":
            token_list.append(current_char)
            i += 1
            if i < length and is_valid_var_name(s[i]):
                token_list.append(s[i])
                i += 1

                # Check if the next character is a valid separator
                if i < length and not s[i].isspace() and s[i] not in ["(", ")", ".", "\\"]:
                    print(f"Invalid lambda expression at {i-2}.")
                    return False
            else:
                # Error validation 
                if i < length and s[i].isspace():
                    print(f"Invalid space inserted after \\ at index {i-1}.")
                else:
                    print(f"Backslashes not followed by a variable name at {i-1}.")
                return False

        # Check for parentheses (open and close)
        elif current_char == "(":
            token_list.append(current_char)
            openParenthesesCount += 1
            i += 1

            # Error validation for missing expression after open parenthesis
            if i < length and s[i] == ")":
                print(f"Missing expression for parenthesis at index {i-1}.")
                return False

        elif current_char == ")":
            # Error validation
            if openParenthesesCount == 0:
                print(f"Bracket ) at index: {i} is not matched with an opening bracket '('.")
                return False
            
            token_list.append(current_char)
            openParenthesesCount-= 1
            i += 1

        # Dot operator

        elif current_char == ".":
            # Error validation
            if i == 0:
            # Encountered dot at invalid index (error validation)
                print(f"Encountered dot at invalid index {i}.")
                return False
            elif i > 0 and not is_valid_var_name(s[i - 1]):
                print(f"Must have a variable name before character '.' at index {i-1}.")
                return False
          
            # Open parenthesis for the lambda body after the dot
            token_list.append("(")
            i += 1

            # Skip whitespaces
            while i < length:
                if s[i].isspace():
                    i += 1  
                    continue

                # Check for valid lambda expressions 

                # Check for open parenthesis
                elif is_valid_var_name(s[i]) or s[i] == "(":
                    token_list.append(s[i])
                    i += 1

                # Check for closing parenthesis
                elif s[i] == ")":  
                    token_list.append(")")
                    i += 1
                    break
                
                else:
                    break

            # Close the lambda expression body
            token_list.append(")") 

        # Handle variable names
        elif is_valid_var_name(current_char):
            token_list.append(current_char)
            i += 1

        # Handle invalid characters
        else:
            if current_char.isdigit():
                print(f"Error at index {i}, variables cannot begin with digits.")
            else:
                print(f"Error at index {i} with invalid character {current_char}.")
            return False

    # Check unmatched opening parentheses
    if openParenthesesCount > 0:
        print(f"Bracket ( at index: {s.find('(')} is not matched with a closing bracket ')'.")
        return False

    return token_list if token_list else False


def read_lines_from_txt_check_validity(fp: [str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, and then
    parses each string  to yield a tokenized list of strings for printing, joined by _ characters
    In the case of a non-valid line, the corresponding error message is printed (not necessarily within
    this function, but possibly within the parse_tokens function).
    :param fp: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    valid_lines = []
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            valid_lines.append(l)
            print(f"The tokenized string for input string {l} is {'_'.join(tokens)}")
    if len(valid_lines) == len(lines):
        print(f"All lines are valid")



def read_lines_from_txt_output_parse_tree(fp: [str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, and then
    parses each string to yield a tokenized output string, to be used in constructing a parse tree. The
    parse tree should call print_tree() to print its content to the console.
    In the case of a non-valid line, the corresponding error message is printed (not necessarily within
    this function, but possibly within the parse_tokens function).
    :param fp: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            print("\n")
            parse_tree2 = build_parse_tree(tokens)
            parse_tree2.print_tree()




def build_parse_tree_rec(tokens: List[str], node: Optional[Node] = None) -> Node:
    """
    An inner recursive inner function to build a parse tree
    :param tokens: A list of token strings
    :param node: A Node object
    :return: a node with children whose tokens are variables, parenthesis, slashes, or the inner part of an expression
    """

    #TODO

    # Check if the token list is empty
    if not tokens:
        return node

    # Remove and get the first token from the list
    token = tokens.pop(0)

    # Checking the lambda expression
    if token == "\\":

        # Check if tokens are not empty before popping
        boundVariable = tokens.pop(0) if tokens else None
        if boundVariable is None:
            raise ValueError("Expected a bound variable after '\\'")  

        # Node for lambda operator
        newNode = Node(elem=["\\"])

        # Add variable node to the lambda node (child node)
        newNode.add_child_node(Node(elem=[boundVariable]))

        # Recursive call to build the parse tree
        newNode.add_child_node(build_parse_tree_rec(tokens))
        return newNode
    
    # Checking for parentheses
    elif token == "(":
        # Recursive call to build subtree
        newNode = build_parse_tree_rec(tokens)

        # Pop only if exist 
        if tokens and tokens[0] == ")":
            tokens.pop(0) 
        return newNode
    
    # Other variables
    else:
        newNode = Node(elem=[token])

        # Check if the next token is a lambda expression or the end of the expression
        if tokens and tokens[0] not in [["\\"], [")"]]:
            newNode.add_child_node(build_parse_tree_rec(tokens))
        return newNode


def build_parse_tree(tokens: List[str]) -> ParseTree:
    """
    Build a parse tree from a list of tokens
    :param tokens: List of tokens
    :return: parse tree
    """
    pt = ParseTree(build_parse_tree_rec(tokens))
    return pt


if __name__ == "__main__":

    print("\n\nChecking valid examples...")
    read_lines_from_txt_check_validity(valid_examples_fp)
    read_lines_from_txt_output_parse_tree(valid_examples_fp)

    print("Checking invalid examples...")
    read_lines_from_txt_check_validity(invalid_examples_fp)