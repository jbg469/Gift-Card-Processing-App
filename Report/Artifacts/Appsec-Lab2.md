# Setting up the environment

Running specified commands in Part 0: we set up the environment as specified.

<img width="1792" alt="Screen Shot 2022-03-13 at 3 51 46 PM" src="https://user-images.githubusercontent.com/72175659/158712594-8fbe96e0-f2e1-4e64-8e1d-ec3e89a79424.png">
<img width="1792" alt="Screen Shot 2022-03-13 at 3 52 36 PM" src="https://user-images.githubusercontent.com/72175659/158712601-5273c1e7-5ccc-4028-ae1b-0563183bda38.png">

# Cross-Site Scripting (XSS)

 Through dynamic analysis of the website (injecting javascript into urls and input fields) we find a vulnerability when we are logged in in the gift mode on http://127.0.0.1/gift/0 . We inject "<script>alert(document.cookie)</script>" into the username field of http://127.0.0.1/gift/0 and 0 in the amount field. 
 
  <img width="921" alt="Screen Shot 2022-03-15 at 2 55 14 PM" src="https://user-images.githubusercontent.com/72175659/158712973-e4b01c9f-08ab-4439-9817-3cb9b3b38c61.png">
  
  <img width="1447" alt="Screen Shot 2022-03-15 at 2 52 29 PM" src="https://user-images.githubusercontent.com/72175659/158712989-a2a55264-9437-4808-b35f-69e7d16287e7.png">
  
  As we can see no data is printed in our alert box meaning the cookie data wasn't printed due to the httponly flag that is set to true. With other input such as alert('hello') we do get "hello in the alert box. Httponly prevents scripts from accessing the cookie.
  
For task 1b we made a script that uses the request libraries. The script works by creating a user session and loging us in. We store the session cookie data and use that for another post request on the site, this time on our vulnerable path, http://127.0.0.1/gift/0. If we find our script text injected the website text then we output "XSS vulnerable" otherwise "Not Vulnerable"
  
  <img width="1440" alt="Screen Shot 2022-03-16 at 8 18 18 PM" src="https://user-images.githubusercontent.com/72175659/158713248-df8a020d-d3d9-4d56-8585-a4e1b07eb68b.png">

 This vulnerability is possible because in views.py we have the following line 
 ```
 target_user = request.POST.get('username', None)
 ```
 
 It takes in any input from the vulnerable  field without sanitizing it. To fix this we import escape from Django libraries and escape the target user. This converts the vulnerable input to a safe string by converting all the script elements to HTML elements effectively rendering the exploit we found completely useless. Our script written earlier also verifies no vulnerability is present 
 
 ```
 from django.utils.html import escape
 target_user = escape(request.POST.get('username', None))
 ```
 
 <img width="1116" alt="Screen Shot 2022-03-17 at 5 22 04 PM" src="https://user-images.githubusercontent.com/72175659/158900203-cec6b656-3cb8-491b-83a6-96c4d65b6c97.png">
 <img width="1103" alt="Screen Shot 2022-03-17 at 5 23 45 PM" src="https://user-images.githubusercontent.com/72175659/158900214-57fc8329-112c-4bd6-a997-0215d954dd64.png">
# CROSS SITE REQUEST FORGERY
 
 First we verify that we can sen giftcard from user on the left to the user on the right
<img width="1115" alt="Screen Shot 2022-03-17 at 9 01 28 PM" src="https://user-images.githubusercontent.com/72175659/158918268-d5338c41-e077-4068-9b00-cebe891a54c8.png">
 
 Successfully give attacker a giftcard
 
<img width="1115" alt="Screen Shot 2022-03-17 at 9 02 14 PM" src="https://user-images.githubusercontent.com/72175659/158918270-119af53d-4eb6-49f8-83d4-c868f6ba5aef.png">

# POC
 we successfully demonstrate a POC attack that works by exploiting the HTML POST method to submit a form with hidden values. We simply dropped the CRSF-POC.html file in the target browser. CSRF-POC.html
 ```
 <html>
	<head>
		<title>POC attack</title>
	</head>
	<body>
		<h1>Pwn press F</h1>
		<form action="http://127.0.0.1:80/gift/0" method="post" target="hiddenframe" name="csrfform">
		
		        <input type="hidden" name="amount" value="666" /> 
			<input type="hidden" name="username" value="bryan" /> 
			
		 <script>document.csrfform.submit();</script>
		</form>
		<iframe name="hiddenframe" style="display: none;"></iframe>
	</body>
</html>

 ```
 
 <img width="1102" alt="Screen Shot 2022-03-18 at 3 44 40 PM" src="https://user-images.githubusercontent.com/72175659/159073383-5d4694e6-de9a-451e-8617-d6c755331e56.png">
We store the POC exploit in an isolated directory and spin up a python server on port 8081 with

```
python3 -m http.server 8081
```
 We go on the targets web browser and go to 0.0.0.0:8081/index.html which will trigger out exploit. The instance of the exploit should gift the attacker a card worth 666
 
 <img width="1101" alt="Screen Shot 2022-03-18 at 3 48 11 PM" src="https://user-images.githubusercontent.com/72175659/159073809-59a23af5-d43d-4649-b5e3-1b2b6c707539.png">
 
 As expected our exploit was successful.

 
<img width="1119" alt="Screen Shot 2022-03-17 at 9 33 30 PM" src="https://user-images.githubusercontent.com/72175659/158921791-69ec6bb5-a2e9-44bf-ba2c-f1438d2ab599.png">

This exploit works because there is not csrf token in the input field. What this token does is essentially give a random hidden input that only that instance of the website will have and recognize on submission. This prevents cross websites forgeries to a large extent as guessing that input would require  time, luck, or both. We made jbrg-csrf.py to check for "csrfmiddlewaretoken" in the gift.html templete . The server prints gift.html and since it doesn't have the mitigating control we output "CSRF Vulnerable".
<img width="1082" alt="Screen Shot 2022-03-18 at 4 21 54 PM" src="https://user-images.githubusercontent.com/72175659/159077999-e0a9b1c7-f30b-4add-a161-5a5d55fbaa5e.png">


When we add {%csrf_ token%} to the input brackets in gift.html we get a hidden field not visible when the website is loaded
```
<input type="hidden" name="csrfmiddlewaretoken" value="PScYCWFX0KaFJP5x4nrhvGytLZYmrmSL7Y3wfRHtSblqIuQww6ohzndKo2bsywaS"> 
```
scanning with jbg469-csrf.py shows us vulnerability is mitigated.

<img width="1099" alt="Screen Shot 2022-03-18 at 4 14 19 PM" src="https://user-images.githubusercontent.com/72175659/159077129-5f9803da-103b-4cb0-aef0-a327747b42cd.png">

That enough did not stop our POC exploit from running again, it was that good. We had to edit the setting.py file to include 'django.middleware.csrf.CsrfViewMiddleware'. After running our exploit again we succesffuly mitaged our POC attack. 


<img width="1099" alt="Screen Shot 2022-03-18 at 4 34 11 PM" src="https://user-images.githubusercontent.com/72175659/159079721-dcdba0e3-3dec-4e6c-ac25-ef90d42d6ce1.png">







