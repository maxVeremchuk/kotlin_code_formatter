from formatter import formatter
from formatter import analyzer
import os
import sys, getopt

def main(argv):
	file = ''
	configfile = ''
	try:
		opts, args = getopt.getopt(argv,"hf:c:",["ifile=","cfile="])
	except getopt.GetoptError:
		print('main.py -f <file> -c <configfile>(just basename without path)')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('main.py -f <file> -c <configfile>(just basename without path)')
			sys.exit()
		elif opt in ("-f", "--ifile"):
			file = arg
		elif opt in ("-c", "--cfile"):
			configfile = arg
	return file, configfile
if __name__ == '__main__':
	file, configfile = main(sys.argv[1:])
	
	analyzer = analyzer.Analyzer(file)
	if analyzer.analyze():
		#fmt = formatter.Formatter(path, indent_list[1], long_line_list[1])
		fmt = formatter.Formatter(file, configfile)
		fmt.format_file()
		with open(os.path.join(os.path.dirname(file), "output.kt").strip(), "w") as formatted_file:
			formatted_file.write(fmt.get_formatted_text())
			fmt.print_finished_content()