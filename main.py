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

        self.btnAddGeoLATLONViaNetacticaDB = Button(self.canvas, text="ADD LAT LON via Netactica", command=self.addGeoLatLonViaNectactica)
        self.btnMacthViaTravelCName = Button(self.canvas, text="Macth via TravelC Name", command=self.macthViaTravelCompositor)

        self.btnTestRndOutput = Button(self.canvas, text="Test OUTPUT", command=self.textOutputData)

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

        self.btnAddGeoLATLONViaNetacticaDB.place(x=300, y=40)
        self.btnMacthViaTravelCName.place(x=300, y=70)

        self.btnTestRndOutput.place(x=600, y=10)


        self.screem.mainloop()

    def loadDATA(self):
        self.controller.loadData()
        self.refreshConsole()

    def addGeoLatLonViaNectactica(self):
        if self.controller.isTheDataLoad():
            self.controller.addGeolatLonViaNetactica()
        self.refreshConsole()

    def macthViaTravelCompositor(self):
        if self.controller.isTheDataLoad():
            self.controller.machingDataViaTravelCName()
        self.refreshConsole()

    def saveDATA(self):
        if self.controller.isTheDataLoad():
            self.controller.saveData()
        self.refreshConsole()

    def textOutputData(self):
        if self.controller.theOutPutIsCretate():
            t = Toplevel()
            t.geometry("720x200")
            t.title("testingDataRnd")
            canvas = Canvas(t,bg="snow", width=720, height=480)
            canvas.place(x=0, y=0)
            lblInfoTurismoi = Label(canvas, text="TurismoiDaTA: ")
            lblInfoTurismoi.place(x=20, y=20)
            lblDataTurismoi = Label(canvas, text="XXXXXXXXXXXXXXX")
            lblDataTurismoi.place(x=150, y=20)
            lblInfoTravelC  = Label(canvas, text="TravelCoData: ")
            lblInfoTravelC.place(x=20, y=60)
            lblDataTravelC = Label(canvas, text="XXXXXXXXXXXXXXX")
            lblDataTravelC.place(x=150, y=60)
            btnNextData = Button(canvas, text="Next RND DATA", command=lambda:self._nextOutPutDataRND(lblDataTurismoi, lblDataTravelC))
            btnNextData.place(x=280, y=140)
            btnRejectTest = Button(canvas, text="Reject Test", bg="red",command=lambda:self._rejectTest(lblDataTurismoi, lblDataTravelC))
            btnRejectTest.place(x=100, y=140)

    def _nextOutPutDataRND(self, lblTurismoi, lblTravelC):
        data = self.controller.getInformeFullHeadersRndData()
        data = data.split("*-*")
        lblTurismoi['text'] = str(data[0])
        lblTravelC['text'] = str(data[1])

    def _rejectTest(self, lblTurismoi, lblTravelC):
        self.controller.saveRejectTest(lblTurismoi['text'], lblTravelC['text'])
            

    def refreshConsole(self):
        self.console.delete('1.0', END)
        self.console.insert(END, self.controller.consoleText)
        self.console.see(END)



s = Sofware()
