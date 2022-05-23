import sqlite3
from tksheet import Sheet
from tkinter import *
from tkinter import ttk, messagebox
import constant as con
import datetime


class Operator():
    def __init__(self, master=None, user=None):
        self.root = master
        self.user = user
        self.page = Frame(self.root)
        self.mytablelist = Sheet(self.page)
        self.drop_location_list = ttk.Combobox(self.page, state="readonly", values=con.LOCATION)
        self.drop_location_list.current(0)
        self.op_page()
        self.table_initail()

    def create_new(self):
        with sqlite3.connect('Database/company.db') as db:
            cursor = db.cursor()
        cursor.execute("""Select MAX(bikeid) from bikes""")
        new_bikeid = cursor.fetchone()[0] + 1
        location = self.drop_location_list.get()
        cursor.execute("insert into bikes VALUES(?,?,?)", (new_bikeid, location, 'AVAILABLE'))
        db.commit()
        db.close()
        refreshOperator(self.root, self.user, self.page)
        messagebox.showinfo(message="New Bike added")

    def repair(self):
        def repair_btn():
            if len(repair_table.get_selected_rows(get_cells_as_rows=True)):
                selected_row = repair_table.get_selected_rows(get_cells_as_rows=True).pop()
                selected_data = repair_table.get_row_data(selected_row, return_copy=True)
                now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                now_time = now_time[0:-3]
                cursor.execute("update repairlog set operatorid=?,fixdate=? where logid=?",
                               (self.user.userid, now_time, selected_data[0]))
                db.commit()
                cursor.execute("update bikes set bikeState=? where bikeid=?",
                               ("AVAILABLE", selected_data[2]))
                db.commit()
                cursor.execute("""Select MAX(systemlogid) from systemlog""")
                new_sysid = cursor.fetchone()[0] + 1
                cursor.execute("insert into systemlog VALUES(?,?,?,?,?)",
                               (new_sysid, self.user.userid, selected_data[2], 'Repair', now_time))
                db.commit()
                messagebox.showinfo(message="Change Done")
                repair_window.destroy()
                refreshOperator(self.root, self.user, self.page)
            else:
                messagebox.showwarning(title="Warning", message="No selected bike")
                repair_window.destroy()
                refreshOperator(self.root, self.user, self.page)


        repair_window = Toplevel(self.page)
        repair_window.title("Repair Info")
        repair_window.geometry("700x700")
        label_info = Label(repair_window, text="Repair Table ")
        label_info.pack(padx=30, pady=40)
        repair_table = Sheet(repair_window)
        repair_table.enable_bindings(("single",
                                      "drag_select",
                                      "column_drag_and_drop",
                                      "column_select",
                                      "row_select",
                                      "arrowkeys",
                                      "column_width_resize",
                                      "row_width_resize",
                                      "copy",
                                      "rc_insert_column",
                                      "rc_insert_row"))
        headers = ("Logid", "Customerid", "bikeid", "Report time", "Location")
        repair_table.headers(headers)
        repair_table.pack(expand=1, fill="both")
        button_repair = Button(repair_window, text="Make Repair", command=repair_btn)
        button_repair.pack(padx=30, pady=40)
        try:
            with sqlite3.connect('Database/company.db') as db:
                cursor = db.cursor()
            cursor.execute(
                "SELECT logid,customerid,bikeid,reporteddate,reportlocation FROM repairlog where operatorid is null")
            h = len(cursor.fetchall())
            data = [[f"Row {r} Column {c}" for c in range(5)] for r in range(h)]
            repair_table.data_reference(data)
            data = cursor.execute(
                "SELECT logid,customerid,bikeid,reporteddate,reportlocation FROM repairlog where operatorid is null")
            rowcount = 0
            for row in data:
                repair_table.set_row_data(rowcount, values=row)
                rowcount += 1
            self.table_initail()

        except:
            messagebox.showinfo(message="Change in Database failed")

    def newwindow(self, data):
        def modify():
            loc = drop_loc_list.get()
            new_states = drop_state_list.get()
            if loc == data[1] and new_states == data[2]:
                messagebox.showinfo(message="No change")
            else:
                with sqlite3.connect('Database/company.db') as db:
                    cursor = db.cursor()
                cursor.execute("update bikes set bikelocation=?,bikestate=? where bikeid=?", (loc, new_states, data[0]))
                db.commit()
                syslog(cursor)
                db.commit()
                cursor.execute("""Select MAX(systemlogid) from systemlog""")
                new_sysid = cursor.fetchone()[0] + 1
                now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                now_time = now_time[0:-3]
                if bike_state_before == states[2] and new_states == states[0]:
                    cursor.execute("insert into systemlog VALUES(?,?,?,?,?)",
                                   (new_sysid, self.user.userid, data[0], 'Repair', now_time))
                    db.commit()
                elif bike_state_before == states[0] and new_states == states[2]:
                    cursor.execute("insert into systemlog VALUES(?,?,?,?,?)",
                                   (new_sysid, self.user.userid, data[0], 'DEFECTIVE', now_time))
                    db.commit()
                db.close()
                self.table_initail()
                messagebox.showinfo(message="Change done")
                new_window.destroy()
                refreshOperator(self.root, self.user, self.page)

        def syslog(cursor):
            if states == 'AVAILABLE' and data[2] == 'DEFECTIVE':
                cursor.execute("""Select MAX(systemlogid) from systemlog""")
                try:
                    new_sysid = cursor.fetchone()[0] + 1
                except:
                    new_sysid = 1
                now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                now_time = now_time[0:-3]
                cursor.execute("insert into systemlog VALUES(?,?,?,?,?)",
                               (new_sysid, self.user.userid, data[0], "R",
                                now_time))  # Userid !!!!!!!!!!!!!!!! to replace "1"

        new_window = Toplevel(self.page)
        new_window.title("Change Info")
        new_window.geometry("500x200")
        label1 = Label(new_window, text="Bike ID")
        label1.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.1, anchor='center')
        id_box = Entry(new_window, text="")
        id_box.place(relx=0.2, rely=0.4, relwidth=0.1, relheight=0.1, anchor='center')
        id_box["justify"] = "left"
        id_box.insert(END, str(data[0]))
        id_box['state'] = 'disable'

        label2 = Label(new_window, text="Location")
        label2.place(relx=0.5, rely=0.1, relwidth=0.1, relheight=0.1, anchor='center')
        drop_loc_list = ttk.Combobox(new_window, values=con.LOCATION)
        drop_loc_list.current(con.LOCATION.index(data[1]))
        drop_loc_list.place(relx=0.5, rely=0.4, relwidth=0.2, relheight=0.1, anchor='center')

        states = ["AVAILABLE", "UNAVAILABLE", "DEFECTIVE", "TRANSIT"]
        label3 = Label(new_window, text="Status")
        label3.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.1, anchor='center')
        drop_state_list = ttk.Combobox(new_window, values=states)
        drop_state_list.current(states.index(data[2]))
        bike_state_before = drop_state_list.get()
        drop_state_list.place(relx=0.8, rely=0.4, relwidth=0.2, relheight=0.1, anchor='center')

        btn_change = Button(new_window, text="Make change", command=modify)
        btn_change.place(relx=0.5, rely=0.6, relwidth=0.3, relheight=0.15, anchor='center')

    def change_bike(self):
        if len(self.mytablelist.get_selected_rows(get_cells_as_rows=True)):
            selected_row = self.mytablelist.get_selected_rows(get_cells_as_rows=True).pop()
            selected_data = self.mytablelist.get_row_data(selected_row, return_copy=True)
            self.newwindow(selected_data)
        else:
            messagebox.showwarning(title="Warning", message="No selected bike")

    def table_initail(self):
        with sqlite3.connect('Database/company.db') as db:
            cursor = db.cursor()
        self.mytablelist.enable_bindings(("single",
                                          "drag_select",
                                          "column_drag_and_drop",
                                          "column_select",
                                          "row_select",
                                          "arrowkeys",
                                          "column_width_resize",
                                          "row_width_resize",
                                          "copy",
                                          "rc_insert_column",
                                          "rc_insert_row"))
        self.mytablelist.grid(row=3, column=0, padx=30, pady=10, columnspan=3, sticky="nswe")
        headers = ("bikeid", "Location", "Status")
        self.mytablelist.headers(headers)
        cursor.execute("SELECT * FROM bikes")
        h = len(cursor.fetchall())
        data = [[f"Row {r} Column {c}" for c in range(3)] for r in range(h)]
        self.mytablelist.data_reference(data)
        data = cursor.execute("SELECT * FROM bikes")
        rowcount = 0
        for row in data:
            self.mytablelist.set_row_data(rowcount, values=row)
            rowcount += 1

    # ------------------------------------------------------------------------
    # below is main
    def op_page(self):

        self.page.pack(side=TOP, fill=BOTH, expand=1)
        label_loc = Label(self.page, text="Location ")
        label_loc.grid(row=0, column=0, padx=30, pady=10)

        self.drop_location_list.grid(row=0, column=1, padx=30, pady=10)

        button1 = Button(self.page, text="Add bike", command=self.create_new)
        button1.grid(row=0, column=2, padx=30, pady=10)

        label_table = Label(self.page, text="Bike Table ")
        label_table.grid(row=1, column=0)

        button3 = Button(self.page, text="Change bike", command=self.change_bike)
        button3.grid(row=1, column=1)
        button_repair = Button(self.page, text="Repair", command=self.repair)
        button_repair.grid(row=1, column=2)


def refreshOperator(root, user, page):
    root = root
    user = user
    page.destroy()
    Operator(root, user)