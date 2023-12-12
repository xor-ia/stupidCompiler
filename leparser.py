from letoken import Token, TokenType
from lelexer import Lexer

class ParsingError(Exception):
	def __init__(self, msg):
		super().__init__(self, msg)
		
class Parser:
	def __init__(self, lexed):
		self.lex = lexed
		self.token = None
		self.ahead = None
		self.next()
		self.next()
	def next(self):
		self.token = self.ahead
		self.ahead = self.lex.nextToken()
	def checkToken(self, ttype):
		return self.token.type == ttype
	def checkAhead(self, ttype):
		return self.ahead.type == ttype
	def program(self):
		while self.checkToken(TokenType.newline):
			self.next()
		while not self.checkToken(TokenType.EOF):
			self.statement()
			self.next()
	def assertT(self, ttype, ermsg = "Unknown error"):
		assert self.checkToken(ttype), ParsingError(ermsg)
		#self.next()
	def assertMul(self, ermsg, *args):
		assert self.token.type in set(*args), ParsingError(ermsg)
	def statement(self):
		#print(self.token.type, self.token.text)
		if self.checkToken(TokenType.LET):
			print("variable declaration :")
		
			self.next()
			self.assertT(TokenType.iden, "Expected identifier")
			print("named :", self.token.text)
			self.next()
			if self.checkToken(TokenType.AS):
				self.next()
				print(" type annotation :")
				self.assertMul("Invalid datatype", [TokenType.I32, TokenType.I64, TokenType.I8, TokenType.U8, TokenType.U32, TokenType.U64, TokenType.F32, TokenType.F64, TokenType.STR, TokenType.BIN])
				print("  datatype =", self.token.type.name)
				self.next()
			if self.checkToken(TokenType.ALWAYS):
				print(" Is constant!")
				self.next()
				# nothing this is a constant
			if self.checkToken(TokenType.SET):
				self.next()
				# this is an expression or value
				if self.token.type in {TokenType.number, TokenType.str}:
					# this is a value
					pass
			#self.assertT(TokenType.FR, "EOL not found")
