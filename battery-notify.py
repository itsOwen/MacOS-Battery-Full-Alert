#!/usr/bin/env python

import psutil
import time
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

your_email = 'example@icloud.com'
send_to = 'example@gmail.com'
app_password = 'app-password-from-icloud-site'

msg = MIMEMultipart()
msg['From'] = your_email
msg['To'] = send_to
msg['Subject'] = 'Your Mac is Successfully Charged :)'
message = 'Please Disconnect your charger, Your Mac Device is successfully charged. Disconnecting your Charger on time can help you increase the lifespan of your battery <3'
msg.attach(MIMEText(message))

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
title = "Battery Successfully Charged :)"
message = "Please Disconnect your Charger, This will help you to improve your battery life!"
send = f''' osascript -e 'display notification "{message}" with title "{title}"' '''

def charger():
	threading.Timer(60, charger).start()
	battery = psutil.sensors_battery()
	if battery.power_plugged == False:
		print("Not connected")
	else:
		batterycheck(battery)

def batterycheck(battery):
	if battery.percent == 100:
		os.system(send)
		sendemail() and print("Successfully Charged")
	else:
		charger()

charger()