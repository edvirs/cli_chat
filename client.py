import os ,socket ,sys ,time ,functions ,threading
from colored import fg ,attr

res_C = attr('reset')
frame_C = fg('#FFD7AF')
nickname_C = fg('#00CD00')
onl_C = fg('#00FFFF')
argv_error_notification = fg('red') + 'Correct usage: current OS(win/linux) , server ip , server port , nickname' + res_C
server_connection = False

if len(sys.argv) != 5:
	print(argv_error_notification)
	sys.exit()

current_OS = str(sys.argv[1])
server_ip = str(sys.argv[2])
server_port = int(sys.argv[3])
nickname = str(sys.argv[4])

teminal_clear = functions.OS_definition(current_OS)
if teminal_clear == 'error':
	print(argv_error_notification)
	sys.exit()

def if_error():
	if server_connection == True:
		sock.send(b'!exit')
	time.sleep(0.1)
	sock.close()
	os.system(teminal_clear)
	print(fg('red') + '\n\nClient closed\n\n' + res_C)

def transmission():
	exit = False
	while not exit:
		while True:
			data = input(frame_C)
			if data == '!exit':
				if_error()
				exit = True
				break
			elif data == '' or data == ' ' or data == '  ' or data == '!server_shutdown':
				break
			sock.send(data.encode('utf-8'))

def receiving():
	while True:
		data = sock.recv(1024).decode('utf-8')
		if data == '!server_shutdown':
			os.system(teminal_clear)
			print(fg('red') + '\n\nServer was closed\n\n' + res_C)
			server_connection = False
			sock.close()
			sys.exit()
		print(data)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
os.system(teminal_clear)

try:
	sock.connect((server_ip, server_port))
except:
	if_error()
	print(fg('red') + 'Failure connection to the server' + res_C )
	sys.exit()
else:
	server_connection = True
	print('[Successful connection to the server]')

sock.send(nickname.encode('utf-8'))

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
	except KeyboardInterrupt:
		if_error()
		sys.exit()
	except:
		if_error()
		sys.exit()
