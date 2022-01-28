# Deployment of FLask App: ECG image Classification / Inference onto AWS 

# [Demo]

<a href="https://www.youtube.com/watch?v=8UBqlBF3ls8"><img src="https://user-images.githubusercontent.com/24941662/131371431-96df26ec-953d-4991-9692-45e348c19f2d.png"></a>


# Default Requirements

```
1. A GitHub repository with files for your working Flask application. 
   Make sure that the application that you want to deploy into AWS has secured required environment variables and is ready to deploy. 
   
2. Create a free account or sign in to your AWS console

3. A credit card for AWS to have on file in case you surpass the Free Tier eligibility options. 
   It is worth noting that you should take extra precautions if you are deploying an app onto AWS. 
   Make sure you stay within the Free Tier limits to avoid surplus charges at the end of the month. 
   Refer to the EC2 pricing guide and proper docs to prevent future charges.
```

# Deployement 

## Heroku

As begginners or intermediate Developers/Data Scientist/ Engineers. we want to showcase our works/projects to the world. So we look up for cheap or free resources like __Heroku__.
But sometimes Even this solution won't work due to some limitaions in the free tiers like the __`Slug Max Size = 500Mo`__ for each Applicaition.

Using Tensorflow/Pytorch and other libaries, plus the saved model will exceed the Slug Size to over 500Mo. 
Which happened to us during a project under Omdena Local Chapters Specially [Morocco Chapter](https://omdena.com/omdena-chapter-page-morocco/).

A bit frustrating. Altough, I could came up with a solution which is using AWS EC2 with Apache to Deploy the Flask App with the saved model and make it live. ( see above the demonstration)

## AWS

---
### Prerequisites

* AWS Account with valid credit or use your Tiers.
* Ubuntu 20.04 EC2 Instance
* Shell Access
* Comfortable with the command line/terminal
---
### Create a User Account if None.
  In order to deploy fast and easily, create an AWS account. Upon logging back into your account, you have the option to login as a Root user or an IAM user.

  * I would recommend logging in as a Root user account to perform tasks requiring unrestricted access or creating an IAM user account that holds all of the permissions that a Root user would have. IAM users have the ability to work on the AWS dashboard with secure control access that can be modified.

`For the purpose of this article, I am logging in as a Root user to accomplish the necessary tasks.`

### Navigate the EC2 Dashboard

Click on the Services tab at the top of the webpage. 
Click on `EC2` under the Compute tab or type the name into the search bar to access the EC2 dashboard.

EC2 is a virtual server in the cloud where the Flask web app will live.

--- 

1. __Step 01 — Launch and configure a new instance__

Let’s start by opening up the EC2 console in your AWS account. From here launch a new instance.
- Select Ubuntu Server 20.04 LTS — 64-bit(86) — ami-0885b1f6bd170450c for your AMI.
- You can use a `T2 micro` version for your instance type, mostly because it has a free tier option. If you have more demanding requirements feel free to choose one that better meets your needs.

__In our case I used a `T2.large with 2Vcpu & 8Gio of RAM` __

![Ubuntu 20.04 LTS](https://github.com/ayoub-berdeddouch/imginference/blob/main/readmeImg/instance.png)

- Create a new or select an existing security group in the next step.
__Note:__ to avoid cluttering your AWS account with multiple security groups that do the same thing, you can reuse an existing security group with these inbound rules, or create a new one if you like:

* SSH
* HTTP
* HTTPS

The SSH setting allows ssh access from any IP address. If you prefer you can set it to only allow access to your Public IP which you would need to update every time it changes unless you have a Static IP. 

HTTP allows you to access your new instance from the browser and HTTPS is for running secure connections if you have an SSL certificate.

![Inbound Rules](https://github.com/ayoub-berdeddouch/imginference/blob/main/readmeImg/rules.png)

- Choose to create a new key pair or reuse an existing one.
There is also an option to reuse public keys, just like security groups it is best to reuse them if it makes sense. 
Make sure to download and save the key pair somewhere where you can find it later, I’ll be referring to this key as "__KEY_GIVE-IT-ANAME__".pem . 
Once everything is configured click on the Launch Instances button.

![KEY](https://github.com/ayoub-berdeddouch/imginference/blob/main/readmeImg/key.png)

Go back to your EC2 dashboard and remember to give your new instance a meaningful name to keep better track of it and wait for the instance state to finish launching. 


__2. Step 02 — Connect to your new instance via SSH__

There are several ways to connect to an instance running on AWS. My favorite one is to connect via SSH. 
You can use FTP if you like but that is no longer the most efficient approach.

- To get the connection details select your new instance and click on the connect button in your EC2 dashboard.

![EC2_Dashboard](https://github.com/ayoub-berdeddouch/imginference/blob/main/readmeImg/ec2_dash.png)

- Follow the instructions listed on the next screen, make sure to click on the SSH client tab.

![SSH_CONNECT](https://github.com/ayoub-berdeddouch/imginference/blob/main/readmeImg/sshco1.png)
![SSH_CONNECT](https://github.com/ayoub-berdeddouch/imginference/blob/main/readmeImg/sshco2.png)

1 — when someone refers to an SSH Client, it could be your Mac terminal, Windows Powershell which I am using.
2 — locate the private key file we previously downloaded and let’s move somewhere where is easier to find. 
I like to keep the key in my root directory in a folder called .ssh Create a new one if you don’t have one. Run the following commands in the terminal.

```bash
$ cd
$ mkdir ~/.ssh
```

The dot in front of that folder means it will be a hidden file. To show it in finder use this keyboard shortcut `cmd + shift + .` to toggle hidden files.

3 — let’s update the permissions for our private key, in our case, this would be:
`chmod 400 ~/.ssh/microservices.pem`

4 — we’ll be using our instance’s Public DNS to connect to the new instance we just created. Copy it and let’s move on to the next step.
- Now that you have the setup ready let’s connect to our instance. Like I previously mentioned you can use any SSH client you like. I’ll be using PowerShell on Windows.



```bash
$ cd 
$ ssh -i “~/.ssh/KEY-NAME.pem” ubuntu@ec2-IP@dress.REGION.compute.amazonaws.com

__Or just__

$ cd folder where you saved the KEY
$ ssh -i "KEY_NAME.pem" ubuntu@ec2-IP@dress.REGION.compute.amazonaws.com
```

__SUCCESSFULLY CONNECTED__


__3. Step 03 — Update and upgrade__

Before we do anything else, let’s make sure we update the local package index and upgrade the system. This makes sure everything is up to date and prevents any errors due to deprecations.

```bash
$ sudo apt-get update
$ sudo apt-get -y upgrade
```

__4. Step 04 — Set up Python 3__

Check the Python version installed in the system, as of this article Python 2 is officially deprecated so you should be using Python 3 on new projects. Ubuntu 20.04 comes with Python 3 pre-installed.
` $ python3 -V` , You should get an output similar to this. __Python 3.8.5__

Install PIP to manage software packages for Python. `$ sudo apt install -y python3-pip`

Check that pip3 installation was successful.  
```bash
pip3 -V  
Output  
pip 20.0.2 from /usr/lib/python3/dist-packages/pip (python 3.8)
```

Install other required dependencies to make sure you have a robust development environment.
`$ sudo apt install -y build-essential libssl-dev libffi-dev python3-dev`


__5. Step 05 — Version Control__

For this tutorial, you will be using GIT to clone our project into this server. Version control allows for easier codebase management and team collaboration. Ubuntu 20.04 also comes with GIT pre-installed.
`$ git — version` , Output __git version 2.25.1__

__6. Step 06 — Install And Configure Apache and WSGI__

Let’s install the Apache webserver with the mod_wsgi module to interface with your Flask app. We need it because web servers don’t natively speak Python and WSGI makes that communication happen.

`$ sudo apt-get install -y apache2`

When installing mod_wsgi make sure to install the version in this guide. If you install libapache2-mod-wsgi instead you might run into an error where it can’t find the Python packages required for your app because that version only works with Python 2.

`$ sudo apt-get install -y libapache2-mod-wsgi-py3`

If you point to your browser at your instance’s Public DNS you should see Apache’s default page, indicating the installation is working correctly.

![Apache2 HomePage](https://github.com/ayoub-berdeddouch/imginference/blob/main/readmeImg/apache2.png)

__7. Step 07 — Create And Configure Flask App__

To make this section less error-prone, let’s first clone our Flask app from github repository, to deploy our full-fledged application.

* Create a symlink to the site root defined in Apache’s configuration.

```bash
$ cd
$ sudo ln -sT ~/imginference /var/www/html/imginference
```
* Install Requirments 

```bash
$ cd ~/imginference
$ sudo pip3 install -r requirements.txt
```

__NOTE:__ You may run into some errors while installing CV2(OpenCV), so just run this 2 lines:

```bash
$ sudo apt-get update
$ sudo apt-get install -y libgl1-mesa-dev
```

Also to instal Torch/Pytorch run : `pip3 install torch torchvision`

__Then,__

* Add a .wsgi script file to load the app.

`$ touch production.wsgi`

* Put the following in the production.wsgifile.

```python
#production.wsgi
import sys
sys.path.insert(0,"/var/www/html/imginference/")
from run import app as application
```

__8. Step 08 — Configure Virtual Hosts__

Apache displays HTML pages by default but to serve dynamic content from Flask make the following changes. 
The default Apache configuration file is located at `etc/apache2/sites-available/000-default.conf`. Instead of overriding that file let's create a new one.

`$ sudo vi /etc/apache2/sites-available/imginference.conf`

Add the following to imginference.conf

```apache2
#imginference.conf

<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    ServerName your_domain
    ServerAlias www.your_domain
    DocumentRoot /var/www/html/imginference
    WSGIDaemonProcess imginference threads=5
    WSGIScriptAlias / /var/www/html/imginference/production.wsgi
     <Directory imginference>
         WSGIProcessGroup imginference
         WSGIApplicationGroup %{GLOBAL}
         Order deny,allow
         Allow from all
     </Directory>
     ErrorLog ${APACHE_LOG_DIR}/error.log
     CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

* Disable the default Apache config by running the following command.

`$ sudo a2dissite 000-default.conf`

```bash
-- Output
Site 000-default disabled.
To activate the new configuration, you need to run:
  systemctl reload apache2
```
  
* Now enable our new conf

`$ sudo a2ensite imginference.conf`

* Reload apache to implement the changes made.

`$ sudo systemctl reload apache2`

* If you run into any error you can look at the logs with this command.

`$ sudo tail -f /var/log/apache2/error.log`

* Reload your browser and instead of the default Apache page you should now see the Web App home page.

![WebApp HOME](https://user-images.githubusercontent.com/24941662/131371431-96df26ec-953d-4991-9692-45e348c19f2d.png)



__9. Step 9: This is the important step for running of the Flask Application.__

From the terminal, you can run the flask application using the command:
`$ sudo python3 app.py` (Make sure you are ssh’ed to the Instance)

__But this command will get automatically killed if we closed the terminal, or exited from the ssh to the instance.__

To keep running the application (so that you may close your laptop and have some fun, while the application keeps running), 
we will use the powerful linux command: `nohup (no hangup).`

So for running the python application we will use the command:

`$ nohup python3 app.py &`  __(& allows us to run the application in background and nohup allows the application to keep running even on hang up/logout)__.


## ✨✨Here we are! Live!✨✨

Now if we wish to kill the process we can use the command: `$sudo kill <process-id>`.(Make sure you are ssh’ed in the instance)


![WebApp HOME](https://user-images.githubusercontent.com/24941662/131371431-96df26ec-953d-4991-9692-45e348c19f2d.png)














