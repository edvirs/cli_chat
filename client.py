import os, socket, sys, time, functions, threading, rsa, json
from colored import fg, attr


def if_error():
	global server_connection
	if server_connection:
		sock.send(rsa.encrypt('!exit'.encode('utf-8'), server_pubkey))
		time.sleep(0.1)
		sock.close()
		os.system(terminal_clear)
		print(fg('red') + '\n\nClient closed\n\n' + res_C)
	time.sleep(0.1)
	sock.close()

def transmission():
	exit = False
	while not exit:
		while True:
			data = input(main_C)
			if data == '!exit':
				if_error()
				exit = True
				break
			elif data == '!help':
				print('''
{green}!help{res} - Display this menu
{green}!aou{res} - Amount of users online
{green}!lou{res} - List of users online
{green}!exit{res} - Exit from the chat
				'''.format(green=green_C, res=res_C))
				break
			elif len(data) > 200:
				print(fg('red') + 'Message is too long' + main_C)
				break
			elif data == '' or data == ' ' or data == '  ' or data == '!server_shutdown':
				break
			sock.send(rsa.encrypt(data.encode('utf-8'), server_pubkey))


def receiving():
	global server_connection
	while True:
		data = sock.recv(2048)
		data = (rsa.decrypt(data, my_privkey)).decode('utf-8')
		if data == '!server_shutdown':
			os.system(terminal_clear)
			print(fg('red') + '\n\nServer has closed\n\n' + '\n\nPress Ctrl+C to exit\n\n' + res_C)
			server_connection = False
			sock.close()
			break
		print(data + main_C)
	sys.exit()


def main():
	global sock, nickname, server_connection, terminal_clear, server_pubkey_e, server_pubkey_n, server_pubkey, my_pubkey, my_privkey, res_C, main_C, green_C, blue_C

	res_C = attr('reset')
	main_C = fg('#FFD7AF')
	green_C = fg('#00CD00')
	blue_C = fg('#00FFFF')
	server_connection = False
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		with open('c_config.json', 'r') as config:
			config_data = json.load(config)
	except:
		print(fg('red') + 'Failed import json config' + res_C)
		sys.exit()

	current_OS = config_data['current_OS']
	server_ip = config_data['server_ip']
	server_port = int(config_data['server_port'])

	try:
		nickname = str(sys.argv[1])
	except:
		print(fg('red') + 'Please enter username as a launch argument' + res_C)
		sys.exit()

	if len(nickname) > 10:
		print(fg('red') + 'Nickname is too long' + res_C)
		sys.exit()

	terminal_clear = functions.OS_definition(current_OS)
	if terminal_clear == 'error':
		print(fg('red') + 'Correct config usage: current_OS = (win/linux)' + res_C)
		sys.exit()

	os.system(terminal_clear)
	print(green_C + 'loading ...' + res_C)

	my_pubkey, my_privkey = rsa.newkeys(2048)
	print('[Keys generated]')

	try:
		sock.connect((server_ip, server_port))
		server_pubkey_n = sock.recv(2048).decode('utf-8')
		server_pubkey_e = sock.recv(2048).decode('utf-8')
		server_pubkey = rsa.PublicKey(int(server_pubkey_n), int(server_pubkey_e))
		sock.send(rsa.encrypt(nickname.encode('utf-8'), server_pubkey))
		time.sleep(int(config_data['keys_exchanging_delay'])/2)
		sock.send(str(my_pubkey.n).encode('utf-8'))
		time.sleep(int(config_data['keys_exchanging_delay'])/2)
		sock.send(str(my_pubkey.e).encode('utf-8'))
	except:
		if_error()
		os.system(terminal_clear)
		print(fg('red') + '\n\nFailed connection to the server\n\n' + res_C)
		sys.exit()
	else:
		os.system(terminal_clear)
		server_connection = True
		print('[Successful connection to the server]')

	transmission_thread = threading.Thread(target=transmission)
	receiving_thread = threading.Thread(target=receiving)

	transmission_thread.setDaemon(True)
	receiving_thread.setDaemon(True)

	print('[Client started]')

	transmission_thread.start()
	receiving_thread.start()

	transmission_thread.join()


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		if_error()
		sys.exit()
	except:
		if_error()
		sys.exit()
