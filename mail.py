# import necessary packages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib



def send_mail(name, text, to="ulyanausachova@yandex.ru"):
    # create message object instance
    msg = MIMEMultipart()
    message = text
    # setup the parameters of the message
    password = "UlyanaAndVladimir111"
    msg['From'] = "antichiterneiro@gmail.com"
    msg['To'] = to
    msg['Subject'] = "УВЕДОМЛЕНИЕ от " + name
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    print("successfully sent email to %s:" % (msg['To']))
