import smtplib
from tkinter import*
from tkinter import scrolledtext
from tkinter import messagebox
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

def closet1():
    t1.destroy()

def login1():
    global user1
    global pass1
    global user
    global password
    try:
        user = user1.get()
        password = pass1.get()
        l = Label(t1,text='PRESS NEXT TO CONTINUE...', bg='Black', fg='GOLD').place(x=350,y=350)
    except:
        l = Label(t1,text='PLEASE ENTER CREDENTIALS!!', bg='Black', fg='GOLD').place(x=350,y=350)
        t1.destroy

def login():
    global t1
    t1=Tk()
    t1.title("LOGIN MENU")
    t1.configure(bg='BLUE')
    t1.geometry("800x450")
    l = Label(t1,text='USERNAME :', bg='Black', fg='GOLD').place(x=250,y=180)
    global user1
    user1 = Entry(t1, width=35, borderwidth=5, bg="white", fg="black")
    user1.place(x=350,y=176)
    l = Label(t1,text='PASSWORD :', bg='BLACK', fg='GOLD').place(x=250,y=220)
    global pass1
    pass1 = Entry(t1, width=35, borderwidth=5, bg="white", fg="black")
    pass1.place(x=350,y=216)
    button = Button(t1, text="LOGIN",width=5, bg="black",fg='gold',command=lambda:login1()).place(x=400,y=260)
    button = Button(t1, text="NEXT",width=5, bg="black",fg='gold',command=lambda:closet1()).place(x=400,y=300)
    t1.mainloop()

def send():
    frame2.place_forget()
    frame1.place(x=5,y=5)

def see():
    frame1.place_forget()
    frame2.place(x=5,y=5)

def send1():
    global user
    global password
    global receiver
    try:
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(user,password)
        subject=subject1.get()
        body=body1.get('1.0', 'end-1c')
        receiver=rec1.get()
        msg= f'Subject:{subject}\n\n{body}'
        server.sendmail(user, receiver,msg)
        messagebox.showinfo('SUCCESS','MESSAGE SENT!!')
    except:
        messagebox.showinfo('FAILED','WRONG CREDENTIALS!!')

def see1():
    global user
    global password
    con=imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        body2.configure(state='normal')
        res1=''
        con.login(user, password)
        con.select("INBOX")
        result,data=con.uid('search', None, "ALL")
        inboxlist=data[0].split()
        for item in inboxlist:
                result2,maildata= con.uid('fetch',item,'(RFC822)')
                rawmail=maildata[0][1].decode("utf-8")
                mailmessage=email.message_from_string(rawmail)
                res1=res1+'To:'+' '+mailmessage['To']+'\n\n'
                res1=res1+'From:'+' '+mailmessage['From']+'\n\n'
                res1=res1+'Subject:'+' '+mailmessage['subject']+'\n\n'
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
                    if "plain" in content_type: res1=res1+part.get_payload()+'\n'
                    elif "html" in content_type:
                        html =part.get_payload()
                        soup =BeautifulSoup (html, "html.parser")
                        text =soup.get_text()
                        res1=res1+text+'\n'
                res1+='____________________________________________________________\n'
        body2.insert(INSERT,str(res1))
        body2.configure(state='disabled')
    except Exception as e:
        messagebox.showinfo('FAILED',e)

def main():
    global t1
    t1=Tk()
    t1.title("EMAIL")
    t1.configure(bg='BLACK')
    t1.geometry("800x450")
    global frame1
    global frame2
    frame1 = Frame(t1,width=790,height=440,bg = 'RED')
    frame2 = Frame(t1,width=790,height=440,bg = 'PURPLE')
    menubar = Menu(t1)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="SEND",command = lambda:send())
    filemenu.add_command(label="INBOX",command = lambda:see())
    menubar.add_cascade(label="MENU", menu=filemenu)
    t1.config(menu=menubar)
    l = Label(frame1,text='RECEIVER :', bg='BLACK', fg='GOLD').place(x=250,y=14)
    global rec1
    rec1 = Entry(frame1, width=35, borderwidth=5, bg="white", fg="black")
    rec1.place(x=350,y=10)
    l = Label(frame1,text='SUBJECT :', bg='BLACK', fg='GOLD').place(x=100,y=54)
    global subject1
    subject1 = Entry(frame1, width=60, borderwidth=0, bg="white", fg="black")
    subject1.place(x=170,y=55)
    global body1
    body1 = scrolledtext.ScrolledText(frame1, wrap= WORD, width=60, height=10, font=("Times New Roman", 15))
    body1.place(x=100,y=100)
    button = Button(frame1, text="SEND",width=5, bg="black",fg='gold',command=lambda:send1()).place(x=350,y=350)
    l = Label(frame2,text='INBOX', bg='BLACK', fg='GOLD',font=("Times New Roman", 20)).place(x=330,y=25)
    global body2
    body2 = scrolledtext.ScrolledText(frame2, wrap= WORD, width=60, height=10, font=("Times New Roman", 15))
    body2.place(x=100,y=100)
    body2.configure(state='disabled')
    button = Button(frame2, text="REFRESH",width=7, bg="black",fg='gold',command=lambda:see1()).place(x=350,y=350)
    t1.mainloop()

login()
main()
