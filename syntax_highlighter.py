import re
import tkinter as tk


class SyntaxHighlighter:
    def __init__(self, text_widget):
        self.text_widget = text_widget

        # Configure tags for syntax highlighting
        self.text_widget.tag_configure("keyword", foreground="blue")
        self.text_widget.tag_configure("number", foreground="orange")
        self.text_widget.tag_configure("string", foreground="green")
        self.text_widget.tag_configure("operator", foreground="red")
        self.text_widget.tag_configure("identifier", foreground="black")
        self.text_widget.tag_configure(
            "comment", foreground="#006400", background="#e6ffe6"
        )

        # Define patterns for syntax highlighting
        self.patterns = [
            (r"//.*?(?:\n|$)", "comment"),
            (r"\b(if|else)\b", "keyword"),
            (r"\b\d*\.?\d+\b", "number"),
            (r'"[^"]*"', "string"),
            (r"'[^']*'", "string"),
            (r"[+\-*/(){};=<>]", "operator"),
            (r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", "identifier"),
        ]

    def highlight(self):
        # Remove all existing tags
        for tag in ["keyword", "number", "operator", "identifier", "comment"]:
            self.text_widget.tag_remove(tag, "1.0", "end")

        # Get the text content
        content = self.text_widget.get("1.0", "end-1c")

        # Apply highlighting for each pattern
        for pattern, tag in self.patterns:
            for match in re.finditer(pattern, content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_widget.tag_add(tag, start, end)
