# Setting up the environment

Running specified commands in Part 0: we set up the environment as specified.

<img width="1792" alt="Screen Shot 2022-03-13 at 3 51 46 PM" src="https://user-images.githubusercontent.com/72175659/158712594-8fbe96e0-f2e1-4e64-8e1d-ec3e89a79424.png">
<img width="1792" alt="Screen Shot 2022-03-13 at 3 52 36 PM" src="https://user-images.githubusercontent.com/72175659/158712601-5273c1e7-5ccc-4028-ae1b-0563183bda38.png">

# Cross-Site Scripting (XSS)
 Through dynamic analysis of the website (injecting javascript into urls and input fields) we find a vulnerability when we are logged in in the gift mode on http://127.0.0.1/gift/0 . We inject "<script>alert(document.cookie)(/script) into the username field of http://127.0.0.1/gift/0 and 0 in the amount field. 
  <img width="921" alt="Screen Shot 2022-03-15 at 2 55 14 PM" src="https://user-images.githubusercontent.com/72175659/158712973-e4b01c9f-08ab-4439-9817-3cb9b3b38c61.png">
  
  <img width="1447" alt="Screen Shot 2022-03-15 at 2 52 29 PM" src="https://user-images.githubusercontent.com/72175659/158712989-a2a55264-9437-4808-b35f-69e7d16287e7.png">
  
  As we can see no data is printed in our alert box meaning the cookie data wasn't printed due to the httponly flag that is set to true. With other input such as alert('hello') we do get "hello in the alert box. Httponly prevents scripts from accessing the cookie.
  
For task 1b we made a script that uses the request libraries. The script works by creating a user session and loging us in. We store the session cookie data and use that for another post request on the site, this time on our vulnerable path, http://127.0.0.1/gift/0. If we find our script text injected the website text then we output "XSS vulnerable" 
  
  <img width="1440" alt="Screen Shot 2022-03-16 at 8 18 18 PM" src="https://user-images.githubusercontent.com/72175659/158713248-df8a020d-d3d9-4d56-8585-a4e1b07eb68b.png">

