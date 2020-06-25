clearimport os ,socket ,sys ,time ,functions , threading , rsa , config_s
from colored import fg ,attr

port = int(config_s.port)
current_OS = config_s.current_OS
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clients = []
list_of_users = []
res_C = attr('reset')
main_C = fg('#FFD7AF')
green_C = fg('#00CD00')
blue_C = fg('#00FFFF')

teminal_clear = functions.OS_definition(current_OS)
if teminal_clear == 'error':
	print(fg('red') + 'Correct config usage: current_OS = (win/linux)' + res_C)
	sys.exit()

try:
	sock.bind(('', port))
except:
	print(fg('red') + 'Port is already in use' + res_C)
	sys.exit()

sock.listen(5)

def keys_generation():
	global server_pubkey , server_privkey
	os.system(teminal_clear)
	print(green_C + 'loading ...' + res_C)
	server_pubkey, server_privkey = rsa.newkeys(2048)
	os.system(teminal_clear)
	print('[Keys generated]')
	print('[Server started]')

def if_error():
	for i in clients:
		client_addr ,client_pubkey = i
		client_addr.send(rsa.encrypt('!server_shutdown'.encode('utf-8') , client_pubkey))

	sock.close()
	os.system(teminal_clear)
	print(fg('red') + '\n\nServer closed\n\n' + attr('reset'))
	sys.exit()

def transmission(data, nickname, current_client):
	global clients
	for i in clients:
		client_addr ,client_pubkey = i
		if client_addr != current_client:
			client_addr.send(rsa.encrypt((green_C + nickname + ': ' + res_C + main_C + data).encode('utf-8'), client_pubkey))

def receiving():
	global clients
	while True:
		client , addr = sock.accept()
		time.sleep(2)
		client.send(str(server_pubkey.n).encode('utf-8'))
		time.sleep(2)
		client.send(str(server_pubkey.e).encode('utf-8'))
		nickname = (rsa.decrypt(client.recv(2048), server_privkey)).decode('utf-8')
		current_client_pubkey_n = client.recv(2048).decode('utf-8')
		current_client_pubkey_e = client.recv(2048).decode('utf-8')
		current_client_pubkey = rsa.PublicKey(int(current_client_pubkey_n) , int(current_client_pubkey_e))
		client_info = client , current_client_pubkey
		for i in clients:
			client_addr ,client_pubkey = i
			client_addr.send(rsa.encrypt(('{res}[{green}{nickname}{res}]{blue} →  Join chat {res}'.format(res = res_C ,nickname = nickname ,green = green_C ,blue = blue_C)).encode('utf-8') , client_pubkey))
		clients.append(client_info)
		list_of_users.append(nickname)
		print('[{addr}] [{nickname}] Conected'.format(addr = str(addr) , nickname = str(nickname)))
		while True:
			permission_to_transmission = True
			data = client.recv(2048)
			data = (rsa.decrypt(data ,server_privkey)).decode('utf-8')
			if data == '!exit':
				client.close()
				print('[{addr}] [{nickname}] Disconected'.format(addr = str(addr) , nickname = str(nickname)))
				time.sleep(0.1)
				clients.remove(client_info)
				list_of_users.remove(nickname)
				for i in clients:
					client_addr , client_pubkey = i
					client_addr.send(rsa.encrypt(('{res}[{green}{nickname}{res}]{blue} →  Left chat {res}'.format(res = res_C ,nickname = nickname ,green = green_C ,blue = blue_C)).encode('utf-8') , client_pubkey))
				break
			elif data == '!aou':
				amount = str(len(list_of_users))
				client.send(rsa.encrypt(('{green}Amount of users online: {blue}{amount}{res}'.format(green = green_C , blue = blue_C , amount = amount , res = res_C)).encode('utf-8'),current_client_pubkey))
				permission_to_transmission = False
			elif data == '!lou':
				for i in list_of_users:
					client.send(rsa.encrypt((green_C + i + res_C).encode('utf-8'),current_client_pubkey ))
				permission_to_transmission = False

			if permission_to_transmission:
				print('[{addr}] [{nickname}] →  '.format(addr = str(addr) , nickname = str(nickname)) + 'sent a message')
				transmission(data, nickname, client)

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
		keys_generation()
		t1.start()
		t2.start()
		t3.start()
		t4.start()
		t5.start()
		t1.join()
	except KeyboardInterrupt:
		if_error()
		pass
	except:
		if_error()
		pass
