import enum
class TokenType(enum.Enum):
	EOF = -1
	newline = 0
	number = 1
	str = 2
	iden = 3
	
	IF = 101 #key words
	ELSE = 102
	LET = 103
	FUNCTION = 104
	AS = 105
	WHILE = 106
	FOR = 107
	RETURN = 108
	ALWAYS = 109 
	FR = 111 

	I32 = 110
	I64 = 112 
	I8 = 113
	U32 = 114
	U64 = 115
	U8 = 116
	F32 = 117
	F64 = 118
	STR = 119
	BIN = 120

	# OPRANDs
	EQ = 201  # =
	SET = 212 # be
	ADD = 202 # + 
	SUB = 203 # -
	MUL = 204 # *
	DIV = 205 # /
	LT = 206 # <
	LTEQ = 207 # <=
	GT = 208 # > 
	GTEQ = 209 # >=
	NOTEQ = 210 # != 
	NOT = 211 # !
	REF = 212 # @
	# PAREN
	PO = 301 # open  paren  (
	PC = 302 # close paren  )
	BO = 303 # open  brace  {
	BC = 304 # close brace  }
	SO = 305 # open  square [
	SC = 306 # close square ]
	# Dtype
	

	
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
"""

class Token:
	def __init__(self, txt, knd):
		self.text = txt
		self.type = knd

def isKeyword(txt):
	for kind in TokenType:
		if kind.name.lower() == txt and kind.value >= 100 and kind.value < 200:
			return kind
	return None