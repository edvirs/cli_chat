# cli_chat
This is a multithreaded TCP chat on python3

## Features:

* Asymmetric encryption (**RSA**)
* Interaction commands:
    
 
 >!help - Display this menu
 !aou - Amount of users online
 !lou - List of users online
 !exit - Exit from the chat
 


## How to use:
1. Install python packages:

   `sudo pip3 install colored rsa`

2. Clone the repo

    `git clone https://github.com/edvirs/cli_chat`

3. Setup config files (config\_s.py / config_c.py)

4. Launch server.py 
    
    `python3 server.py`

5. Launch client.py with argv (nickname)
    
    Exemple:
`python3 client.py edvirs`



# NOTICE!
If you want to use this chat in global network , you have to open port , which you want to use , on your router

**This only applies to the server!**
