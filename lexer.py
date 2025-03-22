import logging

"""
Lexer Module
============
This module provides a `Lexer` class for tokenizing source code into a sequence of tokens using a deterministic finite automaton (DFA). 
The lexer processes the source code character by character, transitioning between states based on the current character and the DFA state. 
It supports tokenizing numbers, identifiers, operators, and comments.

Features
--------
- Tokenizes source code into meaningful tokens.
- Handles different types of tokens such as numbers, identifiers, operators, and comments.
- Supports single-character tokens like braces, parentheses, and assignment operators.
- Logs errors with detailed information for debugging.

License
-------
This code is provided as-is without any warranty. You are free to use, modify, and distribute it under the terms of the MIT License.

Usage
-----
To use the `Lexer` class, initialize it with the source code as a string and call the `tokenize` method. The generated tokens can be accessed via the `tokens` attribute.
Example:
    ```python
    source_code = "if (x == 10) { y = x + 1; }"
    lexer = Lexer(source_code)
    lexer.tokenize()
    print(lexer.tokens)
    ```
Classes
-------
- `Lexer`: The main class for tokenizing source code.

Methods
-------
- `__init__(source_code: str)`: Initializes the lexer with the source code.
- `tokenize()`: Tokenizes the source code into a sequence of tokens.
- `_handle_start_state(next_char: str)`: Handles the START state of the lexer.
- `_handle_in_number_state(next_char: str)`: Handles the IN_NUMBER state of the lexer.
- `_handle_in_identifier_state(next_char: str)`: Handles the IN_IDENTIFIER state of the lexer.
- `_handle_in_operator_state(next_char: str)`: Handles the IN_OPERATOR state of the lexer.
- `_handle_in_comment_state(next_char: str)`: Handles the IN_COMMENT state of the lexer.
- `_append_token_then_transists_start(token_type: str, token_value: str)`: Appends a token and transitions to the START state.

Attributes
----------
- `source_code (str)`: The source code to tokenize.
- `tokens (list)`: The list of tokens generated.
- `current_token (str)`: The token currently being processed.
- `line_number (int)`: The current line number in the source code.
- `index (int)`: The current index in the source code being processed.
- `state (str)`: The current DFA state.

Exceptions
----------
- Logs an error and stops tokenization if an exception occurs during processing. 
"""

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
        """
        Tokenizes the source code into a sequence of tokens using a deterministic finite automaton (DFA).

        The method processes the source code character by character, transitioning between states
        based on the current character and the current DFA state. It handles different types of tokens
        such as numbers, identifiers, operators, and comments.

        States:
            - START: Initial state, determines the type of token to process.
            - IN_NUMBER: State for processing numeric tokens.
            - IN_IDENTIFIER: State for processing identifier tokens.
            - IN_OPERATOR: State for processing operator tokens.
            - IN_COMMENT: State for processing comment tokens.

        Attributes:
            self.source_code (str): The source code to tokenize.
            self.index (int): The current index in the source code being processed.
            self.state (str): The current DFA state.
            self.current_token (str): The token currently being processed.
            self.tokens (list): The list of tokens generated so far.
            self.line_number (int): The current line number in the source code.

        Exceptions:
            Logs an error and stops tokenization if an exception occurs during processing.
            The error log includes the index, line number, current token, state, tokens, and the next character.

        Returns:
            None
        """
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
                    self.state, self.current_token = self._handle_start_state(next_char)

                elif self.state == IN_NUMBER:
                    self.state, self.current_token = self._handle_in_number_state(next_char)

                elif self.state == IN_IDENTIFIER:
                    self.state, self.current_token = self._handle_in_identifier_state(next_char)

                elif self.state == IN_OPERATOR:
                    self.state, self.current_token = self._handle_in_operator_state(next_char)

                elif self.state == IN_COMMENT:
                    self.state, self.current_token = self._handle_in_comment_state(next_char)

                self.index += 1  # Move to the next character
        except Exception as e:
            logger.error(repr(e))
            logger.error(f"Error at index {self.index}, line {self.line_number}, token: {self.current_token}, state: {self.state}, tokens: {self.tokens}, next_char: {next_char}")
            return

    
    def _handle_start_state(self, next_char: str):
        """
        Handles the START state of the lexer by processing the next character and determining the 
        appropriate state transition and token generation.
        Args:
            next_char (str): The next character to process.
        Returns:
            tuple: A tuple containing the next state (str) and the updated current token (str).
        Raises:
            ValueError: If an unexpected character is encountered.
        Behavior:
            - Transitions to "IN_NUMBER" state if the character is a digit.
            - Transitions to "IN_IDENTIFIER" state if the character is an alphabetic character or an underscore.
            - Transitions to "IN_OPERATOR" state if the character is an operator (+, -, *, /, <, >, =).
            - Remains in "START" state if the character is a space or tab.
            - Increments the line number and remains in "START" state if the character is a newline.
            - Emits a single-character token and transitions to "START" state for specific characters 
              ({, }, (, ), =).
            - Raises a ValueError for any unexpected character.
        """

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
    
    def _handle_in_number_state(self, next_char: str):
        """
        Handles the lexer state when parsing a numeric token.
        This method processes the next character while the lexer is in the "IN_NUMBER" state.
        If the character is a digit, it appends it to the current token and remains in the
        "IN_NUMBER" state. If the character is not a digit, it finalizes the current numeric
        token, transitions to the "START" state, and processes the character accordingly.
        Args:
            next_char (str): The next character to process.
        Returns:
            tuple: A tuple containing the next state (str) and the updated token (str or None).
        """

        logger.debug(f"in NUMBER state handling next_char: {next_char}, current_token: {self.current_token}, line_number: {self.line_number}, index: {self.index}")
        if next_char.isdigit():
            return "IN_NUMBER", self.current_token + next_char
        # Emit number token
        state, token =  self._append_token_then_transists_start(token_type="NUMBER", token_value=self.current_token)
        
        if next_char == "\n":
            self.line_number += 1
        
        return state, token

    def _handle_in_identifier_state(self, next_char: str):
        """
        Handles the lexer state when processing an identifier.
        This method determines the next state and token based on the current 
        character (`next_char`) and the current token being built. It processes 
        alphanumeric characters and underscores as part of an identifier, and 
        emits tokens for identifiers or keywords when appropriate.
        Args:
            next_char (str): The next character to process in the input stream.
        Returns:
            tuple: A tuple containing:
                - state (str): The next state of the lexer.
                - token (str): The updated token or the emitted token value.
        Behavior:
            - If `next_char` is alphanumeric or an underscore, it appends it to 
              the current token and remains in the "IN_IDENTIFIER" state.
            - If the current token matches a keyword (e.g., "if", "else", "while"), 
              it emits a keyword token and transitions to the start state.
            - Otherwise, it emits an identifier token and transitions to the start state.
            - If `next_char` is a newline character, it increments the line number.
        """

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

    def _handle_in_operator_state(self, next_char: str):
        """
        Handles the lexer state when processing an operator token.
        This method is responsible for determining the next state and token
        when the lexer is in the "OPERATOR" state and encounters the next character.
        It handles cases such as single-character operators, compound operators,
        and transitions to comments.
        Args:
            next_char (str): The next character to process.
        Returns:
            tuple: A tuple containing:
                - state (str): The next state of the lexer.
                - token (str): The token generated during this transition.
        Behavior:
            - If the current token is "/" and the next character is "/", the lexer
              transitions to the "IN_COMMENT" state.
            - If the current token is "=" and the next character is not "=", the lexer
              generates an "ASSIGN" token and transitions to the start state.
            - If the next character is "=", it appends "=" to the current token to form
              a compound operator and generates an "OPERATOR" token.
            - If the next character is a newline ("\n"), the line number is incremented.
        """

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
        
    def _handle_in_comment_state(self, next_char: str):
        """
        Handles the lexer state when inside a comment.
        This method processes characters while the lexer is in the COMMENT state.
        It skips over all characters until a newline is encountered, effectively
        ignoring the content of the comment. The method also updates the line
        number and index to reflect the position after the comment.
        Args:
            next_char (str): The next character to process.
        Returns:
            tuple: A tuple containing the next state ("START") and an empty string,
                   indicating the end of the comment handling.
        """

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
    