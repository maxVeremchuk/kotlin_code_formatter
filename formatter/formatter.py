import re
from . import regex_consts

class Formatter:

	init_content = list()
	finished_content = list()
	one_line_left_brace_hendler_list = list()
	one_line_right_brace_hendler_list = list()
	iter_input = iter("")
	current_line = ""
	formatted_line = ""
	shift_line = ""
	indent = 0
	indent_const = "    "	#config

	def __init__(self, filename):
		#config
		f = open(filename, "r")
		self.init_content = f.readlines()

	def next_input(self):
		for line in self.init_content:
			yield line

	def left_curly_brace_handler(self, line):
		# left_brace = re.search(r'{', line)
		# if left_brace is not None:
		# 	line_with_brace = line[:left_brace.start() + 1].strip()
		# 	other_line = line[left_brace.start() + 1:]
		# 	line_with_brace = self.handle_if(line_with_brace)
		# 	other_line = self.handle_if(other_line)
		# 	self.one_line_left_brace_hendler_list.append(line_with_brace)
		# 	self.indent += 1
		# 	self.left_curly_brace_handler(other_line)
		# else:
		# 	self.one_line_left_brace_hendler_list.append(self.handle_if(line))
			# current_line += line_with_brace
			# finished_content.append(current_line)
			# current_line = ""
		lines = line.split('{')
		last = lines[-1].rstrip()
		del lines[-1]
		for brace_lines in lines:
			self.one_line_left_brace_hendler_list.append(brace_lines + "{")
		self.one_line_left_brace_hendler_list.append(last)


	def right_curly_brace_handler(self, line):
		# right_brace = re.search(r'}', line)
		# if right_brace is not None:
		# 	if right_brace.start() == 0:
		# 		line_without_brace = line[:right_brace.start() + 1].strip()
		# 		other_line = line[right_brace.start() + 1:]
		# 		self.indent -= 1
		# 		other_line_search = re.search(r'}', other_line)
		# 		first_brace = 
		# 		end_line = other_line[:other_line_search.start()]
		# 		if re.search(r'}', other_line) is None:
		# 			self.one_line_right_brace_hendler_list.append(self.indent * self.indent_const + line)
		# 		else:
		# 			self.one_line_right_brace_hendler_list.append(self.indent * self.indent_const + line)
		# 			self.right_curly_brace_handler(end_line)
		# 	else:
		# 		line_without_brace = line[:right_brace.start()].strip()
		# 		other_line = line[right_brace.start():]
		# 	self.one_line_right_brace_hendler_list.append(self.indent * self.indent_const + line_without_brace)
		# 	if line_without_brace == "":
		# 		self.indent -= 1
		# 	self.right_curly_brace_handler(other_line)
		# else:
		# 	self.one_line_right_brace_hendler_list.append(self.indent * self.indent_const + line)
		# 	self.indent += 1
		lines = line.split('}')
		first = lines[0]
		del lines[0]
		if first != "":
			self.one_line_right_brace_hendler_list.append(first)
		for brace_lines in lines:
			self.one_line_right_brace_hendler_list.append('}' + brace_lines)

	def handle_indentations(self, lines_list):
		identation =  0
		fixed_list = list()
		for line in lines_list:
			if '}' in line:
				identation -= 1

			fixed_list.append(identation * self.indent_const + line)

			if '{' in line:
				identation += 1
			
		return fixed_list

	#def handle_spaces_surrounded(self, line):


	def handle_spaces(self, line):
		while re.search(r'\s\)', line) is not None:
			line = line.replace(' )',')')
		while re.search(r'\(\s', line) is not None:
			line = line.replace('( ','(')
		while re.search(r'\s\]', line) is not None:
			line = line.replace(' ]',']')
		while re.search(r'\[\s', line) is not None:
			line = line.replace('[ ','[')
		
		return line

	def handle_for(self, line):
		while re.search(r'^\sfor', line) is not None:
			line = line.replace('for', ' for')
		while re.search(r'for\(', line) is not None:
			line = line.replace('for(', 'for (')
		return line

	def handle_if(self, line):
		while re.search(r'^\sif', line) is not None:
			line = line.replace('if', ' if')
		while re.search(r'if\(', line) is not None:
			line = line.replace('if(', 'if (')
		return line

	def format_file(self):
		self.iter_input = iter(self.next_input())
		for line in self.iter_input:
			line = ' '.join(line.split())

			line = self.handle_if(line)
			line = self.handle_for(line)
			line = self.handle_spaces(line)

			self.one_line_left_brace_hendler_list = list()
			self.one_line_right_brace_hendler_list = list()
			self.left_curly_brace_handler(line)
			for line_brace in self.one_line_left_brace_hendler_list:
				self.right_curly_brace_handler(line_brace)
			self.finished_content.extend(self.one_line_right_brace_hendler_list)
		self.finished_content = self.handle_indentations(self.finished_content)

	def print_finished_content(self):
		for line in self.finished_content:
			print(line)
	# def find_pattern(self, line, pattern):
	# 	search = re.search(pattern, line)
	# 	if search is not None:

	#def find_patterns(self, line):
		#handle patterns for if when ...

	#def analize():
