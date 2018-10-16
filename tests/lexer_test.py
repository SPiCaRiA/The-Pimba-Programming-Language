from __future__ import absolute_import
from lexer import Lexer
from pimba_token import Token


def lexer_test(characters):
    lexer = Lexer(characters)
    token = lexer.read()
    while token != Token.EOF:
        print "=> " + token.get_text()
        token = lexer.read()

if __name__ == "__main__":
    test_characters = """even = 0
odd = 0
i = 1
while i < 10 {
    if i % 2 == 0 {              // even number?
        even = even + i
    } else {
        odd = odd + i
    }
    i = i + 1
}
even + odd"""
    lexer_test(test_characters)
