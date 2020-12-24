# cli_chat
This is a multithreaded TCP chat on python3

## Features:

* Asymmetric encryption (**RSA**)
* Interaction commands:

>
 !help - Display this menu
>
 !aou - Amount of users online
>
 !lou - List of users online
>
 !exit - Exit from the chat



## How to use:
1. Install python packages:

 `sudo pip3 install colored rsa`

2. Clone the repo

 `git clone https://github.com/edvirs/cli_chat`

3. Setup config files (s_config.json / c_config.json)

 `"amount_of_users": "5"` - means that server will create 5 threads to 
 
 listen clients
 
 `"keys_exchanging_delay": "4"` - means that keys exchange will be delay for 4 second to make stable connection 
 
 (you have to increase this value if you use VPN). This value must be at least 4 in any cases. It`s desirable that these 
 
 values match on server and client

4. Launch server.py

 `python3 server.py`

5. Launch client.py with argv (nickname)

 Exemple:

 `python3 client.py edvirs`



# NOTICE!
If you want to use this chat in global network , you have to open port , which you want to use , on your router

and be sure that you have "white" (dedicated) ip address 

**This only applies to the server!**
