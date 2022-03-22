import requests

loginurl=('127.0.0.1/login.html')
secureurl=('127.0.0.1/index.html')

# Fill in your details here to be posted to the login form.
payload = {
    'uname': 'john',
    'pword': 'johnpass'
}
payload2 = {
    'card_supplied': 'True',
    'card_fname': 'none'
}

def getcookies(s): 
	for c in s.cookies:
		if c.name == "sessionid":
			return c

# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    s.post('http://127.0.0.1/login.html', data = payload)
    sessioncookie=getcookies(s)
    sessioncookie.secure = False
    # An authorised request.
    s.get('http://127.0.0.1/useCard.html')
    a_files = {'card_data': open('jbg469-sqli.gftcrd', 'rb')}
    x = s.post("http://127.0.0.1/useCard.html", data=payload2, files=a_file)
    fullstring = x.text
    substring = 'memoryview: a bytes-like object is required, not'
    if fullstring.find(substring) != -1:
    	print('Vulnerable to SQLi!')
    else:
    	print('Not vulnerable to SQLi')
    
    
    

