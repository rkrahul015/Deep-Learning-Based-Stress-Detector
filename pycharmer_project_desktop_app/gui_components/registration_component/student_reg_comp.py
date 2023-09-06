from tkinter import * 
import customtkinter 
from config.constants import STUDENT_REG_TITLE
from .alert_comp import alert
import requests
from config.url_resources import BACKEND_BASE_URL, STUDENT_REGISTRTION_ENDPOINT
from gui_components.dataview_components.dashboard_component import DashBoardComponent
from gui_components.registration_component.alert_comp import alert
class StudentRegistrationComponent: 

    def __init__(self): 
        self.registerStudentWindow = customtkinter.CTk()
        self.registerStudentWindow.geometry("800x700")
        self.registerStudentWindow.resizable(False, False)
        self.registerStudentWindow.title(STUDENT_REG_TITLE)
        self.registerStudentLabel = customtkinter.CTkLabel(master = self.registerStudentWindow, text = "User Registration", font = customtkinter.CTkFont(size = 30))
        self.registerStudentLabel.place(relx = 0.32, rely = 0.1)

        ## First Name 
        self.firstnameLabel = customtkinter.CTkLabel(master = self.registerStudentWindow, text = 'First Name', font = customtkinter.CTkFont(size = 17))
        self.firstnameEntry = customtkinter.CTkEntry(master = self.registerStudentWindow, font = customtkinter.CTkFont(size = 17), width=200)
        self.firstnameLabel.place(relx = 0.2, rely = 0.2)
        self.firstnameEntry.place(relx = 0.2, rely = 0.25)

        ## Last Name 
        self.lastnameLabel = customtkinter.CTkLabel(master = self.registerStudentWindow, text = 'Last Name', font = customtkinter.CTkFont(size = 17))
        self.lastnameEntry = customtkinter.CTkEntry(master = self.registerStudentWindow, font = customtkinter.CTkFont(size = 17), width=200)
        self.lastnameLabel.place(relx = 0.6, rely = 0.2)
        self.lastnameEntry.place(relx = 0.6, rely = 0.25)

        ### UserName 
        self.usernameLabel = customtkinter.CTkLabel(master = self.registerStudentWindow, text = 'UserName', font = customtkinter.CTkFont(size = 17))
        self.usernameEntry = customtkinter.CTkEntry(master = self.registerStudentWindow, font = customtkinter.CTkFont(size = 17), width = 200)
        self.usernameLabel.place(relx = 0.2, rely = 0.3)
        self.usernameEntry.place(relx = 0.2, rely = 0.35)

        ### Email Address 
        self.userEmailLabel = customtkinter.CTkLabel(master = self.registerStudentWindow, text = "Email Address", font = customtkinter.CTkFont(size = 17))
        self.userEmailEntry = customtkinter.CTkEntry(master = self.registerStudentWindow, font = customtkinter.CTkFont(size = 17), width = 200)
        self.userEmailLabel.place(relx = 0.6, rely = 0.3)
        self.userEmailEntry.place(relx = 0.6, rely = 0.35)

        ### password and confirm password. 
        self.userPasswordLabel = customtkinter.CTkLabel(master = self.registerStudentWindow, text = "Password", font = customtkinter.CTkFont(size = 17))
        self.userPasswordEntry = customtkinter.CTkEntry(master = self.registerStudentWindow, font = customtkinter.CTkFont(size = 17), width = 200)
        self.userPasswordEntry.configure(show = '*')
        self.userPasswordLabel.place(relx = 0.2, rely = 0.4)
        self.userPasswordEntry.place(relx = 0.2, rely = 0.45)

        ### confirm password 
        self.userConfirmPasswordLabel = customtkinter.CTkLabel(master = self.registerStudentWindow, text = "Confirm Password", font = customtkinter.CTkFont(size = 17))
        self.userConfirmPasswordEntry = customtkinter.CTkEntry(master = self.registerStudentWindow, font = customtkinter.CTkFont(size = 17), width = 200)
        self.userConfirmPasswordEntry.configure(show = '*')
        self.userConfirmPasswordLabel.place(relx = 0.6, rely = 0.4)
        self.userConfirmPasswordEntry.place(relx = 0.6, rely = 0.45)

        ### phone number
        self.userPhoneNumberLabel = customtkinter.CTkLabel(master = self.registerStudentWindow, text = "Phone", font = customtkinter.CTkFont(size = 17))
        self.userPhoneNumberEntry = customtkinter.CTkEntry(master = self.registerStudentWindow, font = customtkinter.CTkFont(size = 17), width = 200)
        self.userPhoneNumberLabel.place(relx = 0.2, rely = 0.5)
        self.userPhoneNumberEntry.place(relx = 0.2, rely = 0.55)

        ### interval 
        self.intervalTimeSetLabel = customtkinter.CTkLabel(master = self.registerStudentWindow, text = "Report Interval Time", font = customtkinter.CTkFont(size = 17))
        self.intervalTimeSetLabel.place(relx = 0.6, rely = 0.5)
        self.intervalTimeSetEntry = customtkinter.CTkEntry(master = self.registerStudentWindow, font= customtkinter.CTkFont(size = 17))
        self.intervalTimeSetEntry.place(relx = 0.6, rely = 0.55)
        self.timeLabel = customtkinter.CTkLabel(master = self.registerStudentWindow, text = 'Minutes', font = customtkinter.CTkFont(size = 15))
        self.timeLabel.place(relx = 0.79, rely = 0.55)
        self.userRegistrationBtn = customtkinter.CTkButton(master = self.registerStudentWindow, text = "Register Student", command = self.registerStudent, width=200) 
        self.userRegistrationBtn.place(relx = 0.35, rely = 0.64)
    

    def render(self): 
        self.registerStudentWindow.mainloop()

    def registerStudent(self):
        error_msg = ""
        student_details = {}
        student_details['first_name'] = self.firstnameEntry.get()
        student_details['last_name'] = self.lastnameEntry.get()
        student_details['email'] = self.userEmailEntry.get()
        student_details['password'] = self.userPasswordEntry.get()
        student_details['phone'] = self.userPhoneNumberEntry.get()
        student_details['interval'] = self.intervalTimeSetEntry.get()
        student_details['user_name'] = self.usernameEntry.get()
        print(student_details)
        for i, j in student_details.items(): 
            if len(j) == 0:
                error_msg = " ".join(i.split("_"))  + " Can\'t be Empty !!!"
                break
            try: 
                interval = int(student_details['interval'])
            except Exception as e:
                error_msg = "Please Enter Number in Interval"
        if error_msg != "":
            alert(error_msg=error_msg)
        if student_details['password'] != self.userConfirmPasswordEntry.get(): 
            alert("Passwords Doesnot Match") 
        else: 

            student_details['reportingTime'] = student_details['interval']
            del student_details['interval']
            student_details['contact'] = student_details['phone']
            del student_details['phone']
            student_details['pass_word'] = student_details['password']
            del student_details['password']
            res = requests.post(BACKEND_BASE_URL + STUDENT_REGISTRTION_ENDPOINT, json=student_details)
            res = res.json()
            if res['status_code'] == 200:
                studentDashBoard = DashBoardComponent()
                self.registerStudentWindow.destroy()
                DashBoardComponent.render()
            else:
                alert("Some Error Occured")
            


        
        