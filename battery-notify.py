#!/usr/bin/env python

import psutil
import time
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

your_email = 'youremail@icloud.com'
send_to = 'youremail@gmail.com'
app_password = 'your-apple-app-pass'

msg = MIMEMultipart()
msg['From'] = your_email
msg['To'] = send_to
msg['Subject'] = 'Your Mac is Successfully Charged :)'
message = 'Please Disconnect your charger, Your Mac Device is successfully charged. Disconnecting your Charger on time can help you increase the lifespan of your battery <3'
msg.attach(MIMEText(message))

state = {
    "sent": False
}

# Tip: When you are away from your Mac, and you have your mobile near you.
# 1. Make sure to turn on Email Sync on mobile network, So you get instant notification.


def sendemail():
    try:
        mailserver = smtplib.SMTP('smtp.mail.me.com', 587)
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login(your_email, app_password)
        mailserver.sendmail(your_email, send_to, msg.as_string())
        mailserver.quit()
        return True
    except:
        print("Something went wrong with the email service, Make sure your password and email are correct.")
        return False

# Toast Notifications


def notisend():
    title = "Battery Successfully Charged :)"
    message = "Please Disconnect your Charger, This will help you to improve your battery life!"
    send = f''' osascript -e 'display notification "{message}" with title "{title}"' '''
    os.system(send)


def charger():
    while True:
        time.sleep(60)
        battery = psutil.sensors_battery()
        if battery.power_plugged == False:
            print("Not connected")
        else:
            not state["sent"] and batterycheck(battery)


def batterycheck(battery):
    if battery.percent == 100:
        state["sent"] = True
        notisend()
        sendemail() and print("Successfully Charged")
    else:
        charger()


c = threading.Thread(target=charger)
c.start()
c.join()
