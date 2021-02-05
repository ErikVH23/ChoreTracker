import smtplib, ssl
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from jinja2 import Environment, FileSystemLoader
import os

PORT = 500
SMPT_SERVER = "smpt.gmail.com"
SENDER_EMAIL = "choredaddyRH@gmail.com"
RECEIVER_EMAIL = "eavanhor@mtu.edu"


with open('users.json') as f:
    users = json.load(f)

test = ["eavanhor@mtu.edu"]

def sendMessage():
    try:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.ehlo()
        server.login(SENDER_EMAIL, 'williams19905')

        #generates list of name
        names = []
        for n in users["Users"]:
            print(n["Name"])
            names.append(n["Name"])

        generateHTML(names)

        for name in test:
            try:
                server.sendmail(SENDER_EMAIL, name, createMessage(name))
                print("Sent to {}".format(name))
            except Exception as e:
                print("Could not send to {}".format(name))
                print(e)

    except Exception as e:
        print(e)
        server.quit()
        print('Server closed')

def createMessage(name: str) -> str:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Chores"
    msg['From'] = SENDER_EMAIL
    msg['To'] = name 

    with open('./html/out.html') as html:
        part1 = MIMEText(html.read(), 'html')

    msg.attach(part1)

    return msg.as_string()

#Generates HTML file based on chorelist
def generateHTML(choreList: dict) -> str:
    env = Environment(loader=FileSystemLoader('./templates/'))
    template = env.get_template('email.html')

    with open('./html/out.html','w') as fh:
        fh.write(template.render(
            chores = choreList
        ))


#Function to create name|chore pairs for the week
def createList(users: dict) -> list:
    pass




if __name__ == "__main__":
    sendMessage()    