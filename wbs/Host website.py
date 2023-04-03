import subprocess
from os import path, system
from time import sleep

requiredcmd = ("genrsa -out server.key 2048","req -new -key server.key -out server.csr","x509 -req -days 365 -in server.csr -signkey server.key -out server.crt")
requiredfiles = (path.isfile("server.key"),path.isfile("server.csr"),path.isfile("server.crt"))
extras = (path.exists("C:\Program Files\OpenSSL-Win64"),path.exists("node_modules"),path.isfile("messages.txt"))

if not extras[0]:
    print("do you want to install openssl for generating certifcates?")
    while 1:
        usr = input('Y/N?>')
        if usr.upper() in ("Y","YES"):
            print("It will run itself")
            system('curl https://slproweb.com/download/Win64OpenSSL-3_1_0.msi -O Win64OpenSSL-3_1_0.msi')
            system('Win64OpenSSL-3_1_0.msi')
            break
        if usr.upper() in ("N","NO"):
            quit()

for i in range(0,len(requiredcmd)):
    if not requiredfiles[i]:
        print(f"Please enter required command: {requiredcmd[i]}")

if False in requiredfiles:
    for i in range(30):
        print(i, end='\r')
        sleep(1)
    quit('These are required!')

if not path.exists("node_modules"):
    system("npm install ws")
if not path.isfile("messages.txt"):
    subprocess.Popen(['start', 'cmd', '/c', 'py reset.py'], shell=True)

subprocess.Popen(['start', 'cmd', '/k', 'node rjso'], shell=True)
subprocess.Popen(['start', 'cmd', '/k', 'node wbs'], shell=True)

