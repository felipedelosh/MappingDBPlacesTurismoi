"""
FelipedelosH
this file is create travel compositor Data
0 Code;1 Name;2 Creation date;3 Latitude;4 Longitude;5 Zoom;5 Airport IATA;6 Country
"""
class TravelCompositorData:
    def __init__(self) -> None:
        self.data = {}
        self.isTheDataLoad = False
        self.metadata = {}

    def chargeData(self, txt):
        count = 0
        duplicate_control = 0
        for i in txt.split("\n")[1:-1]:
            data = i.split(";")
            if str(data[0]).__contains__('fake') or str(data[0]).__contains__('_NEW_') or str(data[1]).lower().__contains__('no usar'):
                self.metadata["Test_register:"+str(count)] = str(data)
                count = count + 1
            else:
                id_country = data[-1]
                NAME_country = id_country.split("(")[0]
                NAME_country = NAME_country.lstrip().rstrip()
                iso_country = id_country.split("(")[-1]
                iso_country = iso_country.replace(')', '')
                iso_country = iso_country.strip().lower()

                name_city = str(data[1]).lstrip().rstrip().lower()

                key = iso_country + ":" + name_city

                
                if key in self.data.keys():
                    key = key + "-" + str(duplicate_control)
                    duplicate_control = duplicate_control + 1

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


    def getReportInfo(self, key):
        """
        Retruns 
        """
        data = ""
        if key in self.data.keys():
            info = self.data[key].split(";")
            code = info[0]
            city_name = info[1]
            county = info[6]
            

            latitude = info[3]
            if latitude != "NULL":
                if not self._validatesLatitude(latitude):
                    latitude = "NULL"

            longitude = info[4]
            if longitude != "NULL":
                if not self._validatesLongitude(longitude):
                    longitude = "NULL"

            data = code + "|" + city_name + "|" + county + "|" + latitude + "|" + longitude


        return data

    def getAllInfo(self, key):
        data = ""
        if key in self.data.keys():
            data = self.data[key]
        return data 

