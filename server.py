import os ,socket ,sys ,time ,functions , threading
from colored import fg ,attr

argv_error_notification = fg('red') + 'Correct usage: port, current OS (win/linux)' + attr('reset')

if len(sys.argv) != 3:
	print(argv_error_notification)
	sys.exit()

port = int(sys.argv[1])
current_OS = str(sys.argv[2])
clients = []
res_C = attr('reset')
frame_C = fg('#FFD7AF')
nickname_C = fg('#00CD00')
onl_C = fg('#00FFFF')

teminal_clear = functions.OS_definition(current_OS)
if teminal_clear == 'error':
	print(argv_error_notification)
	sys.exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', port))
sock.listen(5)

def if_error():
	for i in clients:
		i.send(b'!server_shutdown')

	sock.close()
	os.system(teminal_clear)
	print(fg('red') + '\n\nServer closed\n\n' + attr('reset'))
	sys.exit()

def transmission(data, nick, current_client):
	global clients
	data = data.decode('utf-8')
	for i in clients:
		if i != current_client:
			i.send((nickname_C + nick + ': ' + res_C + frame_C + data).encode('utf-8'))

def receiving():
	global clients
	while True:
		client , addr = sock.accept()
		nick = client.recv(1024).decode('utf-8')
		for i in clients:
			i.send((res_C + '[' + nickname_C + str(nick) + res_C + ']' + onl_C + ' →  Join chat' + res_C).encode('utf-8'))
		clients.append(client)
		print('[{addr}] [{nick}] Conected'.format(addr = str(addr) , nick = str(nick)))
		while True:
			data = client.recv(1024)
			if data.decode('utf-8') == '!exit':
				client.close()
				print('[{addr}] [{nick}] Disconected'.format(addr = str(addr) , nick = str(nick)))
				time.sleep(0.1)
				clients.remove(client)
				for i in clients:
					i.send((res_C + '[' + nickname_C + str(nick) + res_C + ']' + onl_C + ' →  Left chat' + res_C).encode('utf-8'))
				break
			print('[{addr}] [{nick}] →  '.format(addr = str(addr) , nick = str(nick)) + data.decode('utf-8'))
			transmission(data, nick, client)

t1 = threading.Thread(target=receiving)
t2 = threading.Thread(target=receiving)
t3 = threading.Thread(target=receiving)
t4 = threading.Thread(target=receiving)
t5 = threading.Thread(target=receiving)

if __name__ == '__main__':
	try:
		t1.setDaemon(True)
		t2.setDaemon(True)
		t3.setDaemon(True)
		t4.setDaemon(True)
		t5.setDaemon(True)
		os.system(teminal_clear)
		print('[Server started]')
		t1.start()
		t2.start()
		t3.start()
		t4.start()
		t5.start()
		t1.join()
	except KeyboardInterrupt:
		if_error()
	except:
		if_error()
