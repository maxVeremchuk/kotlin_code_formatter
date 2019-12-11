import re

class Analyzer:
	init_content = list()
	bracket_stack = []
	open_list = ["[","{","("] 
	close_list = ["]","}",")"] 
	last_bracket = []

	def __init__(self, filename):
		with open(filename, "r") as file:
			self.init_content = file.readlines()

	def analyze(self):
		temp_init_content = "`".join(self.init_content)

		finded_multiline = re.findall(r'"""([^"]*)"""', temp_init_content)
		if finded_multiline is not None:
			for multiline in finded_multiline:
				rep_mult = multiline.replace("{", "~").replace("}", "~").replace("{", "~").replace("(", "~")\
				.replace("}", "~").replace("[", "~").replace("]", "~")
				temp_init_content = temp_init_content.replace(multiline, rep_mult, 1)
		finded_multiline = re.findall(r'"([^"]*)"', temp_init_content)
		if finded_multiline is not None:
			for multiline in finded_multiline:
				rep_mult = multiline.replace("{", "~").replace("}", "~").replace("{", "~").replace("(", "~")\
				.replace("}", "~").replace("[", "~").replace("]", "~")
				temp_init_content = temp_init_content.replace(multiline, rep_mult, 1)

		finded_multiline = re.findall("/\\*.*?\\*/", temp_init_content)
		if finded_multiline is not None:
			for multiline in finded_multiline:
				rep_mult = multiline.replace("{", "~").replace("}", "~").replace("{", "~").replace("(", "~")\
				.replace("}", "~").replace("[", "~").replace("]", "~")
				temp_init_content = temp_init_content.replace(multiline, rep_mult, 1)

		finded_multiline = re.findall("//.*$", temp_init_content)
		if finded_multiline is not None:
			for multiline in finded_multiline:
				rep_mult = multiline.replace("{", "~").replace("}", "~").replace("{", "~").replace("(", "~")\
				.replace("}", "~").replace("[", "~").replace("]", "~")
				temp_init_content = temp_init_content.replace(multiline, rep_mult, 1)
		print(temp_init_content)
		temp_init_content = temp_init_content.split("`")

		for i, line in enumerate(temp_init_content):
			for j, letter in enumerate(line):
				if letter in self.open_list:
					self.last_bracket.clear()
					self.bracket_stack.append(letter)
					self.last_bracket.append(i)
					self.last_bracket.append(j)
				elif letter in self.close_list:
					pos = self.close_list.index(letter)
					if ((len(self.bracket_stack) > 0) and (self.open_list[pos] == self.bracket_stack[-1])): 
						self.bracket_stack.pop()
					else:
						print("Error in line {}, {}; Wrong bracket".format(i + 1, j + 1))
						print(line.rstrip())
						print("~" * (j) + '^')
						return False
		if len(self.bracket_stack) > 0:
			print("Error in line {}, {}; No closing bracket".format(self.last_bracket[0] + 1, self.last_bracket[1] + 1))
			print(self.init_content[self.last_bracket[0]].rstrip())
			print("~" * (self.last_bracket[1]) + '^')
			return False
		return True



