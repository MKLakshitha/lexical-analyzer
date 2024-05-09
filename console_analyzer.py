import re

# Token representation
class Token:
   
    next_token_id = 1

    def __init__(self, token_type, lexeme, value=None):
        self.token_type = token_type
        self.lexeme = lexeme
        self.token_id = Token.next_token_id
        Token.next_token_id += 1 
        self.value = value

    def __str__(self):
        return f"{self.token_type} (ID: {self.token_id}): {self.lexeme}"

# Lexical Analyzer
class Lexer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.tokens = []
        self.current_pos = 0
        self.tokenize()
    
    def tokenize(self):
        # Regular expressions for different token types
        token_patterns = {
            "PLUS": r"\+",
            "TIMES": r"\*",
            "LPAREN": r"\(",
            "RPAREN": r"\)",
            "ID": r"[a-zA-Z0-9]+",
            "WHITESPACE": r"\s+",
        }

        # Compile the patterns into regular expressions
        compiled_patterns = {k: re.compile(v) for k, v in token_patterns.items()}

        while self.current_pos < len(self.input_string):
            for token_type, pattern in compiled_patterns.items():
                match = pattern.match(self.input_string, self.current_pos)
                if match:
                    lexeme = match.group(0)
                    if token_type != "WHITESPACE":  # Ignore whitespaces
                        self.tokens.append(Token(token_type, lexeme))
                    self.current_pos += len(lexeme)
                    break
            else:
                raise ValueError(f"Unexpected character at position {self.current_pos}")

    def get_tokens(self):
        return self.tokens

# Symbol Table
class SymbolTable:
    def __init__(self):
        self.table = {}


    def add_token(self, token):
        
        self.table[token.lexeme] = {
            "type": token.token_type,
            "id": token.token_id,
        }

    def get_table(self):
        return self.table

# Parse Tree Node
class ParseTreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        child_strs = ", ".join(str(c) for c in self.children)
        return f"{self.name} -> [{child_strs}]"

# Recursive Descent Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_index = 0
        self.symbol_table = SymbolTable()
        self.parse_tree = self.parse_E()

    def current_token(self):
        if self.current_index < len(self.tokens):
            return self.tokens[self.current_index]
        return None

    def match(self, expected_type):
        current = self.current_token()
        if current and current.token_type == expected_type:
            self.current_index += 1
            return current
        else:
            raise ValueError(
                f"Expected {expected_type}, found {current.token_type if current else 'None'}"
            )

    def parse_E(self):
        # E → TE´
        node = ParseTreeNode("E")
        node.add_child(self.parse_T())
        node.add_child(self.parse_E_prime())
        return node

    def parse_E_prime(self):
        # E´→ +TE´|Ɛ
        node = ParseTreeNode("E'")
        current = self.current_token()

        if current and current.token_type == "PLUS":
            self.match("PLUS")
            node.add_child(Token("PLUS", "+"))
            node.add_child(self.parse_T())
            node.add_child(self.parse_E_prime())
        else:
            node.add_child(Token("EPSILON", "Ɛ"))

        return node

    def parse_T(self):
        # T → FT´
        node = ParseTreeNode("T")
        node.add_child(self.parse_F())
        node.add_child(self.parse_T_prime())
        return node

    def parse_T_prime(self):
        # T´→ *FT´|Ɛ
        node = ParseTreeNode("T'")
        current = self.current_token()

        if current and current.token_type == "TIMES":
            self.match("TIMES")
            node.add_child(Token("TIMES", "*"))
            node.add_child(self.parse_F())
            node.add_child(self.parse_T_prime())
        else:
            node.add_child(Token("EPSILON", "Ɛ"))

        return node

    def parse_F(self):
        # F → (E) | id
        node = ParseTreeNode("F")
        current = self.current_token()

        if current and current.token_type == "LPAREN":
            self.match("LPAREN")
            node.add_child(Token("LPAREN", "("))
            node.add_child(self.parse_E())
            self.match("RPAREN")
            node.add_child(Token("RPAREN", ")"))
        elif current and current.token_type == "ID":
            id_token = self.match("ID")
            node.add_child(id_token)
            self.symbol_table.add_token(id_token)
        else:
            raise ValueError("Invalid token in F")
        
        return node

    def get_parse_tree(self):
        return self.parse_tree

    def get_symbol_table(self):
        return self.symbol_table.get_table()

# Testing the Lexer, Parser, and Symbol Table
def main():
    # Test input strings
    input_strings = [
        "3 + 4 * 5",
        "(1 + 2) * 3",
        "x + y * z",
        "3 + 4 *",
        "3 + (4 * 5",
    ]

    for input_str in input_strings:
        print(f"\nInput String: {input_str}")

        # Lexical analysis
        lexer = Lexer(input_str)
        Token.next_token_id = 1
        tokens = lexer.get_tokens()
        print("Tokens:")
        for token in tokens:
            print(f"{token}")

        # Parsing
        try:
            parser = Parser(tokens)
            print("Parse Tree:")
            print(parser.get_parse_tree())
            print("Symbol Table:")
            Token.next_token_id = 1
            print(parser.get_symbol_table())
        except ValueError as e:
            print(f"Error: {e}")

        print()

# Run the main function to test the implementation
if __name__ == "__main__":
    main()
