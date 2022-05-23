from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

import constant as CON
import dbo_manager as mgrdb

LOCATIONS = np.copy(CON.LOCATION)
LOCATIONS = np.concatenate([['SELECT'], LOCATIONS]).tolist()
CHARTS = ['Select', 'No. of bikes rented', 'No. of bikes reported defective',
          'No. of bikes fixed', 'Frequency of locations used']


class Manager():
    def __init__(self, master=None, user=None, super=None):
        self.root = master
        self.super = super
        self.user = user
        self.page = Frame(self.root, padx=30, pady=10)
        self.chart_list = ttk.Combobox(self.page, state="readonly", values=CHARTS)
        self.location_list = ttk.Combobox(self.page, state="readonly", values=LOCATIONS)
        self.chart_frame = Frame(self.page)
        self.createPage()

    def disableLocation(self, eventObject):
        if self.chart_list.current() == 4:
            self.location_list['state'] = 'disabled'
        else:
            self.location_list['state'] = 'readonly'

    def createPage(self):
        self.page.pack(side=TOP)

        chart_label = Label(self.page, text='Chart Type: ')
        chart_label.grid(row=0, column=0)
        self.chart_list.current(0)
        self.chart_list.bind("<<ComboboxSelected>>", self.disableLocation)
        self.chart_list.grid(row=0, column=1)

        location_label = Label(self.page, text='From Location: ')
        location_label.grid(row=1, column=0)
        self.location_list.current(0)
        self.location_list.grid(row=1, column=1)

        start_date_label = Label(self.page, text='Start Date (MM/DD/YYYY): ')
        start_date_label.grid(row=2, column=0)
        start_date = DateEntry(self.page, width=12, background='darkblue', foreground='white', borderwidth=2,
                               date_pattern='MM/dd/yyyy')
        start_date.grid(row=2, column=1)

        end_date_label = Label(self.page, text='End Date (MM/DD/YYYY):')
        end_date_label.grid(row=3, column=0)
        end_date = DateEntry(self.page, width=12, background='darkblue', foreground='white', borderwidth=2,
                             date_pattern='MM/dd/yyyy')
        end_date.grid(row=3, column=1)

        displayBtn = Button(self.page, text='Display',
                            command=lambda: self.showChart(
                                self.chart_list.current(),
                                start_date.get_date(),  # returns in yyyy-mm-dd format
                                end_date.get_date(),  # returns in yyyy-mm-dd format
                                self.location_list.get() if self.location_list.get() != 'SELECT' else None
                            )
                            )
        displayBtn.grid(row=4, column=1, padx=30, pady=10)

        self.chart_frame.grid(row=5, column=0, columnspan=2)

    def showChart(self, chart_index, start_date, end_date, location=None):
        self.clearChart(self.chart_frame)
        if start_date <= end_date:
            self.createChart(chart_index, start_date, end_date, location)
        else:
            messagebox.showerror(title="Invalid dates",
                                 message="Start date cannot be after end date",
                                 type="ok")

    def createChart(self, chart_index, start_date, end_date, location=None):
        if chart_index == 0:
            messagebox.showwarning(title="Invalid choice",
                                   message="You have not selected any chart type to display",
                                   type="ok")
        elif chart_index == 1:
            self.bikesRented(start_date, end_date, location)
        elif chart_index == 2:
            self.bikesReported(start_date, end_date, location)
        elif chart_index == 3:
            self.bikesFixed(start_date, end_date, location)
        elif chart_index == 4:
            self.mostToLeastUsedLocation(start_date, end_date)

    def bikesRented(self, start_date, end_date, location=None):
        if location is None:
            results = mgrdb.getNoOfBikesRentedBetween(start_date, end_date)
        else:
            results = mgrdb.getNoOfBikesRentedBetweenWith(start_date, end_date, location)

        if len(results) != 0:
            title = f"No. of Bikes rented between {start_date} and {end_date}" if location is None else \
                f"No. of Bikes rented between {start_date} and {end_date} at {location} station"
            ax, canvas = self.createFigure()
            df = pd.DataFrame(results, columns=['bikes', 'start_date'])
            df1 = df[['bikes', 'start_date']].groupby('start_date').sum()
            df1.plot(kind='barh', ax=ax)
            ax.set_xlabel('No. of Bikes')
            ax.set_yticklabels(df['start_date'], rotation=45, ha='right')
            ax.set_ylabel('Date Rented')
            ax.legend(['Frequency of bikes rented'])
            ax.set_title(title, wrap=True)
            self.createToolbar(canvas)
        else:
            if location is None:
                message = f"No bikes were rented between {start_date} and {end_date}"
            else:
                message = f"No bikes were rented between {start_date} and {end_date} at {location} station"
            self.handleEmptyResults(message)

    def bikesReported(self, start_date, end_date, location=None):
        if location is None:
            results = mgrdb.getNoOfBikesReportedBetween(start_date, end_date)
        else:
            results = mgrdb.getNoOfBikesReportedBetweenWith(start_date, end_date, location)

        if len(results) != 0:
            title = f"No. of Bikes reported between {start_date} and {end_date}" if location is None else \
                f"No. of Bikes reported between {start_date} and {end_date} at {location} station"
            ax, canvas = self.createFigure()
            df = pd.DataFrame(results, columns=['bikes', 'report_date'])
            df1 = df[['bikes', 'report_date']].groupby('report_date').sum()
            df1.plot(kind='barh', ax=ax)
            ax.set_xlabel('No. of Bikes')
            ax.set_yticklabels(df['report_date'], rotation=45, ha='right')
            ax.set_ylabel('Date reported')
            ax.legend(['Frequency of bikes reported'])
            ax.set_title(title, wrap=True)
        else:
            message = f"No bikes were reported between {start_date} and {end_date}" if location is None else \
                f"No bikes were reported between {start_date} and {end_date} at {location} station"
            self.handleEmptyResults(message)

    def bikesFixed(self, start_date, end_date, location=None):
        if location is None:
            results = mgrdb.getNoOfBikesFixedBetween(start_date, end_date)
        else:
            results = mgrdb.getNoOfBikesFixedBetweenWith(start_date, end_date, location)

        if len(results) != 0:
            title = f"No. of Bikes fixed between {start_date} and {end_date}" if location is None else \
                f"No. of Bikes fixed between {start_date} and {end_date} at {location} station"
            ax, canvas = self.createFigure()
            df = pd.DataFrame(results, columns=['bikes', 'fix_date'])
            df1 = df[['bikes', 'fix_date']].groupby('fix_date').sum()
            df1.plot(kind='barh', ax=ax)
            ax.set_xlabel('No. of Bikes')
            ax.set_yticklabels(df['fix_date'], rotation=45, ha='right')
            ax.set_ylabel('Date fixed')
            ax.legend(['Frequency of bikes fixed'])
            ax.set_title(title, wrap=True)
        else:
            message = f"No bikes were fixed between {start_date} and {end_date}" if location is None else \
                f"No bikes were fixed between {start_date} and {end_date} at {location} station"
            self.handleEmptyResults(message)

    def mostToLeastUsedLocation(self, start_date, end_date):
        results = mgrdb.getMostToLeastUsedLocation(start_date, end_date)

        if len(results) != 0:
            ax, canvas = self.createFigure()
            df = pd.DataFrame(results, columns=['bikes', 'location'])
            df1 = df[['bikes', 'location']].groupby('location').sum()
            df1.plot(kind='barh', ax=ax)
            ax.legend(['Frequency of bikes rented across locations'])
            ax.set_xlabel('No. of Bikes')
            ax.set_ylabel('Locations (Bikes rented from)')
            ax.set_yticklabels(df['location'], rotation=45, ha='right')
            ax.set_title(f'Most to least used locations between {start_date} and {end_date}', wrap=True)
        else:
            message = f"None of the locations have been used to rent bikes between {start_date} and {end_date}"
            self.handleEmptyResults(message)

    def clearChart(self, frame):
        # clearing frame to display the new one
        for widget in frame.winfo_children():
            widget.destroy()

    def handleEmptyResults(self, message):
        messagebox.showerror(title="No data available!",
                             message=message,
                             type="ok")

    def createFigure(self):
        figure = plt.Figure(figsize=(6, 6), dpi=100)
        ax = figure.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure, self.chart_frame)
        canvas.get_tk_widget().pack(side=LEFT, fill=BOTH)
        return ax, canvas

    def createToolbar(self, canvas):
        # setup toolbar
        toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
