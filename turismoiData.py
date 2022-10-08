"""
This file is create to save all information from turismoi
0 ID_country|1 ISO_country|2 NAME_country|3 NAME_PRINT_country|4 ISO3_country|5 CODE_country|6 NAME_ESP_country|7 id_city|8 region_id|9 name_place|10 short_name_place|11 slug_place|12 group_id_place|13 province_id_place|14 group_slug_place|15 latitude|16 longitude|17 country_host_id_place|

"""

class TurismoiDATA:
    def __init__(self) -> None:
        self.data = {} # {iso_country.lower().LRstrip() + ":" + city_name.lower().LRstrip()}
        self.isTheDataLoad = False
        self.metadata = {}

    def chargeData(self, txt):
        count = 0
        for i in txt.split("\n")[1:-1]:
            data = i.split("|")
            iso_country = str(data[1]).lower().strip()
            name_city = str(data[11]).lower().lstrip().rstrip()
            key = iso_country + ":" + name_city
            
            

            if key in self.data.keys():
                self.metadata["info"+":"+str(count)] = "Duplicate ID turismoi: " + str(key) + " :( "
                count = count + 1
            else:
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
            data = self.data[key].split("|")
            slug_city = data[11]
            city_name = data[9]
            country = data[2]

            latitude = data[15]
            if latitude != "NULL":
                if not self._validatesLatitude(latitude):
                    latitude = "NULL"

            longitude = data[16]
            if not longitude != "NULL":
                if not self._validatesLongitude(longitude):
                    longitude = "NULL"

            data = slug_city + "|" + city_name + "|" + country + "|" + latitude + "|" + longitude + "|"

        return data

    def getAllInfo(self, key):
        if key in self.data:
            return self.data[key]
        return ""





