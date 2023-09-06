from tkinter import * 
import customtkinter 
from config.constants import DASHBOARD_TITLE
from config.url_resources import BACKEND_BASE_URL, STRESS_BLINK_DETECTOR, SRESS_BLINK_DATA_GET, GET_STEP_COUNT_END_POINT, GET_BOWSING_DETAILS, GET_ALERT_END_POINT
import os
import threading
import numpy as np
import requests 
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class DashBoardComponent: 
    def __init__(self, access_token : str = ""):
        self.access_token = access_token 
        self.activateFlag = False
        self.dashboardWindow = customtkinter.CTk()
        self.dashboardWindow.geometry("1200x700")
        self.dashboardWindow.resizable(False, False)
        self.dashboardWindow.title(DASHBOARD_TITLE)
        self.dashboardWindow.grid_rowconfigure(0, weight=1)
        self.dashboardWindow.grid_columnconfigure(1, weight=1)
        self.navigationFrame = customtkinter.CTkFrame(self.dashboardWindow, corner_radius=0, bg_color=("gray", "gray"))
        self.navigationFrame.grid(row = 0, column = 0, sticky = 'nsew')
        self.navigationFrame.grid_rowconfigure(10, weight=1)
        self.activate_btn = customtkinter.CTkButton(self.navigationFrame, text="Activate", compound="left", 
                        font=customtkinter.CTkFont(size=15, weight="bold"),fg_color='green', 
                        command=self.activate)
        self.activate_btn.grid(row=0, column=0, pady=30, padx = 30)
        ### btn list 
        self.alert_tile = customtkinter.CTkButton(self.navigationFrame, text = "Alerts", fg_color='transparent',font=customtkinter.CTkFont(size = 15),
                     text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), height=40, border_spacing=10,corner_radius=0, command=self.select_alert_tile)
        self.alert_tile.grid(row = 1, column = 0, sticky = 'ew', pady = 10)
        
        self.stress_tile = customtkinter.CTkButton(self.navigationFrame, text = "Blink Rate", fg_color='transparent', font = customtkinter.CTkFont(size = 15),
                    text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), height=40, border_spacing=10,width=200, corner_radius=0, command=self.select_stress_tile )
        self.stress_tile.grid(row = 2, column = 0, sticky = 'ew', pady = 10)

        self.step_count = customtkinter.CTkButton(self.navigationFrame, text = "Step Count", fg_color='transparent', font = customtkinter.CTkFont(size = 15),
                    text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), height=40, border_spacing=10,width=200,  corner_radius=0, command=self.select_step_count_tile)
        self.step_count.grid(row = 3, column = 0, sticky = 'ew', pady = 10)
        self.browsing_classification = customtkinter.CTkButton(self.navigationFrame, text = "Browsing Pattern", fg_color='transparent', font = customtkinter.CTkFont(size = 15),
                    text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), height=40, border_spacing=10,width=200,  corner_radius=0, command=self.select_browsing_title)
        self.browsing_classification.grid(row = 4, column = 0, sticky = 'ew', pady = 10)
        self.alert_frame = customtkinter.CTkFrame(master = self.dashboardWindow)
        self.alert_label = customtkinter.CTkLabel(master = self.alert_frame, text = 'Alert Tab', font = customtkinter.CTkFont(size = 30))
        self.alert_label.place(relx = 0.05, rely = 0.1)
        self.stress_frame = customtkinter.CTkFrame(master = self.dashboardWindow)
        self.stress_frame_label = customtkinter.CTkLabel(master = self.stress_frame, text = 'Stress Level', font = customtkinter.CTkFont(size = 30))
        self.stress_frame_label.place(relx = 0.05, rely = 0.05)
        self.blink_frame_label = customtkinter.CTkLabel(master = self.stress_frame, text = "Blink Rate", font = customtkinter.CTkFont(size =30))
        self.blink_frame_label.place(relx = 0.05, rely = 0.54)
        self.step_count_frame = customtkinter.CTkFrame(master = self.dashboardWindow)
        self.step_count_frame_label = customtkinter.CTkLabel(master = self.step_count_frame, text = "Step Count Tab", font = customtkinter.CTkFont(size = 30))
        self.step_count_frame_label.place(relx = 0.05, rely = 0.1)
        self.browsing_frame = customtkinter.CTkFrame(master = self.dashboardWindow)
        self.browsing_frame_label = customtkinter.CTkLabel(master = self.browsing_frame, text = "Browsing Pattern Tab", font = customtkinter.CTkFont(size = 30))
        self.browsing_frame_label.place(relx = 0.05, rely = 0.1)
        self.select_by_name("alert")



    def render(self): 
        self.dashboardWindow.mainloop()

    def activate(self):
        if self.activateFlag:
            self.activateFlag = False
            self.activate_btn.configure(text = "Activate")
            self.activate_btn.configure(fg_color = 'green')
        else:
            self.activateFlag = True
            thread = threading.Thread(target=os.system("python3 " + STRESS_BLINK_DETECTOR + " --access-token " + f"{self.access_token}"))
            thread.start()
            self.activate_btn.configure(text = "DeActivate")
            self.activate_btn.configure(fg_color = 'red')
        

    def select_by_name(self, name : str): 
        self.alert_tile.configure(fg_color = ("gray75", "gray25") if name == "alert" else "transparent")
        self.stress_tile.configure(fg_color = ("gray75", "gray25") if name == "stress" else "transparent")
        self.step_count.configure(fg_color = ("gray75", "gray25") if name == "step_count" else "transparent")
        self.browsing_classification.configure(fg_color = ("gray75", "gray25") if name == "browsing" else "transparent")
        if name == "alert":
            res = requests.post(BACKEND_BASE_URL + GET_ALERT_END_POINT, json = {
                'access_token': self.access_token
            }) 
            data = res.json()['data']
            print(data)
            frame = customtkinter.CTkFrame(master = self.alert_frame, width=900)
            i = 0 
            for alert in data['alert']:
                label = customtkinter.CTkLabel(master = frame, text = alert, font = customtkinter.CTkFont(size = 15), width=500, bg_color=("gray80", "gray20"))
                label.grid(row = i, column = 0)
                i += 1 
            frame.place(relx = 0.1, rely = 0.2)
            self.alert_frame.grid(row = 0, column = 1, sticky = 'nsew')
        else: 
            self.alert_frame.grid_forget()
        if name == "stress":
            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot()
            res = requests.post(BACKEND_BASE_URL + SRESS_BLINK_DATA_GET, json = {
                "access_token": self.access_token
            })
            data = res.json()
            print(data)
            time_stamp_lst = data['data']['time_stamp_lst']
            blink_count_lst = data['data']['blink_count_lst']
            stress_level_lst = data['data']['stress_level_lst']
            time_lst_1 = []
            time_lst_2 = []
            stress_lst_1 = []
            stress_lst_2 = []
            for i in range(len(stress_level_lst)): 
                if stress_level_lst[i] >= 85:
                    stress_lst_2.append(stress_level_lst[i])
                    time_lst_2.append(datetime.datetime.strptime(time_stamp_lst[i], "%m/%d/%Y, %H:%M:%S")) 
                else: 
                    stress_lst_1.append(stress_level_lst[i])
                    time_lst_1.append(datetime.datetime.strptime(time_stamp_lst[i], "%m/%d/%Y, %H:%M:%S")) 
            print(len(time_lst_1), ", ", len(stress_lst_1))
            ax.scatter(time_lst_1, stress_lst_1,color = 'g')
            ax.scatter(time_lst_2, stress_lst_2,color = 'r')
            ax.set_xlabel("timestamp")
            ax.set_ylabel("stress level")
            ax.set_title("Time vs Stress Level")
            canvas = FigureCanvasTkAgg(fig, master=self.stress_frame)

            fig1 = Figure(figsize=(5, 4), dpi = 100)
            ax1 = fig1.add_subplot()
            ax1.plot([datetime.datetime.strptime(fl, "%m/%d/%Y, %H:%M:%S") for fl in time_stamp_lst], blink_count_lst, marker = 'o',  markerfacecolor = 'red')
            canvas1 = FigureCanvasTkAgg(fig1, master = self.stress_frame)
            canvas1.draw()
            canvas.get_tk_widget().place(x = 60, y = 90, width=800, height=250)
            canvas1.get_tk_widget().place(x = 60, y = 420, width=800, height=250)
            self.stress_frame.grid(row = 0, column = 1, sticky = 'nsew')
        else:
            self.stress_frame.grid_forget()
        if name == "step_count":
            res = requests.post(GET_STEP_COUNT_END_POINT, json = {
                'accessToken': self.access_token
            })
            data = res.json()
            print(data)
            date_string = []
            step_count_lst = []
            for i, j in data['data'].items():
                date_string.append(i) 
                step_count_lst.append(j)
            
            fig = Figure(figsize = (5, 4), dpi = 100)
            ax = fig.add_subplot()
            print(step_count_lst)
            ax.hist(step_count_lst, len(step_count_lst), density = True)
            ax.set_xlabel("Date")
            ax.set_ylabel("Number of Steps")
            ax.set_title("Number of Step Moved by the User")
            ax.set_xticks([datetime.datetime.strptime(d, "%m/%d/%Y") for d in date_string])
            canvas = FigureCanvasTkAgg(fig, master = self.step_count_frame)
            canvas.draw()
            canvas.get_tk_widget().place(x = 60, y = 130, width = 800, height=250)
            self.step_count_frame.grid(row = 0, column = 1, sticky = 'nsew')
        else:
            self.step_count_frame.grid_forget()
        if name == "browsing":
            res = requests.post(BACKEND_BASE_URL + GET_BOWSING_DETAILS, json = {
                'access_token' : self.access_token
            })
            # print(res.txt)
            data = res.json()
            fig1 = Figure(figsize=(5, 4), dpi = 100)
            ax1 = fig1.add_subplot()
            # ax1.plot([datetime.datetime.strptime(fl, "%m/%d/%Y, %H:%M:%S") for fl in time_stamp_lst], blink_count_lst, marker = 'o',  markerfacecolor = 'red')
            dict_obj = {}
            for obj in data['data']:
                for i, j in obj['type'].items():
                    if i not in dict_obj:
                        dict_obj[i] = {
                            'date': [obj['date']],
                            'count': [j]
                        } 
                    else: 
                        dict_obj[i]['date'].append(obj['date'])
                        dict_obj[i]['count'].append(j)
            # print(dict_obj)
            colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
            color_index = 0 
            for t in list(dict_obj.keys()): 
                ax1.scatter(dict_obj[t]['date'], dict_obj[t]['count'], s = 200, c= colors[color_index])
                color_index += 1 
                color_index %= len(colors)
            ax1.set_xlabel("Date")
            ax1.set_ylabel("Number of Visit")
            ax1.set_title("Number of Vists vs Date")
            ax1.legend([t for t in list(dict_obj.keys())])
            canvas1 = FigureCanvasTkAgg(fig1, master = self.browsing_frame)
            canvas1.draw()
            canvas1.get_tk_widget().place(x = 60, y = 200, width=800, height=300)
            self.browsing_frame.grid(row = 0, column = 1, sticky = 'nsew')
        else:
            self.browsing_frame.grid_forget()
    
    def select_alert_tile(self):
        self.select_by_name("alert")

    def select_stress_tile(self):
        self.select_by_name("stress")

    def select_step_count_tile(self):
        self.select_by_name("step_count")

    def select_browsing_title(self):
        self.select_by_name("browsing")