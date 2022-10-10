"""
FelipedelosH
This file is create to save all information from turismoi
0 ID_country|1 ISO_country|2 NAME_country|3 NAME_PRINT_country|4 ISO3_country|5 CODE_country|6 NAME_ESP_country|7 id_city|8 region_id|9 name_place|10 short_name_place|11 slug_place|12 group_id_place|13 province_id_place|14 group_slug_place|15 latitude|16 longitude|17 country_host_id_place|

"""

class TurismoiDATA:
    def __init__(self) -> None:
        self.data = {} # {iso_country.lower().LRstrip() + ":" + city_name.lower().LRstrip()}
        self.control_countries_cities_create = {} # [country] = [[city:name="data.key"]]
        self.machingDataKeys = {} # TusimoiKEY = OtherKey >> Example [co:bogota] = "COLOMBIA:Bog"
        self.country_iso_name = {} # [iso] = name_country
        self.country_name_iso = {} # [name_country] = iso
        self.city_macth_controller = {} # [iso:city_name] = [MacthID, status] >> Example1   [Colombia][Bogota] = ["co:bogota", "co:bogota", "Status0"] 
        self.isTheDataLoad = False
        self.metadata = {} # Charge LOGS
        self.metadataMaching = {}
        self.metadataGeo = {}
        self.count = 0

    def chargeData(self, txt):
        count = 0
        for i in txt.split("\n")[1:-1]:
            data = i.split("|")
            iso_country = str(data[1]).lower().strip()
            name_city = str(data[11])
            key = iso_country + ":" + name_city.lower().lstrip().rstrip()
            
            name_country = data[2]
            


            # Save all iso_country = "name country"
            if iso_country not in self.country_iso_name.keys():
                self.country_iso_name[iso_country] = name_country.lower().lstrip().rstrip()
        

            # Save all name_country = iso
            if name_country not in self.country_name_iso.keys():
                self.country_name_iso[name_country] = iso_country

            if key in self.data.keys():
                # Note slug city is unique 
                self.metadata["info"+":"+str(count)] = "Duplicate ID turismoi: " + str(key) + " :( "
                count = count + 1
            else:
                self.data[key] = i

            # Save all info [country] = [[city:name="data.key"]]
            if not name_country in self.control_countries_cities_create.keys():
                self.control_countries_cities_create[name_country] = {}
            if name_city not in self.control_countries_cities_create[name_country].keys():
                self.control_countries_cities_create[name_country][name_city] = key


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

    def setGeoLatLon(self, key, newGeo):
        if key in self.data.keys():
            dataToEdit = self.data[key]
            dataToEdit = dataToEdit.split("|")
            #print("Antes...", dataToEdit)
            #print("Latitude: ", dataToEdit[15])
            #print("Longitude", dataToEdit[16])
            new_latude = newGeo.split("|")[0]
            new_longitude =  newGeo.split("|")[1]
            #print("Nueva GEO:", new_latude, new_longitude)ç
            dataToEdit[15] = new_latude
            dataToEdit[16] = new_longitude
            # ReStruct the data
            final_data = ""
            for i in dataToEdit:
                final_data = final_data + i + "|"

            final_data = final_data.replace('|||', '||')

            #print("Antes...", self.data[key])
            #print("Despues.", final_data)
            self.data[key] = final_data
            self.metadataGeo[str(self.count)] = "Modify lat lon to " + str(key) + " >> " + newGeo
            self.count = self.count + 1

    def getCountriesWithCities(self):
        """
        return a [str(name_country), str(name_country)...]
        if country contains cities
        
        """
        data = []
        for i in self.control_countries_cities_create:
            if len(self.control_countries_cities_create[i]) > 1:
                data.append(i)

        return data

    def getAllCitiesIdOfCountryViaName(self, name_country):       
        data = []
        try:
            iso_country = self.country_name_iso[name_country]
            for i in self.data:
                if str(iso_country+":") in i:
                    data.append(i)
        except:
            pass


        return data


    def getAllCitymachInfo(self, country, city_name):
        pass

    def getmachingDataKeys(self, key):
        """
        Return a [co:bogota] = "COLOMBIA:Bog"
        """
        data = ""
        if key in self.machingDataKeys.keys():
            data = self.machingDataKeys[key]
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
                    iso_key = j.split(":")[0]
                    if get_iso_key == iso_key:
                        turismoi_data = self.data[j].split("|")
                        # Found in 9 name_place|
                        var_name_place = turismoi_data[9]
                        var_name_place = self._eraseLowerAllNumbersOfString(var_name_place)
                        ext_external_data = external_data[int(i)]
                        ext_external_data = self._eraseLowerAllNumbersOfString(ext_external_data)
                        if turismoi_data[9].strip().lower()  == ext_external_data:
                            self.machingDataKeys[j] = key
                            self.metadataMaching[str(self.count)] = "Found via name_place " + str(j) + " >> " + str(key)
                            self.count = self.count + 1
                            found = True        

                        # 10 short_name_place|
                        var_short_name_place = turismoi_data[10]
                        var_short_name_place = self._eraseLowerAllNumbersOfString(var_short_name_place)
                        ext_external_data = external_data[int(i)]
                        ext_external_data = self._eraseLowerAllNumbersOfString(ext_external_data)
                        if ext_external_data in var_short_name_place and not found:
                            #print("Encontreee...: ", external_data[int(i)], "*  En   ", key, " >> ", j)
                            self.machingDataKeys[j] = key
                            self.metadataMaching[str(self.count)] = "Found via short_name_place " + str(j) + " >> " + str(key)
                            self.count = self.count + 1
                            found = True  

                        # 11 slug_place|
                        var_slug_place = turismoi_data[10]
                        var_name_place = self._eraseLowerAllNumbersOfString(var_slug_place)
                        ext_external_data = external_data[int(i)]
                        ext_external_data = self._eraseLowerAllNumbersOfString(ext_external_data)
                        if ext_external_data in var_slug_place and not found:
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

    def _eraseLowerAllNumbersOfString(self, txt):
        for i in ['0','1','2','3','4','5','6','7','8','9','-','á','é','í','ó','ú','ñ','n',',']:
            txt = txt.replace(i, '')
        return txt.strip().lower()
                        
 
 