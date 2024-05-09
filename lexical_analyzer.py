import re
import tkinter as tk
from tkinter import Canvas, filedialog, messagebox, ttk
import random

primary_color = "#007acc" 
accent_color = "#00509e" 
success_color = "#28a745"  
error_color = "#dc3545"  


class Token:
    # Class-level variable for unique token IDs
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
        token_patterns = {
            "PLUS": r"\+",
            "TIMES": r"\*",
            "LPAREN": r"\(",
            "RPAREN": r"\)",
            "ID": r"[a-zA-Z0-9]+",
            "WHITESPACE": r"\s+",
        }

        compiled_patterns = {k: re.compile(v) for k, v in token_patterns.items()}

        while self.current_pos < len(self.input_string):
            matched = False
            for token_type, pattern in compiled_patterns.items():
                match = pattern.match(self.input_string, self.current_pos)
                if match:
                    lexeme = match.group(0)
                    if token_type != "WHITESPACE":
                        self.tokens.append(Token(token_type, lexeme))
                    self.current_pos += len(lexeme)
                    matched = True
                    break
            if not matched:
                raise ValueError(f"Unexpected character at position {self.current_pos}")

    def get_tokens(self):
        return self.tokens

# Symbol Table
class SymbolTable:
    def __init__(self):
        self.table = {}

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
        return f"{self.name} "

    def to_string(self, indent=0):
        indentation = " " * indent
        tree_str = f"{indentation}{self.name}\n"
        for child in self.children:
            if isinstance(child, ParseTreeNode):
                tree_str += child.to_string(indent + 2)
            else:
                tree_str += f"{indentation + '  '}{child}\n"
        return tree_str

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
        node = ParseTreeNode("E")
        node.add_child(self.parse_T())
        node.add_child(self.parse_E_prime())
        return node

    def parse_E_prime(self):
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
        node = ParseTreeNode("T")
        node.add_child(self.parse_F())
        node.add_child(self.parse_T_prime())
        return node

    def parse_T_prime(self):
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

# Function to draw parse tree on a Tkinter canvas
def draw_parse_tree(canvas, parse_tree):
    start_x = 120
    start_y = 40

    box_padding = 120
    box_width = 220

    def draw_node(node, x, y):
        colors = ["red", "blue", "green", "orange", "purple", "brown", "black"]
        color = random.choice(colors)

        canvas.create_text(x, y-10, text=str(node), anchor='w', fill=color)

        if hasattr(node, 'children'):
            # Spread out children to avoid overlap
            child_spacing = (len(node.children) - 1) * box_padding
            base_y = y - (child_spacing // 2)

            for i, child in enumerate(node.children):
                child_y = base_y + i * box_padding
                canvas.create_line(x + 20, y, x + box_width, child_y, fill=color)
                draw_node(child, x + box_width, child_y)


    canvas.delete("all")
    draw_node(parse_tree, start_x, start_y)

# Function to draw the symbol table on a Tkinter canvas
def draw_symbol_table(canvas, symbol_table):
    start_x = 10
    start_y = 20
    box_height = 30

    canvas.delete("all")

    for i, (key, value) in enumerate(symbol_table.items()):
        text = f"{key}: {value}"
        canvas.create_text(start_x, start_y + i * box_height, text=text, anchor='w', fill="black")

class LexicalAnalyzerGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Lexical Analyzer")
        self.geometry("1000x600")

        # Using better colors for accessibility
        primary_color = "#007acc" 
        success_color = "#28a745"  
       

        # Header
        header_label = tk.Label(self, text="Lexical Analyzer", font=("Helvetica", 20), fg=primary_color)
        header_label.pack(pady=5)

        # Input Field with padding
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=3)
        
        input_label = tk.Label(input_frame, text="Input:", font=("Helvetica", 12))
        input_label.pack(side=tk.LEFT, padx=5)
        
        self.input_field = tk.Entry(input_frame, width=50)
        self.input_field.pack(side=tk.LEFT, padx=10)
        
        # Button Frame with consistent color theme
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=5)
        
        # Button for Analysis
        analyze_button = tk.Button(
            button_frame,
            text="Analyze",
            command=self.analyze_input,
            bg=success_color,
            fg="white",
            font=("Helvetica", 12),
            padx=10, 
            pady=5
        )
        analyze_button.pack(side=tk.LEFT, padx=10)

        # Button for File Upload
        upload_button = tk.Button(
            button_frame,
            text="Upload File",
            command=self.upload_file,
            bg=primary_color,
            fg="white",
            font=("Helvetica", 12),
            padx=10,
            pady=5
        )
        upload_button.pack(side=tk.RIGHT, padx=10)

        # Output Text with a success and error indicator
        self.output_text = tk.Text(self, height=3, width=80, state=tk.DISABLED)
        self.output_text.pack(pady=5)

        # Frame for the Parse Tree with horizontal and vertical scroll
        parse_tree_frame = ttk.Frame(self)
        parse_tree_frame.pack(pady=5, fill='x')

        parse_tree_vscroll = ttk.Scrollbar(parse_tree_frame, orient="vertical")
        parse_tree_hscroll = ttk.Scrollbar(parse_tree_frame, orient="horizontal")

        self.parse_tree_canvas = tk.Canvas(
            parse_tree_frame,
            bg="#c9c6ca",
            height=300,
            yscrollcommand=parse_tree_vscroll.set,
            xscrollcommand=parse_tree_hscroll.set,
            width=1500,
        )
        
        parse_tree_vscroll.config(command=self.parse_tree_canvas.yview)
        parse_tree_hscroll.config(command=self.parse_tree_canvas.xview)

        parse_tree_vscroll.pack(side=tk.RIGHT, fill='y')
        parse_tree_hscroll.pack(side=tk.BOTTOM, fill='x')

        self.parse_tree_canvas.pack(side=tk.LEFT, fill='x', expand=True)

        # Frame for the Symbol Table with horizontal and vertical scroll
        symbol_table_frame = ttk.Frame(self)
        symbol_table_frame.pack(pady=5, fill='x')

        symbol_table_vscroll = ttk.Scrollbar(symbol_table_frame, orient="vertical")
        symbol_table_hscroll = ttk.Scrollbar(symbol_table_frame, orient="horizontal")

        self.symbol_table_canvas = tk.Canvas(
            symbol_table_frame,
            bg="#c9c6ca",
            height=200,
            yscrollcommand=symbol_table_vscroll.set,
            xscrollcommand=symbol_table_hscroll.set,
            width=1500,
        )
        
        symbol_table_vscroll.config(command=self.symbol_table_canvas.yview)
        symbol_table_hscroll.config(command=self.symbol_table_canvas.xview)

        symbol_table_vscroll.pack(side=tk.RIGHT, fill='y')
        symbol_table_hscroll.pack(side=tk.BOTTOM, fill='x')

        self.symbol_table_canvas.pack(side=tk.LEFT, fill='x', expand=True)

    def analyze_input(self):
        input_str = self.input_field.get().strip()
        Token.next_token_id = 1
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)

        try:
          
            lexer = Lexer(input_str)
            tokens = lexer.get_tokens()

            parser = Parser(tokens)
            parse_tree = parser.get_parse_tree()
            symbol_table = parser.get_symbol_table()

            self.output_text.insert(tk.END, "Accepted!\n")
            self.output_text.tag_configure("green", foreground=success_color)
            self.output_text.tag_add("green", "1.0", "end")

            draw_parse_tree(self.parse_tree_canvas, parse_tree)
            draw_symbol_table(self.symbol_table_canvas, symbol_table)

        except ValueError as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")
            self.output_text.tag_configure("red", foreground=error_color)
            self.output_text.tag_add("red", "1.0", "end")
            self.parse_tree_canvas.delete("all")
            self.symbol_table_canvas.delete("all")
        

        self.output_text.configure(state=tk.DISABLED)
   
    def upload_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, "r") as file:
                    lines = file.readlines()

                self.output_text.configure(state=tk.NORMAL)
                self.output_text.delete(1.0, tk.END)

                for line in lines:
                    input_str = line.strip()

                    lexer = Lexer(input_str)
                    tokens = lexer.get_tokens()

                    parser = Parser(tokens)
                    parse_tree = parser.get_parse_tree()
                    symbol_table = parser.get_symbol_table()

                    self.output_text.insert(tk.END, f"Accepted: {input_str}\n")
                    self.output_text.tag_configure("green", foreground=success_color)
                    self.output_text.tag_add("green", "1.0", "end")

                    draw_parse_tree(self.parse_tree_canvas, parse_tree)
                    draw_symbol_table(self.symbol_table_canvas, symbol_table)

                self.output_text.configure(state=tk.DISABLED)
            except Exception as e:
                print(e)

# Run the Application
if __name__ == "__main__":
    app = LexicalAnalyzerGUI()
    app.mainloop()

