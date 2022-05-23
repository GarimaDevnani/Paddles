from tkinter import ttk
from tkinter import Button

import page_login_signup as login
import page_operator as operator
import page_customer as customer
import page_manager as manager

import constant as con


class TabbedView():
    def __init__(self, master=None, user=None):
        self.root = master
        self.user = user
        self.root.geometry(con.WINDOWS_SIZE)
        self.root.title('Paddles')
        self.tabControl = ttk.Notebook(self.root)
        self.logout = Button(self.root, text="Log out", command=self.logout)
        self.createPage()

    def createPage(self):
        custTab = ttk.Frame(self.tabControl)
        operTab = ttk.Frame(self.tabControl)
        mgrTab = ttk.Frame(self.tabControl)

        userPermission = self.user.permission
        if userPermission == 'CUST':
            self.tabControl.add(custTab, text='Customer')
        elif userPermission == 'OPER':
            self.tabControl.add(custTab, text='Customer')
            self.tabControl.add(operTab, text='Operator')
        else:
            self.tabControl.add(custTab, text='Customer')
            self.tabControl.add(operTab, text='Operator')
            self.tabControl.add(mgrTab, text='Manager')

        self.tabControl.pack(expand=1, fill="both")

        # Embed screens for each tabs
        self.addCustomerView(custTab)
        self.addOperatorPage(operTab)
        self.addManagerView(mgrTab)

        self.logout.pack(padx=30, pady=20)

    def logout(self):
        self.tabControl.destroy()
        self.logout.destroy()
        login.LoginPage(self.root)

    def addOperatorPage(self, frame):
        operator.Operator(frame, self.user)

    def addCustomerView(self, frame):
        customer.Homepage(frame, self.user, self.root)

    def addManagerView(self, frame):
        manager.Manager(frame, self.user, self.root)
