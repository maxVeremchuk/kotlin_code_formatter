from formatter import formatter
if __name__ == '__main__':
	fmt = formatter.Formatter("test.kt")
	fmt.format_file()

	print(fmt.print_finished_content())