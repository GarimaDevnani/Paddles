import datetime
import time
import tkinter
import tkinter.messagebox
from tkinter import *
import constant as CON

from tkinter import ttk
import dbo_login_signup as dbo
import page_login_signup as pageL


class Bikes():
    def __int__(self):
        self.bikeid = 0
        self.bikelocation = ''
        self.bikestate = ''

    def show(self):
        print((self.bikeid, self.bikelocation, self.bikestate))


class Logs():
    def __int__(self):
        self.logid = -1
        self.userid = -1
        self.bikeid = -1
        self.datestart = ''
        self.dateend = ''
        self.rentfrom = ''
        self.returnto = ''
        self.price = -1

    def show(self):
        pass


class Homepage():
    def __init__(self, master=None, user=None, super=None):
        self.root = master
        self.super = super
        self.page = Frame(self.root)
        self.user = user
        self.createPage()

    def createPage(self):
        self.page.pack(side=TOP, pady=10)
        Label(self.page).grid(row=0, stick=W)

        Label(self.page, text=f'Hi, {self.user.username}. Welcome to Paddles.').grid(row=1, stick=W, pady=10)

        Label(self.page, text='Balance:').grid(row=2, stick=W, pady=10)
        Label(self.page, text=f'￡ {round(self.user.balance, 2)}').grid(row=2, column=1, stick=E)

        Label(self.page, text='Rent History:').grid(row=3, stick=W, pady=10)

        self.tree = ttk.Treeview(self.root)
        self.tree.pack()
        self.tree['columns'] = ('DateStart', 'DateEnd', 'RentFrom', 'ReturnTo', 'Price')
        self.tree.column('DateStart', width=80)
        self.tree.column('DateEnd', width=80)
        self.tree.column('RentFrom', width=80)
        self.tree.column('ReturnTo', width=80)
        self.tree.column('Price', width=80)

        self.tree.heading('DateStart', text='DateStart')
        self.tree.heading('DateEnd', text='DateEnd')
        self.tree.heading('RentFrom', text='RentFrom')
        self.tree.heading('ReturnTo', text='ReturnTo')
        self.tree.heading('Price', text='Price')
        try:
            logs = self.getRentHistory()
            count = 1
            for log in logs:
                self.tree.insert('', count, text=f'{count}.', values=(log[0][:11], log[1][:11], log[2], log[3], log[4]))
                count += 1
        except:
            pass

        self.frame = Frame(self.root)
        Button(self.frame, text='HOME').grid(row=3, column=0, pady=10)
        Button(self.frame, text='ADD FUNDS', command=self.gotoAddFundsPage).grid(row=3, column=1, pady=10)
        Button(self.frame, text='RENT', command=self.gotoRentPage).grid(row=3, column=2, pady=10)
        Button(self.frame, text='STATUS', command=self.gotoStatusPage).grid(row=3, column=3, pady=10)
        self.frame.pack(pady=50)

        self.deactivate = Frame(self.root)
        Button(self.deactivate, text='DEACTIVATE ACCOUNT', command=self.gotoDeactivate).grid(row=0, column=1, pady=10)
        self.deactivate.pack(pady=50)

    def getRentHistory(self):
        return dbo.getRentHistory(self.user.userid)

    def gotoHomePage(self):
        self.page.destroy()
        self.frame.destroy()
        self.deactivate.destroy()
        try:
            self.tree.destroy()
        except:
            pass
        Homepage(self.root, self.user)

    def gotoAddFundsPage(self):
        self.page.destroy()
        self.frame.destroy()
        self.deactivate.destroy()
        try:
            self.tree.destroy()
        except:
            pass
        Addfundspage(self.root, self.user)

    def gotoRentPage(self):
        self.page.destroy()
        self.frame.destroy()
        self.deactivate.destroy()
        try:
            self.tree.destroy()
        except:
            pass
        Rentpage(self.root, self.user)

    def gotoStatusPage(self):
        self.page.destroy()
        self.frame.destroy()
        self.deactivate.destroy()
        try:
            self.tree.destroy()
        except:
            pass
        Statuspage(self.root, self.user)

    def gotoDeactivate(self):
        dbo.updateUserstatus(self.user.userid, -1)
        self.logout()

    def logout(self):
        for widgets in self.super.winfo_children():
            widgets.destroy()
        pageL.LoginPage(self.super)


class Addfundspage():
    def __init__(self, master=None, user=None):
        self.root = master
        self.page = Frame(self.root)
        self.user = user
        self.amount = StringVar()
        self.createPage()

    def createPage(self):
        self.page.pack(side=TOP, pady=50)

        Label(self.page).grid(row=0, stick=W)

        Label(self.page, text='Current Balance:').grid(row=1, stick=W, pady=10)
        Label(self.page, text=f'￡ {round(self.user.balance, 2)}').grid(row=1, column=1, stick=E)

        Label(self.page, text='Amount: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.amount).grid(row=2, column=1, stick=E, pady=10)

        Button(self.page, text='CREDIT/DEBIT CARD', command=self.gotoPayPage).grid(row=3, pady=10)

        self.frame = Frame(self.root)
        Button(self.frame, text='HOME', command=self.gotoHomePage).grid(row=0, column=0, pady=10)
        Button(self.frame, text='ADD FUNDS').grid(row=0, column=1, pady=10)
        Button(self.frame, text='RENT', command=self.gotoRentPage).grid(row=0, column=2, pady=10)
        Button(self.frame, text='STATUS', command=self.gotoStatusPage).grid(row=0, column=3, pady=10)
        self.frame.pack(pady=50)

    def gotoPayPage(self):
        if self.amount.get() == '':
            tkinter.messagebox.showinfo(title='Pay Amount', message='Please enter the amount!', type='ok')
        else:
            try:
                amount = float(self.amount.get())
                if amount > 0.0:
                    self.page.destroy()
                    self.frame.destroy()
                    Paypage(self.root, self.user, amount)
                else:
                    tkinter.messagebox.showinfo(title='Pay Error', message='Please enter positive amount.', type='ok')
            except:
                tkinter.messagebox.showinfo(title='Pay Error', message='Please enter the number.', type='ok')

    def gotoHomePage(self):
        self.page.destroy()
        self.frame.destroy()
        Homepage(self.root, self.user)

    def gotoRentPage(self):
        self.page.destroy()
        self.frame.destroy()
        Rentpage(self.root, self.user)

    def gotoStatusPage(self):
        self.page.destroy()
        self.frame.destroy()
        Statuspage(self.root, self.user)


class Paypage():
    def __init__(self, master=None, user=None, amount=None):
        self.root = master
        self.page = Frame(self.root)
        self.amount = amount
        self.user = user
        self.cardnumber = StringVar()
        self.expirationdate = StringVar()
        self.securitycode = StringVar()
        self.createPage()

    def createPage(self):
        self.page.pack(side=TOP, pady=50)

        Label(self.page).grid(row=0, stick=W)

        Label(self.page, text=f'Total: {self.amount} GBP').grid(row=1, pady=5)

        Label(self.page, text='Payment Information').grid(row=2, stick=W, pady=5)

        Label(self.page, text='Name on Card:').grid(row=3, stick=W, pady=10)
        Entry(self.page).grid(row=4, stick=W)

        Label(self.page, text='Card Number:').grid(row=5, stick=W, pady=10)
        Entry(self.page, textvariable=self.cardnumber).grid(row=6, stick=W)

        Label(self.page, text='Expiration Date:').grid(row=7, stick=W, pady=10)
        Entry(self.page, textvariable=self.expirationdate).grid(row=8, stick=W)

        Label(self.page, text='Security Code:').grid(row=9, stick=W, pady=10)
        Entry(self.page, textvariable=self.securitycode).grid(row=10, stick=W)

        Button(self.page, text='Pay', command=self.judgePaymentInfo).grid(row=11, stick=W, pady=15)
        Button(self.page, text='Back', command=self.gotoAddFundsPage).grid(row=11, column=1, stick=E, pady=15)

    def judgePaymentInfo(self):
        try:
            self.user.balance += float(self.amount)
            dbo.updateUserbalance(self.user.userid, self.user.balance)
            self.gotoHomePage()
        except:
            tkinter.messagebox.showinfo(title='Pay Error', message='Please enter the number.', type='ok')
            self.gotoAddFundsPage()

    def gotoHomePage(self):
        self.page.destroy()
        Homepage(self.root, self.user)

    def gotoAddFundsPage(self):
        self.page.destroy()
        Addfundspage(self.root, self.user)


class Rentpage():
    def __init__(self, master=None, user=None):
        self.root = master
        self.user = user
        self.page_index = -1
        self.bikes = []
        self.isRentbyMin = 'True'
        self.listbox_value = StringVar()
        self.location_index = IntVar()
        self.page = Frame(self.root)
        self.createPage()

    def createPage(self):
        self.page.pack(side=TOP, pady=50)

        if self.user.userstatus == 0 and self.user.balance <= 0:
            Label(self.page, text='You do not have enough money!').grid()
        if self.user.userstatus != 0 and self.user.balance <= 0:
            Label(self.page, text='You already have one bike in use!').grid()
        if self.user.userstatus != 0 and self.user.balance > 0:
            Label(self.page, text='You already have one bike in use!').grid()
        if self.user.userstatus == 0 and self.user.balance > 0:
            self.page.destroy()

            self.page = Frame(self.root)
            self.page.pack(side=TOP, pady=50)

            Label(self.page, text='Where do you rent a bike from?(5 penny per minute/ 58 pound one day)').grid(row=0,
                                                                                                               pady=10)
            Button(self.page, text='Rent by minute', command=self.chooseBike).grid(row=1, column=0, pady=10,
                                                                                   sticky=tkinter.W)
            Button(self.page, text='Rent by Day', command=self.chooseBikeByDay).grid(row=1, column=1, pady=10,
                                                                                     sticky=tkinter.W)
            for i in range(5):
                Radiobutton(self.page, variable=self.location_index, text=CON.LOCATION[i], value=i).grid(
                    sticky=tkinter.W)

        self.frame = Frame(self.root)
        self.frame.pack(pady=50)
        Button(self.frame, text='HOME', command=self.gotoHomePage).grid(row=0, column=0, pady=10)
        Button(self.frame, text='ADD FUNDS', command=self.gotoAddFundsPage).grid(row=0, column=1, pady=10)
        Button(self.frame, text='RENT').grid(row=0, column=2, pady=10)
        Button(self.frame, text='STATUS', command=self.gotoStatusPage).grid(row=0, column=3, pady=10)


    def createBikeChoosePage(self):
        self.page.destroy()
        self.frame.destroy()

        self.page = Frame(self.root)
        self.page.pack(side=TOP, pady=50)

        if self.page_index == 0:
            Label(self.page, text='Sorry, there are currently no available vehicles in this area.').grid()
            Button(self.page, text='Back', command=self.gotoRentPage).grid()
        elif self.page_index == 1:
            Label(self.page, text='Please choose your bike: ').grid()
            self.listbox = tkinter.Listbox(self.root)
            self.listbox.pack()

            count = 1
            for bike in self.bikes:
                self.listbox.insert(tkinter.END, f'{count}. {bike.bikestate}')
                count += 1

            Button(self.page, text='Confirm', command=self.confirm).grid()
        else:
            Label(self.page, text='Program error, please try again.').grid()
            Button(self.page, text='Back', command=self.gotoRentPage).grid()

        self.frame = Frame(self.root)
        self.frame.pack(pady=50)
        Button(self.frame, text='HOME', command=self.gotoHomePage).grid(row=0, column=0, pady=10)
        Button(self.frame, text='ADD FUNDS', command=self.gotoAddFundsPage).grid(row=0, column=1, pady=10)
        Button(self.frame, text='RENT', command=self.gotoRentPage).grid(row=0, column=2, pady=10)
        Button(self.frame, text='STATUS', command=self.gotoStatusPage).grid(row=0, column=3, pady=10)

    def confirm(self):
        try:
            self.getListBoxValue()
            self.writeLog()
            logid = self.getLogid()
            self.user.userstatus = logid
            self.changeUserstatus(logid)
            self.changeBikelocation()
            self.gotoStatusPage()
        except:
            tkinter.messagebox.showinfo(title='Rent Error', message='Please select the bike', type='ok')

    def writeLog(self):
        bikeid = self.bikes[int(self.listbox_value[0]) - 1].bikeid
        bikelocation = self.bikes[int(self.listbox_value[0]) - 1].bikelocation
        if self.isRentbyMin == 'True':
            dbo.insertTologs(self.user.userid, bikeid, bikelocation)
        else:
            dbo.insertTologsbyDay(self.user.userid, bikeid, bikelocation)

    def getLogid(self):
        result = dbo.getLogid(self.user.userid)
        logid = int(result[-1][0])
        return logid

    def changeUserstatus(self, logid):
        dbo.updateUserstatus(self.user.userid, logid)

    def changeBikelocation(self):
        bikeid = self.bikes[int(self.listbox_value[0]) - 1].bikeid
        dbo.updateBikeLocation(bikeid)

    def getListBoxValue(self):
        try:
            self.listbox_value = self.listbox.get(self.listbox.curselection())
            # print(self.listbox_value[0])
        except:
            pass

    def chooseBikeByDay(self):
        if self.user.balance >= 58.0:
            self.isRentbyMin = 'False'
            self.chooseBike()
        else:
            tkinter.messagebox.showinfo(title='Pay Error', message='Not Enough Wallet amount to rent bike for day!.', type='ok')

    def chooseBike(self):
        bikes = dbo.getLocationBikes(CON.LOCATION[self.location_index.get()])
        bike_num = len(bikes)

        if bike_num == 0:
            self.page_index = 0
        else:
            self.page_index = 1

        for bike in bikes:
            b = Bikes()
            b.bikeid = bike[0]
            b.bikelocation = CON.LOCATION[self.location_index.get()]
            b.bikestate = bike[1]
            if b.bikestate == 'AVAILABLE':
                self.bikes.append(b)

        self.createBikeChoosePage()

    def gotoRentPage(self):
        self.page.destroy()
        self.frame.destroy()
        try:
            self.listbox.destroy()
        except:
            pass
        Rentpage(self.root, self.user)

    def gotoHomePage(self):
        self.page.destroy()
        self.frame.destroy()
        try:
            self.listbox.destroy()
        except:
            pass
        Homepage(self.root, self.user)

    def gotoAddFundsPage(self):
        self.page.destroy()
        self.frame.destroy()
        try:
            self.listbox.destroy()
        except:
            pass
        Addfundspage(self.root, self.user)

    def gotoStatusPage(self):
        self.page.destroy()
        self.frame.destroy()
        try:
            self.listbox.destroy()
        except:
            pass
        Statuspage(self.root, self.user)


class Statuspage():
    def __init__(self, master=None, user=None):
        self.root = master
        self.user = user
        self.log = Logs()
        self.isRentbyMin = 'True'
        self.hour = 0
        self.amount = 0
        self.location_index = IntVar()
        self.page = Frame(self.root)
        self.statusFrame = Frame(self.page)
        self.blank = tkinter.Label(self.statusFrame, text='')
        self.clock = tkinter.Label(self.statusFrame, text='')
        self.price = tkinter.Label(self.statusFrame, text='')
        self.getLog()
        self.createPage()

    def createPage(self):

        if self.log.userid == -1:
            self.page.pack()
            Label(self.page).grid(row=0, stick=W)
            Label(self.page, text='')
            Label(self.page, text='You do not have any bike in use.').grid()
        else:
            self.blank.pack(side=TOP, pady=10)
            self.clock.pack()
            self.price.pack()
            self.update_clock()
            self.statusFrame.pack()

            self.page.pack()
            Button(self.page, text='Return', command=lambda: self.returnBike(False)).pack(pady=10, padx=30)
            Button(self.page, text='Report', command=lambda: self.returnBike(True)).pack(pady=10, padx=30)

        self.frame = Frame(self.root)
        self.frame.pack(pady=50)
        Button(self.frame, text='HOME', command=self.gotoHomePage).grid(row=0, column=0, pady=10)
        Button(self.frame, text='ADD FUNDS', command=self.gotoAddFundsPage).grid(row=0, column=1, pady=10)
        Button(self.frame, text='RENT', command=self.gotoRentPage).grid(row=0, column=2, pady=10)
        Button(self.frame, text='STATUS', command=self.gotoStatusPage).grid(row=0, column=3, pady=10)

    def update_clock(self):
        hour = 0
        minute = 0
        second = 0

        past = self.log.datestart
        now = time.strftime('%Y-%m-%d %H:%M:%S')

        second = int(now[17:19]) - int(past[17:19])
        if second < 0:
            second += 60
            minute -= 1
        minute = int(now[14:16]) - int(past[14:16])
        if minute < 0:
            minute += 60
            hour -= 1
        hour = int(now[11:13]) - int(past[11:13])
        if hour < 0:
            hour += 24
        if int(now[8:10]) - int(past[8:10]) > 1:
            hour = 24
            second = 0
            minute = 0
        if now[0:4] != past[0:4] or now[5:7] != past[5:7]:
            hour = 24
            second = 0
            minute = 0

        self.log.price = round((hour * 60 + minute) * 0.05, 2)

        try:
            self.clock.configure(text=f'Used Time: {hour}:{minute}:{second}')
            self.price.configure(text=f'Price: ￡ {self.log.price}')
            self.root.after(1000, self.update_clock)
        except:
            pass

    def returnBike(self, isReported=False):
        self.returnBikePage(isReported)

    def returnBikePage(self, isReported=False):
        self.page.destroy()
        self.frame.destroy()
        try:
            self.blank.destroy()
            self.clock.destroy()
            self.price.destroy()
        except:
            pass

        self.page = Frame(self.root)
        self.page.pack(side=TOP, pady=50)
        Label(self.page, text='Where do you return the bike to?').grid()
        for i in range(5):
            Radiobutton(self.page, variable=self.location_index, text=CON.LOCATION[i], value=i).grid(sticky=tkinter.W)
        Button(self.page, text='Confirm', command=lambda: self.chooseRentLocation(isReported)).grid()

        self.frame = Frame(self.root)
        Button(self.frame, text='HOME', command=self.gotoHomePage).grid(row=0, column=0, pady=10)
        Button(self.frame, text='ADD FUNDS', command=self.gotoAddFundsPage).grid(row=0, column=1, pady=10)
        Button(self.frame, text='RENT', command=self.gotoRentPage).grid(row=0, column=2, pady=10)
        Button(self.frame, text='STATUS', command=self.gotoStatusPage).grid(row=0, column=3, pady=10)
        self.frame.pack(pady=50)

    def chooseRentLocation(self, isReported=False):
        location = CON.LOCATION[self.location_index.get()]
        dbo.updateBikelocation_withbikelocation(self.log.bikeid, location)
        dbo.updateLogdateend_returnto(self.log.logid, location)
        dbo.emptyUserstatus(self.log.userid)
        self.user.balance -= self.log.price
        dbo.updateUserbalance(self.user.userid, self.user.balance)
        dbo.updateLogprice(self.log.logid, self.log.price)
        self.user.userstatus = 0
        if isReported:
            self.reportError(location)
        self.gotoHomePage()

    def reportError(self, location):
        if self.isRentbyMin != 'True':
            if self.hour > 24:
                self.log.price = self.amount
            else:
                if self.amount > 58:
                    self.log.price = 58
                else:
                    self.log.price = self.amount

        dbo.updateBikestate(self.log.bikeid)
        dbo.reportError(self.log.logid, self.log.userid, self.log.bikeid, location)

    def getLog(self):
        result = dbo.getLoginfo(self.user.userstatus)
        if not result:
            self.log.userid = -1
        else:
            self.log.logid = self.user.userstatus
            self.log.userid = result[0][0]
            self.log.bikeid = result[0][1]
            self.log.datestart = result[0][2]
            self.log.dateend = result[0][3]
            self.log.rentfrom = result[0][4]
            self.log.returnto = result[0][5]
            self.log.price = result[0][6]
        try:
            if self.log.price == 58:
                self.isRentbyMin = 'False'
        except:
            pass

    def gotoHomePage(self):
        self.page.destroy()
        self.frame.destroy()
        try:
            self.blank.destroy()
            self.clock.destroy()
            self.price.destroy()
        except:
            pass
        Homepage(self.root, self.user)

    def gotoStatusPage(self):
        self.page.destroy()
        self.frame.destroy()
        try:
            self.blank.destroy()
            self.clock.destroy()
            self.price.destroy()
        except:
            pass
        Statuspage(self.root, self.user)

    def gotoAddFundsPage(self):
        self.page.destroy()
        self.frame.destroy()
        try:
            self.blank.destroy()
            self.clock.destroy()
            self.price.destroy()
        except:
            pass
        Addfundspage(self.root, self.user)

    def gotoRentPage(self):
        self.page.destroy()
        self.frame.destroy()
        try:
            self.blank.destroy()
            self.clock.destroy()
            self.price.destroy()
        except:
            pass
        Rentpage(self.root, self.user)
