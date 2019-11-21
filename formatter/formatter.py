import re

class Formatter:

	init_content = list()
	finished_content = list()
	one_line_left_brace_hendler_list = list()
	one_line_right_brace_hendler_list = list()
	iter_input = iter("")
	is_multiline_comment = False
	indent_const = "    "	#config
	max_line_length_const = 60 #config
	space_positions = list()
	multi_strings = list()
	strings = list()
	strings_indent = list()

	def __init__(self, filename, indent_const, max_line_length_const):
		with open(filename, "r") as file:
			self.init_content = file.readlines()
			


	def next_input(self):
		for line in self.init_content:
			yield line

	def left_curly_brace_handler(self, line):
		lines = line.split('{')
		last = lines[-1].rstrip()
		del lines[-1]
		for brace_lines in lines:
			self.one_line_left_brace_hendler_list.append(brace_lines.strip() + " {")
		self.one_line_left_brace_hendler_list.append(last)


	def handle_multiline_comment(self, line):
		line.replace(' *', '*')
		line.replace('* ', '*')
		if not self.is_multiline_comment and "/**" in line:
			self.is_multiline_comment = True
			print("inside", self.is_multiline_comment)
			#line = line.strip()
			return line#.replace("/ * *", "/**")
		else:
			if '*/' in line:
				self.is_multiline_comment = False
			else:
				line = line.replace('*','* ')
				#line = line.replace("* /", "*/").strip()
				#self.space_positions.append(len(self.finished_content))
				#line.replace('* ', '*')
				#line.replace('*', '* ')	
			# elif line.startswith("*"):
			# 	line = "~~~space_in_start~~~" + line	
			return line	
		

	def right_curly_brace_handler(self, line):
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

			if len(line) > self.max_line_length_const and not line.startswith("~"):
				fixed_list.extend(self.handle_long_line(line, identation))
			else:	
				if line.startswith("*"):
					fixed_list.append(identation * self.indent_const + " " + line.strip())
				else:
					if "~~~formatter_multi_string~~~" in line:
						self.strings_indent.append(identation)
					fixed_list.append(identation * self.indent_const + line.strip())

			if '{' in line:
				identation += 1
			
		return fixed_list


	def handle_long_line(self, line, identation):

		finished_list = list()
		if line.strip().startswith("import"):
			finished_list.append(line)
			return finished_list
		if len(line) < self.max_line_length_const:
			finished_list.append((self.indent_const * identation + line))
			return finished_list
		
		if "class" in line and ") :" in line:
			der, base = line.split(") :")
			finished_list.extend(self.split_by_comma(der, identation + 1))
			base = ") :" + base
			#finished_list.extend(self.split_by_comma(base, identation + 1))
			#finished_list.extend(self.handle_long_line(base, identation))
			finded_braces = re.findall(r'\([^\)]+\)', base)
			if finded_braces is not None:
				for generics in finded_braces:
					old_generics = generics
					if ',' in generics:
						generics = generics.replace(',', '`')
						base = base.replace(old_generics, generics)
			temp_list = self.split_by_comma_last(base, identation + 1)
			finished_list.extend(item.replace('`', ',') for item in temp_list)

		elif "class" in line:
			der, base = line.split(":")
			der = der + ":"
			finished_list.extend(self.split_by_comma_last(der, identation))
			finished_list.extend(self.split_by_comma_last(base, identation + 1))
		elif "if (" in line or "when (" in line:
			temp_list = list()
			split_by_or_op = line.split("||")
			for item_or in split_by_or_op:
				split_by_and_op = item_or.split("&&")
				for item_and in split_by_and_op:
					temp_list.append(self.indent_const * (identation + 1) + item_and.strip() + " &&")
				temp_list[-1] = temp_list[-1].replace("&&", "||")
			temp_list[0] = temp_list[0].strip()
			last = temp_list[-1].replace("||", "")
			rightest_brace_idnex = last.rfind(')')
			temp_list[-1] = last[:rightest_brace_idnex]
			temp_list.append(last[rightest_brace_idnex:])
			finished_list.extend(temp_list)
		elif (" val " in line or " var " in line) and "=" in line:
			bef_equal, after_equal = line.split('=', 1)
			finished_list.append(bef_equal + '=')
			finished_list.extend(self.handle_long_line(after_equal.strip(), identation + 1))
		elif "." in line:
			finished_list.extend(self.split_by_dot(line, identation + 1))
		elif "," in line:
			finished_list.extend(self.split_by_comma(der, identation + 1))
		elif "->" in line:
			bef_sign, after_sign = line.split('->', 1)
			finished_list.append(bef_sign + '->')
			finished_list.extend(self.handle_long_line(after_sign.strip(), identation + 1))
		else:
			finished_list.append(line)
		return finished_list

	def split_by_dot(self, line, identation):
		finished_list = list()
		sep_by_dot = line.split('.')
		finished_list.append(self.indent_const * identation + sep_by_dot[0].strip())
		for i, dot_item in enumerate(sep_by_dot):
			if i == 0:
				continue
			if len(sep_by_dot[i - 1]) > 0 and sep_by_dot[i - 1][-1] == "?":
				finished_list[-1] = finished_list[-1][:-1]
				finished_list.append(self.indent_const * identation + "?." + dot_item.strip())
			elif len(dot_item) > 0:
				finished_list.append(self.indent_const * identation + "." + dot_item.strip())
		return finished_list

	def split_by_comma(self, line, identation):
		finished_list = list()
		sep_by_comma = line.split(',')
		first = sep_by_comma[0].strip()
		del sep_by_comma[0]
		rightest_brace_idnex = first.rfind('(')
		finished_list.append(first[:rightest_brace_idnex + 1])
		if len(sep_by_comma) > 0:
			finished_list.append(self.indent_const * identation + first[rightest_brace_idnex + 1:].strip() + ',')
		else:
			finished_list.append(self.indent_const * identation + first[rightest_brace_idnex + 1:].strip())
		for comma_item in sep_by_comma:
			finished_list.append(self.indent_const * identation + comma_item.strip() + ',')
		return finished_list

	def split_by_comma_last(self, line, identation):
		finished_list = list()
		sep_by_comma = line.split(',')
		last = sep_by_comma[-1].strip()
		del sep_by_comma[-1]
		for comma_item in sep_by_comma:
			finished_list.append(self.indent_const * identation + comma_item.strip() + ',')
		finished_list.append(self.indent_const * identation + last.strip())	
		return finished_list

	def handle_space_constructs(self, line):
		line = line.replace(r'=', r' = ')
		line = line.replace(r'>', r' > ')
		line = line.replace(r'<', r' < ')
		line = line.replace(r':', r' : ')
		line = line.replace(r'+', r' + ')
		line = line.replace(r'-', r' - ')
		line = line.replace(r'*', r' * ')
		line = line.replace(r'/', r' / ')
		return line

	def handle_spaces(self, line):
		while re.search(r'\s\)', line) is not None:
			line = line.replace(' )',')')
		while re.search(r'\(\s', line) is not None:
			line = line.replace('( ','(')
		while re.search(r'\s\]', line) is not None:
			line = line.replace(' ]',']')
		while re.search(r'\[\s', line) is not None:
			line = line.replace('[ ','[')
		line = line.replace('{', ' {')
		if r'\\ ' not in line: 
			line = line.replace(r'\\',r'\\ ')
		line = line.replace(r'= =',r'==')
		line = line.replace(r'! =',r'!=')
		line = line.replace(r'> =',r'>=')
		line = line.replace(r'< =',r'<=')
		line = line.replace(r'? .',r'?.')
		line = line.replace(r'>:', r'> :')
		line = line.replace(r'):', r') :')
		line = line.replace(r': :', r'::')
		line = line.replace(r'object:', r'object :')
		line = line.replace(r'- >', r'->')
		line = line.replace(r' ?', r'?')
		line = line.replace(r'. ', r'.')
		line = line.replace(r' .', r'.')
		line = line.replace(r'/ * *', r'/**')
		line = line.replace(r'* /', r'*/')
		return line

	def handle_colon(self, line):
		finded_braces = re.findall(r'\([^\)]+\)', line)
		if finded_braces is not None:
			for generics in finded_braces:
				old_generics = generics
				if ':' in generics:
					generics = generics.replace(' :', ':')
					line = line.replace(old_generics, generics)

		finded_braces = re.findall(r'val\s.*:', line)
		finded_braces += re.findall(r'var\s.*:', line)
		if finded_braces is not None:
			for generics in finded_braces:
				old_generics = generics
				if ':' in generics:
					generics = generics.replace(' :', ':')
					line = line.replace(old_generics, generics)
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

	def handle_while(self, line):
		while re.search(r'^\swhile', line) is not None:
			line = line.replace('while', ' while')
		while re.search(r'while\(', line) is not None:
			line = line.replace('while(', 'while (')
		return line

	def handle_when(self, line):
		while re.search(r'^\swhen', line) is not None:
			line = line.replace('when', ' when')
		while re.search(r'when\(', line) is not None:
			line = line.replace('when(', 'when (')
		return line

	def handle_generics(self, line):
		finded_generics = re.findall(r'<[^>]+>', line)
		if finded_generics is not None:
			for generics in finded_generics:
				old_generics = generics	
				if '||' not in generics and '&&' not in generics:
					generics = generics.replace('< ', '<')
					generics = generics.replace(' >', '>')
					line = line.replace(old_generics, generics)
					line = line.replace(' ' + generics, generics)
					line = line.replace(generics + ' ', generics) 
		return line

	def pre_handle_string(self):
		temp_init_content = "`".join(self.init_content)
		finded_multiline = re.findall(r'"""([^"]*)"""', temp_init_content)
		if finded_multiline is not None:
			for multiline in finded_multiline:
				self.multi_strings.append(multiline)
				temp_init_content = temp_init_content.replace("\"\"\"" + multiline  + "\"\"\"", "~~~formatter_multi_string~~~", 1)

		finded_line = re.findall(r'"([^"]*)"', temp_init_content)
		if finded_line is not None:
			for line in finded_line:
				self.strings.append(line)
				temp_init_content = temp_init_content.replace("\"" + line  + "\"", "~~~formatter_string~~~", 1)
		self.init_content = temp_init_content.split("`")

	def post_handle_string(self):
		temp_init_content = "`".join(self.finished_content)

		for i, indent in enumerate(self.strings_indent):
			res_str = "\"\"\""
			skip_first = 0
			for multiline in self.multi_strings[i].split('`'):
				res_str += indent * self.indent_const * skip_first + multiline + "\n"
				skip_first = 1
			res_str = res_str[:-1]
			res_str += "\"\"\""
			temp_init_content = temp_init_content.replace("~~~formatter_multi_string~~~", res_str, 1)
		for str in self.strings:
			temp_init_content = temp_init_content.replace("~~~formatter_string~~~", "\"" + str + "\"", 1)
		self.finished_content = temp_init_content.split("`")

	def format_file(self):
		for i, line in enumerate(self.init_content):
			self.init_content[i] = line.strip()
		self.pre_handle_string()
		#self.iter_input = iter(self.next_input())
		for line in self.init_content:

			#line = self.handle_space_constructs(line)
			line = ' '.join(line.split())
			#line = self.handle_spaces(line)

			line = self.handle_multiline_comment(line)
			if not self.is_multiline_comment:
				line = self.handle_space_constructs(line)
			
				line = ' '.join(line.split())

				line = self.handle_if(line)
				line = self.handle_for(line)
				line = self.handle_colon(line)
				line = self.handle_generics(line)
				line = self.handle_spaces(line)
			
				self.one_line_left_brace_hendler_list = list()
				self.one_line_right_brace_hendler_list = list()
				self.left_curly_brace_handler(line)
				for line_brace in self.one_line_left_brace_hendler_list:
					self.right_curly_brace_handler(line_brace)
				self.finished_content.extend(self.one_line_right_brace_hendler_list)
			else:
				self.finished_content.append(line)
		self.finished_content = self.handle_indentations(self.finished_content)
		self.post_handle_string()

	def print_finished_content(self):
		for line in self.finished_content:
			print(line)
