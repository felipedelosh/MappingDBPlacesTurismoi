"""
FelipedelosH

This programs is create to read turismoi cities
ID_country|ISO_country|NAME_country|NAME_PRINT_country|ISO3_country|CODE_country|NAME_ESP_country|id_city|region_id|name_place|short_name_place|slug_place|group_id_place|province_id_place|group_slug_place|latitude|longitude|country_host_id_place|


1 -> Put latitude and longitude in 

"""
from tkinter import *
from controller import *

class Sofware:
    def __init__(self) -> None:
        self.controller = Controller()
        self.screem = Tk()
        self.canvas = Canvas(self.screem)
        self.lblBannerProgram = Label(self.canvas, text="Mapeo turismoi >> travelCompositor.")
        self.lblFooterProgram = Label(self.canvas, text="FelipedelosH")
        self.console = Text(self.canvas, fg="green", cursor="circle", bg="black", width=86, height=14)
     
     
        self.btnLoadData = Button(self.canvas, text="Load DATA", command=self.loadDATA)
        self.btnSaveData = Button(self.canvas, text="Save DATA", command=self.saveDATA)

        self.btnMactGeoLATLONViaTravelC = Button(self.canvas, text="Macth via TravelC", command=self.macthViaTravelCompositor)

        self.vizualizedAndRun()

    def vizualizedAndRun(self):
        self.screem.title("MappingTurismoiTravelCOm By Loko")
        self.screem.geometry("720x480")
        self.canvas['width'] = 720
        self.canvas['height'] = 480
        self.canvas['bg'] = "snow"
        self.canvas.place(x=0, y=0)
        self.lblBannerProgram.place(x=20, y=20)
        self.lblFooterProgram.place(x=250, y=450)
        self.console.place(x=10, y=200)

        self.btnLoadData.place(x=100, y=70)
        self.btnSaveData.place(x=100, y=120)

        self.btnMactGeoLATLONViaTravelC.place(x=300, y=80)


        self.screem.mainloop()

    def loadDATA(self):
        self.controller.loadData()
        self.refreshConsole()

    def macthViaTravelCompositor(self):
        if self.controller.isTheDataLoad():
            self.controller.machingData()
        self.refreshConsole()

    def saveDATA(self):
        if self.controller.isTheDataLoad():
            self.controller.saveData()
        self.refreshConsole()


    def refreshConsole(self):
        self.console.delete('1.0', END)
        self.console.insert(END, self.controller.consoleText)
        self.console.see(END)



s = Sofware()
