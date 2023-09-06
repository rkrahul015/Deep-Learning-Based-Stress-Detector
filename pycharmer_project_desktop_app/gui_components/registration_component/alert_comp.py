from tkinter import *
import customtkinter

def alert(error_msg : str):
    error_msg = error_msg.capitalize()
    alert_root = customtkinter.CTk()
    alert_root.geometry("400x150")
    alert_root.title("Alert Box")
    alert_root.resizable(False, False)
    error_message_label = customtkinter.CTkLabel(master=alert_root, text = error_msg, font = customtkinter.CTkFont(size = 17))
    error_message_label.place(relx = .3, rely = .1)
    cancel_btn = customtkinter.CTkButton(master = alert_root, text = "OK", command= lambda : alert_root.destroy())
    cancel_btn.place(relx = 0.35, rely = .4)
    alert_root.mainloop()