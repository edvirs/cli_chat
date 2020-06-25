import os ,socket ,sys ,time ,functions ,threading ,rsa ,config_c
from colored import fg ,attr


res_C = attr('reset')
main_C = fg('#FFD7AF')
green_C = fg('#00CD00')
blue_C = fg('#00FFFF')
server_connection = False
current_OS = config_c.current_OS
server_ip = config_c.server_ip
server_port = int(config_c.server_port)
nickname = str(sys.argv[1])

if len(nickname) > 10:
	print(fg('red') + 'Nickname is too long' + res_C)
	sys.exit()

teminal_clear = functions.OS_definition(current_OS)
if teminal_clear == 'error':
	print(fg('red') + 'Correct config usage: current_OS = (win/linux)' + res_C)
	sys.exit()

def if_error():
	global server_connection
	if server_connection == True:
		sock.send(rsa.encrypt('!exit'.encode('utf-8') ,server_pubkey))
	time.sleep(0.05)
	sock.close()
	os.system(teminal_clear)
	print(fg('red') + '\n\nClient closed\n\n' + res_C)

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
				'''.format(green = green_C , res = res_C ))
				break
			elif len(data) > 200:
				print(fg('red') + 'Message is too long' + main_C)
				break
			elif data == '' or data == ' ' or data == '  ' or data == '!server_shutdown':
				break
			sock.send(rsa.encrypt(data.encode('utf-8') , server_pubkey))

def receiving():
	global server_connection
	while True:
		data = sock.recv(2048)
		data = (rsa.decrypt(data ,my_privkey)).decode('utf-8')
		if data == '!server_shutdown':
			os.system(teminal_clear)
			print(fg('red') + '\n\nServer has closed\n\n' + res_C)
			server_connection = False
			sock.close()
			break
		print(data + main_C)
	sys.exit()

os.system(teminal_clear)
print(green_C + 'loading ...' + res_C)

my_pubkey, my_privkey = rsa.newkeys(2048)
print('[Keys generated]')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	sock.connect((server_ip, server_port))
	server_pubkey_n = sock.recv(2048).decode('utf-8')
	server_pubkey_e = sock.recv(2048).decode('utf-8')
	server_pubkey = rsa.PublicKey(int(server_pubkey_n) , int(server_pubkey_e))
	sock.send(rsa.encrypt(nickname.encode('utf-8') , server_pubkey))
	time.sleep(2)
	sock.send(str(my_pubkey.n).encode('utf-8'))
	time.sleep(2)
	sock.send(str(my_pubkey.e).encode('utf-8'))
except:
	if_error()
	print(fg('red') + 'Failure connection to the server' + res_C)
	sys.exit()
else:
	os.system(teminal_clear)
	server_connection = True
	print('[Successful connection to the server]')

trans = threading.Thread(target = transmission)
rece = threading.Thread(target=receiving)

if __name__ == '__main__':
	try:
		trans.setDaemon(True)
		rece.setDaemon(True)
		print('[Client started]')
		rece.start()
		trans.start()
		rece.join()
		trans.join()
	except KeyboardInterrupt:
		if_error()
		sys.exit()
	except:
		if_error()
		sys.exit()
