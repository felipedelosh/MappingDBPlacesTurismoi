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

    def chargeData(self, txt):
        count = 0
        duplicated_control = 0
        for i in txt.split("\n")[1:-1]:
            data = i.split("|")
            iso_code = data[1].strip().lower()
            city_name = data[2].lower().lstrip().rstrip()

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
                    print(latitude)
                    latitude = "NULL"

            longitude = data[7]
            if not longitude != "NULL":
                if not self._validatesLongitude(longitude):
                    longitude = "NULL"


            data = latitude + "|" + longitude

        return data


