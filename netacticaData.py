"""
FelipedelosH
This archive contain several information
0 "id"|1 "country_code"|2 "name_es"|3 "name_full_es"|4 "name_en"|5 "name_full_en"|6 "latitude"|7 "longitude"

"""

class NetacticaData:
    def __init__(self) -> None:
        self.data = {}
        self.isTheDataLoad = False
        self.metadata = {}
        self.metadataGEO = {}
        self.count = 0

    def chargeData(self, txt):
        count = 0
        duplicated_control = 0
        for i in txt.split("\n")[1:-1]:
            data = i.split("|")
            iso_code = data[1].strip().lower()
            city_name = data[2].lower().lstrip().rstrip().replace('-', ' ')

            key = iso_code + ":" + city_name

            if key in self.data.keys():
                key = key + "-" + str(duplicated_control)
            
            self.data[key] = i

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

    
    def getLatLonViaID(self, key):
        data = ""
        if key in self.data.keys():
            data = self.data[key].split("|")

            latitude = data[6]
            if latitude != "NULL":
                if not self._validatesLatitude(latitude):
                    latitude = "NULL"

            longitude = data[7]
            if not longitude != "NULL":
                if not self._validatesLongitude(longitude):
                    longitude = "NULL"


            data = latitude + "|" + longitude

        return data

    def searchPlace(self, iso_code, city_name, allRegInfo, delimiter, vecPosToSearch=[]):
        """
        Return latitude|longitude if find the place.
        1 -> Search via id
        2 -> Seach Sequencial // Brute force
        

        """
        data = "NULL|NULL"
        found = False
        # First search via key
        key = iso_code+":"+city_name
        if key in self.data.keys():
            self.metadataGEO[str(self.count)] = " >> Macth via id " + str(key)
            self.count = self.count + 1
            data = self.getLatLonViaID(key)

        if not found:
            seraching = allRegInfo.split(delimiter)
            for i in self.data:
                if iso_code+":" in i and city_name != "null":
                    for j in vecPosToSearch:
                        clean_seraching = self._eraseLowerAllNumbersOfString(seraching[j])
    
                        ## Search name es
                        name_es = self.data[i].split("|")[2]
                        name_es = self._eraseLowerAllNumbersOfString(name_es)
                        if name_es == clean_seraching:
                            self.metadataGEO[str(self.count)] = " >> Macth name_es equals " + str(key) + " >> " + str(i)
                            self.count = self.count + 1
                            data = self.getLatLonViaID(i)
                            found = True
                            break

                        ## Search full_name_es
                        #full_name_es = self.data[i].split("|")[3]
                        #full_name_es = self._eraseLowerAllNumbersOfString(full_name_es)
                        #if clean_seraching == full_name_es:
                        #    print("Encontre otro...", key, " >> ", i)

                        ##Seach name_en
                        name_en = self.data[i].split("|")[4]
                        name_en = self._eraseLowerAllNumbersOfString(name_en)
                        if name_en == clean_seraching:
                            self.metadataGEO[str(self.count)] = " >> Macth name_en equals " + str(key) + " >> " + str(i)
                            self.count = self.count + 1
                            data = self.getLatLonViaID(i)
                            found = True
                            break


                        ## Serach full_name_en
                        #full_name_en = self.data[i].split("|")[5]
                        #full_name_en = self._eraseLowerAllNumbersOfString(full_name_en)
                        #if full_name_en == clean_seraching:
                        #    print("Encontre full ingles ", key, " >> ", i)
                        
                        
                    if found:
                        break


                if found:
                    break
                            
                
        return data


    def _eraseLowerAllNumbersOfString(self, txt):
        for i in ['0','1','2','3','4','5','6','7','8','9','-','á','é','í','ó','ú','ñ','n',',','(provincia)','(',')','\'','.','_']:
            txt = txt.replace(i, '')
        return txt.strip().lower()



