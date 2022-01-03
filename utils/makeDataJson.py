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
                    "2" : "atearBefore"
                }
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
                    "eachVoc" : False
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

    def getSchoolAndYear(self):
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
                return self.showSchoolType()
        else:
            return self.showSchoolType()

    def reqToData(self):
        r = requests.get(self.data["school"][self.schoolType]["yearType"][self.yearType]["link"])
        print(r)
    # def allSchoolVoc(self,schoolId,yearType):
    #     if school

a = MakeDataJson()
a.getSchoolAndYear()
a.reqToData()
