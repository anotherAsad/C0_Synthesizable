#! /usr/bin/python

# INST_TYPE | 00->JMP, 01->MOV, 10->CMP, 11->MATH
# ALU_CODE  | 0000->ADD, X001->XOR, X010->AND, 0011->OR, 1011->NOR, X100->SHL, X101->SHR, X110->ROL, X111->ROR, 1000->SUB
type_op = {
	"MOV"	: ("01", "0000", 3),
# COMPARISON
	"CMP"	: ("10", "1000", 3),
# JUMPS
	"JMP"	: ("00", "0111", 2),

	"JC"	: ("00", "1000", 2),
	"JAE"	: ("00", "1000", 2),
	"JNB"	: ("00", "1000", 2),
	"JNC"	: ("00", "0000", 2),
	"JNAE"	: ("00", "0000", 2),
	"JB"	: ("00", "0000", 2),

	"JO"	: ("00", "1001", 2),
	"JNO"	: ("00", "0001", 2),
	
	"JS"	: ("00", "1010", 2),
	"JL"	: ("00", "1010", 2),
	"JNGE"	: ("00", "1010", 2),
	"JNS"	: ("00", "0010", 2),
	"JNL"	: ("00", "0010", 2),
	"JGE"	: ("00", "0010", 2),

	"JZ"	: ("00", "1011", 2),
	"JE"	: ("00", "1011", 2),
	"JNZ"	: ("00", "0011", 2),
	"JNE"	: ("00", "0011", 2),

	"JA"	: ("00", "1100", 2),
	"JNBE"	: ("00", "1100", 2),
	"JNA"	: ("00", "0100", 2),
	"JBE"	: ("00", "0100", 2),
	
	"JLE"	: ("00", "1101", 2),
	"JNG"	: ("00", "1101", 2),
	"JNLE"	: ("00", "0101", 2),
	"JG"	: ("00", "0101", 2),
# MATH
	"ADD"	: ("11", "0000", 4),
	"XOR"	: ("11", "0001", 4),
	"NOT"	: ("11", "0001", 3),
	"AND"	: ("11", "0010", 4),
	"OR"	: ("11", "0011", 4),
	"NOR"	: ("11", "1011", 4),
	"SHL"	: ("11", "0100", 3),
	"SHR"	: ("11", "0101", 3),
	"ROL"	: ("11", "0110", 3),
	"ROR"	: ("11", "0111", 3),
	}

reg = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "R7": "111"}

def decToBin(num):
	string = ""
	while num != 0:
		string = str(num & 1)+string
		num = num >> 1
	string = (8-len(string))*"0" + string
	return string

def assemble(string):
	string = string.replace(",", "")
	tokenized = string.split()
	instr = "21'b"
	# NOP
	if tokenized[0] == "NOP":
		return "21'b110001000000000000000"
	if len(tokenized) != type_op[tokenized[0]][2]:
		return "err"
	else:
		# Instruction Type
		instr += type_op[tokenized[0]][0]
		# I/R
		if tokenized[-1][0] == '#':
			instr += '1'
		else:
			instr += '0'
		# OPCODE
		instr += type_op[tokenized[0]][1]
		# TARGET REG
		if type_op[tokenized[0]][0][1] == '1':		# instr is move or math type
			instr += reg[tokenized[1]]
		else:
			instr += "000"
		# AMUX
		if type_op[tokenized[0]][0] == "00":		# instr is jump type
			instr += "000"
		elif type_op[tokenized[0]][0] == "11":		# instr is math type
			instr += reg[tokenized[2]]
		elif type_op[tokenized[0]][0] == "01":		# instr is move type
			if instr[6] == '1':
				instr += "000"						# instr is move with immed. Does not need AMUX arg
			else:
				instr += reg[tokenized[2]]
		else:										
			instr += reg[tokenized[1]]				# instr is comp type
		# BMUX and IMMED
		if tokenized[0] == "NOT":
			instr += "11111111"
		elif instr[6] != '1':
			instr += reg[tokenized[-1]]
			instr += "00000"
		else:
			instr += decToBin(int(tokenized[-1][1:]))
		# DONE
		return instr
