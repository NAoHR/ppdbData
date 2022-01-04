# still on development, dont use this
import json
import requests


class MakeDataJson:    
    def __init__(self):
        self.schoolType = ""
        self.yearType = ""
        self.schoolCred = ""
        self.data = {
            "accepted" : {
                "sctype" : {
                    "1" : "smp",
                    "2" : "sma",
                    "3" : "smk"
                },
                "scYear" : {
                    "1" : "current",
                    "2" : "ayearBefore"
                }
            },
            "linkSchool" :{
                "current" : "https://ppdb.jakarta.go.id/seleksi/prestasi/",
                "ayearBefore" : "https://arsip.siap-ppdb.com/2020/jakarta/seleksi/prestasi/"
            },
            "school" : {
                "smp" : {
                    "yearType" : {
                        "current" : {
                            "link" : "https://ppdb.jakarta.go.id/sekolah/1-smp-prestasi.json",
                            "prefix" : "1"
                        },
                        "ayearBefore" : {
                            "link" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/2-smp-prestasi.json",
                            "prefix" : "2"
                        }
                    },
                    "eachVoc" : {
                        "current" : "https://ppdb.jakarta.go.id/sekolah/kompetensi/1-smp-prestasi.json",
                        "ayearBefore" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/kompetensi/2-smp-prestasi.json"
                    }
                },
                "sma" : {
                    "yearType" : {
                        "current" : {
                            "link" : "https://ppdb.jakarta.go.id/sekolah/1-sma-prestasi.json",
                            "prefix" : "1"
                        },
                        "ayearBefore" : {
                            "link" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/1-sma-prestasi.json",
                            "prefix" : "2"
                        }
                    },
                    "eachVoc" : {
                        "current" : "https://ppdb.jakarta.go.id/sekolah/kompetensi/1-sma-prestasi.json",
                        "ayearBefore" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/kompetensi/1-sma-prestasi.json"
                    }
                },
                "smk" : {
                    "yearType" : {
                        "current" : {
                            "link" : "https://ppdb.jakarta.go.id/sekolah/1-smk-prestasi.json",
                            "prefix" : "1"
                        },
                        "ayearBefore" : {
                            "link" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/2-smk-prestasi.json",
                            "prefix" : "2"
                        }
                    },
                    "eachVoc" : {
                        "current" : "https://ppdb.jakarta.go.id/sekolah/kompetensi/1-smk-prestasi.json",
                        "ayearBefore" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/kompetensi/2-smk-prestasi.json"
                    }
                }
            }
        }

    def __getSchoolAndYear(self):
        schoolType = int(input("schoolType : "))
        if schoolType in range(1,4):
            isThere = self.data["accepted"]["sctype"].get(str(schoolType))
            if isThere != None:
                self.schoolType = isThere
                while True:
                    year = int(input("yearType : "))
                    notNone = self.data["accepted"]["scYear"].get(str(year))
                    if notNone != None:
                        self.yearType = notNone
                        break
                return True if self.schoolType != "" and self.yearType != "" else False
            else:
                return self.__getSchoolAndYear()
        else:
            return self.__getSchoolAndYear()

    def __reqAllSchool(self):
        def ask(data):
            try:
                school = int(input("number : "))
                if school not in range(len(data)):
                    return ask(data)
                else:
                    self.schoolCred = jsonedData[school -1]
                    return True
            except ValueError:
                return ask(data)
        try:
            r = requests.get(self.data["school"][self.schoolType]["yearType"][self.yearType]["link"],timeout=3)
            jsonedData = r.json()
            for num,item in enumerate(jsonedData):
                print(num+1,item["nama"])
            return ask(jsonedData)
        except Exception as e:
            return False

    def __getCredsData(self):
        try:
            r = requests.get(self.data["school"][self.schoolType]["eachVoc"][self.yearType],timeout=3)
            jsonedData = r.json()
            return jsonedData[self.schoolCred["sekolah_id"]]
        except Exception as e:
            print(e)
            return []

    def __loopDataInCred(self,data):
        for item in data:
            link = self.data["linkSchool"][self.yearType]
            prefix = self.data["school"][self.schoolType]["yearType"][self.yearType]["prefix"]
            merged = f"{link}{self.schoolType}/{prefix}-{self.schoolCred['sekolah_id']}-{item[0]}.json"
            try:
                r = requests.get(merged,timeout=3)
                print(r.status_code)
            except:
                print("Error")

    def make(self):
        try:
            isSchoolandYearDone = self.__getSchoolAndYear()
            if isSchoolandYearDone:
                reqSchool = self.__reqAllSchool()
                if reqSchool:
                    credData = self.__getCredsData()
                    if credData:
                        self.__loopDataInCred(credData)
        except KeyboardInterrupt:
            print("adios")

a = MakeDataJson()
a.make()

