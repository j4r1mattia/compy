import logging

logger = logging.getLogger(__name__)

class Lexer():
        
    def __init__(self, source_code: str):
        logging.basicConfig(level=logging.INFO)
        self.source_code = source_code.lstrip()
        self.tokens = []    
        
        self.current_token = ""
        self.line_number = 1
        self.index = 0 

    def tokenize(self):
        # DFA states
        START = "START"
        IN_NUMBER = "IN_NUMBER"
        IN_IDENTIFIER = "IN_IDENTIFIER"
        IN_OPERATOR = "IN_OPERATOR"
        IN_COMMENT = "IN_COMMENT"

        self.state = START
        try:
            while self.index < len(self.source_code):
                next_char = self.source_code[self.index]

                if self.state == START:
                    self.state, self.current_token = self.handle_start_state(next_char)

                elif self.state == IN_NUMBER:
                    self.state, self.current_token = self.handle_in_number_state(next_char)

                elif self.state == IN_IDENTIFIER:
                    self.state, self.current_token = self.handle_in_identifier_state(next_char)

                elif self.state == IN_OPERATOR:
                    self.state, self.current_token = self.handle_in_operator_state(next_char)

                elif self.state == IN_COMMENT:
                    self.state, self.current_token = self.handle_in_comment_state(next_char)

                self.index += 1  # Move to the next character
        except Exception as e:
            logger.error(repr(e))
            logger.error(f"Error at index {self.index}, line {self.line_number}, token: {self.current_token}, state: {self.state}, tokens: {self.tokens}, next_char: {next_char}")
            return

    
    def handle_start_state(self, next_char: str):
        logger.debug(f"in START state handling next_char: {next_char}")
        if next_char.isdigit():
            return "IN_NUMBER", self.current_token + next_char
        elif next_char.isalpha() or next_char == "_":
            return "IN_IDENTIFIER", self.current_token + next_char
        elif next_char in "+-*/<>=":
            return "IN_OPERATOR", self.current_token + next_char 
        elif next_char in " \t":
            return "START", ""
        elif next_char == "\n":
            self.line_number += 1
            return "START", ""
        elif next_char in "{}()=":
            token_map = {
                '{': 'LBRACE',
                '}': 'RBRACE',
                '(': 'LPAREN',
                ')': 'RPAREN',
                '=': 'ASSIGN'
            }
            # Emit single-character tokens
            return self._append_token_then_transists_start(token_type=token_map[next_char], token_value=next_char)
        else:
            raise ValueError(f"Unexpected character '{next_char}' at line {self.line_number}")
    
    def handle_in_number_state(self, next_char: str):
        logger.debug(f"in NUMBER state handling next_char: {next_char}, current_token: {self.current_token}, line_number: {self.line_number}, index: {self.index}")
        if next_char.isdigit():
            return "IN_NUMBER", self.current_token + next_char
        # Emit number token
        state, token =  self._append_token_then_transists_start(token_type="NUMBER", token_value=self.current_token)
        
        if next_char == "\n":
            self.line_number += 1
        
        return state, token

    def handle_in_identifier_state(self, next_char: str):
        logger.debug(f"in IDENTIFIER state handling next_char: {next_char}, current_token: {self.current_token}, line_number: {self.line_number}, index: {self.index}")
        if next_char.isalnum() or next_char == "_":
            state, token =  "IN_IDENTIFIER", self.current_token + next_char
        # Emit identifier or keyword token
        elif self.current_token in {"if", "else", "while"}:
            state, token =  self._append_token_then_transists_start(token_type=self.current_token.upper(), token_value=self.current_token)
        else:
            state, token =  self._append_token_then_transists_start(token_type="IDENTIFIER", token_value=self.current_token)
        
        if next_char == "\n":
            self.line_number += 1
        
        return state, token

    def handle_in_operator_state(self, next_char: str):
        logger.debug(f"in OPERATOR state handling next_char: {next_char}, current_token: {self.current_token}, line_number: {self.line_number}, index: {self.index}")
        # Check if it's the start of a comment
        if self.current_token == "/" and next_char == "/":
            state, token = "IN_COMMENT", ""

        elif self.current_token == "=" and next_char != "=":
            state, token = self._append_token_then_transists_start(token_type="ASSIGN", token_value=self.current_token)

        else:
            # Check for compound operators like <=, >= or ==
            if next_char == "=":
                self.current_token += next_char
                self.index += 1  # Skip the second character
            state, token =  self._append_token_then_transists_start(token_type="OPERATOR", token_value=self.current_token)
        
        if next_char == "\n":
            self.line_number += 1

        return state, token
        
    def handle_in_comment_state(self, next_char: str):
        logger.debug(f"in COMMENT state handling next_char: {next_char}, current_token: {self.current_token}, line_number: {self.line_number}, index: {self.index}")
        if next_char == "\n":
            self.line_number += 1
        while self.index < len(self.source_code) and self.source_code[self.index] != "\n":
            self.index += 1
        self.line_number += 1
        return "START", ""

    def _append_token_then_transists_start(self, token_type: str, token_value: str):
        self.tokens.append((token_type, token_value, self.line_number))
        return "START", ""
    