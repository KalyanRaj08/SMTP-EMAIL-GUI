import smtplib
import os
from email import*
import mimetypes
from bs4 import BeautifulSoup
import imaplib, email

#For senders Email use the below mentioned ID
#username: testperson458@gmail.com
#password: test458!

global user
global password
global receiver

user=input('ENTER MAIL\nSender: ')
password=input("Password:")
receiver=''

def sendmail():
    global user
    global password
    global receiver
    receiver=input("enter a valid email to whom you want to send\n receiver:")
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    try:
        server.login(user,password)
        print("login success\n")
    except:
        print("Wrong login credentials....")
        enter=input('Press Enter to Continue....')
        exit()
    subject=input("enter subject\n\n")
    body=input('enter body\n\n')
    msg= f'Subject:{subject}\n\n{body}'
    server.sendmail(user, receiver,msg)
    print("email has been sent\n")
    print()
    print("do you want to send mail to any one else.IF YES give input as yes else no")
    again=input("yes or no for resending:")
    while again=='yes':
        receiver=input ("enter a valid email to whom you want to send\n receiver:")
        subject=input('enter subject\n\n')
        body=input('enter body\n\n')
        msg= f'Subject:{subject}\n\n{body}'
        server.sendmail(user, receiver,msg)
        print("email has been sent\n")
        print()
        print("do you want to send mail to any one else.IF YES give input as yes else no")
        again=input("yes or no for resending:")

def seeinbox():
    global user
    global password
    print()
    print('Now we are going to retrieve mails: \n')
    con=imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        con.login(user, password)
    except:
        print("Wrong login credentials....")
        enter=input('Press Enter to Continue....')
        exit()
    print('we have successfully logged into the account',user,password,'to retrive mails')
    print("Now you are seeing the list of mails in the inbox:")
    con.select("INBOX")
    result,data=con.uid('search', None, "ALL")
    print('the above numbers represent the unique id of mails')
    print()
    print(data)
    print()

    inboxlist=data[0].split()              
    print (inboxlist)
    var='yes'
    print()

    while var == 'yes':
        print()
        if var=='yes':
            for item in inboxlist:
                result2,maildata= con.uid('fetch',item,'(RFC822)')
                print()
                print()
                rawmail=maildata[0][1].decode("utf-8")
                mailmessage=email.message_from_string(rawmail)
                print()
                print()
                print('To:',mailmessage['To'])
                print()
                print('From:',mailmessage['From'])
                print()
                print('Subject:',mailmessage['subject'])
                print()
                date=mailmessage['date']
                counter=1
                for part in mailmessage.walk():
                    if part.get_content_maintype()=="multipart":
                        continue
                    filename=part.get_filename()
                    content_type=part.get_content_type()
                    if not filename:
                        ext=mimetypes.guess_extension(content_type)
                        if not ext:
                            ext='.bin'
                    filename='msg-part-%08d%s' %(counter,ext)
                    counter += 1
                    if "plain" in content_type: print (part.get_payload())
                    elif "html" in content_type:
                        html =part.get_payload()
                        soup =BeautifulSoup (html, "html.parser")
                        text =soup.get_text()
                        print('Subject',mailmessage['subject'])
                        print()
                        print (text)
                    else:
                        print()
                        print("enter the no in the list which u want to retreive: PLZ ENTER THE NO IN THE DATA ")
                        print()
                        item=input ("enter no: ")
                        result2,maildata=con.uid('fetch', item, '(RFC822)')
                        print()
                        print()
                        rawmail=maildata[0][1].decode("utf-8")
                        mailmessage=email.message_fron_string(rawmail)
                        print()
                        print()
                        print('To',mailmessage['To'])
                        print()
                        print('From', mailmessage['From'])
                        print()
                        print('Subject',mailmessage['subject'])
                        print()
                        date_=mailmessage['date']
                        counter=1
        var='no'

ch=0
while ch != 3:
    print('1.Send Email')
    print('2.See Inbox')
    print('3.Exit')
    ch=input('Enter your choice:')
    try:
        ch=int(ch)
        if ch==1:sendmail()
        elif ch==2:seeinbox()
        elif ch==3:
            print('THANK YOU FOR USING THIS APP')
            enter=input('Press Enter to Continue....')
            break
        else:
            print('Invalid option')
            enter=input('Press Enter to Continue....')
    except:
            print('Invalid option')
            enter=input('Press Enter to Continue....')

