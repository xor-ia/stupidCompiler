import os
import lelexer as lexer
import leparser as parser
from letoken import TokenType, Token

src = "example1.xr"
src = open(src, "r").read()

lexed = lexer.Lexer(src)
parsed = parser.Parser(lexed)
parsed.program()
	

#parsed = parser.parse()