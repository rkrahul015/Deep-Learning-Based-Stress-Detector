from tkinter import * 
import customtkinter 
from config.constants import TOPBAR_TITLE
from gui_components.registration_component.student_login_comp import StudentLoginComponent

class FirstPage:

    def __init__(self): 
        self.root = customtkinter.CTk()
        self.root.title(TOPBAR_TITLE)
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.textLabel = customtkinter.CTkLabel(master = self.root, text = "Welcome Back !!!",
                            font = customtkinter.CTkFont(size = 40, weight="bold"))
        self.textLabel.place(relx = 0.35, rely = 0.3)
        self.studentBtn = customtkinter.CTkButton(master = self.root, text = "login", height=40, width = 150, command=self.studentBtnCommandAction)
        self.studentBtn.place(relx = 0.45, rely = 0.5)
    
    def render(self): 
        self.root.mainloop()

    def studentBtnCommandAction(self): 
        self.root.destroy()
        studentLoginComponent = StudentLoginComponent()
        studentLoginComponent.render()