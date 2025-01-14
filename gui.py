import tkinter as tk
from tkinter import ttk, filedialog
from lexer import Lexer
from parser import Parser
from syntax_highlighter import SyntaxHighlighter


class SyntaxCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.highlighter = SyntaxHighlighter(self.code_text)

    def setup_ui(self):
        self.root.title("Syntax Checker")
        self.root.geometry("1700x1900")
        self.create_main_frame()
        self.create_grammar_display()
        self.create_code_input()
        self.create_buttons()
        self.create_result_output()
        self.setup_grid_weights()
        self.update_line_numbers()

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def create_grammar_display(self):
        ttk.Label(
            self.main_frame, text="Grammar Rules:", font=("Arial", 12, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W)
        rules_text = """Program    -> StmtList
StmtList   -> Stmt StmtList | ε
Stmt       -> AssignStmt | IfStmt
AssignStmt -> id = Expr ;
IfStmt     -> if (Expr) { StmtList } else { StmtList }
Expr       -> Term ((+ | -) Term)*
Term       -> Factor ((* | /) Factor)*
Factor     -> num | id | (Expr)"""
        self.rules = tk.Text(self.main_frame, height=8, width=80, font=("Courier", 11))
        self.rules.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        self.rules.insert("1.0", rules_text)
        self.rules.configure(state="disabled")

    def create_code_input(self):
        ttk.Label(
            self.main_frame, text="Enter your code:", font=("Arial", 12, "bold")
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))

        text_frame = ttk.Frame(self.main_frame)
        text_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.create_line_numbers(text_frame)
        self.create_code_text(text_frame)
        self.create_scrollbar(text_frame)

    def create_line_numbers(self, frame):
        self.line_numbers = tk.Text(
            frame,
            width=4,
            padx=3,
            takefocus=0,
            font=("Courier", 11),
            state="disabled",
            background="lightgray",
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

    def create_code_text(self, frame):
        self.code_text = tk.Text(frame, height=15, width=80, font=("Courier", 11))
        self.code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.bind_events()

    def create_scrollbar(self, frame):
        code_scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.on_scroll)
        code_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.code_text["yscrollcommand"] = code_scroll.set
        self.line_numbers["yscrollcommand"] = code_scroll.set

    def create_buttons(self):
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        buttons = [
            ("Check Syntax", self.check_syntax),
            ("Load Example", self.load_example),
            ("Clear", self.clear_code),
            ("Save", self.save_code),
            ("Load", self.load_code),
        ]

        for text, command in buttons:
            ttk.Button(button_frame, text=text, command=command).pack(
                side=tk.LEFT, padx=5
            )

    def create_result_output(self):
        ttk.Label(self.main_frame, text="Result:", font=("Arial", 12, "bold")).grid(
            row=5, column=0, columnspan=2, sticky=tk.W
        )
        self.result_text = tk.Text(
            self.main_frame, height=10, width=80, font=("Courier", 11), state="disabled"
        )
        self.result_text.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E))

        result_scroll = ttk.Scrollbar(
            self.main_frame, orient=tk.VERTICAL, command=self.result_text.yview
        )
        result_scroll.grid(row=6, column=2, sticky=(tk.N, tk.S))
        self.result_text["yscrollcommand"] = result_scroll.set

    def setup_grid_weights(self):
        self.main_frame.columnconfigure(0, weight=1)
        for i in [1, 3, 6]:
            self.main_frame.rowconfigure(i, weight=1)

    def bind_events(self):
        self.code_text.bind("<KeyRelease>", self.on_text_change)
        self.code_text.bind("<Return>", self.on_return)
        self.code_text.bind("<BackSpace>", self.on_backspace)

    def on_scroll(self, *args):
        self.code_text.yview(*args)
        self.line_numbers.yview(*args)

    def on_text_change(self, event=None):
        self.update_line_numbers()
        self.highlighter.highlight()

    def on_return(self, event=None):
        self.root.after(1, self.on_text_change)
        return None

    def on_backspace(self, event=None):
        self.root.after(1, self.on_text_change)
        return None

    def update_line_numbers(self):
        lines = self.code_text.get("1.0", "end-1c").split("\n")
        line_numbers_text = "\n".join(str(i + 1).rjust(3) for i in range(len(lines)))
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", line_numbers_text)
        self.line_numbers.configure(state="disabled")

    def check_syntax(self):
        code = self.code_text.get("1.0", tk.END).strip()

        try:
            lexer = Lexer(code)
            parser = Parser(lexer)
            is_valid = parser.program()

            self.result_text.configure(state="normal")
            self.result_text.delete("1.0", tk.END)

            if is_valid:
                result = "✅ Syntax is valid!\n\nYour code follows all the grammar rules correctly."
                self.result_text.configure(background="#e6ffe6")
            else:
                result = "❌ Syntax errors found:\n\n" + "\n".join(parser.errors)
                self.result_text.configure(background="#ffe6e6")

            self.result_text.insert("1.0", result)
            self.result_text.configure(state="disabled")

        except Exception as e:
            self.result_text.configure(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", f"❌ Error: {str(e)}")
            self.result_text.configure(background="#ffe6e6")
            self.result_text.configure(state="disabled")

    def load_example(self):
        example = """// This is a test program demonstrating all features
// Numbers, strings, and expressions

// 1. Basic assignments with different types
num1 = 42;        // Integer
num2 = 3.14159;   // Float
str1 = "Hello";   // Double quoted string
str2 = 'World';   // Single quoted string

// 2. Arithmetic expressions
result = num1 + num2 * 2;
x = (10 + 5) * 2;

// 3. Nested if statements
if (x) {
    y = y + 1;    // Increment
    z = x * (y + 2.5);  // Float arithmetic
} else {
    y = y - 1;    // Decrement
    z = x / 2;    // Division
}

// 4. More complex expressions
total = (x + y) * (z / 2.0);

// End of example program"""
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", example)
        self.on_text_change()

    def clear_code(self):
        self.code_text.delete("1.0", tk.END)
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.configure(state="disabled")
        self.result_text.configure(background="white")
        self.on_text_change()

    def save_code(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.code_text.get("1.0", tk.END))

    def load_code(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, "r") as file:
                self.code_text.delete("1.0", tk.END)
                self.code_text.insert("1.0", file.read())
                self.on_text_change()
