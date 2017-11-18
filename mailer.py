#!/usr/bin/env python

import smtplib
from email.mime.text import MIMEText
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def send_mail(to, subject, content):
    sender = config['DEFAULT']['sender']
    login = config['DEFAULT']['login']
    password = config['DEFAULT']['password']

    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(login, password)
    mail.sendmail(sender, [to], msg.as_string())

    print("Mail to " + to + " sent.\nSubject: " + subject + "\nMessage: " + content)
    mail.quit()

    # sendMail('testing')
