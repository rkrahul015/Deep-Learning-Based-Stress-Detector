import customtkinter
customtkinter.set_appearance_mode("dark")
from gui_components.dataview_components.dashboard_component import DashBoardComponent 
app = DashBoardComponent()
app.render()