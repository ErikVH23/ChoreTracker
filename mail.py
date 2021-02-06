import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from jinja2 import Environment, FileSystemLoader
import os
import getpass
import sys

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
        password = getpass.getpass(stream=sys.stderr)
        server.login(SENDER_EMAIL, password)

        #generates list of name
        names = []
        for n in users["Users"]:
            names.append(n["Name"])

        generateHTML(createList(users))

        for user in users["Users"]:
            try:
                server.sendmail(SENDER_EMAIL, user["Email"], createMessage(user["Name"]))
                print("Sent to {}".format(user["Name"]))
            except Exception as e:
                print("Could not send to {}".format(user["Name"]))
                print(e)

    except Exception as e:
        print(e)
        server.quit()
        print('Server closed')

def createMessage(name: str) -> str:
    """

    """
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Chores"
    msg['From'] = SENDER_EMAIL
    msg['To'] = name 

    with open('./html/out.html') as html:
        part1 = MIMEText(html.read(), 'html')

    msg.attach(part1)

    return msg.as_string()

def generateHTML(choreList: dict):
    """
    Takes in a dict containg chores, writes to out.html
    based on the template email.html 

    Parameters
    ----------
    choreList: dict, required

    Returns
    -------
    None
    """
    env = Environment(loader=FileSystemLoader('./templates/'))
    template = env.get_template('email.html')


    with open('./html/out.html','w') as fh:
        fh.write(template.render(
            chores = choreList
        ))

"""ANDERS THIS IS WHAT YOU NEED TO DO"""
def createList(users: dict) -> list:
    """
    Generates list of tuples pairing individuals with their weekly
    chores. Takes into account circumstances such as floor, cat duty
    and special (Basically if you are Jacob or not)

    Parameters
    ----------
    users: dict
    Returns
    -------
    choreList: list
    """

    chores = []
    people = []

    for person in users["Users"]:
        people.append(person["Name"])
    for chore in users["Chores"]:
        chores.append(chore["Title"]) 

    #print("People: {}".format(len(people)))
    #print("Chores: {}".format(len(chores)))
    choreList = []

    for x in people:
        if len(chores) == 0:
            break
        else:
            choreList.append(x+"   -   "+chores.pop())


    return choreList 





if __name__ == "__main__":
    generateHTML(createList(users))
