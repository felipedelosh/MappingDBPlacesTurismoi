"""
FelipedelosH
"""
from turismoiData import *
from travelCompositorData import *
from netacticaData import *

class Controller:
    def __init__(self) -> None:
        self.turismoiData = TurismoiDATA()
        self.travelCData = TravelCompositorData()
        self.netacticaData = NetacticaData()
        self.consoleText = ""
        self.metadata = ""
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

            #This file contain a several places with lat and lon
            dataNetactica = self.rtnArcheveInfo("RESORCES/all_cities_with_lat_and_lon.csv")
            self.netacticaData.chargeData(dataNetactica)
            self.saveMetadata("LOAD/loadingNetactica.txt", self.netacticaData.metadata)
            self.appendTextInConsoleText("Lading LAT N LON info via.... Netactica")


        except:
            self.appendTextInConsoleText("Error Lading information....")

    def machingData(self):
        try:
            # Search a travel compositor places in turismoi Via Names
            for i in self.travelCData.data:
                self.turismoiData.seachPlaceViaISOName(i, self.travelCData.getAllInfo(i), ";", [1])
            
            self.saveMetadata("MATCH/macthingTurismoi.txt", self.turismoiData.metadataMaching)
            self.appendTextInConsoleText("Macht DATA....")
        except:
            self.appendTextInConsoleText("Error Maching data....")


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

    def isTheDataLoad(self):
        return self.turismoiData.isTheDataLoad and self.travelCData.isTheDataLoad and self.netacticaData.isTheDataLoad



