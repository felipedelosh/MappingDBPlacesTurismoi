"""
FelipedelosH

This programs is create to read turismoi cities
ID_country|ISO_country|NAME_country|NAME_PRINT_country|ISO3_country|CODE_country|NAME_ESP_country|id_city|region_id|name_place|short_name_place|slug_place|group_id_place|province_id_place|group_slug_place|latitude|longitude|country_host_id_place|

0 -> Load the data
1 -> Put latitude and longitude in 
2 -> Try macth via name
3 -> Try mach via GEO
4 -> Save the file

Note= view Logs and use tools


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
        self.btnViewTusrismoiMacthStatus = Button(self.canvas, text="Turismoi Macth Status", command=self.viewWindowStateTurismoiMacth)

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
        self.btnViewTusrismoiMacthStatus.place(x=600, y=40)


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

    def viewWindowStateTurismoiMacth(self):
        if self.controller.isTheDataLoad():
            t = Toplevel()
            t.geometry("1280x720")
            t.title("Integridad de los datos")
            canvas = Canvas(t, bg="snow", width=1280, height=720)
            canvas.place(x=0, y=0)
            w = int(canvas['width'])
            h = int(canvas['height'])
            canvas.create_text(w*0.03, h*0.03, text="turismoi")
            x0 = 0
            y0 = 0
            btnsCountriesTurismoi = []
            counter = 0
            posx_counter = 0
            posy_counter = 0
            for i in self.controller.getCountrisWithCitiesInTurismoi():
                name_btn = i
                btnsCountriesTurismoi.append(Button(canvas, text=name_btn))
                btnsCountriesTurismoi[counter].bind("<Button-1>", lambda key: self._showCitiesOfCountryInformation(key.widget.cget('text')))

                posy_counter = posy_counter + 1
                if posx_counter == 20: 
                    x0 = x0 + 120
                    y0 = 0
                    posx_counter = 0
                    posy_counter = 0
                y0 = ((posy_counter+1)*30)
                btnsCountriesTurismoi[counter].place(x=x0, y=y0)

                posx_counter = posx_counter + 1
                counter = counter + 1

    def _showCitiesOfCountryInformation(self, country_name):
        result = self.controller.getAllCitiesInCountryName(country_name)
        data = ""
        for i in result:
            getMacthStatus = self.controller.getMacthStatus(i)
            if getMacthStatus == "":
                getMacthStatus = " No Maching... :( "
            data = data + str(i) + " >> " + getMacthStatus + "\n"

        self._showWindowWithText(country_name, data)
        
        


    def _showWindowWithText(self, title, text):
        """
        
        """
        t = Toplevel()
        t.geometry("640x480")
        t.title(title)
        canvas = Canvas(t, width=640, height=480, bg="snow")
        textArea = Text(canvas, width=76, height=25)
        canvas.place(x=0, y=0)
        textArea.place(x=10, y=10)
        textArea.delete('1.0', END)
        textArea.insert(END, text)




s = Sofware()
