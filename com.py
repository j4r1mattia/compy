import json


class Compiler:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.ast = None

    def lexer(self):
        # DFA states
        START = "START"
        IN_NUMBER = "IN_NUMBER"
        IN_IDENTIFIER = "IN_IDENTIFIER"
        IN_OPERATOR = "IN_OPERATOR"
        IN_COMMENT = "IN_COMMENT"

        state = START
        current_token = ""
        line_number = 1
        i = 0  # Index to track the current character

        while i < len(self.source_code):
            char = self.source_code[i]

            if state == START:
                if char.isdigit():
                    state = IN_NUMBER
                    current_token += char
                elif char.isalpha() or char == "_":
                    state = IN_IDENTIFIER
                    current_token += char
                elif char in "+-*/<>=":
                    if char == "/":
                        # Check if it's the start of a comment
                        if i + 1 < len(self.source_code) and self.source_code[i + 1] == "/":
                            state = IN_COMMENT
                            i += 1  # Skip the second `/`
                        else:
                            state = IN_OPERATOR
                            current_token += char
                    elif char in "<>=":
                        # Check for compound operators like <= or >=
                        if i + 1 < len(self.source_code) and self.source_code[i + 1] == "=":
                            current_token += char + "="
                            self.tokens.append(("OPERATOR", current_token, line_number))
                            current_token = ""
                            i += 1  # Skip the second character
                        else:
                            current_token += char
                            self.tokens.append(("OPERATOR", current_token, line_number))
                            current_token = ""
                    else:
                        state = IN_OPERATOR
                        current_token += char
                elif char in " \t":
                    pass  # Skip whitespace
                elif char == "\n":
                    line_number += 1
                elif char in "{}()=":
                    token_map = {
                        '{': 'LBRACE',
                        '}': 'RBRACE',
                        '(': 'LPAREN',
                        ')': 'RPAREN',
                        '=': 'ASSIGN'
                    }
                    # Emit single-character tokens
                    self.tokens.append((token_map[char], char, line_number))
                else:
                    raise Exception(f"Unexpected character '{char}' at line {line_number}")

            elif state == IN_NUMBER:
                if char.isdigit():
                    current_token += char
                else:
                    # Emit number token
                    self.tokens.append(("NUMBER", current_token, line_number))
                    current_token = ""
                    state = START
                    continue  # Reprocess the current character

            elif state == IN_IDENTIFIER:
                if char.isalnum() or char == "_":
                    current_token += char
                else:
                    # Emit identifier or keyword token
                    if current_token in {"if", "else", "while"}:
                        self.tokens.append((current_token.upper(), current_token, line_number))
                    else:
                        self.tokens.append(("IDENTIFIER", current_token, line_number))
                    current_token = ""
                    state = START
                    continue  # Reprocess the current character

            elif state == IN_OPERATOR:
                # Emit operator token
                self.tokens.append(("OPERATOR", current_token, line_number))
                current_token = ""
                state = START
                continue  # Reprocess the current character

            elif state == IN_COMMENT and char != "\n":
                state = START
                line_number += 1  # Skip the comment

            i += 1  # Move to the next character

        # Handle any remaining token
        if current_token:
            if state == IN_NUMBER:
                self.tokens.append(("NUMBER", current_token, line_number))
            elif state == IN_IDENTIFIER:
                self.tokens.append(("IDENTIFIER", current_token, line_number))
            elif state == IN_OPERATOR:
                self.tokens.append(("OPERATOR", current_token, line_number))

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