import json
from lexer import Lexer


class Compiler:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.ast = None

    def lexer(self):
        lexer = Lexer(self.source_code)
        lexer.tokenize()
        self.tokens = lexer.tokens
        
    def parser(self):
        # Parse tokens into an AST
        self.ast = {"type": "Assignment", "left": self.tokens[0], "right": self.tokens[2]}

    def semantic_analysis(self):
        # Check semantics (e.g., variable declaration)
        if not self.ast["left"].isidentifier():
            raise Exception("Invalid identifier")

    def code_generation(self):
        # Generate target code
        return f"MOV {self.ast['left']}, {self.ast['right']}"

    def compile(self):
        self.lexer()
        self.parser()
        self.semantic_analysis()
        return self.code_generation()


# Example usage
source = """
x = 5 + 3
// This is a comment
if x > 5 {
    y = x - 2
} else {
    y = 0
}
"""
compiler = Compiler(source)
compiler.lexer()
print(json.dumps(compiler.tokens, indent=4))