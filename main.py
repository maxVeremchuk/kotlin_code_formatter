from formatter import formatter
from formatter import analyzer
import os
if __name__ == '__main__':
	indent_list = list()
	long_line_list = list()
	with open("config.txt") as config:
		for line in config:
			indent, long_line = line.split(" ")
			indent_list.append(indent)
			long_line_list.append(long_line)
	for i, indent in enumerate(indent_list):
		print(str(i) + " --------------------")
		print("indent_const: " + indent)
		print("long_line_const: " + long_line_list[i])
	print("Enter number of fromatting: ")
	num = int(input())	
	print("Enter file path: ")
	path = input()
	analyzer = analyzer.Analyzer(path)
	if analyzer.analyze():
		#fmt = formatter.Formatter(path, indent_list[1], long_line_list[1])
		fmt = formatter.Formatter(path, indent_list[num], long_line_list[num])
		fmt.format_file()
		with open(os.path.join(os.path.dirname(path), "output.kt").strip(), "w") as formatted_file:
			formatted_file.write(fmt.get_formatted_text())
			print(fmt.print_finished_content())