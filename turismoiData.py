"""
FelipedelosH
This file is create to save all information from turismoi
0 ID_country|1 ISO_country|2 NAME_country|3 NAME_PRINT_country|4 ISO3_country|5 CODE_country|6 NAME_ESP_country|7 id_city|8 region_id|9 name_place|10 short_name_place|11 slug_place|12 group_id_place|13 province_id_place|14 group_slug_place|15 latitude|16 longitude|17 country_host_id_place|

"""

from time import pthread_getcpuclockid


class TurismoiDATA:
    def __init__(self) -> None:
        self.data = {} # {iso_country.lower().LRstrip() + ":" + city_name.lower().LRstrip()}
        self.machingDataKeys = {} # TusimoiKEY = OtherKey >> Example [co:bogota] = "COLOMBIA:Bog"
        self.country_iso_name = {} # [iso] = name_country
        self.city_macth_controller = {} # [iso:city_name] = [MacthID, status] >> Example1   [Colombia][Bogota] = ["co:bogota", "co:bogota", "Status0"] 
        self.isTheDataLoad = False
        self.metadata = {} # Charge LOGS
        self.metadataMaching = {}
        self.count = 0

    def chargeData(self, txt):
        count = 0
        for i in txt.split("\n")[1:-1]:
            data = i.split("|")
            iso_country = str(data[1]).lower().strip()
            name_city = str(data[11]).lower().lstrip().rstrip()
            key = iso_country + ":" + name_city
            
            name_country = data[2]


            name_country = name_country.lower().lstrip().rstrip()
            if iso_country not in self.country_iso_name.keys():
                self.country_iso_name[iso_country] = name_country

            if key in self.data.keys():
                # Note slug city is unique 
                self.metadata["info"+":"+str(count)] = "Duplicate ID turismoi: " + str(key) + " :( "
                count = count + 1
            else:
                self.data[key] = i


            self.city_macth_controller[key] = []

        
        self.isTheDataLoad = True 
        self.metadata["Total_Reg_Inserted"] = str(len(self.data))
        self.metadata["Counter_err"] = str(count)

    def _validatesLatitude(self, latitude):
        """
        Beetween +-90,90
        """
        try:
            value = float(latitude)
            if value >= -90 and value <= 90:
                return True
            else:
                return False
        except:
            return False 

    def _validatesLongitude(self, longitude):
        """
        Beetween +-180,180
        """
        try:
            value = float(longitude)
            if value >= -180 and value <= 180:
                return True
            else:
                return False
        except:
            return False 

    def getReportInfo(self, key):
        """
        Retruns 
        """
        data = ""
        if key in self.data.keys():
            data = self.data[key].split("|")
            slug_city = data[11]
            city_name = data[9]
            country = data[2] + " (" + data[1] + ")"
 
            latitude = data[15]
            if latitude != "NULL":
                if not self._validatesLatitude(latitude):
                    print(latitude)
                    latitude = "NULL"

            longitude = data[16]
            if not longitude != "NULL":
                if not self._validatesLongitude(longitude):
                    longitude = "NULL"

            data = slug_city + "|" + city_name + "|" + country + "|" + latitude + "|" + longitude

        return data

    def getAllInfo(self, key):
        if key in self.data:
            return self.data[key]
        return ""

    def getCountryNameViaIso(self, iso):
        name = ""
        iso = str(iso).strip().lower()
        if iso in self.country_iso_name.keys():
            name = self.country_iso_name[iso]
        return name

    def getGeoLatLon(self, key):
        data = ""
        if key in self.data.keys():
            data = self.data[key].split("|")
            latitude = data[15]
            if latitude != "NULL":
                if not self._validatesLatitude(latitude):
                    print(latitude)
                    latitude = "NULL"

            longitude = data[16]
            if not longitude != "NULL":
                if not self._validatesLongitude(longitude):
                    longitude = "NULL"

            data = latitude+"|"+longitude


        return data


    def seachPlaceViaISOName(self,key, allDATAofKey, delimiter, vecPosOfNames=[]):
        """
        return True or False if the key or AllDataOfKey inside self.turismoi data
        In the process the key is register in self.machingDataKeys[key] = key
        key = is a key od dict >> Exampe iso:city_name
        allDataOfKey = is all info exmaple code|name|name2|shortName|info|lat|lon
        delimiter = separator >> Example | or ;
        vecPosNames = where i find names of allDATAofKey >> example [1,2,3]
        """
        found = False
        # First i search via key
        if key in self.data.keys():
            self.machingDataKeys[key] = key
            self.metadataMaching[str(self.count)] = "Found via Key " + str(key)
            self.count = self.count + 1
            found = True

        # Seach sequencial via names
        if not found:
            external_data = allDATAofKey.split(delimiter)
            get_iso_key = key.split(":")[0]
            for i in vecPosOfNames:
                for j in self.data:
                    if get_iso_key in j:
                        turismoi_data = self.data[j].split("|")
                        # Found in 9 name_place|
                        if turismoi_data[9].strip().lower() == external_data[int(i)].strip().lower():
                            self.machingDataKeys[j] = key
                            self.metadataMaching[str(self.count)] = "Found via name_place " + str(j) + " >> " + str(key)
                            self.count = self.count + 1
                            found = True        

                        # 10 short_name_place|
                        if external_data[int(i)].strip().lower() in turismoi_data[10].strip().lower() and not found:
                            #print("Encontreee...: ", external_data[int(i)], "*  En   ", key, " >> ", j)
                            self.machingDataKeys[j] = key
                            self.metadataMaching[str(self.count)] = "Found via short_name_place " + str(j) + " >> " + str(key)
                            self.count = self.count + 1
                            found = True  

                        # 11 slug_place|
                        if external_data[int(i)].strip().lower().replace('-', '') in turismoi_data[10].strip().lower().replace('-', '') and not found:
                            #print("Encontre Slug similar en: ...", external_data[int(i)], " >> ", key, "  >> ", j)
                            self.machingDataKeys[j] = key
                            self.metadataMaching[str(self.count)] = "Found via slug_place " + str(j) + " >> " + str(key)
                            self.count = self.count + 1
                            found = True 

                        if found:
                            break
                
                if found:
                    break


        return found
                        
 
 