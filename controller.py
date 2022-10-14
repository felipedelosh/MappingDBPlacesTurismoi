"""
FelipedelosH
"""
from turismoiData import *
from travelCompositorData import *
from netacticaData import *
import random

class Controller:
    def __init__(self) -> None:
        self.turismoiData = TurismoiDATA()
        self.travelCData = TravelCompositorData()
        self.netacticaData = NetacticaData()
        self.consoleText = ""
        self.metadata = ""
        self.tempOutPutData = []
        self.headers_excel_full_data = "turismoi_slug_place|turismoi_city_name|turismoi_country|turismoi_latitude|turismoi_longitude|travelC_provider_code|travelC_city_name|travelC_country|travelC_latitude|travelC_longitude"
        self.viewFullConsoleLogs = True
        
    
    def loadData(self):
        try:
            dataTurismoi = self.rtnArcheveInfo("DATA/destinos_turismoi.csv")
            self.turismoiData.chargeData(dataTurismoi)
            self.saveMetadata("LOAD/loadingTurismoi.txt", self.turismoiData.metadata)
            self.appendTextInConsoleText("Lading information.... Turismoi:"+str(len(self.turismoiData.data)))

            dataTravelCompositor = self.rtnArcheveInfo("DATA/destinos_travel_compositor.csv")
            self.travelCData.chargeData(dataTravelCompositor)
            self.saveMetadata("LOAD/loadingTravelCompositor.txt", self.travelCData.metadata)
            self.appendTextInConsoleText("Lading information.... TravelCompositor:"+str(len(self.travelCData.data)))

            #This file contain a several places with lat and lon
            dataNetactica = self.rtnArcheveInfo("RESORCES/all_cities_with_lat_and_lon.csv")
            self.netacticaData.chargeData(dataNetactica)
            self.saveMetadata("LOAD/loadingNetactica.txt", self.netacticaData.metadata)
            self.appendTextInConsoleText("Lading LAT N LON info via.... Netactica:"+str(len(self.netacticaData.data)))

            manualMacth = self.rtnArcheveInfo("TEST/manual.txt")
            if manualMacth != None:
                self.appendTextInConsoleText("Cargando macheos manuales: "+str(len(manualMacth.split("\n"))))
                self.turismoiData.setManualMacth(manualMacth)
            else:
                self.appendTextInConsoleText("No hay macheos manuales :o")

            self.saveLogs()
        except:
            self.appendTextInConsoleText("Error Lading information....")
            self.saveLogs()

    def addGeolatLonViaNetactica(self):
        """
        Macth via turismoi.names and netactica.names
        if someName == someName 
        the LAT LONG is update
        And save a report
        """
        try:
            """
            count_netactica_macth = 0
            count_not_netactica_mach = 0
            count_modify_regs = 0
            count_not_modify_regs = 0
            order_turismoi_keys = sorted(self.turismoiData.data.keys())
            for i in order_turismoi_keys:
                
                data = i.split(":")
                iso_code = data[0]
                name_city = data[1]
                geoDATA = self.turismoiData.getGeoLatLon(i) # Get turismoi lat long
                result = self.netacticaData.searchPlace(iso_code, name_city, self.turismoiData.data[i], "|", [9,10,11]) # get Macth lat long

                info =  "|" + str(iso_code).upper() + "|" + name_city + "|"
                if result != "NULL|NULL":
                    count_netactica_macth = count_netactica_macth + 1
                    info = info + "ok MACTH TT|"
                    if geoDATA == "NULL|NULL":
                        self.turismoiData.setGeoLatLon(i, result)
                        count_modify_regs = count_modify_regs + 1
                    else:
                        count_not_modify_regs = count_not_modify_regs + 1
                else:
                    count_not_netactica_mach = count_not_netactica_mach + 1
                    count_not_modify_regs = count_not_modify_regs + 1
                    info = info + "no MACTH TT|"
                
                self.netacticaData.macthingTurismoi[i] =  info           
            """
            count_netactica_macth = 0
            count_not_netactica_mach = 0
            count_modify_regs = 0
            count_not_modify_regs = 0
            order_turismoi_keys = sorted(self.turismoiData.data.keys())
            order_turismoi_keys = sorted(self.turismoiData._adan_argentina.keys())
            for i in order_turismoi_keys:
                data = i.split(":")
                iso_code = data[0]
                name_city = data[1]
                geoDATA = self.turismoiData.getGeoLatLon(i) # Get turismoi lat long
                result = self.netacticaData.searchPlace(iso_code, name_city, self.turismoiData.data[i], "|", [9,10,11]) # get Macth lat long

                info =  "|" + str(iso_code).upper() + "|" + name_city + "|"
                if result != "NULL|NULL":
                    count_netactica_macth = count_netactica_macth + 1
                    info = info + "ok MACTH TT|"
                    if geoDATA == "NULL|NULL":
                        self.turismoiData.setGeoLatLon(i, result)
                        count_modify_regs = count_modify_regs + 1
                    else:
                        count_not_modify_regs = count_not_modify_regs + 1
                else:
                    count_not_netactica_mach = count_not_netactica_mach + 1
                    count_not_modify_regs = count_not_modify_regs + 1
                    info = info + "no MACTH TT|"
                
                self.netacticaData.macthingTurismoi[i] =  info   


            

            txtoutp = "Adding GEO data via Netactica\n"
            txtoutp = txtoutp + "Total reg MACTH: " + str(count_netactica_macth) + "\n"
            txtoutp = txtoutp + "Toral reg NOT MACTH: " + str(count_not_netactica_mach) + "\n"
            txtoutp = txtoutp + "Total reg Modify: " + str(count_modify_regs) + "\n"
            txtoutp = txtoutp + "Total reg not Modify: " + str(count_not_modify_regs) + "\n"
            self.appendTextInConsoleText(txtoutp)
            self.saveMetadata("MATCH/turimoi.join.netactica.csv", self.netacticaData.macthingTurismoi)
            self.saveMetadata("GEO/statusTruismoiNetacticaGEOLATLON.txt", self.netacticaData.metadataGEO)
            self.saveMetadata("GEO/addTurismoiViaNectactica.txt", self.turismoiData.metadataGeo)   
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
            self.appendTextInConsoleText("Macht DATA via TravelCompositor via Name....\nTotal Macth:"+str(count_macth)+"\nNo Macth:"+str(count_not_macth)+"\n")
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
            
            for i in self.turismoiData.manualMachingDataKeys:
                data = data + self.turismoiData.getReportInfo(i) + "|" + self.travelCData.getReportInfo(self.turismoiData.manualMachingDataKeys[i]) + "\n"


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

    def getInformeFullHeadersRndData(self):
        k = len(self.tempOutPutData)
        k = random.randint(0, (k-1))
        data = self.tempOutPutData[k].split("|")
        count = 0
        info = ""
        for i in data:
            if count <=4:
                info = info + i + "|"
            
            if count == 4:
                info = info + "*-*"

            if count > 4 and count <=10:
                info = info + i + "|"

            count = count + 1
            
        #data = [data[0:5], data[6:10]]
        return info

    def getCountrisWithCitiesInTurismoi(self):
        return self.turismoiData.getCountriesWithCities()

    def getCountriesWithCitiesInTravelCompositor(self):
        return self.getCountriesOnlyWithMacthInTurismoi()


    def getCountriesOnlyWithMacthInTurismoi(self):
        data = self.travelCData.getCountriesWithCities()
        final_data = []
        for i in data:
            iso = self.travelCData.getCountryIsoViaName(i)
            for j in self.turismoiData.machingDataKeys:
                if iso+":" in j:
                    final_data.append(i)
                    break
            
        return final_data

    def getAllCitiesInCountryNameTurismoi(self, country_name):
        return self.turismoiData.getAllCitiesIdOfCountryViaName(country_name)

    def getAllCitiesInTRavelCviaNameCountry(self, name):
        data = ""
        iso_country = self.travelCData.getCountryIsoViaName(name)
        temp = self.travelCData.getAllCodesOfIso(iso_country)
        for i in temp:
            info = str(i)
            len_ourput_info = len(info) - 1
            if len_ourput_info >= 20:
                info = info[0:20] + " *"
            else:
                info = info + (" "*(20-len_ourput_info)) + "*"
            macth_status =  "  NO MACTH    "
            
            for j in self.turismoiData.machingDataKeys:
                if iso_country+":" in j:
                    if self.turismoiData.machingDataKeys[j] == i:
                        macth_status =  " Auto Macth >> " + str(j)
            for j in self.turismoiData.manualMachingDataKeys:
                if iso_country+":" in j:
                    if self.turismoiData.manualMachingDataKeys[j] == i:
                        macth_status =  " ManualMacth>> " + str(j)



            data = data + info + macth_status + "\n" 

        return data

    def getAllCitiesWithNoMacthInTravelCWithIsoCode(self, iso):
        """
        iso is only a code.
        ejem : pe, co, es ...
        """
        data = ["TravelCompositor NOT MACTH"]
        for i in self.travelCData.data:
            found = False
            for j in self.turismoiData.machingDataKeys:
                if str(iso)+":" in j:
                    if i == self.turismoiData.machingDataKeys[j]:

                        found = True
                        break
            for j in self.turismoiData.manualMachingDataKeys:
                if str(iso)+":" in j:
                    if i == self.turismoiData.manualMachingDataKeys[j]:

                        found = True
                        break
            if not found and str(iso)+":" in i:
                data.append(i)

        return data

    def getLikeCitiesWithCodeInTravelC(self, iso):
        """
        iso is only code.
        ejem : pe:a, co:bog, es:madrid ...
        """
        data = ["TravelC NOT MACTH"]
        t_iso = iso.split(":")[0]

        for i in self.travelCData.data:
            if t_iso+":" in i:
                found = False
                for j in self.turismoiData.machingDataKeys:
                    if t_iso+":" in j:
                        tc_key = self.turismoiData.machingDataKeys[j]
                        if tc_key == i:
                            found = True
                            break
                for j in self.turismoiData.manualMachingDataKeys:
                    if t_iso+":" in j:
                        tc_key = self.turismoiData.manualMachingDataKeys[j]
                        if tc_key == i:
                            found = True
                            break
                
                if not found:
                    data.append(i)

        return data


    def getAllCitiesWithNoMacthInTurismoiWithIsoCode(self, iso):
        """
        iso is only a code.
        ejem : pe, co, es ...
        """
        data = ["Turismoi NOT MACTH"]
        for i in self.turismoiData.data:
            if str(iso)+":" in i:
                if i not in self.turismoiData.machingDataKeys.keys() and i not in self.turismoiData.manualMachingDataKeys.keys():
                    data.append(i)

        return data

    def getLikeCitiesWithCodeInTurismoi(self, iso):
        """
        iso is only code.
        ejem : pe:a, co:bog, es:madrid ...
        """
        data = ["Turismoi NOT MACTH"]
        t_iso = iso.split(":")[0]
        for i in self.turismoiData.data:
            if t_iso+":" in i:
                if (iso in i or iso == i) and i not in self.turismoiData.machingDataKeys.keys() and i not in self.turismoiData.manualMachingDataKeys.keys():
                    data.append(i)
        return data


    def getMacthStatus(self, key):
        
        return self.turismoiData.getmachingDataKeys(key)


    def saveRejectTest(self, regA, regB):
        try:
            data = ""
            try:
                f = open('TEST/reject.txt', 'r', encoding="UTF-8")
                data = f.read()
                exist = True
            except:
                exist = False

            f = open('TEST/reject.txt', 'w', encoding="UTF-8")
            f.write(data + "\n" + regA + regB + "\n")
            f.close()
    
        except:
            self.appendTextInConsoleText("Error write reject test")

    def saveManualReg(self, regA, regB):
        try:
            if regA in self.turismoiData.data.keys() and self.travelCData.data.keys():
                data = ""
                try:
                    f = open("TEST/manual.txt", 'r', encoding="UTF-8")
                    data = f.read()
                    f.close()
                except:
                    data = "turismoi_key|travelC_key\n"
                data =  data + regA + "|" + regB + "\n"
                g = open("TEST/manual.txt", 'w', encoding="UTF-8")
                g.write(data)
                g.close()
            else:
                print("Error Asociando: ", regA, ":", regB)
        except:
            print("Error insertando nuevo registro: ", str(regA), ":", str(regB))


    def theOutPutIsCretate(self):
        """
        
        """
        try:
            info = self.rtnArcheveInfo("OUTPUT/informe_full_headers.csv")
            for i in info.split("\n")[1:-1]:
                self.tempOutPutData.append(i)

            return self.tempOutPutData != []
        except:
            return False

    def existsTravelCKey(self, key):
        return key in self.travelCData.data.keys()

    def existsTurismoiKey(self, key):
        return key in self.turismoiData.data.keys()