from tkinter import * 
import customtkinter 
from config.constants import STUDENT_LOGIN_TITLE
from .alert_comp import alert
from .student_reg_comp import StudentRegistrationComponent
from config.url_resources import BACKEND_BASE_URL, USER_LOGIN_ENDPOINT
import requests
from gui_components.dataview_components.dashboard_component import DashBoardComponent 
from config.url_resources import FILE_PATH
import json

class StudentLoginComponent: 
    
    def __init__(self): 
        self.studentLoginWindow = customtkinter.CTk()
        self.studentLoginWindow.geometry("800x700")
        self.studentLoginWindow.resizable(False, False)
        self.studentLoginWindow.title(STUDENT_LOGIN_TITLE)
        self.studentLabel = customtkinter.CTkLabel(master = self.studentLoginWindow, text = "User Login", font = customtkinter.CTkFont(size = 30, weight='bold'))
        self.studentLabel.place(relx = 0.35, rely = 0.25)
        self.studentEmailAddressLabel = customtkinter.CTkLabel(master = self.studentLoginWindow, text = "Email Address", font = customtkinter.CTkFont(size = 15, weight='bold'))
        self.studentEmailAddressLabel.place(relx = 0.3, rely = 0.35)
        self.studentEmailAddress = customtkinter.CTkEntry(master=self.studentLoginWindow, height=40, width=300, font = customtkinter.CTkFont(size = 12))
        self.studentEmailAddress.place(relx = 0.3, rely = 0.4)
        self.studentPassWordLabel = customtkinter.CTkLabel(master = self.studentLoginWindow, text = "Password", font = customtkinter.CTkFont(size = 15, weight='bold'))
        self.studentPassWordLabel.place(relx = 0.3, rely = 0.47)
        self.studentPassword = customtkinter.CTkEntry(master=self.studentLoginWindow, height=40, width=300, font = customtkinter.CTkFont(size = 12))
        self.studentPassword.configure(show = "*")
        self.studentPassword.place(relx = 0.3, rely = 0.52)
        self.logiBtn = customtkinter.CTkButton(master = self.studentLoginWindow, text = "Login", command=self.loginBtnCommand)
        self.logiBtn.place(relx = 0.4, rely = 0.6)
        self.studentSignupLabel = customtkinter.CTkLabel(master=self.studentLoginWindow, text = "create a new account.", font = customtkinter.CTkFont(size = 14))
        self.studentSignupLabel.place(relx = 0.38, rely = 0.65)
        self.signupLabel = customtkinter.CTkLabel(master = self.studentLoginWindow, text = "sign up", text_color='blue', font = customtkinter.CTkFont(size = 14))
        self.signupLabel.place(relx = 0.56, rely = 0.65)
        self.signupLabel.bind("<Button-1>", lambda e : self.signUpBtnCommand())
    def render(self):
        self.studentLoginWindow.mainloop()

    def loginBtnCommand(self): 
        email = self.studentEmailAddress.get()
        password = self.studentPassword.get()
        if len(email) == 0 or len(password) == 0:
            error_msg = ""
            if len(email) == 0:
                error_msg = "Please Enter the Email"
            elif len(password) == 0:
                error_msg = "Please Enter the Password"
            alert(error_msg=error_msg)
        else: 
            req_body = {
                'email': email,
                'pass_word': password
            }
            res = requests.post(BACKEND_BASE_URL + USER_LOGIN_ENDPOINT, json = req_body)
            print(res.text)
            res = res.json()
            print(res)
            if res['status_code'] != 200:
                alert(res['message']) 
            else: 
                access_token_details = {
                    'access_token': res['data']['access_token']
                }
                json_obj = json.dumps(access_token_details)
                with open(FILE_PATH + "accesstoken.json", 'w') as f:
                    f.write(json_obj)
                self.studentLoginWindow.destroy()
                studetnDasthBoard = DashBoardComponent(res['data']['access_token'])
                studetnDasthBoard.render()


    def signUpBtnCommand(self): 
        self.studentLoginWindow.destroy()
        studentRegComponent = StudentRegistrationComponent()
        studentRegComponent.render()