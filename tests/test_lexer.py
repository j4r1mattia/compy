import unittest

from lexer import Lexer as LexerBasic
from lexer_tt import Lexer as LexerTT

class TestLexer(unittest.TestCase):
    def test_lexer(self):

        source_code = """
            x = 5 + 3
            // This is a comment
            if x > 5 {
                y = x - 2
            } else {
                y = 0
            }
            """
        
        expected = [
            ('IDENTIFIER', 'x', 1),
            ('ASSIGN', '=', 1),
            ('NUMBER', '5', 1),
            ('OPERATOR', '+', 1),
            ('NUMBER', '3', 1),
            ('IF', 'if', 3),
            ('IDENTIFIER', 'x', 3),
            ('OPERATOR', '>', 3),
            ('NUMBER', '5', 3),
            ('LBRACE', '{', 3),
            ('IDENTIFIER', 'y', 4),
            ('ASSIGN', '=', 4),
            ('IDENTIFIER', 'x', 4),
            ('OPERATOR', '-', 4),
            ('NUMBER', '2', 4),
            ('RBRACE', '}', 5),
            ('ELSE', 'else', 5),
            ('LBRACE', '{', 5),
            ('IDENTIFIER', 'y', 6),
            ('ASSIGN', '=', 6),
            ('NUMBER', '0', 6),
            ('RBRACE', '}', 7)
        ]

        lexer = LexerBasic(source_code=source_code)
        lexer.tokenize()
        tokens = lexer.tokens
        self.assertEqual(tokens, expected)

        lexer_tt = LexerTT(source_code=source_code)
        lexer_tt.tokenize()
        tokens_tt = lexer_tt.tokens
        self.assertEqual(tokens_tt, expected)