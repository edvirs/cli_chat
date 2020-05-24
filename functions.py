def OS_definition(current_OS):
	if current_OS == 'linux':
		return('clear')
	elif current_OS == 'win':
		return('cls')
	else:
		return('error')
