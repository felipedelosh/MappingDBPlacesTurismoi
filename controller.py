"""
FelipedelosH
"""
from turismoiData import *
from travelCompositorData import *

class Controller:
    def __init__(self) -> None:
        self.turismoiData = TurismoiDATA()
        self.travelCData = TravelCompositorData()
        self.consoleText = ""
        self.metadata = ""
        self.isTheDataLoad = False
        self.viewFullConsoleLogs = True
        
    
    def loadData(self):
        try:
            dataTurismoi = self.rtnArcheveInfo("DATA/destinos_turismoi.csv")
            self.turismoiData.chargeData(dataTurismoi)
            self.saveMetadata("LOAD/loadingTurismoi.txt", self.turismoiData.metadata)
            self.appendTextInConsoleText("Lading information.... Turismoi")

            dataTravelCompositor = self.rtnArcheveInfo("DATA/destinos_travel_compositor.csv")
            self.travelCData.chargeData(dataTravelCompositor)
            self.saveMetadata("LOAD/loadingTravelCompositor.txt", self.travelCData.metadata)
            self.appendTextInConsoleText("Lading information.... TravelCompositor")

                
            
        except:
            self.appendTextInConsoleText("Error Lading information....")


    def rtnArcheveInfo(self, path):
        info = None
        try:
            f = open(path, 'r', encoding="utf-8")
            return f.read()
        except:
            return info

    def appendTextInConsoleText(self, txt):
        if self.viewFullConsoleLogs:
            self.consoleText = self.consoleText + txt + "\n"
        self.metadata = self.metadata + txt + "\n"

    def saveMetadata(self, filename, information):
        try:
            data = ""
            for i in information:
                data = data + str(i) + " >> " +  information[i] + "\n"

            f = open("METADATA/"+filename, "w", encoding="UTF-8")
            f.write(data)
            f.close()
        except:
            self.appendTextInConsoleText("Error write metadata >> " + filename)



