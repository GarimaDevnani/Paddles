import tkinter.messagebox as messagebox
from tkinter import *
import re

import dbo_login_signup as dbo
import page_home as pageH
import constant as CONSTANT


class Users():
    def __int__(self):
        self.userid = 0
        self.username = ''
        self.email = ''
        self.password = ''
        self.balance = 0
        self.permission = 'CUST'
        self.userstatus = 0

    def show(self):
        print((self.username, self.email, self.balance, self.permission, self.userstatus))


class LoginPage():
    def __init__(self, master=None):
        self.root = master
        self.root.geometry(CONSTANT.WINDOWS_SIZE)
        self.root.title('Paddles')
        self.email = StringVar()
        self.password = StringVar()
        self.page = Frame(self.root)
        self.createPage()

    def createPage(self):
        self.page.pack(pady=180)
        Label(self.page).grid(row=0, stick=W)

        Label(self.page, text='Email:').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.email).grid(row=1, column=1, stick=E)

        Label(self.page, text='Password:').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.password, show='*').grid(row=2, column=1, stick=E)

        Button(self.page, text='Login', command=self.loginCheck).grid(row=3, stick=W, pady=10)
        Button(self.page, text='Quit', command=self.page.quit).grid(row=3, column=1, stick=E)

        Button(self.page, text='Signup', command=self.gotoSignupPage, bd=0, fg='blue', activeforeground='black').grid(
            row=4, stick=W, pady=10)

    def loginCheck(self):
        email = self.email.get()
        password = self.password.get()
        result = dbo.authenticateUser(email, password)

        if result == 1:
            user = self.getUser()
            userStatus = user.userstatus
            if userStatus == 0 or userStatus == 1:
                self.page.destroy()
                pageH.TabbedView(self.root, user)
            else:
                self.reactivateAccount()
        elif result == 0:
            messagebox.showinfo(title='Account Authenticate', message='Please check your email or password.',
                                type='ok')
        else:
            messagebox.showwarning(title='Program Error', message='Authenticate DB Error!', type='ok')

    def getUser(self):
        user = Users()
        user.email = self.email.get()
        user.password = self.password.get()
        result = dbo.getUser(user.email)
        user.username = result[0][0]
        user.permission = result[0][1]
        user.balance = result[0][2]
        user.userstatus = result[0][3]
        user.userid = result[0][4]
        return user

    def gotoSignupPage(self):
        self.page.destroy()
        SignupPage(self.root)

    def reactivateAccount(self):
        messageBox = messagebox.askquestion(
            'Account inactive!!',
            'Do you want to reactivate your account?',
            icon='warning')
        if messageBox == 'yes':
            dbo.updateUserstatus(self.getUser().userid, 0)
            messagebox.showinfo(
                'Account reactivated!',
                'You can now login to get access to Paddles!')
        else:
            messagebox.showinfo(
                'Invalid access',
                'You will need to reactivate account to get access to Paddles!')


class SignupPage():
    def __init__(self, master=None):
        self.root = master
        self.root.geometry(CONSTANT.WINDOWS_SIZE)
        self.root.title('Signup')
        self.username = StringVar()
        self.email = StringVar()
        self.password = StringVar()
        self.page = Frame(self.root)
        self.createPage()

    def createPage(self):
        self.page.pack(pady=180)

        Label(self.page).grid(row=0, stick=W)

        Label(self.page, text='Username:').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=E)

        Label(self.page, text='Email:').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.email).grid(row=2, column=1, stick=E)

        Label(self.page, text='Password:').grid(row=3, stick=W, pady=10)
        Entry(self.page, textvariable=self.password, show='*').grid(row=3, column=1, stick=E)

        Button(self.page, text='Create', command=self.signupUser).grid(row=4, stick=W, pady=10)
        Button(self.page, text='Back', command=self.gotoLoginPage).grid(row=4, column=1, stick=E)

    def gotoLoginPage(self):
        self.page.destroy()
        LoginPage(self.root)

    def signupUser(self):
        username = self.username.get()
        email = self.email.get()
        password = self.password.get()
        symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
        passwdFlag = True
        text = ''

        if not any(char in symbols for char in password):
            passwdFlag = False
        text += '*Invalid Password. Make sure at least one special character is present!\n '

        if "@" in email and ".com" in email:
            emailFlag = True
        else:
            emailFlag = False
        text += '*Invalid emaiid!\n'

        if len(username) != 0:
            usernameFlag = True
        else:
            usernameFlag = False
        text += "*User name cannot be empty!\n"

        if usernameFlag and passwdFlag and emailFlag:
            result = dbo.insertTousers(username, email, password)
            if result == 1:
                messagebox.showinfo(title='Account Create', message='Successfully!', type='ok')
                self.gotoLoginPage()
            else:
                messagebox.showinfo(title='Account Create', message='Signup failed! Username already present', type='ok')
        else:
            messagebox.showinfo(title='Account Create', message=text, type='ok')


if __name__ == '__main__':
    root = Tk()
    LoginPage(root)
    root.mainloop()
