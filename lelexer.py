from letoken import Token, TokenType, isKeyword

class LexingError(Exception):
	def __init__(self, msg):
		super().__init__(msg)
class Lexer:
	def __init__(self, src):
		self.src = src+"\n"
		self.curChar = ""
		self.curInd = -1
		self.nextChar()
	def nextChar(self):
		self.curInd += 1
		if self.curInd >= len(self.src):
			self.curChar = "\0"
		else:
			self.curChar = self.src[self.curInd]
	def lookAhead(self, n=1):
		return "\0" if self.curInd+n>=len(self.src) else self.src[self.curInd+n]
	def skipWhitespace(self):
		while self.curChar in {" ", "\t", "\r"}:
			self.nextChar()
	def nextToken(self):
		token = None
		self.skipComment()
		self.skipWhitespace()
		if self.curChar == "+":
			token = Token("+", TokenType.ADD)
		elif self.curChar == "-":
			token = Token("-", TokenType.SUB)
		elif self.curChar == "*":
			token = Token("*", TokenType.MUL)
		elif self.curChar == "/" and self.lookAhead() != "/":
			token = Token("/", TokenType.DIV)
		elif self.curChar == "(":
			token = Token(self.curChar, TokenType.PO)
		elif self.curChar == ")":
			token = Token(self.curChar, TokenType.PC)
		elif self.curChar == "[":
			token = Token(self.curChar, TokenType.SO)
		elif self.curChar == "]":
			token = Token(self.curChar, TokenType.SC)
		elif self.curChar == "{":
			token = Token(self.curChar, TokenType.BO)
		elif self.curChar == "}":
			token = Token(self.curChar, TokenType.BC)
		elif self.curChar == "@":
			token = Token(self.curChar, TokenType.REF)
		
		elif self.curChar == "\0":
			token = Token("\0", TokenType.EOF)
		elif self.curChar == "\n":
			token = Token("\0", TokenType.newline)
		elif self.curChar == "=":
			token = Token("=", TokenType.EQ)
		elif self.curChar == ">":
			if self.lookAhead() == "=":
				token = Token(">=", TokenType.GTEQ)
				self.nextChar()
			else:
				token = Token(">", TokenType.GT)
		elif self.curChar == "<":
			if self.lookAhead() == "=":
				token = Token("<=", TokenType.LTEQ)
				self.nextChar()
			else:
				token = Token("<", TokenType.LT)
		elif self.curChar == "!":
			if self.lookAhead()=="=":
				token = Token("!=", TokenType.NOTEQ)
				self.nextChar()
			else:
				token = Token("!", TokenType.NOT)
		elif self.curChar == "b" and self.lookAhead() == "e":
			token = Token("be", TokenType.SET)
			self.nextChar()
		elif self.curChar == "\"":
			self.nextChar()
			st = self.curInd
			while self.curChar != "\"":
				if self.curChar in {"\0"}:
					raise LexingError("String was never closed @{}-EOF".format(st))
				self.nextChar()
			token = Token(self.src[st:self.curInd], TokenType.str)
		elif self.curChar.isdigit():
			st = self.curInd
			while self.lookAhead().isdigit():
				self.nextChar()
			if self.lookAhead() == ".":
				self.nextChar()
				if not self.lookAhead().isdigit():
					raise LexingError("Invalid number @{}-{}".format(st, self.curInd))
				while self.lookAhead().isdigit():
					self.nextChar()
			token = Token(self.src[st:self.curInd+1], TokenType.number)
		elif self.curChar.isalnum():
			st = self.curInd
			while self.lookAhead().isalnum():
				self.nextChar()
			txt = self.src[st:self.curInd+1]
			kwon = isKeyword(txt)
			kwon = TokenType.iden if kwon == None else kwon
			token = Token(txt, kwon)
		else:
			raise LexingError("Unknown token {}".format(self.curChar))
		self.nextChar()
		return token
	def skipComment(self):
		if self.curChar == "/" and self.lookAhead() == "/":
			while self.curChar != "\n":
				self.nextChar()
	def lex(self):
		buffer = []
		self.curChar = ""
		self.curInd = -1
		self.nextChar()
		res = self.nextToken()
		while res.type != TokenType.EOF:
			buffer.append(res)
			res = self.nextToken()
		buffer.append(res)
		return res



"""
kwrds

let      : define variable
be       : = sign
function : declare function
as       : declare variable type
always   : declare const value
while    : while loop
if       : if
else     : else
for      : for loop
return   : return value from function


grammar
 value declaration
  >let varname as TYPE always be expression fr
  - 
 function declaration 

"""

def lex(src):
	src = src.replace("\n", "")
	buffer = ""
	kwrds = set(["let", "be", "function", "as", "fr", "while", "if", "for", "else", "return", "fact", "cap", "num", "str"])
	breaker = set(["(",")",":","{","}", ",","[","]"])
	op = set(["+","-","*","/"])
	ignore = set([" "])
	res = []
	instr = False
	comm = False
	for i in range(len(src)):
		c = src[i]
		if c == "\"":
			instr = not instr
		if (c in breaker|op|ignore) and not instr:
			if buffer in kwrds:
				res.append((buffer, "kwrd"))
			elif len(buffer)!=0:
				res.append((buffer, "id"))
			if c in breaker:
				res.append((c, "spec"))
			elif c in op:
				res.append((c, "op"))
				
			buffer=""
			c=""
		buffer+=c
	return res
