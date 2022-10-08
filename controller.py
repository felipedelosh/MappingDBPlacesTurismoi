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
        self.headers_excel_full_data = "turismoi_slug_place|turismoi_city_name|turismoi_country|turismoi_latitude|turismoi_longitude|travelC_provider_code|travelC_city_name|travelC_country|travelC_latitude|travelC_longitude"
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


            self.saveLogs()
        except:
            self.appendTextInConsoleText("Error Lading information....")
            self.saveLogs()

    def addGeolatLonViaNetactica(self):
        try:
            self.appendTextInConsoleText("Adding GEO LAT LON via netactica....")
            self.saveLogs()
        except:
            self.appendTextInConsoleText("Error to ADD LAT LON via netactica....")
            self.saveLogs()

    def machingDataViaTravelCName(self):
        try:
            # Search a travel compositor places in turismoi Via Names
            for i in self.travelCData.macthControl:
                status = self.turismoiData.seachPlaceViaISOName(i, self.travelCData.getAllInfo(i), ";", [1])
                if status:
                    self.travelCData.macthControl[i] = 1

            count_macth = 0
            count_not_macth = 0
            for i in self.travelCData.macthControl:
                if self.travelCData.macthControl[i] == 1:
                    count_macth = count_macth + 1
                else:
                    count_not_macth = count_not_macth + 1

            
            self.saveMetadata("MATCH/macthingTurismoi.txt", self.turismoiData.metadataMaching)
            self.appendTextInConsoleText("Macht DATA via TravelCompositor Name....\nTotal Macth:"+str(count_macth)+"\nNo Macth:"+str(count_not_macth)+"\n")
            self.saveLogs()
        except:
            self.appendTextInConsoleText("Error Maching data via TravelCompositor Name....")
            self.saveLogs()


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


    def saveData(self):
        try:
            data = self.headers_excel_full_data + "\n"
            for i in self.turismoiData.machingDataKeys:
                data = data + self.turismoiData.getReportInfo(i) + "|" + self.travelCData.getReportInfo(self.turismoiData.machingDataKeys[i]) + "\n"
            
            f = open("OUTPUT/informe_full_headers.csv", "w", encoding="UTF-8")
            f.write(data)
            f.close()

            self.appendTextInConsoleText("Generado Excel de la info....")
        except:
            self.appendTextInConsoleText("Error generando Excel....")

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

    def saveLogs(self):
        try:
            f = open("METADATA/logs.txt", "w", encoding="UTF-8")
            f.write(self.consoleText)
            f.close()
        except:
            self.appendTextInConsoleText("Error write LOGs")

    def isTheDataLoad(self):
        return self.turismoiData.isTheDataLoad and self.travelCData.isTheDataLoad and self.netacticaData.isTheDataLoad



