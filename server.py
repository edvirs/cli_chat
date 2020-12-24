import os, socket, sys, time, functions, threading, rsa, json
from colored import fg, attr


def if_error():
    for i in clients:
        client_addr, client_pubkey = i
        client_addr.send(rsa.encrypt('!server_shutdown'.encode('utf-8'), client_pubkey))

    sock.close()
    os.system(terminal_clear)
    print(fg('red') + '\n\nServer closed\n\n' + '\n\nPress Ctrl+C to exit\n\n' + attr('reset'))
    sys.exit()


def keys_generation():
    global server_pubkey, server_privkey
    os.system(terminal_clear)
    print(green_C + 'loading ...' + res_C)
    server_pubkey, server_privkey = rsa.newkeys(2048)
    os.system(terminal_clear)
    print('[Keys generated]')
    print('[Server started]')


def transmission(data, nickname, current_client):
    global clients
    for i in clients:
        client_addr, client_pubkey = i
        if client_addr != current_client:
            client_addr.send(
                rsa.encrypt((green_C + nickname + ': ' + res_C + main_C + data).encode('utf-8'), client_pubkey))


def receiving():
    global clients
    while True:
        client, addr = sock.accept()
        time.sleep(int(config_data['keys_exchanging_delay'])/2)
        client.send(str(server_pubkey.n).encode('utf-8'))
        time.sleep(int(config_data['keys_exchanging_delay'])/2)
        client.send(str(server_pubkey.e).encode('utf-8'))
        nickname = (rsa.decrypt(client.recv(2048), server_privkey)).decode('utf-8')
        current_client_pubkey_n = client.recv(2048).decode('utf-8')
        current_client_pubkey_e = client.recv(2048).decode('utf-8')
        current_client_pubkey = rsa.PublicKey(int(current_client_pubkey_n), int(current_client_pubkey_e))
        client_info = client, current_client_pubkey
        for i in clients:
            client_addr, client_pubkey = i
            client_addr.send(rsa.encrypt(('{res}[{green}{nickname}{res}]{blue} →  Join chat {res}'.format(res=res_C,
            nickname=nickname, green=green_C, blue=blue_C)).encode('utf-8'), client_pubkey))
        clients.append(client_info)
        list_of_users.append(nickname)
        print('[{addr}] [{nickname}] Connected'.format(addr=str(addr), nickname=str(nickname)))
        while True:
            permission_to_transmission = True
            data = client.recv(2048)
            data = (rsa.decrypt(data, server_privkey)).decode('utf-8')
            if data == '!exit':
                client.close()
                print('[{addr}] [{nickname}] Disconnected'.format(addr=str(addr), nickname=str(nickname)))
                time.sleep(0.1)
                clients.remove(client_info)
                list_of_users.remove(nickname)
                for i in clients:
                    client_addr, client_pubkey = i
                    client_addr.send(rsa.encrypt(('{res}[{green}{nickname}{res}]{blue} →  Left chat {res}'.format(res=res_C,
                        nickname=nickname, green=green_C, blue=blue_C)).encode('utf-8'), client_pubkey))
                break
            elif data == '!aou':
                amount = str(len(list_of_users))
                client.send(rsa.encrypt(('{green}Amount of users online: {blue}{amount}{res}'.format(green=green_C, blue=blue_C,
                amount=amount, res=res_C)).encode('utf-8'), current_client_pubkey))
                permission_to_transmission = False
            elif data == '!lou':
                for i in list_of_users:
                    client.send(rsa.encrypt((green_C + i + res_C).encode('utf-8'), current_client_pubkey))
                permission_to_transmission = False

            if permission_to_transmission:
                print('[{addr}] [{nickname}] →  '.format(addr=str(addr), nickname=str(nickname)) + 'sent a message')
                transmission(data, nickname, client)


def main():
    global port, current_OS, sock, clients, list_of_users, res_C, main_C, green_C, blue_C, terminal_clear, config_data

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clients = []
    list_of_users = []
    res_C = attr('reset')
    main_C = fg('#FFD7AF')
    green_C = fg('#00CD00')
    blue_C = fg('#00FFFF')

    try:
        with open('s_config.json', 'r') as config:
            config_data = json.load(config)
    except:
        print(fg('red') + 'Failed import json config' + res_C)
        sys.exit()

    current_OS = config_data['current_OS']
    port = int(config_data['port'])

    terminal_clear = functions.OS_definition(current_OS)

    if terminal_clear == 'error':
        print(fg('red') + 'Correct config usage: current_OS = (win/linux)' + res_C)
        sys.exit()

    try:
        sock.bind(('', port))
    except:
        print(fg('red') + 'Port is already in use' + res_C)
        sys.exit()

    sock.listen(int(config_data['amount_of_users']))

    list_of_threads = []

    for i in range(int(config_data['amount_of_users'])):
        list_of_threads.append(threading.Thread(target=receiving))

    for i in list_of_users:
        i.setDaemon(True)

    os.system(terminal_clear)
    keys_generation()

    for i in list_of_threads:
        i.start()

    list_of_threads[0].join()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if_error()
        pass
    except:
        if_error()
        pass
